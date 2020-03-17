#!/usr/bin/env python3

from pydub import AudioSegment
import numpy as np

def prepare_input(audio_path):
    """Ensures audio matches the sample rate supported by Deep Speech,
       and truncates the audio to the required length.
    Args:
        audio_path: path ot the audio file
    Returns:
        A tuple with (sample_rate, converted_audio)
    """
    import subprocess
    import scipy.io.wavfile as wav
    sample_rate = 16000
    duration_secs = 6

    fs, audio = wav.read(audio_path)
    if fs != sample_rate:
        if fs < sample_rate:
            print('Warning: original sample rate (%d) is lower than 16kHz. Up-sampling might produce erratic speech recognition.' % (fs), file=sys.stderr)

        # print('Resampling audio from {}kHz to 16kHz'.format(fs/1000))
        sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} - '.format(audio_path, sample_rate)
        try:
            p = subprocess.Popen(sox_cmd.split(),
                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output, err = p.communicate()

            if p.returncode:
                raise RuntimeError('SoX returned non-zero status: {}'.format(err))

        except OSError as e:
            raise OSError('SoX not found, use 16kHz files or install it: ', e)

        audio = np.fromstring(output, dtype=np.int16)

    # Truncate to smaller length, as DeepSpeech is trained on
    # short utterances (a few seconds long)
    # print('Truncating audio from {}s to {}s'.format(len(audio)/sample_rate, duration_secs))

    # max_frames = sample_rate * duration_secs
    # audio = audio[:max_frames]
    return sample_rate, audio

def stereo_to_mono(audio_path):
    sound = AudioSegment.from_wav(audio_path)
    sound = sound.set_channels(1)
    sound.export(audio_path.rsplit('.', 1)[0] + "_mono.wav", format="wav")
    return
