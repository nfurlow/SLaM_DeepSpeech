#!/usr/bin/env python3

################################################################################
#   DeepSpeech 0.6.1 transcriber implementing a pretrained DeepSpeech model    #
#   Copyright (C) 2020 Nathan Furlow                                           #
################################################################################

import os, sys, math

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
    toolbar_width = 40
    inputfile_len = file_len(inputfile)
    if (inputfile_len > toolbar_width):
        incriment = math.trunc(inputfile_len / toolbar_width)
    else:
        toolbar_width = inputfile_len
        incriment = 1
    count = 1
    outputList = []

    BEAM_WIDTH = 500
    LM_ALPHA = 0.00
    LM_BETA = 0.00

    deep = Model(md + '/output_graph.pbmm', BEAM_WIDTH)
    enabled = deep.enableDecoderWithLM(md + '/lm.binary',
    md + '/trie',
    LM_ALPHA,
    LM_BETA)
    print('Decoder Enabled <0=true>:', enabled)

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    with open(inputfile, 'r') as reader:
        for line in reader.read().splitlines():
            fs,audio = wav.read("/home/nat/deepspeech-venv/SLaM_DeepSpeech/SLaM_DeepSpeech/temp/EnglishCCC_v1.2/confusionWavs_mono/T_" + line + "_mono.wav")
            result = deep.stt(audio)
            outputList.append(result + "\n")
            #print(count, "/", inputfile_len)
            if (count == incriment):
                sys.stdout.write("-")
                sys.stdout.flush()
                count = 0
            count += 1

    sys.stdout.write("]\n") # this ends the progress bar

    with open(outputfile, 'w') as writer:
            writer.writelines(outputList)

    return

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
