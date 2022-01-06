# create Vocal training set:
import os

import pandas as pd
from shutil import copyfile
#import sox
from distutils.dir_util import copy_tree

# 根据分轨文件所在的乐器种类进行统一命名，为后续自动混音的识别做准备
# 其实也可以不进行统一命名，只需在读取数据时知道该分轨文件属于哪个乐器种类，即可（现在显然是可以做到的）。保留分轨文件原始命名，信息会更丰富，也有好处吧。
    
if __name__ == "__main__":
    csv_path = r'mixing_secret_dataset_modified.csv'
    root_path = './dataset/track'
    output_path = './dataset/sox_vocal_dataset'
    location = ''

    # with open(csv_path, 'rb') as f1:
    #     result = f1.read()
    result = pd.read_csv(csv_path,encoding = 'latin1')
    #print(result.columns[:])
    print(result)
    fail_list = []




    for ii, (root,dirs,files) in enumerate(os.walk(root_path)):
        try:
            print("Root = ",root)
            print("Dirs = ",dirs)

            if root ==root_path:
                continue    
            if dirs == []:
                dir_path = root
            else:
                
                dir_path = os.path.join(root,dirs[0])
            print("Dir_path = ",dir_path)
            Song_Title = root.split('/')[-1]
            Song_Title = Song_Title.split('_')[0]



            for index,name in enumerate(result['Music_Title']):
                
                if name == Song_Title:
                    i = index
                    break

            vocal_quality = result['Vocal_Quality'].iloc[i] 
            lead_vocal = result['Lead_Vocal'].iloc[i].strip('[]')
            print(root, vocal_quality)
            
            if vocal_quality ==1 and lead_vocal != '':

                if not os.path.exists(os.path.join(output_path,Song_Title)):

                    os.makedirs(os.path.join(output_path,Song_Title))
                    copy_tree(os.path.join('./dataset/sox_output', Song_Title),os.path.join(output_path, Song_Title))
                    print("Successfully copy folder, ", Song_Title)
                else:
                    print(root, " Already exists")


        except:
            fail_list.append(root)
            with open('fail_music_vocal_set.txt') as f2:
                for s in fail_list:
                    f2.write(s+'\n')
            continue         

    print("fail_music: ", fail_list)