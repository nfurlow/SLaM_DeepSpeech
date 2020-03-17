import os
from pydub import AudioSegment
from scipy.io import wavfile

path = os.path.abspath(".")

gain = -5

os.mkdir("gain" + str(abs(gain)))

for filename in os.listdir(path):
    if os.path.isdir(filename):
        # skip directories
        continue
    if filename == "noise_intensity_mod.py":
        continue

    print(filename)
    fs, data = wavfile.read(filename) # reading the file

    # signal
    wavfile.write(filename.rsplit('.', 1)[0] + '_left.wav', fs, data[:, 0]) # saving first column which corresponds to channel 1
    # noise
    wavfile.write(filename.rsplit('.', 1)[0] + '_right.wav', fs, data[:, 1]) # saving second column which corresponds to channel 2

    signal = AudioSegment.from_file(path + "/" + filename.rsplit('.', 1)[0] + '_left.wav')
    noise = AudioSegment.from_file(path + "/" + filename.rsplit('.', 1)[0] + '_right.wav')

    # change gain by some dB
    quieter_via_method = noise.apply_gain(gain)

    # make stereo audio segment from signal and nosie
    stereo_sound = AudioSegment.from_mono_audiosegments(signal, noise)

    # export
    stereo_sound.export(path + "/gain" + str(abs(gain)) + "/" + filename.rsplit('.', 1)[0] + "_g" + str(abs(gain)) + ".wav", format="wav")

    # delete channel files
    os.remove(filename.rsplit('.', 1)[0] + '_left.wav')
    os.remove(filename.rsplit('.', 1)[0] + '_right.wav')
