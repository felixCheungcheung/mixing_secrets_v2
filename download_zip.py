import os
import sys
from urllib import request
import progressbar


opener = request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
request.install_opener(opener)

# dataset_location = str(sys.argv[1])
dataset_location = 'H:'
print(dataset_location)

pbar = None


def show_progress(block_num, block_size, total_size):
    global pbar
    #print(total_size)


    if pbar is None and total_size > 0:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None
        
if os.path.exists('failed_download_info.txt'):

    with open('failed_download_info.txt') as f0:
        error_info = []
        for j in f0.readlines():
            error_info.append(j)
else:
    error_info = []

success_info = []


with open('downloadurls.txt') as f1:
    
    for i in f1.readlines():
        broad_genre = i.split(',')[0]
        sub_genre = i.split(',')[1]
        track_name = i.split(',')[2].replace(' ','_')
        artist_name = i.split(',')[3]
        multitrack_url = i.split(',')[4]
        mixture_url = i.split(',')[5]
        
        multitrack_location = dataset_location+'/multitrack_zip/'+track_name+'.zip'
        mixture_location = dataset_location+'/mixture/'+track_name+'.mp3'

        # create folders 
        if not os.path.exists(dataset_location+'/multitrack_zip/'):
            os.makedirs(dataset_location+'/multitrack_zip/')
        # if not os.path.exists(dataset_location+'/mixture/'):
        #     os.makedirs(dataset_location+'/mixture/')

        print(track_name)
        print(multitrack_location)
        try:

            if i in error_info:
                print('Downloading multitrack of ', track_name)
                request.urlretrieve(multitrack_url,multitrack_location,show_progress)
            elif not os.path.exists(multitrack_location):
                print('Downloading multitrack of ', track_name)
                request.urlretrieve(multitrack_url,multitrack_location,show_progress)

            else:
                print(track_name, ' Multitrack already exists.')
                
            # if i in error_info:
            #     print('Downloading mixture of ', track_name)    
            #     request.urlretrieve(mixture_url,mixture_location,show_progress)
            # elif not os.path.exists(mixture_location):
            #     print('Downloading mixture of ', track_name)    
            #     request.urlretrieve(mixture_url,mixture_location,show_progress)
            # else:
            #     print(track_name, ' Mixture already exists.')
            
            success_info.append(i)
            
            with open('success_download_info.txt','w') as f3:
                for k in success_info:
                    f3.write(k)

        except Exception as error:
            print(error)
            error_info.append(i)
            with open('failed_download_info.txt','w') as f0:
                for j in error_info:
                    f0.write(j)
                        
            
                        
print('Number of Failed ID: ',len(error_info))
print('Number of Success ID: ',len(success_info))

        


