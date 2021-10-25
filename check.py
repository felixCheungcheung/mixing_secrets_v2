import os
import shutil

root_path = 'E:\\unzip_multitrack\\'
zip_path = 'H:\\multitrack_zip\\'
file_list = []

for i in os.listdir(root_path):
    
    if i+'.zip' not in os.listdir(zip_path): 
        print("Zip missing ", i)
