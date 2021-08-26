import os
import soundfile
import sox

root_path = './dataset/sox_vocal_dataset'
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
            
            sample_rate = sox.file_info.sample_rate(source_path)
            
            
            if sample_rate != 44100:
                # resampling
                s_error.append(source_path)
                print('sampling rate error:', source_path)
                output_path = os.path.join(root,'44k_'+file)
                tfm = sox.Transformer()
                tfm.set_output_format(rate=44100)
                
                tfm.build_file(input_filepath=source_path,sample_rate_in= sample_rate,output_filepath = output_path)
                print('Successfully resample: ',output_path)

                os.remove(source_path)
                print("Successfully remove, ", source_path)

                os.rename(output_path,source_path)
                print("Successfully rename, ", source_path)
        except sox.core.SoxiError as err:
            error.append(source_path)
            print(err)


print('sampling rate error:', s_error)
for e in error:
    print('soundfile error:', e)