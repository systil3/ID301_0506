from pydub import AudioSegment
import numpy as np
import librosa
import pyrubberband as pyrb
import fractions

DEFAULT_SAMPLE_RATE = 44100
PRINT_STATE = True

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

#-------------------------------------- stretching section ----------------------------------------------

def detectBPM(audio, np_type):
    np_sound = np.frombuffer(audio, dtype=np_type).astype(
        np.float16 if np_type in (np.int16, np.float16)
        else np.float32
    )  # Change the dtype to float
    tempo, beat_frames = librosa.beat.beat_track(y=np_sound, sr=DEFAULT_SAMPLE_RATE)
    if tempo < 100:
        if PRINT_STATE:
            print(f'Estimated tempo: {round(tempo)} or {round(tempo * 2)} bpm')
            tempo *= 2 #to be fixed. todo
    else:
        if PRINT_STATE:
            print(f'Estimated tempo: {tempo[0]} bpm')
    return tempo[0]

def stretchFromBPM(audio, np_type, original_bpm, modified_bpm, nfft = 2048):
    """
    open-source algorithm in https://github.com/gaganbahga/time_stretch
    """

    try:
        np_sound = np.frombuffer(audio, dtype=np_type).astype(
            np.float16 if np_type in (np.int16, np.float16)
            else np.float32
        )
        factor = modified_bpm / original_bpm
        print(factor)
        '''
        stretch an audio sequence by a factor using FFT of size nfft converting to frequency domain
        :param x: np.ndarray, audio array in PCM float32 format
        :param factor: float, stretching or shrinking factor, depending on if its > or < 1 respectively
        :return: np.ndarray, time stretched audio
        '''
        stft = librosa.core.stft(np_sound, n_fft=nfft).transpose()  # i prefer time-major fashion, so transpose
        stft_cols = stft.shape[1]

        times = np.arange(0, stft.shape[0], factor)  # times at which new FFT to be calculated
        hop = nfft/4                                 # frame shift
        stft_new = np.zeros((len(times), stft_cols), dtype=np.complex_)
        phase_adv = (2 * np.pi * hop * np.arange(0, stft_cols))/ nfft
        phase = np.angle(stft[0])

        stft = np.concatenate( (stft, np.zeros((1, stft_cols))), axis=0)

        for i, time in enumerate(times):
            left_frame = int(np.floor(time))
            local_frames = stft[[left_frame, left_frame + 1], :]
            right_wt = time - np.floor(time)                        # weight on right frame out of 2
            local_mag = (1 - right_wt) * np.absolute(local_frames[0, :]) + right_wt * np.absolute(local_frames[1, :])
            local_dphi = np.angle(local_frames[1, :]) - np.angle(local_frames[0, :]) - phase_adv
            local_dphi = local_dphi - 2 * np.pi * np.floor(local_dphi/(2 * np.pi))
            stft_new[i, :] =  local_mag * np.exp(phase*1j)
            phase += local_dphi + phase_adv

        stretched_audio = librosa.core.istft(stft_new.transpose()).astype(np_type).tobytes()
        print(type(audio), len(audio), type(stretched_audio), len(stretched_audio))
        return stretched_audio

    except Exception as e:
        print(f"error:{e}")
