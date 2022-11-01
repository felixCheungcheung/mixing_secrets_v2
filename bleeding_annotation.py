from numpy import NaN
import yaml
import os
import sys
import pandas as pd

"""
Manually annotate bleeding information for each multi-track,
Semi-automatically group multi-tracks to instrument labels (70): track2inst level grouping, based on actual music content of each track.
"""
dataset_path = "E:\\ADDMS21_DB" # sys.argv[1]
save_path = "E:\\ADD_Bleed_annotation"
csv_path = 'MTG_2021_MASTER_THESIS\\mixing_secret_dataset_annotation_with_comment.csv'
csv_anno = pd.read_csv(csv_path)
drum_inst_list = ["Drum_Kick", "Drum_Snare", "Drum_HiHat", "Drum_Cymbals", "Drum_Tom"]
bleeding_dict = {"Track2inst": {}}

for split in os.listdir(dataset_path):
    if split != 'TEMP':
        continue
    for song in os.listdir(os.path.join(dataset_path, split)):
        track_list = os.listdir(os.path.join(dataset_path,split, song, song+"_RAW"))
        track_df = csv_anno.loc[csv_anno['Music_Title']==song]
        if track_df['Drums_Clean'].values[0] == 0:
            drum_bleed = 'Yes'
        else:
            drum_bleed = 'No'
        
        if track_df['Clean'].values[0] == 0:
            other_bleed = 'Yes'
        else:
            other_bleed = 'No'
        comment = track_df['Comment'].values[0]

        # To get 70 instrument and its tracks, to form a dict
        for inst_name in track_df.columns[5:-6]:
            bleeding_dict["Track2inst"][inst_name] = {}
            # process not drum instrument:
            if inst_name not in drum_inst_list:
                wav_list = track_df[inst_name].tolist()[0]
                if wav_list !='[]':
                    for i, wav in enumerate(wav_list.strip('[]').split(', ')):
                        track_path = wav.strip("'")
                        wav_dict = {"Track_path": os.path.join(song, song+"_RAW", track_path), "Bleeding": other_bleed, "Bleeding_Instrument": '', "Comment": ''}
                        bleeding_dict["Track2inst"][inst_name][track_path] = wav_dict
            else:
                wav_list = track_df[inst_name].tolist()[0]
                if wav_list !='[]':
                    for i, wav in enumerate(wav_list.strip('[]').split(', ')):
                        track_path = wav.strip("'")
                        b_instrument = ''
                        if isinstance(comment, str) :
                            if "All Drum tracks leak to each other." in comment:
                                # print(comment)
                                b_instrument = 'Drum_Overheads'
                            
                        wav_dict = {"Track_path": os.path.join(song, song+"_RAW", track_path), "Bleeding": drum_bleed, "Bleeding_Instrument": b_instrument, "Comment": ''}
                        bleeding_dict["Track2inst"][inst_name][track_path] = wav_dict

        # save bleeding_annotation to somewhere
        json_dir = os.path.join(save_path, split)
        os.makedirs(json_dir, exist_ok=True)
        with open(os.path.join(json_dir,song+"_track2inst_bleeding_info.yaml"), 'w') as f1:
            yaml.dump(bleeding_dict, f1, default_flow_style=False, sort_keys=False)
        f1.close()