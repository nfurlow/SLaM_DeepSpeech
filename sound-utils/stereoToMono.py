from pydub import AudioSegment
import os

path = os.path.abspath(".")

with open(path + '/references/englishccc_ids.txt', 'r') as reader:
    for line in reader.read().splitlines():
        sound = AudioSegment.from_wav(path + "/EnglishCCC_v1.2/confusionWavs/T_" + line + ".wav")
        sound = sound.set_channels(1)
        sound.export(path + "/EnglishCCC_v1.2/confusionWavs_mono/T_" + line + "_mono.wav", format="wav")
