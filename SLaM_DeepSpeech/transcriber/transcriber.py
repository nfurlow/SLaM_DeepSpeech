#!/usr/bin/env python3

################################################################################
#   DeepSpeech 0.6.1 transcriber implementing a pretrained DeepSpeech model    #
#   Copyright (C) 2020 Nathan Furlow                                           #
################################################################################

import os, sys, math
from sound_utils import sound_utils

try:
    from deepspeech import Model
    import fnmatch
    import pyaudio
    import scipy.io.wavfile as wav
    import tensorflow as tf
except ImportError:
    print("Error: missing one of the libraries (deepspeech, fnmatch, pyaudio, scipy, tensorflow)")
    sys.exit()

path = os.path.abspath(".")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def transcriber(inputdir, md, lm_alpha, lm_beta):
    toolbar_width = 40
    inputdir_len = len(fnmatch.filter(os.listdir(path + inputdir), '*.wav'))
    print(inputdir_len)
    if (inputdir_len > toolbar_width):
        incriment = math.trunc(inputdir_len / toolbar_width)
    else:
        toolbar_width = inputdir_len
        incriment = 1
    count = 1
    outputList = []

    BEAM_WIDTH = 500

    deep = Model(md + '/output_graph.pbmm', BEAM_WIDTH)
    enabled = deep.enableDecoderWithLM(md + '/lm.binary',
    md + '/trie',
    lm_alpha,
    lm_beta)
    print('Decoder Enabled <0=true>:', enabled)

    # setup progress bar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    filelist = sorted(os.listdir(path + inputdir))
    # writes filelist to an output file
    with open(os.path.join(path + inputdir, inputdir.rsplit('/', 1)[1] + '_filelist.txt'), 'w') as writer:
            writer.writelines('\n'.join(filelist) + '\n')

    for filename in filelist:
        with open(os.path.join(path + inputdir, filename), 'r') as f: # open in readonly mode

            # if the file is not a wav file skip
            if filename.rsplit('.', 1)[1] != "wav":
                continue

            # Check if filename end in _mono.wav, if yes, skip the file
            if filename.rsplit('_', 1)[1] == "mono.wav":
                continue

            # Check if the file has an associated _mono.wav file in the directory
            if filename.rsplit('.', 1)[0] + "_mono.wav" in os.listdir(path + inputdir):
                #if yes, prepare the _mono.wav file
                fs,audio = sound_utils.prepare_input(path + inputdir +  "/" + filename.rsplit('.', 1)[0] + "_mono.wav")
            else:
                #if no, create an _mono.wav file and prepare that file
                sound_utils.stereo_to_mono(path + inputdir + "/" + filename)
                fs,audio = sound_utils.prepare_input(path + inputdir +  "/" + filename.rsplit('.', 1)[0] + "_mono.wav")

            # run prepared audio through DeepSpeech
            result = deep.stt(audio)
            # remove generated processed file
            os.remove(path + inputdir +  "/" + filename.rsplit('.', 1)[0] + "_mono.wav")
            # add the result to the outputList
            outputList.append(result + "\n")

            # progress bar incriment
            if (count == incriment):
                sys.stdout.write("-")
                sys.stdout.flush()
                count = 0
            count += 1

    sys.stdout.write("]\n") # this ends the progress bar

    # writes results to an output file
    with open(os.path.join(path + inputdir, inputdir.rsplit('/', 1)[1] + '_output.txt'), 'w') as writer:
            writer.writelines(outputList)

    return
