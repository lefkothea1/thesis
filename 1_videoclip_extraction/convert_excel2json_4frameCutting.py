# -*- coding: utf-8 -*-
"""
Created on Fri May 26 15:26:45 2023

@author: lefko
reading in excel file with 26 participants' timelocked framenumbers, each one containing 26 rows
converting it to JSON with the needed structure.
"""
import pandas as pd
import os
import json

dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\creatinPipe_Wabhi'
os.chdir(dir1)
configdf = pd.read_json('config.json')
df = pd.read_excel('Participant_frame_data2.xlsx', engine='openpyxl')



json_data = []
y = 1 #holding id number, index of each pp
for i in range(0, len(df), 26):
    #selecting the 26rows belonging to one pp
    pp_slice = df.iloc[i : i + 26]
    
    participant = {
        "id": y,
        "participant_id": pp_slice['partcipant-number'].iloc[0],
        "status": 0,
        "extension": [
            {
                "name": "mkv",
                "input_path": pp_slice['input-mkv-path'].iloc[0],
                "output_path": pp_slice['output_path'].iloc[0],
                "status": 0,
                "block": []
            },
            {
                "name": "mp4",
                "input_path": pp_slice['input-mp4-path'].iloc[0],
                "output_path": pp_slice['output_path'].iloc[0],
                "status": 0,
                "block": []
            }
            ]
    }          
    for _, row in pp_slice.iterrows():
        block_mkv =  {
            "name": row['block-number'],
            "start_frame": row['start-frame-MKV'],
            "end_frame": row['end-frame-MKV'],
            "status": 0                        
            }
        block_mp4 =  {
            "name": row['block-number'],
            "start_frame": row['start-frame-MP4'],
            "end_frame": row['end-frame-MP4'],
            "status": 0                        
            }
        participant['extension'][0]['block'].append(block_mkv)
        participant['extension'][1]['block'].append(block_mp4)
    # now dropping 6 first blocks(b1-1 etc) from the mp4
    participant['extension'][1]['block'] = participant['extension'][1]['block'][6:]
    json_data.append(participant)
    y = y+1
                    
    
# Save the JSON data to a file
with open('outputWOmp4-1.json', 'w') as file:
    json.dump(json_data, file, indent=4)

