#!/usr/bin/env python3

################################################################################
#   DeepSpeech 0.6.1 model interface for use in the SLaM lab at UF             #
#   Copyright (C) 2020 Nathan Furlow                                           #
################################################################################

import getopt, sys
from transcriber import transcriber
from error_utils import error_utils

def main(argv):

    # Declare input variables and initialize default settings
    inputdir = ''
    outputfile = ''
    md = ''
    errortype = ''
    ground_truth = ''
    lm_alpha = 0.75
    lm_beta = 1.85

    # Command line argument setup
    try:
        opts, args = getopt.getopt(argv,"hi:o:m:r:g:a:b:",["idir=","ofile=","md=","rtype=","ground_truth=","lm_alpha=","lm_beta"])
    except getopt.GetoptError:
        print('interface.py -i <inputdir> -m <model directory> -r <errortype> -g <ground_truth> -a <lm_alpha> -b <lm_beta>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('interface.py -i <inputdir> -m <model directory> -r <errortype> -g <ground_truth> -a <lm_alpha> -b <lm_beta>')
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
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

    # Print received values for debug purposes
    print('\n')
    print('Input Directory:', inputdir)
    # print('Output file:', outputfile)
    print('Model Directory:', md)
    print('Error Type:', errortype)
    print('Ground Truth:', ground_truth)
    print('LM alpha:', lm_alpha)
    print('LM beta:', lm_beta)

    # Check that a valid errortype was entered
    if ((errortype != 'word') and (errortype != 'phone') and (errortype != '')):
        print('Invalid errortype')
        return

    # Run transcriber
    transcriber.transcriber(inputdir, md, lm_alpha, lm_beta)

    item = outputfile, ground_truth

    # Run error functions
    if ((errortype != '') and (errortype == 'word')):
        print("WER is:", error_utils.wordError(item))
    if ((errortype != '') and (errortype == 'phone')):
        print("PER is:", error_utils.phoneError(item))
