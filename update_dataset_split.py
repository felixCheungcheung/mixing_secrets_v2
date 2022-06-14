# This script is to make the 44.1kHz ms21 dataset share the same dataset split with the 16kHz version

import os
import sys
from typing import List
import pandas as pd
import csv

base_path = sys.argv[1]


dataframe = {'test': [], 'train': [],'val':[]}
test_id = []
train_id = []
val_id = []
print(dataframe)
for test_track in os.listdir(os.path.join(base_path, 'test')):
    dataframe['test'].append(test_track)

for train_track in os.listdir(os.path.join(base_path, 'train')):
    dataframe['train'].append(train_track)

for val_track in os.listdir(os.path.join(base_path, 'val')):
    dataframe['val'].append(val_track)

column_name = ['test', 'train', 'val']
def show(list):
    for i in list:
        print(i)

# for key, val in dataframe.items():
#     print(key, '*'*50)
#     show(val)

print(list(set(dataframe['test']).intersection(dataframe['train'])))
show(list(set(dataframe['val']).intersection(dataframe['train'])))
print(list(set(dataframe['test']).intersection(dataframe['val'])))
def get_artist(list):
    artist = [i.split(' - ')[0] for i in list]
    return artist
print(list(set(get_artist(dataframe['test'])).intersection(get_artist(dataframe['train']))))
print(list(set(get_artist(dataframe['val'])).intersection(get_artist(dataframe['train']))))
print(list(set(get_artist(dataframe['val'])).intersection(get_artist(dataframe['test']))))

# server_frame = pd.read_excel("D:\smc_master_thesis_2021\MTG_2021_MASTER_THESIS\ms21_dataset_split.xlsx")
# print(list(set(dataframe['train']).difference(server_frame['train'])))
