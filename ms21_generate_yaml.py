from multiprocessing import Process
from multiprocessing.dummy import Pool as ThreadPool
import yaml
import re
import os, errno
import librosa
import soundfile as sf
import numpy as np
import pandas as pd
import json
from pydub import AudioSegment
import pyloudnorm as pyln
import shutil
import sys

# Reference: https://github.com/SiddGururani/mixing_secrets/blob/master/generate_yaml.py


def gen_yaml(directory, move_raw = True):
    csv_anno = pd.read_csv(anno_file_path)
    hierarchy_file = json.load(open(hierarchy_path, 'r'))
    
    track_df = csv_anno.loc[csv_anno['Music_Title']==directory]
    artist = track_df['Artist'].values[0]
    song = track_df['Track_Name'].values[0]
    ID = directory
    yaml_obj = init_medley_yaml()
    yaml_obj['csv_anno_path'] = anno_file_path
    yaml_obj['hieararchy_file_path'] = hierarchy_path
    yaml_obj['artist'] = artist
    yaml_obj['genre'] = track_df['Sub_Genre'].values[0]
    yaml_obj['title'] = song
    if track_df["Vocal_Quality"].values[0] == 1 :
        yaml_obj['vocal_has_bleed'] = 'no'  
    else: 
        yaml_obj['vocal_has_bleed'] = 'yes' # check vocal has bleed or not

    vocal = np.any([i != '[]' for i in track_df.T.loc["Lead_Vocal":"Backing_Vocal"].values] )

    if vocal:
        yaml_obj['instrumental'] = 'no' 
    else:
        yaml_obj['instrumental'] = 'yes' 
    yaml_obj['mix_filename'] = ID+'_MIX.wav'
    yaml_obj['origin'] = 'Mixing Secrets'
    yaml_obj['raw_dir'] = ID+'_RAW'
    yaml_obj['stem_dir'] = ID+'_STEMS'
    yaml_obj['version'] = '3.0'
    make_dir(os.path.join(save_path, ID))
    make_dir(os.path.join(save_path, ID, ID+'_RAW'))
    make_dir(os.path.join(save_path, ID, ID+'_STEMS'))
    make_dir(os.path.join(save_path, ID, ID+'_STEMS', 'Inst'))
    make_dir(os.path.join(save_path, ID, ID+'_STEMS', 'MUSDB'))
    # if os.path.isfile(os.path.join(save_path, ID, ID+'_METADATA.yaml')):
    #     # Write code here to fix the drum tracks by adding the room mic to the drum stem.
    #     print('Metadata exists')
    #     return
    
    # Get all track paths
    all_tracks = os.listdir(os.path.join(base_path, directory))
    all_tracks = [os.path.join(base_path, directory, track) for track in all_tracks if track.endswith('.wav')]
    
    # Make stems for drums, sfx, loops and synths
    # TODO loudness normalization should be considered
    

    for inst, tracks_name in hierarchy_file["mix"]["track2inst"].items():
        # print(inst, tracks_name)
        make_stem(yaml_obj, os.path.join(save_path, ID, ID+'_STEMS', 'Inst'), os.path.join(base_path, directory), track_df, tracks_name, inst, ID+f'_STEM_Inst_{inst}.wav')
    for stem, inst_name in hierarchy_file["mix"]["inst2stem"].items():
        # print(inst, tracks_name)
        make_stem(yaml_obj, os.path.join(save_path, ID, ID+'_STEMS', 'MUSDB'), os.path.join(save_path, ID, ID+'_STEMS', 'Inst'), track_df, inst_name, stem, ID+f'_STEM_MUSDB_{stem}.wav')
    # create mix file
    make_mix(yaml_obj, os.path.join(save_path, ID, ID+'_STEMS', 'MUSDB'), os.path.join(save_path, ID), yaml_obj['mix_filename'])

    # Move all raw files to RAW folder. Default False
    if move_raw == True:
        copy_raw_tracks(all_tracks, os.path.join(save_path, ID, ID+'_RAW'))
    
    # Write YAML
    f = open(os.path.join(save_path, ID, ID+'_METADATA.yaml'),'w')
    yaml.dump(yaml_obj, f, default_flow_style=False)
    f.close()
    
def init_medley_yaml():
    object = {}
    object['album'] = ''
    object['artist'] = ''
    object['composer'] = ''
    object['excerpt'] = ''
    object['genre'] = ''
    object['has_bleed'] = ''
    object['instrumental'] = ''
    object['mix_filename'] = ''
    object['mix_integrated_loudness']  = ''
    object['origin'] = ''
    object['producer'] = ''
    object['raw_dir'] = ''
    object['stem_dir'] = ''
    object['stems_Inst'] = {}
    object['stems_MUSDB'] = {}
    object['title'] = ''
    object['version'] = ''
    object['website'] = ''
    object['csv_anno_path'] = ''
    object['hieararchy_file_path'] = ''

    return object
    

def make_mix(obj,stems_path, directory_path, file_name):
    # get all stem tracks
    tracks = [os.path.join(stems_path, i) for i in os.listdir(stems_path)]
    # print(tracks)
    
    if len(tracks) == 0:
        print('Empty track list sent for mix creation')
        return

    y, sr = librosa.load(tracks[0], sr=None)
    for i in range(len(tracks) - 1):
        y_add = librosa.load(tracks[i+1], sr=None)[0]
        l = len(y)
        l_add = len(y_add)
        if l > l_add:
            y_add = np.pad(y_add, (0, l - l_add), 'constant')
        elif l < l_add:
            y = np.pad(y, (0, l_add - l), 'constant')
        y += y_add
    y, loudness, types = loudness_normalization(y, sr, 'mix', -25)
    obj['mix_integrated_loudness'] = types + f'{loudness:.4f}' + ' LUFS'
    path_to_write = os.path.join(directory_path, file_name)
    sf.write(path_to_write, y, sr)
    
    print("Successfully output mix.wav", path_to_write)

def make_stem(obj, stems_path, directory_path, track_df, inst_names, stem_inst_name, file_name):
    tracks = []
    if 'MUSDB' in stems_path:
        # Add stem to yaml object
        count = len(obj['stems_MUSDB'])
        if count+1 < 10:
            count = '0'+str(count+1)
        else:
            count = str(count+1)
        obj['stems_MUSDB']['S'+count] = {}
        obj['stems_MUSDB']['S'+count]['component'] = ''
        obj['stems_MUSDB']['S'+count]['filename'] = file_name
        obj['stems_MUSDB']['S'+count]['instrument'] = stem_inst_name
        obj['stems_MUSDB']['S'+count]['raw'] = {}
        for i, name in enumerate(inst_names):
            for wav in os.listdir(directory_path):
                # print(f"name: {name}; wav: {wav}")
                if wav.split('_Inst_')[-1]  == name + '.wav':
                    # print(f"adding {wav} into stem {stem_inst_name}")
                    tracks.append(os.path.join(directory_path, wav))
                    if i < 10:
                        raw_count = '0'+str(i+1)
                    else:
                        raw_count = str(i+1)
                    obj['stems_MUSDB']['S'+count]['raw']['R'+raw_count] = {}
                    obj['stems_MUSDB']['S'+count]['raw']['R'+raw_count]['filename'] = wav
                    obj['stems_MUSDB']['S'+count]['raw']['R'+raw_count]['instrument'] = name
        if len(tracks) == 0:
            # print('Empty track list sent for stem creation')
            # delete the empty stem dict
            obj['stems_MUSDB'].pop('S'+count)
            return               
    else:
                # Add stem to yaml object
        count = len(obj['stems_Inst'])
        if count+1 < 10:
            count = '0'+str(count+1)
        else:
            count = str(count+1)
        obj['stems_Inst']['S'+count] = {}
        obj['stems_Inst']['S'+count]['component'] = ''
        obj['stems_Inst']['S'+count]['filename'] = file_name
        obj['stems_Inst']['S'+count]['instrument'] = stem_inst_name
        obj['stems_Inst']['S'+count]['raw'] = {}
        for idx, name in enumerate(inst_names):
            wav_lists = track_df[name].tolist()[0]
            if wav_lists == '[]':
                continue
            for i, wav in enumerate(wav_lists.strip('[]').split(', ')):
                wav = wav.strip("'")
                if i < 10:
                    raw_count = '0'+str(i+1)
                else:
                    raw_count = str(i+1)
                obj['stems_Inst']['S'+count]['raw']['R'+raw_count] = {}
                obj['stems_Inst']['S'+count]['raw']['R'+raw_count]['filename'] = wav
                obj['stems_Inst']['S'+count]['raw']['R'+raw_count]['instrument'] = name
            
                tracks.append(os.path.join(directory_path, wav))

        if len(tracks) == 0:
            # print('Empty track list sent for stem creation')
            # delete the empty stem dict
            obj['stems_Inst'].pop('S'+count)
            return
        

    y, sr = librosa.load(tracks[0], sr=None)
    for i in range(len(tracks) - 1):
        y_add = librosa.load(tracks[i+1], sr=None)[0]
        l = len(y)
        l_add = len(y_add)
        if l > l_add:
            y_add = np.pad(y_add, (0, l - l_add), 'constant')
        elif l < l_add:
            y = np.pad(y, (0, l_add - l), 'constant')
        y += y_add
    y, loudness, types = loudness_normalization(y, sr, stem_inst_name, -25)
    if 'MUSDB' in stems_path:
        obj['stems_MUSDB']['S'+count]['loudness'] = types + f'{loudness:.4f}' + ' LUFS'
    else:
        obj['stems_Inst']['S'+count]['loudness'] =types + f'{loudness:.4f}' + ' LUFS'
    path_to_write = os.path.join(stems_path, file_name)
    sf.write(path_to_write, y, sr)
    
    

         
def add_rem_tracks(obj, save_path, rem_tracks):
    for i, track in enumerate(rem_tracks):
        track_name = os.path.split(track)[1]
        inst_name = get_instrument_from_track_name(track_name)
        make_stem(obj, save_path, [track], inst_name, track_name)
        
        
def get_instrument_from_track_name(track_name):
    track_name = track_name.strip('.wav')
    regex = r"(\d*_)([a-zA-Z\D]*)"
    match = re.findall(regex, track_name)
    inst_name = '_'.join([x for (_,x) in match])
    return inst_name
        
def find_all_instruments(base_path):
    instruments = set()
    regex = r"(\d*_)([a-zA-Z\D]*)"
    for x in os.listdir(base_path):
        for track in os.listdir(os.path.join(base_path, x)):
            if track.endswith(".wav"):
                try:
                    track_name = track.strip('.wav')
                    match = re.findall(regex, track_name)
                    inst_name = '_'.join([x for (_,x) in match])
                    instruments.add(inst_name)
                except:
                    print(track)
    return instruments

def copy_raw_tracks(tracks, destination):
    for track in tracks:
        track_name = os.path.split(track)[1]
        shutil.copyfile(track, os.path.join(destination, track_name))

def make_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
def match_target_amplitude(root, file, output_path, target_dBFS=-20):
    if file.endswith('.wav'):
        path = os.path.join(root,file)
        dir = root.split('\\')[-1]
        sound = AudioSegment.from_file(path)
        change_in_dBFS = target_dBFS - sound.dBFS
        # loudness normalization over this audio clip
        # TODO normailization over chunks, 
        # set up a threshold to filter out silent clips and only consider the chunks above threshold
        audio = sound.apply_gain(change_in_dBFS)
        os.makedirs(os.path.join(output_path,dir),exist_ok=True)
        audio.export(os.path.join(output_path,dir,file), format="wav")
        print("Suceessfully normalized ", file)

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
    
root_path = sys.argv[1] # '/media/felix/dataset/ms21/train' need to contain the subfolder

out_path = sys.argv[2] #  '/media/felix/dataset/ms21_DB
# print(output_path)
os.makedirs(out_path,exist_ok=True)

anno_file_path = './mixing_secret_dataset_final_name.csv'
hierarchy_path = './hierarchy.json'



pool = ThreadPool(int(sys.argv[3]))
arg_list = []
for split in os.listdir(root_path):
    base_path = os.path.join(root_path, split)
    save_path = os.path.join(out_path,split)
    os.makedirs(save_path, exist_ok=True)
    with pool:
        pool.map(gen_yaml, [i for i in os.listdir(base_path)])
