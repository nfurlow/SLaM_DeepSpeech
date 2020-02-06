#!/usr/bin/env python3

################################################################################
#   DeepSpeech 0.6.1 model interface for use in the SLaM lab at UF             #
#   Copyright (C) 2020 Nathan Furlow                                           #
################################################################################

import getopt, sys
import transcriber
import error_utils

def main(argv):
    inputfile = ''
    outputfile = ''
    errortype = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:md:r:",["ifile=","ofile=","md=","rtype="])
    except getopt.GetoptError:
        print('interface.py -i <inputfile> -o <outputfile> -md <model directory> -r <errortype>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('interface.py -i <inputfile> -o <outputfile> -md <model directory> -r <errortype>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-md", "--md"):
            lmPath = arg
        elif opt in ("-r", "--rtype"):
            errortype = arg
    print('Input file is', inputfile)
    print('Output file is', outputfile)
    print('Model Directory is', md)
    print('Error Type is', errortype)

    if (errortype != ("word" or "phone")) and errortype != '':
        print('Invalid errortype')
        return

    transcriber(inputfile, outputfile, md)

    if ((errortype != '') and (errortype = 'word')):
        wer(inputfile, outputfile)
    if ((errortype != '') and (errortype = 'phone')):
        per(inputfile, outputfile)
