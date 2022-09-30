import os 
import pandas
import sys
import csv
#from MTG_2021_MASTER_THESIS.check import check_annotation
import check

if __name__ == "__main__":
    dataset_file = "mixing_secret_dataset_auto.csv"
    dataset_w = open(dataset_file, 'w',encoding = 'latin-1',newline='')
    writer = csv.writer(dataset_w)
    writer.writerow(['Music_Title','Drum_Kick','Drum_Snare','Drum_HiHat','Drum_Cymbals','Drum_Overheads','Drum_Tom','Drum_Room','Percussion','Bass','Acoustic_Guitar','Electric_Guitar','Piano','Electric_Piano','Brass','String','WoodWind','Other','Lead_Vocal', 'Backing_Vocal','Unused'])



    # raed track name
    root_path = sys.argv[1] # path to unzip_multitrack
    in_dir = os.listdir(root_path)
    fail_id = []
    #print(in_dir)
    # not_anno_list = check.check_annotation()
    # print(not_anno_list)
    for i in in_dir:

        try:
            result_row = []

            Music_Title = []
            Music_Genre = []
            Lead_Vocal = []
            Backing_Vocal = []
            Acoustic_Guitar = []
            Electric_Guitar = []
            Piano = []
            Electric_Piano = []
            Bass = []
            Drum_Kick = []
            Drum_Snare = []
            Drum_HiHat = []
            Drum_Cymbals = []
            Drum_Overheads = []
            Drum_Tom = []
            Drum_Room = []
            Percussion = []
            Brass = []
            Strings = []
            WoodWind = []
            Other = []
            Unused = []
            
            #Music_Title = 
            
            #if len(os.listdir(root)) < 2: continue # count 底层目录
            #if ii == 0 : continue # not counting track/目录
            #print(root)
            
            Music_Title = i
            
            result_row.append(Music_Title)   
            #print(Music_Title)
            
            # folder_name = Music_Title.replace(' ','_')
            for track_name in os.listdir(os.path.join(root_path,i)) :
                if track_name.split('.')[-1] == 'wav' and track_name.split('_')[0] != '.':



                    if any(item in track_name.lower() for item in ['leadvox','vocal','vox ld']):
                        Lead_Vocal.append(track_name)
                    elif any(item in track_name.lower() for item in ['backingVox','vox','vox bg','harm','bgv','chorus vocal','group vocal','choir']):
                        Backing_Vocal.append(track_name)
                    elif any(item in track_name.lower() for item in ['acousticgtr','acgtr','acoustic guitar','acguitar','aco guitar']):
                        Acoustic_Guitar.append(track_name)
                    elif any(item in track_name.lower() for item in ['electricgtr','elecgtr','electric guitar','gtr','ele guitar','guitar']):
                        Electric_Guitar.append(track_name)
                    elif any(item in track_name.lower() for item in ['_piano']):
                        Piano.append(track_name)
                    elif any(item in track_name.lower() for item in ['_elecpiano', 'rhodes','key','organ']):
                        Electric_Piano.append(track_name)
                    elif any(item in track_name.lower() for item in ['bass' ]):
                        Bass.append(track_name)
                    elif any(item in track_name.lower() for item in ['kick']):
                        Drum_Kick.append(track_name)
                    elif any(item in track_name.lower() for item in ['snare']):
                        Drum_Snare.append(track_name)
                    elif any(item in track_name.lower() for item in ['hihat','hi hat','hat']):
                        Drum_HiHat.append(track_name)
                    elif any(item in track_name.lower() for item in ['cymbal','cymbl','ride','crash']):
                        Drum_Cymbals.append(track_name)
                    elif any(item in track_name.lower() for item in ['tom']):
                        Drum_Tom.append(track_name)
                    elif any(item in track_name.lower() for item in ['room','floor','chamber']):
                        Drum_Room.append(track_name)
                    elif any(item in track_name.lower() for item in ['overhead','drum','oh']):
                        Drum_Overheads.append(track_name)
                    elif any(item in track_name.lower() for item in ['percussion','cowbell', 'congas','taiko','shaker','clap','loop','beat','timpani','tambourine','tamb','anvil','woodblock','djembe']):
                        Percussion.append(track_name)
                    elif any(item in track_name.lower() for item in ['sax','horn', 'trumpet', 'tuba', 'brass', 'trombone']):
                        Brass.append(track_name)
                    elif any(item in track_name.lower() for item in ['string','violin' ,'viola' ,'cello' ]):
                        Strings.append(track_name)
                    elif any(item in track_name.lower() for item in ['woodwind','flute', 'oboe', 'clarinet', 'piccolo','bassoon']):
                        WoodWind.append(track_name)
                    elif any(item in track_name.lower() for item in ['pair']):
                        Unused.append(track_name)
                    else:
                        Other.append(track_name)
            
            #print(Lead_Vocal[:])
                


            result_row.append(Drum_Kick)
            result_row.append(Drum_Snare)
            result_row.append(Drum_HiHat)
            result_row.append(Drum_Cymbals)
            result_row.append(Drum_Overheads)
            result_row.append(Drum_Tom)
            result_row.append(Drum_Room)
            result_row.append(Percussion)
            result_row.append(Bass)
            result_row.append(Acoustic_Guitar)
            result_row.append(Electric_Guitar)
            result_row.append(Piano)
            result_row.append(Electric_Piano)
            result_row.append(Brass)
            result_row.append(Strings)
            result_row.append(WoodWind)
            result_row.append(Other)
            result_row.append(Lead_Vocal)
            result_row.append(Backing_Vocal)
            result_row.append(Unused)
            #print(result_row[3] == [])
            if all(item == [] for item in result_row[1:]):
                if len(os.listdir(os.path.join(root_path,'test',folder_name))) ==1:
                    print(Music_Title)
                continue
            else:
                writer.writerow(result_row)
        except Exception as ex:
            fail_id.append(i)
            continue
        

    print("fail",fail_id)