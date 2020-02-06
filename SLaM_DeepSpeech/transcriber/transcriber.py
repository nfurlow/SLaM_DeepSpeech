#!/usr/bin/env python3

################################################################################
#   DeepSpeech 0.6.1 transcriber implementing a pretrained DeepSpeech model    #
#   Copyright (C) 2020 Nathan Furlow                                           #
################################################################################

import os, sys

try:
    from deepspeech import Model
    import pyaudio
    import scipy.io.wavfile as wav
    import tensorflow as tf
except ImportError:
    print("Error: missing one of the libraries (deepspeech, pyaudio, scipy, tensorflow)")
    sys.exit()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def transcriber(inputfile, outputfile, md):
    inputfile_len = file_len(inputfile)

    BEAM_WIDTH = 500
    LM_ALPHA = 1.50
    LM_BETA = 2.10

    deep = Model(md + '/output_graph.pbmm', BEAM_WIDTH)
    enabled = deep.enableDecoderWithLM(md + '/lm.binary',
    md + '/trie',
    LM_ALPHA,
    LM_BETA)
    print(enabled)

    outputList = []

    with open(inputfile, 'r') as reader:
        for line in reader.read().splitlines():
            fs,audio = wav.read("$HOME/deepspeech-venv/SLaM_DeepSpeech/SLaM_DeepSpeech/temp/EnglishCCC_v1.2/confusionWavs_mono/T_" + line + "_mono.wav")
            result = deep.stt(audio)
            outputList.append(result + "\n")
            print(count, "/", inputfile_len)

            with open(outputfile, 'w') as writer:
                writer.writelines(outputList)
    return

    def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
