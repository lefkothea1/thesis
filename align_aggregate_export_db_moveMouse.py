# -*- coding: utf-8 -*-
"""
Created on Wed May 31 18:23:14 2023

@author: lefko
works for move mouse table
DONT USE THIS SCRIPT, USE THE 'ALIGN DB TABLES DATA-'. IT INCLUDES MOVE MOUSE AND CLICK MOUSE TABLES
"""
import os
import dill
import pandas as pd
import numpy as np
import datetime
from openpyxl import load_workbook

#it will create output folder on dir up from dir_in
def make_output_folder(name):
    now = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    dir_out = dir_in+ name + now +'/'
    os.makedirs(dir_out)
    print('created folder'+str(dir_out))
    return dir_out     


dir_in = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\pp_db'
os.chdir(dir_in)

#dir_out includes the last/
dir_out = make_output_folder('_AggregatedFeat_output')


data_file_name = 'ALLdata_1685716514_W0pp8.dill'



with open(data_file_name, 'rb') as f:
      data = dill.load(f)
      
# pp_idx = range(len(data)) #its the dictionary size
table_names = ["click_mouse", "press_keyboard", "move_mouse", "scroll_mouse"]


#def...MOVE MOUSE....-----------------------------------------------------------------------------
# 
table = "move_mouse"
useful_cols = [0,3,4]
col_names = ['ts','cum_move_dist', 'cum_move_time']



for pp_idx in range(len(data)):
    print('ppindx: '+str(pp_idx))
    for cond in [0,1]: 
        # print('condition is : '+str(cond))
       
        cond_df = pd.DataFrame(data[pp_idx][table][cond][:,useful_cols], columns = col_names)
        #adding cols with duration and distance of every mouse move (not cummulative)
        cond_df['dist_diff'] = cond_df['cum_move_dist'].diff()
        cond_df['time_diff'] = cond_df['cum_move_time'].diff()
        # making it index in order to resample/group in timebins
        cond_df = cond_df.set_index('ts', drop=True)
        #converting unix into datetime
        cond_df.index = pd.to_datetime(cond_df.index,unit='s')
        
        #adding needed cols before resampling
        cond_df['speed'] = cond_df['dist_diff']/cond_df['time_diff']
        
        #resampling to 1min, droping cols and renaming
        outdf = cond_df.resample('1T').mean()
        outdf = outdf.drop(['cum_move_dist', 'cum_move_time'], axis=1)
        outdf = outdf.rename(columns={'dist_diff':'move_dist', 'time_diff':'move_duration','speed':'move_speed'})
        
        # # write the 2 cond in two excel sheets, one file per pp--------------------
        # name = 'clickMouse_ppIndex_'+str(pp_idx)
        
        # if cond==0:
        #     condition = 'neutral'
        #     fileOut = dir_out+ name +'.xlsx' 
        #     with pd.ExcelWriter(fileOut, datetime_format="YYYY-MM-DD HH:MM:SS") as writer:
        #         outdf.to_excel(writer, index=True, sheet_name=condition)
        # elif cond ==1:
        #     condition='stress'
        #     fileOut = dir_out+ name +'.xlsx' 
        #     wb = load_workbook(fileOut)
        #     writer = pd.ExcelWriter(fileOut, datetime_format="YYYY-MM-DD HH:MM:SS", engine = 'openpyxl')
        #     writer.book = wb
        #     outdf.to_excel(writer, index=True, sheet_name=condition)
        #     wb.save(fileOut)