import os
import torchaudio

if __name__ == "__main__":
    root_path = 'E:/unzip_multitrack/train'
    file_list = []
    error = []
    s_error = []
    count = 0

    for i,(root,dirs,files) in enumerate(os.walk(root_path)):

        for file in files:
            if file.split('.')[-1]=='txt':
                continue
            source_path = os.path.join(root,file)
            try:
                
                info = torchaudio.info(source_path)
                

                
                if ((not info.sample_rate == 44100) or (not info.bits_per_sample ==16) or (not source_path.split('.')[-1]=='wav')):
                    # resampling
                    s_error.append(source_path)
                    print('sampling rate error:', source_path)
                    output_path = source_path
                    audio, original_sf = torchaudio.load(source_path,normalize = True)
                    resampled_audio = torchaudio.transforms.Resample(original_sf, 44100)(audio)
                    torchaudio.save(filepath=output_path, src=resampled_audio, sample_rate=44100,encoding="PCM_S", bits_per_sample=16)
                    print('Successfully resample: ',output_path)


            except Exception as err:
                error.append(source_path)
                print(err)


    print('sampling rate error:', s_error)
    for e in error:
        print('soundfile error:', e)