import os
from zipfile import ZipFile
import sys

if __name__ == "__main__":
    dataset_location = sys.argv[1]
    multitrack_zip_location = dataset_location+'/multitrack_zip/'
    multitrack_unzip_location = dataset_location+'/unzip_multitrack/'
    # create folders 
    if not os.path.exists(multitrack_unzip_location):
        os.makedirs(multitrack_unzip_location)

    error_info = []
    for i in os.listdir(multitrack_zip_location):
        try:
            if i.split('.')[-1] == 'zip':
                file_path = multitrack_zip_location+i
                track_name = i.split('.')[:-1]
                print(file_path)
                with ZipFile(file_path, 'r') as zip:
                    # extracting all the files
                    print(f'Extracting all the files in {i}now...', )
                    zip.extractall(path=multitrack_unzip_location)
                    print(f'Sucessfully unzip {i}')
        except Exception as error:
                print(error)
                error_info.append(i)
                with open('failed_unzip_info.txt','w') as f0:
                    for j in error_info:
                        f0.write(j)
                
