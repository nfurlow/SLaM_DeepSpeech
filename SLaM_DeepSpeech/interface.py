#!/usr/bin/env python3

################################################################################
#   DeepSpeech 0.6.1 model interface for use in the SLaM lab at UF             #
#   Copyright (C) 2020 Nathan Furlow                                           #
################################################################################

import getopt, sys
from transcriber import transcriber
from error_utils import wer

def main(argv):
    inputfile = ''
    outputfile = ''
    md = ''
    errortype = 'word'
    ground_truth = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:m:r:g:",["ifile=","ofile=","md=","rtype=","ground_truth="])
    except getopt.GetoptError:
        print('interface.py -i <inputfile> -o <outputfile> -m <model directory> -r <errortype> -g <ground_truth>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('interface.py -i <inputfile> -o <outputfile> -m <model directory> -r <errortype> -g <ground_truth>')
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
    print('\n')
    print('Input file:', inputfile)
    print('Output file:', outputfile)
    print('Model Directory:', md)
    print('Error Type:', errortype)
    print('Ground Truth:', ground_truth)

    if (errortype != ("word" or "phone")) and errortype != '':
        print('Invalid errortype')
        return

    transcriber.transcriber(inputfile, outputfile, md)

    if ((errortype != '') and (errortype == 'word')):
        print("WER is:", wer.wordError(outputfile, ground_truth))
    if ((errortype != '') and (errortype == 'phone')):
        per.per()
