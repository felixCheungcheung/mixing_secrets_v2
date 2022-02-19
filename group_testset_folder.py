asteroid_validation_tracks = [
    "Actions - One Minute Smile",
    "Clara Berry And Wooldog - Waltz For My Victims",
    "Johnny Lokke - Promises & Lies",
    "Patrick Talbot - A Reason To Leave",
    "Triviul - Angelsaint",
    "Alexander Ross - Goodbye Bolero",
    "Fergessen - Nos Palpitants",
    "Leaf - Summerghost",
    "Skelpolu - Human Mistakes",
    "Young Griffo - Pennies",
    "ANiMAL - Rockshow",
    "James May - On The Line",
    "Meaxic - Take A Step",
    "Traffic Experiment - Sirens",
]
musdb18_test_tracks = [
    'Al James - Schoolboy Facination', 
    'AM Contra - Heart Peripheral', 
    "Angels In Amplifiers - I'm Alright", 
    'Arise - Run Run Run', 
    "Ben Carrigan - We'll Talk About It All Tonight", 
    'BKS - Bulldozer', 
    'BKS - Too Much', 
    'Bobby Nobody - Stitch Up', 
    'Buitraker - Revo X', 
    'Carlos Gonzalez - A Place For Us', 
    'Cristina Vane - So Easy', 
    'Detsky Sad - Walkie Talkie', 
    'Enda Reilly - Cur An Long Ag Seol', 
    'Forkupines - Semantics', 
    'Georgia Wonder - Siren', 
    'Girls Under Glass - We Feel Alright', 
    'Hollow Ground - Ill Fate', 
    'James Elder & Mark M Thompson - The English Actor', 
    "Juliet's Rescue - Heartbeats", 
    "Little Chicago's Finest - My Own", 
    'Louis Cressy Band - Good Time', 
    'Lyndsey Ollard - Catching Up', 
    'M.E.R.C. Music - Knockout', 
    'Moosmusic - Big Dummy Shake', 
    'Motor Tapes - Shore', 
    'Mu - Too Bright', 
    'Nerve 9 - Pray For The Rain', 
    'PR - Happy Daze', 
    'PR - Oh No', 
    'Punkdisco - Oral Hygiene', 
    'Raft Monk - Tiring', 
    'Sambasevam Shanmugam - Kaathaadi', 
    'Secretariat - Borderline', 
    'Secretariat - Over The Top', 
    'Side Effects Project - Sing With Me', 
    'Signe Jakobsen - What Have You Done To Me', 
    'Skelpolu - Resurrection', 
    'Speak Softly - Broken Man', 
    'Speak Softly - Like Horses', 
    'The Doppler Shift - Atrophy', 
    'The Easton Ellises (Baumi) - SDRNR', 
    'The Easton Ellises - Falcon 69', 
    'The Long Wait - Dark Horses', 
    'The Mountaineering Club - Mallory', 
    'The Sunshine Garcia Band - For I Am The Moon', 
    'Timboz - Pony', 
    'Tom McKenzie - Directions', 
    'Triviul feat. The Fiend - Widow', 
    'We Fell From The Sky - Not You', 
    'Zeno - Signs']

import os
import shutil
import pandas as pd
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path', '-t', type=str, help='Dataset train directory')
    parser.add_argument('--des_path', '-d', type=str, help='Dataset destination directory')
    
    exp = parser.parse_args()
    root_path = exp.train_path
    des_path = exp.des_path


    count = 0
    tracklist_path = 'musdb18_tracklist.csv'
    tracklist_csv = pd.read_csv(tracklist_path)

    for track in musdb18_test_tracks:
    #for track in asteroid_validation_tracks:
        # print(track)
        
        track_df = tracklist_csv.loc[tracklist_csv["Track Name"]==track]
        source = track_df["Source"].to_list()[0]

        track_title = track.split('- ')[-1]
        test_path = os.path.join(root_path,track_title.replace(' ','_'))
        if os.path.exists(test_path):
            # print(f"{track_title} exists.")
            new_path = os.path.join(des_path,track_title.replace(' ','_'))
            shutil.move(test_path,new_path)
            print(f"sucessfully move {test_path} to {new_path}")
        else:
            print(f"{track} --from-- {source} ----- does not exist")
            count +=1 
    print(count)
