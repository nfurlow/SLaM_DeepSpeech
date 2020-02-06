#!/usr/bin/python3

from jiwer import wer

def wordError(outputfile, ground_truth):
    hypothesis_list = []
    ground_truth_list = []

    with open(outputfile, 'r') as reader:
        for line in reader.read().splitlines():
            hypothesis_list.append(line)
    with open(ground_truth, 'r') as reader:
        for line in reader.read().splitlines():
            ground_truth_list.append(line)

    return wer(ground_truth_list, hypothesis_list)


#ground_truth = ["hello baby", "yes", "no", "world"]
#hypothesis = ["hello", "", "", "duck"]

#print(wer(ground_truth, hypothesis))
