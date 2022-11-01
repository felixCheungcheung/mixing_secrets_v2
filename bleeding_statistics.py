import os
import json
# from ruamel import yaml
import yaml




bleedAnno_path = 'MTG_2021_MASTER_THESIS\\Bleed_annotation'
hierarchy_path = 'MTG_2021_MASTER_THESIS\\hierarchy.json'
hierarchy_file = json.load(open(hierarchy_path, 'r'))
# From leaf to top level submixes, caculate the bleeding information for every instrument given a hierarchy

# initialize count variable
count = {}
inst_lvl_count = {}


for root,dir,files in os.walk(bleedAnno_path):
    if 'removed' in root:
        continue
    for file in files:
        track2inst = {}
        f1 = open(os.path.join(root, file), 'r')
        track2inst = yaml.load(f1.read(), Loader=yaml.FullLoader)
        f1.close()
        # initialize inst14_count
        for mode, mode_value in hierarchy_file['mix'].items():
            if mode not in inst_lvl_count.keys():
                inst_lvl_count[mode] = {group_name: {'component': group_value, 'Bleed': 0, \
                    'Total_MultiTrack_Num': 0, 'Song_num': 0} for group_name, group_value in mode_value.items()}
                    
        for inst_key, inst_item in track2inst['Track2inst'].items():
            # initialize count inst keys
            if inst_key not in count.keys():
                count[inst_key] = {'Bleed': 0, 'Total_MultiTrack_Num': 0, 'Song_num': 0, 'Bleed_Inst': {}}

            if inst_item != {}:
                count[inst_key]['Song_num'] += 1
                # TODO
                for track_key, track_item in inst_item.items():
                    count[inst_key]['Total_MultiTrack_Num'] += 1
                    if track_item['Bleeding'] == 'Yes':
                        count[inst_key]['Bleed'] += 1
                        bl_inst = track_item['Bleeding_Instrument'].strip("'")
                        if  bl_inst != '':
                            if ', ' in bl_inst:
                                for each_bl_inst in bl_inst.split(', '):
                                    # initialize
                                    if each_bl_inst not in count[inst_key]['Bleed_Inst'].keys():
                                        count[inst_key]['Bleed_Inst'][each_bl_inst] = 0
                                    count[inst_key]['Bleed_Inst'][each_bl_inst] += 1
                            else:
                                if bl_inst not in count[inst_key]['Bleed_Inst'].keys():
                                    count[inst_key]['Bleed_Inst'][bl_inst] = 0
                                count[inst_key]['Bleed_Inst'][bl_inst] += 1
                        
                        else: 
                            # default: if the bleeding label is yes while the bleeding_instrument is empty, 
                            # it means that this track contains huge leakage from all other instrument, e.g. live recording set up.
                            if 'Band' not in count[inst_key]['Bleed_Inst'].keys():
                                count[inst_key]['Bleed_Inst']['Band'] = 0
                            count[inst_key]['Bleed_Inst']['Band'] += 1

yaml_dir = 'bleed_statistics_ms21.yaml'
with open(yaml_dir, 'w') as f1:
    yaml.dump(count, f1, default_flow_style=False, sort_keys=False)
f1.close()