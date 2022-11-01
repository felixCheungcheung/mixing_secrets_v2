from logging import root
import os
import soundfile as sf
import pyloudnorm as pyln
import numpy as np
from scipy.signal import correlate
from scipy.signal import stft
import sys

# For better automatically generated backing_vocal and lead_vocal inst stems
# track2inst 


def loudness_normalization(data, rate, stem_inst_name, target_loudness=-20.0):

    if stem_inst_name in ['nontonal_percussion', 'drum_set']:
        # peak normalize audio to -1 dB
        normalized_audio = pyln.normalize.peak(data, -1.0)
        meter = pyln.Meter(rate) # create BS.1770 meter
        return normalized_audio, meter.integrated_loudness(normalized_audio), 'PEAK'
    else:
        # measure the loudness first 
        meter = pyln.Meter(rate) # create BS.1770 meter
        loudness = meter.integrated_loudness(data)
        normalized_audio = pyln.normalize.loudness(data, loudness, target_loudness)
        return normalized_audio, meter.integrated_loudness(normalized_audio), 'INTEGRATED'

def correlation(audio1, audio2):
    
    return correlate(audio1, audio2)

def salient_info(X, nfft, threshold):
    with np.errstate(divide='ignore'):
        if len(X.shape) == 3:
            magdB = 20*np.log10(sum(np.abs(X[0][:])))   # only calculate the first channel
        else:
            magdB = 20*np.log10(sum(np.abs(X[:,])))
        print(np.min(magdB))
        mask = (magdB >= threshold)                 # same dimension as X
    return mask

def find_true_stereo(audio, threshold = -60):
    """
    given 2 channel audio 
    return the channel correltation index
    """
    
    # STFT parameters
    nfft = 4096
    eps = np.finfo(np.float).eps
    X = stft(audio.T, nperseg=nfft )[-1] + eps
    (I, F, T) = X.shape
    
    mask = salient_info(X, nfft, threshold)
    
    complex_left = np.angle(X[0]) + eps
    complex_right = np.angle(X[1]) + eps
    
    phase = np.arctan(complex_left / complex_right)
    
    idx = np.mean(phase / (np.pi/4),axis = 0)   # frequency-wise mean
    idx = np.mean(idx, where= mask)             # select frames above threshold
    
    return np.real(idx)

def unit_assign(audio_list, threshold = -60):
    """
    given a list of tracks,
    calculate the similarity, defined by salient chunt, or by music content(F0)
    1) to see whether they are a unit and should be symetrically panned
    tracks of identical performance should be panned, otherwise comb filtering would occur
    e.g. Backing Vocal, acoustic GTR

    return groups of the indexes of the tracks that should be treated together and the index of independent tracks
    """
    
    # STFT parameters
    nfft = 4096

    selected_idx = []
    units = []
    idp_idx = []
    while set(selected_idx) != set(range(len(audio_list))):
        for ref_idx in range(len(audio_list)):
            if ref_idx in selected_idx:
                continue
            unit_idx = []
            selected_idx.append(ref_idx)
            X_ref = stft(audio_list[ref_idx].T, nperseg=nfft )[-1]
            salient_reference = salient_info(X_ref, nfft, threshold)
            uniques_ref, counts_ref = np.unique(salient_reference, return_counts=True)
            count_ref = dict(zip(uniques_ref, counts_ref))
            if False in count_ref.keys():
                if count_ref[False] == len(salient_reference) :
                    print("Found Silent Reference Track")
                    continue
            else:
                print("This track is salient all the time, probably contains leakage")
                idp_idx.append(ref_idx)
                continue

            salient_ref_frame_num = count_ref[True]
            for can_idx in range(len(audio_list)):
                if can_idx in selected_idx:
                    continue
                X = stft(audio_list[can_idx].T, nperseg=nfft )[-1]
                salience = salient_info(X, nfft, threshold)     # for those track that contain leakage, they can be all salient
                uniques_can, counts_can = np.unique(salience, return_counts=True)
                count_can = dict(zip(uniques_can, counts_can))
                if False in count_can.keys():
                    if count_can[False] == len(salience) :
                        print("Found Silent Candidate Track")
                        continue
                else:
                    print("This track is salient all the time, probably contains leakage")
                    continue
                # only consider the salient part of the reference and current audio
                denominator = max(count_can[True], salient_ref_frame_num)
                equal = np.equal(salient_reference, salience) * salient_reference  
                uniques, counts = np.unique(equal, return_counts=True)
                percentages = dict(zip(uniques, counts))
                
                # TODO: musical content criteria
                if percentages[False] == len(equal):
                    continue
                elif percentages[True] * 100.0 / denominator >= 90:
                    unit_idx.append(can_idx)            
                    selected_idx.append(can_idx)
            if unit_idx == []:
                idp_idx.append(ref_idx)
            else:
                unit_idx.append(ref_idx)
                units.append(unit_idx)   # get one pair based on only one reference, assuming that each of them also correlates
            
    return units, idp_idx



def corre_among_tracks():
    """
    TODO
    given one reference track and query tracks
    return the correlation, 
    1) to see whether they are a unit and should be symetrically panned
    tracks of identical performance should be panned, otherwise comb filtering would occur
    e.g. Backing Vocal, acoustic GTR

    2) check polarity for drum multitrack, 
    e.g., kick in & out (using a low pass filter to inspect specific frequency region)
    """
    
    pass

def assign_panning(audio_list, unit_list, stem_inst_name):
    """
    Given a list of mono tracks,
    first assing unit based on similarity,
    then assign panning to each unit to create loudness normalized stereo submixes, 
    then mix all unit together, finally loudness normalization
    """
    units_audio = []
    for unit_idx in unit_list:
        
        num_track = len(unit_idx)
        # naive mix, without considering the correlation between the tracks
        # far left
        left_channel = np.zeros_like(audio_list[0]) 
        right_channel = np.zeros_like(audio_list[0])
        left_count = 0
        right_count = 0
        pan_pair = 0
        total_pair = num_track // 2
        pan_resolution = 90
        for channel_num, audio_idx in enumerate(unit_idx):
            # pan_para = 
            if channel_num % 2 == 0:
                left_channel += audio_list[audio_idx] 
                left_count += 1
                
            # elif channel_num == num_track -1 and num_track != 2:
            #     right_channel = left_channel    
            #     break
            else:
                right_channel += audio_list[audio_idx]
                right_count += 1
                pan_pair += 1
                if channel_num == num_track -2:
                    left_channel += audio_list[unit_idx[num_track-1]]
                    right_channel += audio_list[unit_idx[num_track-1]]
                    break
        units_audio.append(np.array([left_channel, right_channel]).T)
    
    final_audio = np.zeros_like(units_audio[0])
    for i in range(len(units_audio)):
        norm_unit_audio, _, _ = loudness_normalization(units_audio[i], 44100, stem_inst_name, -25)
        final_audio += norm_unit_audio
        
    return final_audio

def inst_spec_mix(track_path_list, stem_inst_name, threshold = -60):
    
    if stem_inst_name == 'backing_vocal':
        mono_audio_pan = []
        st_audio_pan = []
        count = 0
        for path in track_path_list:
            # find true stereo and exclude them from panning
            print(path)
            audio, rate = sf.read(path, always_2d=True)

            if audio.shape[1]==2:
                # define
                if count == 0:
                    count += 1
                    mono2st_submix = np.zeros_like(audio[:,0])
                    mono_submix = np.zeros_like(audio[:,0])
                    norm_mono_submix = np.tile(mono_submix, (2,1)).T
                    norm_mono2st_submix = np.tile(mono2st_submix, (2,1)).T
                    st_submix = np.zeros_like(audio)
                    norm_st_submix = np.zeros_like(audio)

                st_idx = find_true_stereo(audio, threshold)
                # print("Correlation Index: ", st_idx, "Path: ", path)
                if st_idx >=0.98:
                    # print(path, " is Mono")
                    mono_audio_pan.append(audio[:,0]) # only use left channel
                else:
                    st_audio_pan.append(audio)
                    # TODO
                    # frame wise loudness normalization

            else:
                # print("Mono audio",audio.shape)
                mono_audio_pan.append(audio[:,0])
                if count == 0:
                    count += 1
                    mono2st_submix = np.zeros_like(audio[:,0])
                    mono_submix = np.zeros_like(audio[:,0])
                    norm_mono_submix = np.tile(mono_submix, (2,1)).T
                    norm_mono2st_submix = np.zeros_like(norm_mono_submix)
                    st_submix = np.zeros_like(norm_mono_submix)
                    norm_st_submix = np.zeros_like(norm_mono_submix)

        if mono_audio_pan != []:
            units, idp_idx = unit_assign(mono_audio_pan, threshold)
            if units != []:
                mono2st_submix = assign_panning(mono_audio_pan, units, stem_inst_name)
                norm_mono2st_submix, _, _ = loudness_normalization(mono2st_submix, rate, stem_inst_name, -25)

            if idp_idx != []:
                for i in range(len(idp_idx)):
                    mono_submix += mono_audio_pan[idp_idx[i]]
                
                mono_submix = np.tile(mono_submix, (2,1)).T
                norm_mono_submix, _, _ = loudness_normalization(mono_submix, rate, stem_inst_name, -25)
                
        else:
            print("No mono tracks for panning")

        if st_audio_pan != []:
            # print(st_audio_pan.shape)
            for i in range(len(st_audio_pan)):
                st_submix += st_audio_pan[i]
            
            norm_st_submix, _, _ = loudness_normalization(st_submix, rate, stem_inst_name, -25)    
        else:
            print("No stereo tracks")
            

        final_mix = norm_mono_submix + norm_st_submix + norm_mono2st_submix
        norm_final_mix, loudness, types = loudness_normalization(final_mix, rate, stem_inst_name, -25)
  
    return norm_final_mix, loudness, types

if __name__ == "__main__":

    root_path = "E:\\ms21hq_finalDB_44k_norm\\val"
    stem_inst_name = 'backing_vocal'

    for i in os.listdir(root_path):
        track_path_list = []
        for track in os.listdir(os.path.join(root_path, i, i+"_RAW")):
            if 'backingvox' in track.lower():
                track_path_list.append(os.path.join(root_path, i, i+"_RAW",track))
        print(track_path_list)
        
        norm_final_mix, loudness, types = inst_spec_mix(track_path_list, stem_inst_name, -60)
