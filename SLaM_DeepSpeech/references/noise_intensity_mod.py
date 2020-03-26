import os
from pydub import AudioSegment
from scipy.io import wavfile

import parselmouth
from parselmouth.praat import call

path = os.path.abspath(".")

snrdBTarget = 10

os.mkdir("snr" + str(abs(snrdBTarget)))

for filename in os.listdir(path):
    if os.path.isdir(filename):
        # skip directories
        continue
    if filename == "noise_intensity_mod.py":
        continue
    if filename.rsplit('_', 1)[1] == 'left.wav' or filename.rsplit('_', 1)[1] == 'right.wav':
        continue
    if filename.rsplit('_', 1)[1] == 'snr' + str(abs(snrdBTarget)) + '.wav':
        continue

    print(filename)
    fs, data = wavfile.read(filename) # reading the file

    # signal
    wavfile.write(filename.rsplit('.', 1)[0] + '_left.wav', fs, data[:, 0])
    # noise
    wavfile.write(filename.rsplit('.', 1)[0] + '_right.wav', fs, data[:, 1])

    sound = parselmouth.Sound(filename.rsplit('.', 1)[0] + '_left.wav')
    noise = parselmouth.Sound(filename.rsplit('.', 1)[0] + '_right.wav')

    dBSig_original = call(sound, 'Get intensity (dB)')
    dBnoi_original = call(noise, 'Get intensity (dB)')

    noise_sampFreq = call(noise, 'Get sampling frequency')
    targetsampFreq = call(sound, 'Get sampling frequency')
    if noise_sampFreq != targetsampFreq:
        noise = call(noise, 'Resample', targetsampFreq, 50)

    dBnoi_Target = dBSig_original - snrdBTarget

    call(noise,'Scale intensity',dBnoi_Target)

    targetwithnoise = parselmouth.Sound(sound.values + noise.values,
         sampling_frequency = targetsampFreq)

    targetwithnoise.save(path + '/' + 'snr' + str(abs(snrdBTarget)) + '/'
        + filename.rsplit('.', 1)[0] + '_snr' + str(abs(snrdBTarget)) + '.wav', "WAV")

    # delete channel files
    os.remove(filename.rsplit('.', 1)[0] + '_left.wav')
    os.remove(filename.rsplit('.', 1)[0] + '_right.wav')
