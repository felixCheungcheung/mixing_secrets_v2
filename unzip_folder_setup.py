import os
import shutil
import sys

if __name__ == "__main__":
    """
    Put all the unzipped song folders in a parent folder
    """
    root_path = sys.argv[1] # 'E:\\new_training_tracks'
    file_list = []
    count = 0
    for root,dirs,files in os.walk(root_path):
        # delete _MACOSX flder
        for dir in dirs:
            if 'MACOSX' in dir:
                print("Root = ",root)
                print('Dir = ',dir)
                # os.rmdir(root)
                shutil.rmtree(os.path.join(root,dir))
                print("Successfully deleted ", root+'\\'+dir)

        for file in files:
            if root.split('\\')[-2] != root_path.split('\\')[-1]:

                print("Root = ",root)
                print('Dir = ',dir)
                print("file = ",file)
                
                parentdir = os.path.dirname(root)
                print(parentdir)
                
                source = os.path.join(root,file)
                destination = os.path.join(parentdir,file)
                dest = shutil.move(source, destination)
                print("Destination Path: ",dest)
        
        # delete empty folder
        folder_path = root
        if os.path.exists(folder_path):

        # checking whether the folder is empty or not
            if len(os.listdir(folder_path)) == 0:
                # removing the file using the os.remove() method
                os.rmdir(folder_path)
                
        


                