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
    librispeech_lexicon = getDict()
    outputfile, ground_truth = item
    hypothesis_list = []
    ground_truth_list = []

    with open(outputfile, 'r') as reader:
        for line in reader.read().splitlines():
            line_words = line.split(' ')
            temp = ""
            for element in line_words:
                if (element in librispeech_lexicon):
                    transcription = librispeech_lexicon.get(element)
                    temp += transcription
                else:
                    hypothesis_list.append("\n")
                    break
                hypothesis_list.append(temp)

    with open(ground_truth, 'r') as reader:
        for line in reader.read().splitlines():
            line_words = line.split(' ')
            temp = ""
            for element in line_words:
                if (element in librispeech_lexicon):
                    transcription = librispeech_lexicon.get(element)
                    temp += transcription
                else:
                    ground_truth_list.append("\n")
                    break
            ground_truth_list.append(temp)
    for e in ground_truth_list:
        print(e + "\n")
    for e in hypothesis_list:
        print(e + "\n")

    return wer(ground_truth_list, hypothesis_list)


def getDict():
    librispeech_lexicon = {}

    with open("/home/nat/deepspeech-venv/SLaM_DeepSpeech/SLaM_DeepSpeech/references/librispeech-lexicon.txt") as f:
        for line in f:
            line = line.rstrip()
            (key, val) = line.split(None, 1)
            librispeech_lexicon[str(key)] = val
        return librispeech_lexicon


# The following code is from: http://hetland.org/coding/python/levenshtein.py

# This is a straightforward implementation of a well-known algorithm, and thus
# probably shouldn't be covered by copyright to begin with. But in case it is,
# the author (Magnus Lie Hetland) has, to the extent possible under law,
# dedicated all copyright and related and neighboring rights to this software
# to the public domain worldwide, by distributing it under the CC0 license,
# version 1.0. This software is distributed without any warranty. For more
# information, see <http://creativecommons.org/publicdomain/zero/1.0>

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
