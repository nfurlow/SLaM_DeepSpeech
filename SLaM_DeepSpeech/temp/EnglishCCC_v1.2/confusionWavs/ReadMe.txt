The wavs folder contains all the waveforms needed to reconstruct the stimuli which generated interesting confusions. The files are named using the convention T_[ID].wav. The corresponding confusion in the spreadsheet can be located via the ID (first column).

The waveform files are in stereo format. The left channel corresponds to the spoken utterance in clean, while the right channel corresponds to the noise masker. To recreate the stimuli listeners heard, left and right channel have to be summed together and presented in mono. We used a presentation level of 75 ± 1.5 dB(A) SPL throughout the experiment; signal levels might need to be adjusted for your setup. The processing steps to obtain the signals are described below. Capitalised items refer to spreadsheet columns.


* The target speech is embedded in 200ms lead and lag silence
* A segment is selected from the continuous Masker [SSN, BMN3 or BAB4] corresponding to the confusion, starting at the Onset specified in the spreadsheet and with Length equal to the target speech (also given in spreadsheet).
* An additional 200 ms is added to the segment in both head and tail to obtain a segment whose length is equal to that of the speech embedded in silence. 
* The obtained masker segment is scaled so the SNR of the region where the speech is present (excluding the lead lag silence) is at the value specified in the spreadsheet.
* The speech signal embedded in silence and the masker segment are scaled with the same value so that RMS value of the mix is 0.5
* A 20 ms linear ramp is applied at the onset and offset of both signals.
* As a final step both signals are scaled by the maximum of the absolute value of their sum to avoid clipping when saved in .wav format.

The resulting signals are written to the left and right channels of the stereo waveform. The presented mixture can be obtained by : signal[left channel]+noise[right channel]=mix