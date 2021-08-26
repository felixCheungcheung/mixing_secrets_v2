import os
import shutil

root_path = './dataset/sox_vocal_dataset/valid'
file_list = []
count = 0
for i,(root,dirs,files) in enumerate(os.walk(root_path)):
    for file in files:
        if file.split('.')[0] =='Unused':
            
            
            os.remove(os.path.join(root,file))
            print("Successfully remove, ", os.path.join(root,file))
    
    #remove empty folder
    if len(os.listdir(root)) == 0: # Check if the folder is empty
        #shutil.rmtree(root) # If so, delete it
        print("Successfully remove, ", root)
    else:
        count+=1

print(count)