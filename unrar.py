import os
from zipfile import ZipFile

if __name__ == "__main__":
    dataset_location = 'E:'
    multitrack_zip_location = dataset_location+'/multitrack_zip/'
    multitrack_unzip_location = dataset_location+'/unzip_multitrack/'
    # create folders 
    if not os.path.exists(multitrack_unzip_location):
        os.makedirs(multitrack_unzip_location)

    for i in os.listdir(multitrack_zip_location):
        if i.split('.')[-1] == 'zip':
            file_path = multitrack_zip_location+i
            track_name = i.split('.')[:-1]
            print(file_path)
            with ZipFile(file_path, 'r') as zip:
                # extracting all the files
                print('Extracting all the files now...', )
                zip.extractall(path=multitrack_unzip_location)
                print('Done!')
                exit()
