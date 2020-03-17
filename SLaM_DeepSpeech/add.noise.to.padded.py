#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import codecs
import os,re,sys

import parselmouth
from parselmouth.praat import call
import tgt

path = os.path.abspath(".")

#def read_textgrid(tginpath,include_empty_intervals_para):
    ##tmp_script_path = fix_linebreak_textgrid(tginpath)

    #try:
        #tg = tgt.read_textgrid(tginpath,include_empty_intervals = include_empty_intervals_para)
    #except:
        #print ('Error reading textgrid file: '  + tginpath)
        #print ('Please ensure that the textgrid file is encoded in UTF-8.')
        #quit()
    #return tg

def read_textgrid(tginpath,include_empty_intervals_para,encoding_setting):
    #tmp_script_path = fix_linebreak_textgrid(tginpath)

    try:
        tg = tgt.read_textgrid(tginpath,include_empty_intervals = include_empty_intervals_para, encoding = encoding_setting)
    except:
        print ('Error reading textgrid file: '  + tginpath)
        print ('Please ensure that the textgrid file is encoded in UTF-8 or the correct encoding.')
        quit()

    #os.remove(tmp_script_path)
    #tier_names = tg.get_tier_names()
    #if tier_name not in tier_names:
        #print ('Error grabbing tier with name: '  + tier_name)
        #print ('Please check the tier name is correct.')
        #quit()
    #try:
    #tg_tier = tg.get_tier_by_name(tier_name)
    return tg



output_main_dir = path + ''
#for directory in directories:
directory = path + ''
#directory = '/home/kevintang/Dropbox/Tang_Shaw/ChineseHomophone/Codes/ProcessRecordings/Noise/data/target/high_low_1_compressed'

bits = os.path.split(directory)
output_sub_dir = os.path.join(output_main_dir,bits[1])
if not os.path.exists(output_sub_dir):
    os.makedirs(output_sub_dir)


noise_path = '/media/kevintang/Seagate Expansion Drive/Kevin_Tang_Main/ZJU_SPIN_Mandarin/Processing/Step7_noise/60snoise.by60schunk.full.corpus/SpeechShapedNoise.wav'

snrdBTarget = 5
signal_presence = True
##if true we replace the target words with silence
if signal_presence == False:
    snrdBTarget = -65
    ###also we set noise to 70 and signal to 0

noise_buffer = 0 # positive to take into account of coarticulation?
count_buffered_signal = False #if True, then buffered region plus the target word will be used to compute Signal dB, if not only the target word will be used.
scale_or_sample_noise = 'sample'

files = os.listdir(directory)

wavs = [i for i in files if u'.wav' in i]
tgs = [i for i in files if u'.TextGrid' in i]
labels_to_skip = [u'第',u'一',u'个',u'词',u'是',u'二',u'行',u'吗']


condition = str(snrdBTarget).replace('-','neg').replace('+','pos') + 'dB'
output_dir = os.path.join(output_sub_dir,condition)
output_noise_dir = output_dir + '_noise'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(output_noise_dir):
    os.makedirs(output_noise_dir)
output_files = os.listdir(output_dir)
output_noise_files = os.listdir(output_noise_dir)

import random,math
def get_random_start_end(desired_duration,noise_start_time,noise_end_time):
    #make sure to back the end time to at least the desired duration
    start_time_ms = random.randint(0,int(round((noise_end_time-desired_duration)*1000)))
    start_time = start_time_ms/1000
    end_time = start_time + desired_duration
    if end_time > noise_end_time:
	print ('strange')
	quit()
    return (start_time,end_time)

for wav in wavs:
    wav_path = os.path.join(directory,wav)
    tg_filename = wav.replace('.wav','.TextGrid')
    if tg_filename not in tgs:
	quit()
    tg_path = os.path.join(directory,tg_filename)

    #wav_path = '/home/kevintang/Dropbox/Tang_Shaw/ChineseHomophone/Codes/ProcessRecordings/Noise/data/temp/recording1.1.wav'
    #tg_path = '/home/kevintang/Dropbox/Tang_Shaw/ChineseHomophone/Codes/ProcessRecordings/Noise/data/temp/recording1.1.TextGrid'
    #

    wav_dir, wav_filename = os.path.split(wav_path)

    wav_filename_core,ext = os.path.splitext(wav_filename)
    wav_filename_core_new = wav_filename_core + '.' + str(snrdBTarget).replace('-','neg').replace('+','pos') + 'dB'
    output_wav_path = os.path.join(output_dir,wav_filename_core_new + '.wav')
    output_noise_wav_path = os.path.join(output_noise_dir,wav_filename_core_new + '.noise.wav')
    output_gap_wav_path = os.path.join(output_noise_dir,wav_filename_core_new + '.gap.wav')

    if wav_filename_core_new + '.wav' in output_files and wav_filename_core_new + '.noise.wav' in output_noise_files:
	#we can skip
	continue


    noise = parselmouth.Sound(noise_path)
    sound = parselmouth.Sound(wav_path)
    rec_tgt = read_textgrid(tg_path,True,'UTF-8')
    #rec_tgt = read_textgrid(tg_path,include_empty_intervals_para=True)

    tgt_dur = rec_tgt.end_time - rec_tgt.start_time
    #sound_dur = sound.get_total_duration()
    sound_dur = sound.end_time - sound.start_time
    print sound_dur - tgt_dur
    if sound_dur != tgt_dur:
	print 'length not match'

    wordtier = rec_tgt.get_tier_by_name(u'words')

    noise_sampFreq = call(noise,'Get sampling frequency')
    targetsampFreq = call(sound,'Get sampling frequency')

    sound_start_time = sound.start_time
    sound_end_time = sound.end_time
    #sound_start_time = rec_tgt.start_time
    #sound_end_time = rec_tgt.end_time
    noise_start_time = noise.start_time
    noise_end_time = noise.end_time

    target_word_store = []
    for nr,word_ in enumerate(wordtier):
	if word_.text == '':
	    continue
	if word_.text in labels_to_skip:
	    continue
	print (word_.text)
	target_word_store.append(word_)

    if signal_presence == False:

	time_stamps = []
	for target_word_ in target_word_store:
	    start_time = target_word_.start_time
	    end_time = target_word_.end_time
	    time_stamps.append((start_time,end_time))

	#create silence
	silence_signal_store = []
	for nr, time_stamp in enumerate(time_stamps):
	    if nr == 0:
		if time_stamp[0] > 0:
		    silent_start_time = sound_start_time
		    silent_end_time = time_stamp[0]
		    silence_signal_store += [('signal',silent_start_time,silent_end_time),
		                               ('sil',time_stamp[0],time_stamp[1])]
		else:
		    silence_signal_store += [None,
		                               (sil,time_stamp[0],time_stamp[1])]
	    else:
		silent_start_time = time_stamps[nr-1][1]
		silent_end_time = time_stamp[0]

		silence_signal_store += [('signal',silent_start_time,silent_end_time),
	                                           ('sil',time_stamp[0],time_stamp[1])]
	#add final signal if any
	if silence_signal_store[-1][-1] < sound_end_time:
	    silence_signal_store.append(('signal',silence_signal_store[-1][-1],sound_end_time))

	#grab signals and generate silence
	mod_sound_signal_store = []
	for silence_signal_store_ in silence_signal_store:
	    signaltype = silence_signal_store_[0]
	    signal_start_time = silence_signal_store_[1]
	    signal_end_time = silence_signal_store_[2]

	    if signaltype == 'sil':
		silence_dur = signal_end_time-signal_start_time
		#silence = call("Create Sound as pure tone", 'silence', 1, 0, silence_dur,targetsampFreq, 1e-008, 0.1, 0.01, 0.01)
		#Create Sound as pure tone... sil 1 0 buffVal sampFreq 1e-008 0.1 0.01 0.01
		silence = call("Create Sound from formula", 'silence', 'Mono', 0, silence_dur,targetsampFreq, "0")
		mod_sound_signal_store.append(silence)

		#here we can get the actual sound's length and pad it
		#non_sil_sound = sound.extract_part(from_time=signal_start_time,to_time=signal_end_time, preserve_times=False)
		#if len(non_sil_sound.values[0]) != len(silence.values[0]):
		    #print len(silence.values[0])
		    #print len(non_sil_sound.values[0])
		    #print len(silence.values[0]) - len(non_sil_sound.values[0])
		    #print ('Strange')
		    #quit()

	    elif signaltype == 'signal':
		signal_sound = sound.extract_part(from_time=signal_start_time,to_time=signal_end_time, preserve_times=False)
		mod_sound_signal_store.append(signal_sound)



	original_sound = sound
	sound = call(mod_sound_signal_store,'Concatenate')
	#print original_sound.values[1]
	#print original_sound
	#sound.values[0] = sound.values[0][0:-1]
	#sound.values[0] = original_sound.values[0]
	#sound_new = sound.extract_part(from_time=signal_start_time,to_time=signal_end_time, preserve_times=False)
	#if original_sound.end_time < sound.end_time:
	    #sound = sound.extract_part(from_time=sound.start_time,to_time=original_sound.end_time, preserve_times=False)
	#if len(original_sound.values[0]) != len(sound.values[0]):
	    ##44100*2.507755102040816
	    #print len(sound.values[0])
	    #print len(original_sound.values[0])
	    #print sound.get_total_duration()
	    #print original_sound.get_total_duration()
	    #print len(sound.values[0]) - len(original_sound.values[0])
	    #print ('Strange')
	    #continue
	    #quit()

	sound.save(output_gap_wav_path, "WAV")


    #get the times for the two labels

    if len(target_word_store) != 1:
	quit()

    target_word_ = target_word_store[0]
    #create the noise with the right dB and duration
    #store them for later
    start_time = target_word_.start_time
    end_time = target_word_.end_time

    #why do we do this? Well, the computation of the dB ratio depends on the signal of the target portion
    #if we include this then we are taking into account of the buffered portion of the signal.
    #if we don't then we are using the only target word as the dB signal baseline.

    #if count_buffered_signal:
    #
    start_time_mod = start_time
    end_time_mod = end_time
    if noise_buffer>0:
	#if buffer overreach start time, then set to sound start time
	if (start_time - noise_buffer) < 0:
	    start_time_mod = 0
	else:
	    start_time_mod = start_time - noise_buffer
	#if buffer overreach end time, then set to sound end time
	if (end_time + noise_buffer) > sound_end_time:
	    end_time_mod = sound_end_time
	else:
	    end_time_mod = end_time + noise_buffer

    #resample noise file if necessary
    if noise_sampFreq != targetsampFreq:
	noise = call(noise,'Resample',targetsampFreq,50)

    #rescale duration for noise
    #ask Jason if we should crop instead
    durNoise = call(noise,'Get total duration')
    if count_buffered_signal:
	targetwordsound = sound.extract_part(from_time=start_time_mod,to_time=end_time_mod, preserve_times=False)
	#durTarget = call(targetwordsound,"Get total duration")
    else:
	targetwordsound = sound.extract_part(from_time=start_time,to_time=end_time, preserve_times=False)
	#durTarget = call(targetwordsound,"Get total duration") + 2*noise_buffer

    durTarget = end_time_mod - start_time_mod

    #use sound_dur instead of durtarget, since we have padding
    durTarget = sound_dur

    if scale_or_sample_noise == 'scale':
	# Get the duration ratio between the target file (+ silence buffers) and the noise.
	ratio=durTarget/durNoise
	noise_time_scaled = call(noise, "Lengthen (overlap-add)",75,600,ratio)
    else:
	noise_random_start_time,noise_random_end_time = get_random_start_end(durTarget,noise_start_time,noise_end_time)
	noise_time_scaled = noise.extract_part(from_time=noise_random_start_time,to_time=noise_random_end_time, preserve_times=False)
	if noise_random_start_time+0.5 > 60 or noise_random_end_time-0.5 < 0:
	    print 'outside the range of noise'
	    quit()
	if (noise_random_start_time+0.5) > (noise_random_end_time-0.5):
	    print 'something is wrong'
	    quit()
	noise_time_durtarget_scaled = noise.extract_part(from_time=noise_random_start_time+0.5,to_time=noise_random_end_time-0.5, preserve_times=False)
	#print (noise_random_start_time,noise_random_end_time)

    #rescale noise dB
    dBSig = call(targetwordsound,'Get intensity (dB)')
    #targetwordsound.save('/home/kevintang/Dropbox/Tang_Shaw/ChineseHomophone/Codes/ProcessRecordings/Noise/data/target_manipulation/high_low_wav_tg_compressed/neg70dB/temp.wav', "WAV")
    #if  dBSig==
    print 'dBSig_raw:' + str(dBSig)
    print 'dBNoi_raw_with_padding:' + str(call(noise_time_scaled,'Get intensity (dB)'))
    print 'dBNoi_raw_targetonly:' + str(call(noise_time_durtarget_scaled,'Get intensity (dB)'))
    if math.isnan(dBSig) or dBSig < 0:
	dBSig = 0

	#if silence signal, use the original noise?
    if signal_presence == False:
	if dBSig != 0:
	    print 'estimating intensity for silence doesnt always give zero/nan'
	dBSig = 0

    #else:
    dBnoi = dBSig - snrdBTarget
    print 'dBSig:' + str(dBSig)
    print 'dBnoi:' + str(dBnoi)

    pre_scaled_noise_dB = call(noise_time_scaled,'Get intensity (dB)')
    pre_scaled_noise_durtarget_dB = call(noise_time_durtarget_scaled,'Get intensity (dB)')
    call(noise_time_scaled,'Scale intensity',dBnoi)
    call(noise_time_durtarget_scaled,'Scale intensity',dBnoi)
    post_scaled_noise_dB = call(noise_time_scaled,'Get intensity (dB)')
    post_scaled_noise_durtarget_dB = call(noise_time_durtarget_scaled,'Get intensity (dB)')

    if pre_scaled_noise_dB == post_scaled_noise_dB:
	print 'noise rescale intensity didnt work'
	quit()

    #print pre_scaled_noise_dB
    #print post_scaled_noise_dB

    #print pre_scaled_noise_durtarget_dB
    #print post_scaled_noise_durtarget_dB

    #target_word_noise_store = []
    #for target_word_ in target_word_store:

	#target_word_noise_store.append(((start_time_mod,end_time_mod),noise_time_scaled))

    #Here we create a sound that is silence + noise + silence + noise



    #time_stamps = []
    #for target_word_noise_ in target_word_noise_store:
	#target_word_ = target_word_noise_[0]
	#target_word_start_time = target_word_[0]
	#target_word_end_time = target_word_[1]
	#target_noise_ = target_word_noise_[1]

	#time_stamps.append((target_word_start_time,target_word_end_time))

    ##create silence
    #silence_noise_store = []
    #for nr, time_stamp in enumerate(time_stamps):
	#if nr == 0:
	    #if time_stamp[0] > 0:
		#silent_start_time = sound_start_time
		#silent_end_time = time_stamp[0]
		#silence_noise_store += [('sil',silent_start_time,silent_end_time),
	                                   #(('noise',nr),time_stamp[0],time_stamp[1])]
	    #else:
		#silence_noise_store += [None,
	                                   #(('noise',nr),time_stamp[0],time_stamp[1])]
	#else:
	    #silent_start_time = time_stamps[nr-1][1]
	    #silent_end_time = time_stamp[0]

	    #silence_noise_store += [('sil',silent_start_time,silent_end_time),
	                                       #(('noise',nr),time_stamp[0],time_stamp[1])]
    ##add final silence if any
    #if silence_noise_store[-1][-1] < sound_end_time:
	#silence_noise_store.append(('sil',silence_noise_store[-1][-1],sound_end_time))

    #signal_store = []
    #for silence_noise_store_ in silence_noise_store:
	#signaltype = silence_noise_store_[0]
	#signal_start_time = silence_noise_store_[1]
	#signal_end_time = silence_noise_store_[2]

	#if signaltype == 'sil':
	    #silence_dur = signal_end_time-signal_start_time
	    #silence = call("Create Sound from formula", 'silence', 'Mono', 0, silence_dur,targetsampFreq, "0")
	    #signal_store.append(silence)


	#else:
	    #targetnoise = target_word_noise_store[signaltype[1]][1]
	    #signal_store.append(targetnoise)

    #silencenoisecombined = call(signal_store,'Concatenate')


	#quit()
    if sound.end_time < noise_time_scaled.end_time:
	print sound.end_time
	print noise_time_scaled.end_time
	print (sound.end_time-noise_time_scaled.end_time)
	noise_time_scaled = noise_time_scaled.extract_part(from_time=noise_time_scaled.start_time,to_time=sound.end_time, preserve_times=False)
    elif sound.end_time > noise_time_scaled.end_time:
	print sound.end_time
	print noise_time_scaled.end_time
	print (sound.end_time-noise_time_scaled.end_time)
	sound = sound.extract_part(from_time=sound.start_time,to_time=noise_time_scaled.end_time, preserve_times=False)



    if round(noise_time_scaled.get_total_duration(),10) != round(sound.get_total_duration(),10):
	print wav
	print noise_time_scaled.get_total_duration()
	print sound.get_total_duration()
	print ('Strange')
	#continue
	quit()

    if len(noise_time_scaled.values[0]) != len(sound.values[0]):
	print wav
	print len(noise_time_scaled.values[0])
	print len(sound.values[0])
	print len(noise_time_scaled.values[0]) - len(sound.values[0])
	print ('Strange')
	continue
	#quit()
    #if abs(len(noise_time_scaled.values[0]) - len(sound.values[0])) > 1:
	#print ('Too large a difference')
	#quit()


    targetwithnoise = parselmouth.Sound(sound.values + noise_time_scaled.values, sampling_frequency=targetsampFreq)

    targetwithnoise.save(output_wav_path, "WAV")
    noise_time_scaled.save(output_noise_wav_path, "WAV")

##print signal_store[0].get_total_duration()
##print signal_store[1].get_total_duration()
##print new.get_total_duration()

##comment What volume (dB) should serve as the baseline for determining the noise volume (i.e. what is the volume in dB of the signal)?
	##positive dBSig 74.76517784427243
##comment What signal-to-noise ratio (in dB) would you like?
	##real snrdBTarget -8
##We need to get intensity of the target word
##dBSig = 60
##snrdBTarget = 0

##intensV = Get intensity (dB)
#durNoise = call(noise,'Get total duration')
#start_time = 0.63
#end_time = 1.03

#sampFreq = call(sound,'Get sampling frequency')



#targetwordsound = sound.extract_part(from_time=start_time,to_time=end_time, preserve_times=False)
#dBSig = call(targetwordsound,'Get intensity (dB)')
#target_word_sound_sampFreq = call(targetwordsound,'Get sampling frequency')
#noise_sampFreq = call(noise,'Get sampling frequency')

#if noise_sampFreq != target_word_sound_sampFreq:
    #noise = call(noise,'Resample',sampFreq,50)

#targetwordsound_dur = call(targetwordsound,"Get total duration")

#durTarget=end_time-start_time

## Get the duration ratio between the target file + silence buffers and the noise.
#ratio=durTarget/durNoise

## Adjust the duration of noise to match the target file + silence buffers.
##select Sound 'noise$'
##Lengthen (overlap-add)... 75 600 'ratio'
##noiseL$=selected$("Sound")
#noise_time_scaled = call(noise, "Lengthen (overlap-add)",75,600,ratio)

## Adjust the amplitude of the newly created noise file.
## Now scale the intensity
## https://en.wikipedia.org/?title=Signal-to-noise_ratio#Decibels
## SNR(dB) = 20*log_10(RMS_sig/RMS_noi)
## SNR/20 = log_10(RMS_sig/RMS_noi)
## 10^(SNR/20) = RMS_sig/RMS_noi
## RMS_noi = RMS_sig/(10^(SNR/20))

##rmsNoi = rmsSig/(10^(snrTarget/20))
#dBnoi = dBSig - snrdBTarget

#pre_scaled_noise_dB = call(noise_time_scaled,'Get intensity (dB)')
#call(noise_time_scaled,'Scale intensity',dBnoi)
#post_scaled_noise_dB = call(noise_time_scaled,'Get intensity (dB)')
#print pre_scaled_noise_dB
#print post_scaled_noise_dB
##w=noise_time_scaled.scale_intensity(80)
##sound.get_total_duration

#targetwithnoise = parselmouth.Sound(targetwordsound.values + noise_time_scaled.values, sampling_frequency=target_word_sound_sampFreq)

#targetwithnoise.save('/home/kevintang/Dropbox/Tang_Shaw/ChineseHomophone/Codes/ProcessRecordings/Noise/data/temp/temp.mixed.wav', "WAV")

#targetwordsound.name = 'one'
#noise_time_scaled.name = 'two'
#base = call("Create Sound from formula", 'base', 'Mono', 0, durTarget,target_word_sound_sampFreq, "0")
#praat_script = ["Create Sound from formula... base Mono 0 "+str(durTarget)+" "+str(soundonesampfreq)+" 0",
 #"select Sound base",
 #"Formula... self [col] + Sound_one [col]",
 #"Formula... self [col] + Sound_two [col]"]
#targetwithnoise2list=parselmouth.praat.run([targetwordsound,noise_time_scaled], '\n'.join(praat_script))
#targetwithnoise2 = targetwithnoise2list[0]
#targetwithnoise2.save('/home/kevintang/Dropbox/Tang_Shaw/ChineseHomophone/Codes/ProcessRecordings/Noise/data/temp/temp.mixed2.wav', "WAV")

#soundone = parselmouth.Sound(wav_path)
#soundone.name = 'one'
#soundonedur = call(soundone,"Get total duration")
#soundonesampfreq = call(soundone,'Get sampling frequency')
#base = call("Create Sound from formula", 'base', 'Mono', 0, soundonedur,soundonesampfreq, "0")
#praat_script = ["Create Sound from formula... base Mono 0 "+str(soundonedur)+" "+str(soundonesampfreq)+" 0",
 #"select Sound base",
 #"Formula... self [col] + Sound_one [col]"]
#w=parselmouth.praat.run([soundone], '\n'.join(praat_script))



#select Sound 'noiseFile$'
#baseplusone = call(base,"Formula","self [col] + Sound_one [col]")
#Aha, I see `soundone = parselmouth.Sound(wav_path)`
#`soundone.name = 'one'`
#`soundonedur = call(soundone,"Get total duration")`
#`soundonesampfreq = call(soundone,'Get sampling frequency')`
#`base = call("Create Sound from formula", 'base', 'Mono', 0, soundonedur,soundonesampfreq, "0")`
#`baseplusone = call(base,"Formula","self [col] + Sound_one [col]")`
#call('select all')
#self [col] + Sound_noise [col]

#sound_one.name = "ONE"
#parselmouth.praat.run([sound_one], a_string_with_your_praat_script)




#manipulation = call(sound, "To Manipulation", 0.001, 75, 600)
#duration_tier = call(manipulation, "Extract duration tier")
#call(duration_tier, "Add point", sound.xmin, 1)
#call(duration_tier, "Add point", hf_int.start_time-0.000001, 1)
#call(duration_tier, "Add point", hf_int.start_time, scale_target_ratio)
#call(duration_tier, "Add point", hf_int.end_time, scale_target_ratio)
#call(duration_tier, "Add point", hf_int.end_time+0.000001, 1)
#call(duration_tier, "Add point", sound.xmax, 1)
#call([duration_tier, manipulation], "Replace duration tier")
#sound_octave_up = call(manipulation, "Get resynthesis (overlap-add)")
#sound_octave_up.save(out_wav_path, "WAV")
