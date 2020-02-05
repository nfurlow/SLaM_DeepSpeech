#!/usr/bin/python3

from jiwer import wer
import sys, getopt, os

#path = os.path.abspath(".")

#with open(path + '/references/' + sys.argv, 'r') as reader:


#ground_truth = ["hello baby", "yes", "no", "world"]
#hypothesis = ["hello", "", "", "duck"]

#print(wer(ground_truth, hypothesis))


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('wer.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('wer.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print('Input file is "', inputfile)
   print('Output file is "', outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
