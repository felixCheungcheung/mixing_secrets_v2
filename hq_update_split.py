import shutil
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path', '-t', type=str, help='Dataset train directory')
    parser.add_argument('--des_path', '-d', type=str, help='subset destination directory')
    
    exp = parser.parse_args()
    root_path = exp.train_path
    des = exp.des_path
    if des.split('/')[-1]=='test':
        
        for track in os.listdir('/home/data/ms21_DB/test'):
            hq_track = track.split(' - ')[-1].replace(' ', '_')
            if os.path.exists(os.path.join(root_path,hq_track)):
                shutil.copytree(os.path.join(root_path,hq_track),os.path.join(des,track))
                print("Successfully find ", track)
            else:
                print("error finding ", track)

    elif des.split('/')[-1] =='val':
        for track in os.listdir('/home/data/ms21_DB/val'):
            hq_track = track.split(' - ')[-1].replace(' ', '_')
            if os.path.exists(os.path.join(root_path,hq_track)):
                shutil.copytree(os.path.join(root_path,hq_track),os.path.join(des,track))
                print("Successfully find ", track)
            else:
                print("error finding ", track)
    elif des.split('/')[-1] =='train':
        for track in os.listdir('/home/data/ms21_DB/train'):
            hq_track = track.split(' - ')[-1].replace(' ', '_')
            if os.path.exists(os.path.join(root_path,hq_track)):
                shutil.copytree(os.path.join(root_path,hq_track),os.path.join(des,track))
                print("Successfully find ", track)
            else:
                print("error finding ", track)
