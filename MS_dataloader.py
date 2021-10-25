# ================================================================== #
#                5. Input pipeline for custom dataset                 #
# ================================================================== #
# From pytorch-tutorial

import torch 
import torchvision
import torch.nn as nn
import numpy as np
import torchvision.transforms as transforms

# You should build your custom dataset as below.

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self):
        
        # 1. Initialize file paths or a list of file names. 
        self.



        pass
    def __getitem__(self, index):
        # TODO
        # 1. Read one data from file (e.g. using numpy.fromfile, PIL.Image.open).
        # 2. Preprocess the data (e.g. torchvision.Transform).
        # 3. Return a data pair (e.g. image and label).
        pass
    def __len__(self):
        # You should change 0 to the total size of your dataset.
        song_numbers = len(self.df_music)
        return song_numbers

# You can then use the prebuilt data loader. 
custom_dataset = CustomDataset()
train_loader = torch.utils.data.DataLoader(dataset=custom_dataset,
                                           batch_size=64, 
                                           shuffle=True)