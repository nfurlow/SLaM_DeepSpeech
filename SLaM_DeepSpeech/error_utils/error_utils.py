#!/usr/bin/python3

################################################################################
#   Use jiwer wer for file scale word error rate calculations                  #
#   Copyright (C) 2020 Nathan Furlow                                           #
################################################################################
import sys

try:
    from jiwer import wer
except ImportError:
    print("Error: missing one of the libraries (jiwer)")
    sys.exit()

def wordError(item):
    outputfile, ground_truth = item
    hypothesis_list = []
    ground_truth_list = []

    with open(outputfile, 'r') as reader:
        for line in reader.read().splitlines():
            hypothesis_list.append(line)
    with open(ground_truth, 'r') as reader:
        for line in reader.read().splitlines():
            ground_truth_list.append(line)

    return wer(ground_truth_list, hypothesis_list)

def phoneError(item):

    # separate outputfile path and ground_truth file path from item
    outputfile, ground_truth = item
    # outputfile contains the list of interences made by the deepspeech model
    # ground_truth contains the list of expected outputs
    # these files should be in the same order

    #initialize as empty lists
    hypothesis_list = []
    ground_truth_list = []

    # open outputfile
    with open(outputfile, 'r') as reader:
        # loop through each line in outputfile
        for line in reader.read().splitlines():

            # assign temp variable with line transcription
            temp = getTranscription(line)

            # append complete transcription of the line to hypothesis_list
            hypothesis_list.append(temp)

    with open(ground_truth, 'r') as reader:
        for line in reader.read().splitlines():

            # assign temp variable with line transcription
            temp = getTranscription(line)

            # append complete transcription of the line to ground_truth_list
            ground_truth_list.append(temp)

    # FIXME: prints added for debugging and should be removed
    for e in ground_truth_list:
        print(e + "\n")
    for e in hypothesis_list:
        print(e + "\n")

    # use jiwer wer() fucntion to compute word error rate of phonemes
    # transcriptions are represented as 'words' in the arpabet system
    return wer(ground_truth_list, hypothesis_list)


def getTranscription(line):

    # return a dictionary structure containing the librishpeech lexicon, see error_utils.getDict()
    librispeech_lexicon = getDict()

    # initialize as empty string
    fullTranscription = ""

    # split line at spaces and initialize as a list of words
    line_words = line.split(' ')

    # loop through each element of line_words
    for element in line_words:

        # check that element exists in dictionary
        if (element in librispeech_lexicon):
            # return transcription for element
            elementTranscription = librispeech_lexicon.get(element)
            # concatinate transcription to the end of temp
            fullTranscription = fullTranscription + elementTranscription
        else:
            # if any word in the line does not exist in the dictionary,
            # temp is assigned "*DNE*" and the loop ends
            fullTranscription = "*DNE*"
            break

    return fullTranscription

# returns librispeech lexicon dictionary
def getDict():
    librispeech_lexicon = {}

    # FIXME: update absolute path to relative path

    # open librispeech_lexicon
    with open("/home/nat/deepspeech-venv/SLaM_DeepSpeech/SLaM_DeepSpeech/references/librispeech-lexicon.txt") as f:

        # loop through lines
        for line in f:

            # remove trailing characters
            line = line.rstrip()

            # split line at the first whitespace from the left
            (key, val) = line.split(None, 1)

            # initialize key val structure
            librispeech_lexicon[str(key)] = val

        return librispeech_lexicon


# FIXME: remove levenshtein distance method after phone error works
# or use in phone error if jiwer does not work

################################################################################
# The following code is from: http://hetland.org/coding/python/levenshtein.py  #
#                                                                              #
# This is a straightforward implementation of a well-known algorithm, and thus #
# probably shouldn't be covered by copyright to begin with. But in case it is, #
# the author (Magnus Lie Hetland) has, to the extent possible under law,       #
# dedicated all copyright and related and neighboring rights to this software  #
# to the public domain worldwide, by distributing it under the CC0 license,    #
# version 1.0. This software is distributed without any warranty. For more     #
# information, see <http://creativecommons.org/publicdomain/zero/1.0>          #
################################################################################

def levenshtein(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = list(range(n+1))
    for i in range(1, m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1, n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]
