# SLaM_DeepSpeech
An implementation of DeepSpeech's pre-trained English model for use in
the SLaM lab at the University of Florida.

## Package Versions
* deepspeech               0.6.1
* jiwer                    1.3.2
* PyAudio                  0.2.11
* scipy                    1.3.1
* tensorflow               1.14.0

## Using the SLaM DeepSpeech Interface
This interface is intended to make using DeepSpeech pre-trained models more
compatible with large batches of audio files. It also includes build-in error
calculations. Currently [Word Error Rate] is implemented using the [jiwer]
Package.

[Word Error Rate]: https://en.wikipedia.org/wiki/Word_error_rate
[jiwer]: https://pypi.org/project/jiwer/

### Command Line Functionality
* `-h` help
* `-i` inputfile, the path to a `.txt` file containing paths to audio files;
audio files should be mono and in `.wav` format; audio paths should each be on a
new line
* `-o` outputfile, the path to an empty `.txt` file where the results are
written
* `-m` model directory, the path to the directory containing the DeepSpeech
pre-trained model
* `-r` error type, current options: `word` <word error rate>; defaults to word
* `-g` ground_truth, the path to a `.txt` file containing the intended
transcriptions of the audio files listed in the inputfile; used to calculate
error rate; transcriptions should be in the order of inputfile and separated by
new lines
