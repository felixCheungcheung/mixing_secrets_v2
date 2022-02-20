
val_set = ['1125', '21_Grams', 'Access_Denied', 'Alive_(Yet_Free)', 'Angelsaint', 'Animal', 'A_Reason_To_Leave', 'Back_Down', 'Better_Way', 'Black_Out_Betty', 'Can_You_Say_The_Same', 'Celebrate', 'Come_Around', 'Comfort_Lives_In_Belief', 'Crazy', 'Crazy_Girl', 'Deny_Control', 'Dune_Rider', 'Easy_Tiger', 'Echo_(feat._Analise_Rios)', 'Eliza_Jane', 'El_Marinero', 'EnDance', 'Fool', 'Four_Graham', 'Gone', 'Human_Mistakes', 'Jump_Across', 'King_Rascal', 'Koishii_(feat._N.I.A.)', 'Life_Gets_In_The_Way', 'Light_It_Up_(Remix)', 'Little_Lighter', 'Living_Lie', 'Lost_My_Way', 'Maggie_May', 'Mouche', 'Muddy_Water', 'My_Childhood_Sweetheart', 'Never_Ebb_But_Flow', 'Nostalgic', 'Nos_Palpitants', 'Not_Alone', 'Of_Ice_And_Hopeless_Fate', 'Oh_Life', 'One_Minute_Smile', 'On_The_Line', 'Paraisso', 'Parole_Vuote', 'Pennies', 'Post_Rock_Is_Dumb', 'Promises_&_Lies', 'Red_On_You', 'Relentlessly', 'Rockshow', 'Same_Kind_Of_Life', 'Sirens', 'Sorry', 'South_Of_The_Water', 'Still_Flyin', 'Stop_And_Rise', 'Suit_You', 'Summerghost', 'Symphony_Of_Silence', 'Take_It_Off', 'Temporary_Happiness', "That's_How_I_Got_To_Memphis", 'The_Blues_Is_A_Lady', 'The_Elephant', 'The_Things_We_Do_For_Love', 'This_Town', 'Timeless_(Part_2)', 'To_The_Wolves', 'What_Child_Is_This', 'Who_I_Am']
test_set = ['54', 'Atrophy', 'A_Place_For_Us', 'Back_From_The_Start', 'Better', 'Big_Dummy_Shake', 'Borderline', 'Broken_Man', 'Catching_Up', 'Colour_Me_Red', 'Cur_An_Long_Ag_Seol', 'Dark_Horses', 'Directions', "Everybody's_Falling_Apart", 'For_I_Am_The_Moon', 'Good_Time', 'Heartbeats', 'Heart_Peripheral', 'Howlin', "I'm_Alright", 'Ill_Fate', 'Kaathaadi', 'Knockout', 'Mallory', 'My_Own', 'Never_Let_You_Go', 'Not_You', 'Oral_Hygiene', 'Over_The_Top', 'Passing_Ships', 'Pony', 'Pray_For_The_Rain', 'Revo_X', 'Run_Run_Run', 'Schoolboy_Fascination', 'Semantics', 'Shore', 'Signs', 'Sing_With_Me', 'Siren', 'Stitch_Up', 'The_English_Actor', 'The_Glass', 'Tiring', 'Too_Bright', 'Walkie_Talkie', "We'll_Talk_About_It_All_Tonight", 'We_Feel_Alright', 'What_Have_You_Done_To_Me', 'Widow_(feat._The_Fiend)']

import shutil
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path', '-t', type=str, help='Dataset train directory')
    parser.add_argument('--des_path', '-d', type=str, help='subset destination directory')
    
    exp = parser.parse_args()
    root_path = exp.train_path
    des = exp.des_path
    if des.split('/')[-1]=='test':
        
        for track in test_set:
            track = track.replace(' ','_')
            if os.path.exists(os.path.join(des,track)):
                continue
            shutil.move(os.path.join(root_path,track),os.path.join(des,track))
    elif des.split('/')[-1] =='val':
        for track in val_set:
            track = track.replace(' ','_')
            if os.path.exists(os.path.join(des,track)):
                continue
            shutil.move(os.path.join(root_path,track),os.path.join(des,track))
