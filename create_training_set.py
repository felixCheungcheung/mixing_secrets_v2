import os

import pandas as pd
from shutil import copyfile
import sox
import soundfile

# 根据分轨文件所在的乐器种类进行统一命名，为后续自动混音的识别做准备
# 其实也可以不进行统一命名，只需在读取数据时知道该分轨文件属于哪个乐器种类，即可（现在显然是可以做到的）。保留分轨文件原始命名，信息会更丰富，也有好处吧。
#

if __name__ == "__main__":

    csv_path = r'mixing_secret_dataset_modified.csv'
    root_path = './dataset/track'
    output_path = './dataset/casual_test'
    location = ''

    # with open(csv_path, 'rb') as f1:
    #     result = f1.read()
    result = pd.read_csv(csv_path,encoding = 'latin1')
    #print(result.columns[:])
    print(result)
    fail_list = []


    for ii, (root,dirs,files) in enumerate(os.walk(root_path)):
        try:
            print(root)
            print(dirs)

            if root ==root_path:
                continue
            if dirs == []:
                dir_path = root
            else:    
                dir_path = os.path.join(root,dirs[0])
            #dir_path = root
            print(dir_path)
            Song_Title = root.split('/')[-1]
            Song_Title = Song_Title.split('_')[0]
            #Song_Title = 'Howlin'

            if not os.path.exists(os.path.join(output_path,Song_Title)):
                os.makedirs(os.path.join(output_path,Song_Title))

            for index,name in enumerate(result['Music_Title']):
                
                if name == Song_Title:
                    i = index
                    break
            #max_length = 0
            # to find the max length of all tracks.
            for k in result.columns[1:-2]: # regardless of Music_Titile, Unused, Vocal_Quality column
                print(k)
                tracks_same_class = result[k].iloc[i].strip('[]') 
                print(tracks_same_class)
                
                if tracks_same_class !='':
                    if ', ' in tracks_same_class:
                        track_file_name = [dir_path + '/' + i.strip("'") for i in tracks_same_class.split(', ')]
                        print(track_file_name)

                        #print(original_track_name)
                        wav_name = k +'.wav'
                        #print(wav_name)

                        if not os.path.exists(os.path.join(output_path, Song_Title,wav_name)):
                            cbn = sox.Combiner()
                            cbn.convert(samplerate=44100, n_channels = 2)
                            cbn.build(track_file_name,os.path.join(output_path,Song_Title,wav_name),'mix')
                            print('successfully output, ',  tracks_same_class, 'to ', wav_name)
                        else:
                            print(wav_name, " Already exists")
                        
                            
                    else:
                        original_track_name = tracks_same_class.strip("'")
                        #print(original_track_name)
                        wav_name = k +'.wav'
                        #print(wav_name)

                        sample_rate = sox.file_info.sample_rate(os.path.join(dir_path,original_track_name))
                        tfm = sox.Transformer()
                        tfm.set_output_format(rate=44100)
                        output_path = os.path.join(output_path, Song_Title, wav_name)
                        tfm.build_file(input_filepath=os.path.join(dir_path,original_track_name),sample_rate_in= sample_rate,output_filepath = output_path)
                        
                        print('successfully output, ',  original_track_name, 'to ', wav_name)

                    
        except Exception as e:
            print(e)
            fail_list.append(root)
            with open('fail_music.txt') as f2:
            for s in fail_list:
                f2.write(s+'\n')
            continue         

    print(fail_list)