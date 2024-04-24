from pydub import AudioSegment
import numpy as np
import struct

def byte_string_to_binary_array(byte_string):
    binary_array = []
    for byte in byte_string:
        binary_representation = bin(byte)[2:].zfill(8)  # Removing '0b' prefix and zero-padding to 8 bits
        # Convert each binary digit to 0 or 1 and add to the array
        for bit in binary_representation:
            binary_array.append(int(bit))
    return binary_array

def binary_array_to_byte_object(binary_array):
    byte_string = b""
    for i in range(0, len(binary_array), 8):
        byte_bits = binary_array[i:i+8]
        byte_value = int("".join(map(str, byte_bits)), 2)
        byte_string += bytes([byte_value])
    return byte_string

def reverseAudio(audio, np_type):
    audio_arr = np.frombuffer(audio, dtype=np_type)
    reversed_audio = audio_arr[::-1]
    return reversed_audio.tobytes()

def retriggerAudio(audio, np_type, fraction = 4, samplerate = 44100):
    length = len(audio)

    start_time = 0  # Start from the beginning
    end_time = length // fraction # End at the duration of 1/16 beat chunk
    chunk = audio[start_time:end_time]

    repeated_chunk = chunk * fraction
    return repeated_chunk

def gatedAudio(audio, np_type, fraction = 8, samplerate = 44100):
    length = len(audio)
    chunk_size = length // fraction
    ret = AudioSegment.silent(duration=0)

    for i in range(fraction):
        if i % 2 == 0:
            ret += audio[chunk_size*i:chunk_size*(i+1)]
        else:
            ret += AudioSegment.silent(duration=chunk_size)
    return ret

def downsampleAudio(audio, np_type, fraction=8):

    def sin_wave(freq, duration, sample_rate):
        t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
        sinw = np.sin(2 * np.pi * freq * t)
        return sinw

    audio_arr = np.frombuffer(audio, dtype=np_type).copy()  # Create a copy of the array
    downsampled_audio = audio_arr
    length = len(downsampled_audio)
    for i in range(length):
        if i % fraction != 0:
            downsampled_audio[i] = downsampled_audio[i - i % fraction]

    ret = downsampled_audio.tobytes()
    return ret

'''def downsampleAudio(audio, target_sample_rate):
    # Get the audio data as a numpy array
    audio_data = np.array(audio.get_array_of_samples())

    # Resample the audio data
    current_sample_rate = audio.frame_rate
    ratio = current_sample_rate / target_sample_rate
    new_length = int(len(audio_data) / ratio)
    new_audio_data = np.interp(np.linspace(0, len(audio_data) - 1, new_length),
                               np.arange(len(audio_data)), audio_data).astype(np.int16)

    # Create a new AudioSegment with the downsampled data
    downsampled_audio = AudioSegment(
        new_audio_data.tobytes(),
        frame_rate=target_sample_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    return downsampled_audio'''

def tape_effect(input_audio, wow_factor=0.1, flutter_factor=0.1, saturation_factor=0.1, noise_factor=0.1):
    # Simulate wow and flutter by modulating the playback speed
    wow = np.random.normal(1, wow_factor, len(input_audio))
    flutter = np.random.normal(1, flutter_factor, len(input_audio))
    print(len(len(input_audio) * flutter * wow), len(input_audio))
    output_audio = np.interp(np.arange(len(input_audio)) * flutter * wow, np.arange(len(input_audio)), input_audio)

    # Simulate saturation by clipping the audio signal
    output_audio = np.clip(output_audio * saturation_factor, -1.0, 1.0)

    # Simulate tape noise
    noise = np.random.normal(0, noise_factor, len(input_audio))
    output_audio += noise

    return output_audio