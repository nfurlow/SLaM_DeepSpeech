#!/usr/bin/env python3

################################################################################
#   DeepSpeech 0.6.1 model interface for use in the SLaM lab at UF             #
#   Copyright (C) 2020 Nathan Furlow                                           #
################################################################################

import getopt, sys
from transcriber import transcriber
from error_utils import error_utils

def main(argv):
    inputfile = ''
    outputfile = ''
    md = ''
    errortype = 'word'
    ground_truth = ''
    lm_alpha = 1.50
    lm_beta = 2.00
    try:
        opts, args = getopt.getopt(argv,"hi:o:m:r:g:a:b:",["ifile=","ofile=","md=","rtype=","ground_truth=","lm_alpha=","lm_beta"])
    except getopt.GetoptError:
        print('interface.py -i <inputfile> -o <outputfile> -m <model directory> -r <errortype> -g <ground_truth> -a <lm_alpha> -b <lm_beta>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('interface.py -i <inputfile> -o <outputfile> -m <model directory> -r <errortype> -g <ground_truth> -a <lm_alpha> -b <lm_beta>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-m", "--md"):
            md = arg
        elif opt in ("-r", "--rtype"):
            errortype = arg
        elif opt in ("-g", "--ground_truth"):
            ground_truth = arg
        elif opt in ("-a", "--lm_alpha"):
            lm_alpha = float(arg)
        elif opt in ("-b", "--lm_beta"):
            lm_beta = float(arg)
    print('\n')
    print('Input file:', inputfile)
    print('Output file:', outputfile)
    print('Model Directory:', md)
    print('Error Type:', errortype)
    print('Ground Truth:', ground_truth)
    print('LM alpha:', lm_alpha)
    print('LM beta:', lm_beta)

    if (errortype != ("word" or "phone")) and errortype != '':
        print('Invalid errortype')
        return

    transcriber.transcriber(inputfile, outputfile, md, lm_alpha, lm_beta)

    item = outputfile, ground_truth

    if ((errortype != '') and (errortype == 'word')):
        print("WER is:", error_utils.wordError(item))
    if ((errortype != '') and (errortype == 'phone')):
        print("PER is:", error_utils.phoneError(item))
