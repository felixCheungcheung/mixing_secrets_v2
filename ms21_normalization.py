import yaml
import re
import os, errno
import librosa
import soundfile as sf
import numpy as np
import pandas as pd
import json
import sys
import pyloudnorm as pyln
import shutil


base_path = sys.argv[1] # '/media/felix/dataset/ms21' 

output_path = sys.argv[2] #  '/media/felix/dataset/ms21_norm'
# print(output_path)
os.makedirs(output_path,exist_ok=True)
# print(base_path)
fail_list = []
def loud_norm(path, output_path, dir):
    data, rate = sf.read(path) # load audio
    # measure the loudness first 
    meter = pyln.Meter(rate) # create BS.1770 meter
    loudness = meter.integrated_loudness(data)
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -25.0) 
    sf.write(os.path.join(output_path,dir,file),loudness_normalized_audio, rate)
    print("Normalized ",path)

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.wav'):
            path = os.path.join(root,file)
            dir = root.split('\\')[-1]
            print(dir)
            os.makedirs(os.path.join(output_path,dir),exist_ok=True)
            try:
                loud_norm(path, output_path, dir)
            except:
                print("something wrong", path)
                fail_list.append(path)
                
with os.path.join(output_path,'fail_list.txt','w') as f0:
    for i in fail_list:
        f0.write(i)