import os
import wave
import threading

import numpy as np
import pyaudio
from soundeffects import *
from bytes import *
from math import sqrt

EFFECT_NORM = 0
EFFECT_REVERSE = 1
EFFECT_RETRIGGER = 2
EFFECT_GATED = 3
EFFECT_DOWNSAMPLE = 4
NUM_OF_EFFECTS = 5

pyaudio_to_numpy_type = {
    pyaudio.paFloat32: np.float32,
    pyaudio.paInt32: np.int32,
    pyaudio.paInt16: np.int16,
    pyaudio.paInt8: np.int8,
}

default_block_sizes = {
    np.float32: 8,
    np.int32: 8,
    np.float16: 4,
    np.int16: 4,
    np.int8: 2
}
class WavePlayerLoop(threading.Thread):
    CHUNK = 1024

    def __init__(self, filepath, loop=True):
        """
        Initialize `WavePlayerLoop` class.
        PARAM:
            -- filepath (String) : File Path to wave file.
            -- loop (boolean)    : True if you want loop playback.
                                   False otherwise.
        """
        super(WavePlayerLoop, self).__init__()
        self.filepath = os.path.abspath(filepath)
        self.loop = loop

        self.player = pyaudio.PyAudio()
        self.wf = wave.open(self.filepath, 'rb')
        sample_width = self.wf.getsampwidth()
        if sample_width == 1:
            self.audio_type = np.int8
        elif sample_width == 2:
            self.audio_type = np.int16
        elif sample_width == 3:
            self.audio_type = np.int16
        elif sample_width == 4:
            self.audio_type = np.int32
        else:
            raise ValueError("Unsupported sample width")
        print(f"audio datatype : {self.audio_type}")

        self.total_frames = self.wf.getnframes()
        self.frame_rate = self.wf.getframerate()

        #init chunks
        self.chunk_length = self.total_frames // 8
        self.chunks = []

        #default audio file stream (for stretching)
        self.default_buffer = self.wf.readframes(self.total_frames)
        print(type(self.default_buffer))
        self.original_bpm = detectBPM(self.default_buffer, self.audio_type)

        #init chunks (default number of chunks : 8)
        block_size = default_block_sizes[self.audio_type]
        for i in range(8):
            if sample_width == 5: #should be fixed, todo
                chunk_data_24 = self.default_buffer[self.chunk_length*block_size*i:self.chunk_length*block_size*(i+1)]
                chunk_data = convert_24bit_to_32bit(chunk_data_24)
            else:
                chunk_data = self.default_buffer[self.chunk_length*block_size*i:self.chunk_length*block_size*(i+1)]
            self.chunks.append(chunk_data)
        self.empty_chunk = [0] * len(self.chunks[0])

        self.enabled = [True] * 8
        self.patterns = [i for i in range(8)]

        self.effects = [EFFECT_NORM for i in range(8)]
        self.effect_buffer = [[] for i in range(8)]
        self.multiplier = np.float16(1)

    def toggleEnable(self, chunk_num):
        assert 0 <= chunk_num < 8
        self.enabled[chunk_num] = not self.enabled[chunk_num]

    def writeEffectBuffer(self, effect, time_pos, chunk_num):
        if effect != EFFECT_NORM:
            if effect == EFFECT_REVERSE:
                self.effect_buffer[time_pos] = reverseAudio(self.chunks[chunk_num], self.audio_type)
            if effect == EFFECT_RETRIGGER:
                self.effect_buffer[time_pos] = retriggerAudio(self.chunks[chunk_num], self.audio_type)
            if effect == EFFECT_GATED:
                self.effect_buffer[time_pos] = gatedAudio(self.chunks[chunk_num], self.audio_type)
            if effect == EFFECT_DOWNSAMPLE:
                self.effect_buffer[time_pos] = downsampleAudio(self.chunks[chunk_num], self.audio_type)

    def changePattern(self, time_pos, chunk_num):
        print(time_pos)
        assert 0 <= chunk_num < 8
        self.patterns[time_pos] = chunk_num
        effect = self.effects[time_pos]
        self.writeEffectBuffer(effect, time_pos, chunk_num)

    def changeEffect(self, time_pos):
        self.effects[time_pos] = (self.effects[time_pos]+1) % NUM_OF_EFFECTS
        effect = self.effects[time_pos]
        chunk_num = self.patterns[time_pos]
        self.writeEffectBuffer(effect, time_pos, chunk_num)

    def changeVolume(self, volume):
        self.multiplier = pow(2, (sqrt(sqrt(sqrt(volume))) * 192 - 192) / 6)

    def stretch(self, bpm):
        stretched = stretchFromBPM(self.default_buffer, self.audio_type, self.original_bpm, bpm)
        block_size = default_block_sizes[self.audio_type]
        st_chunk_length = len(stretched) // (8 * block_size)
        self.chunks = []
        for i in range(8):
            if self.wf.getsampwidth() == 5: #should be fixed, todo
                chunk_data_24 = stretched[st_chunk_length*block_size*i:st_chunk_length*block_size*(i+1)]
                chunk_data = convert_24bit_to_32bit(chunk_data_24)
            else:
                chunk_data = stretched[st_chunk_length*block_size*i:st_chunk_length*block_size*(i+1)]
            self.chunks.append(chunk_data)

        for time_pos in range(8):
            chunk_num = self.patterns[time_pos]
            effect = self.effects[time_pos]
            self.writeEffectBuffer(effect, time_pos, chunk_num)

    def run_stretch(self, bpm):
        t = threading.Thread(target=lambda: self.stretch(bpm))
        t.start()

    def setDataBytes(self):
        data = []
        for i in range(8):
            if not self.enabled[i]:
                data += self.empty_chunk
            elif self.effects[i] == EFFECT_NORM:
                data += self.chunks[self.patterns[i]]
            else:
                data += self.effect_buffer[i]
        data_bytes = bytes(data)
        return data_bytes

    def run(self):
        try:
            self.player = pyaudio.PyAudio()
            # Open Output Stream (based on PyAudio tutorial)
            stream = self.player.open(format=self.player.get_format_from_width(self.wf.getsampwidth()),
                                 channels=self.wf.getnchannels(),
                                 rate=self.wf.getframerate(),
                                 output=True)

            # PLAYBACK LOOP
            data_bytes = self.setDataBytes()
            stream.write(data_bytes)

            time_interval = 24

            while self.loop:
                data_bytes = self.setDataBytes()
                n = len(data_bytes)
                pos = 0
                while pos < n:
                    interval = data_bytes[pos:pos + time_interval]

                    audio_samples = np.frombuffer(interval, dtype=np.int16)  # Assuming 16-bit audio

                    mul = ((audio_samples.astype(np.float32) * self.multiplier)
                        .clip(-32768, 32767).astype(np.int16))
                    # Clip to prevent overflow

                    stream.write(mul.tobytes())
                    pos += time_interval

                if self.wf.readframes(self.CHUNK) == b'':  # If file is over then rewind.
                    self.wf.rewind()

            stream.close()
            self.player.terminate()

        except Exception as e:
            print(f"error while running : {e}")

    def start_playback(self):
        """
        Start playback(with multithread).
        """
        thread = threading.Thread(target=self.run)
        thread.start()

    def stop(self):
        """
        Stop playback.
        """
        self.loop = False

