from deepspeech import Model
import tensorflow as tf
import scipy.io.wavfile as wav
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pyaudio

path = os.path.abspath(".")
BEAM_WIDTH = 500
LM_ALPHA = 1.50
LM_BETA = 2.10

deep = Model(path + "/deepspeech-0.6.1-models/output_graph.pb",
BEAM_WIDTH)
enabled = deep.enableDecoderWithLM(path + "/deepspeech-0.6.1-models/lm.binary",
path + "/deepspeech-0.6.1-models/trie",
LM_ALPHA,
LM_BETA)
print(enabled)

outputList = []

with open(path + '/references/englishccc_ids.txt', 'r') as reader:
    for line in reader.read().splitlines():
        fs,audio = wav.read(path + "/EnglishCCC_v1.2/confusionWavs_mono/T_" + line + "_mono.wav")
        result = deep.stt(audio)
        outputList.append(result + "/n")
        print("~~~~we finished one tho")

with open(path + '/references/output.txt', 'w') as writer:
    writer.writelines(outputList)
