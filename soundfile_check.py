import os
from numpy import roots
import torchaudio
import torch
import argparse
from multiprocessing.dummy import Pool as ThreadPool

# python soundfile_check.py -p E:/ms21/train -sr 16000 -bt 16 -m true -pd true
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', type=str, help='Dataset directory')
    # parser.add_argument('--thread', '-t', type=int, help='number of threads')
    parser.add_argument('--samplerate', '-sr', type=int, help='Sampling Rates')
    parser.add_argument('--bitrate', '-bt', type=int, help='Bit Rate')
    parser.add_argument('--mono', '-m', action='store_true', help='Stereo: False, Mono: True')
    parser.add_argument('--pad', '-pd', action='store_true', help='For zero-padding, boolean')

    exp = parser.parse_args()
    root_path = exp.path
    sampling_rate = exp.samplerate
    bit_rate = exp.bitrate
    Mono = exp.mono
    zeropad = exp.pad
    
    file_list = []
    error = []
    s_error = []
    count = 0

    for i,(root,dirs,files) in enumerate(os.walk(root_path)):
        for dir in dirs:

            
            max_len_multitrack = []

            for file in os.listdir(os.path.join(root,dir)):
                if file.split('.')[-1] != 'wav' or file.split('.')[0]=='':
                    continue
                source_path = os.path.join(root,dir,file)

                    
                info = torchaudio.info(source_path)

                
                if ((not info.sample_rate == sampling_rate) or (not info.bits_per_sample ==bit_rate) or (not info.num_channels ==1)):
                    # resampling
                    s_error.append(source_path)
                    print('sampling rate error:', source_path)
                    output_path = source_path
                    audio, original_sf = torchaudio.load(source_path,normalize = True)
                    resampled_audio = torchaudio.transforms.Resample(original_sf, sampling_rate)(audio)
                    if Mono == True:
                        resampled_audio = torch.mean(resampled_audio, dim=0, keepdim=True)
                        print('Successfully monorize: ',output_path)
                    torchaudio.save(filepath=output_path, src=resampled_audio, sample_rate=sampling_rate,encoding="PCM_S", bits_per_sample=bit_rate)
                    print('Successfully resample: ',output_path)


            # find max len        
            for file in os.listdir(os.path.join(root,dir)):
                if file.split('.')[-1] != 'wav' or file.split('.')[0]=='':
                    continue
                source_path = os.path.join(root,dir, file)
                audio, original_sf = torchaudio.load(source_path,normalize = True)
                max_len_multitrack.append(audio.shape[1])

            # zero padding
            if zeropad == True:
                
                print(dir)
                for file in os.listdir(os.path.join(root,dir)):
                    if file.split('.')[-1] != 'wav' or file.split('.')[0]=='':
                        continue
                    max_len = max(max_len_multitrack)
                    # print(max_len)
                    source_path = os.path.join(root,dir, file)
                    audio, original_sf = torchaudio.load(source_path,normalize = True)
                    if audio.shape[1] < max_len:
                        # print('Start zeropadding')
                        output_path = source_path
                        if Mono:
                            target = torch.zeros(1,max_len)
                        else:
                            target = torch.zeros(2,max_len)
                        source_len = audio.shape[1]
                        target[:,:source_len] = audio
                        torchaudio.save(filepath=output_path, src=target, sample_rate=sampling_rate,encoding="PCM_S", bits_per_sample=bit_rate)
                        print('Successfully zeropad: ',output_path)
                    elif audio.shape[1] == max_len:
                        continue
                    elif audio.shape[1] > max_len:
                        error.append(source_path)
            


    print('sampling rate error:', s_error)
    for e in error:
        print('soundfile error:', e)