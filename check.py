import os
import shutil
import pandas as pd


def check_annotation():
    test_path = 'E:\\unzip_multitrack\\test'
    train_path = 'E:\\unzip_multitrack\\train'
    csv_path = 'D:\smc_master_thesis_2021\MTG_2021_MASTER_THESIS\mixing_secret_dataset_modified.csv'
    csv_file = pd.read_csv(csv_path)
    
    # zip_path = 'H:\\multitrack_zip\\'
    file_list = []

    for i in os.listdir(train_path):
        i = i.replace('_',' ')
        if i not in list(csv_file['Music_Title']): 
            # print("Annotation missing ", i)
            file_list.append(i)
    for i in os.listdir(test_path):
        i = i.replace('_',' ')
        if i not in list(csv_file['Music_Title']): 
            # print("Annotation missing ", i)
            file_list.append(i)
    print(file_list)
    return file_list