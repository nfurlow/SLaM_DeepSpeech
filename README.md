# SLaM_DeepSpeech
An implementation of DeepSpeech's pre-trained English model for use in
the SLaM lab at the University of Florida.

## Package Versions
* deepspeech               0.6.1
* jiwer                    1.3.2
* numpy                    1.17.3
* PyAudio                  0.2.11
* scipy                    1.3.1
* tensorflow               1.14.0

## Using the SLaM DeepSpeech Interface
This interface is intended to make using DeepSpeech pre-trained models more
compatible with large batches of audio files. It also includes build-in error
calculations. Currently, [Word Error Rate] is implemented using the [jiwer]
Package.

[Word Error Rate]: https://en.wikipedia.org/wiki/Word_error_rate
[jiwer]: https://pypi.org/project/jiwer/

### Command Line Functionality
* `-h` help
* `-i` inputdir, the path to a directory containing audio files;
audio files should be in `.wav` format; transcriber will skip any files without
a `.wav` extension
* `-o` outputfile, the path to an empty `.txt` file where the results are
written
* `-m` model directory, the path to the directory containing the DeepSpeech
pre-trained model; should contain
* `-r` error type, current options: `word` <word error rate> `phone`
<phone error rate>; if `-r` is not included, error will not be calculated
* `-g` ground_truth, the path to a `.txt` file containing the intended
transcriptions of the audio files; used to calculate error rate; transcriptions
should be in sorted order, separated by new lines
* `-a` lm_alpha, the relative weight of language model vs. Correctionist
Temporal Classification (CTC)
* `-b` lm_beta, considers more words

## Example
`python3 SLaM_DeepSpeech
-i $HOME/deepspeech-venv/SLaM_DeepSpeech/SLaM_DeepSpeech/temp
-o $HOME/deepspeech-venv/SLaM_DeepSpeech/SLaM_DeepSpeech/temp/output.txt
-m $HOME/deepspeech-venv/deepspeech-0.6.1-models
-r word
-g $HOME/deepspeech-venv/SLaM_DeepSpeech/SLaM_DeepSpeech/temp/gt.txt`
