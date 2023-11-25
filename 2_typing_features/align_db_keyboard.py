# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:03:13 2023

@author: lefko
ALIGN DB TABLE FOR PRESS KEYBOARD
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



data_file_name = 'data_1683723426_W0pp8.dill'



with open(data_file_name, 'rb') as f:
      data = dill.load(f)
      
# pp_idx = range(len(data)) #its the dictionary size
table_names = ["click_mouse", "press_keyboard", "move_mouse", "scroll_mouse"]





for pp_idx in range(len(data)):
    # print('ppindx: '+str(pp_idx))
    for cond in [0,1]: 
        #----------------------------------------------------------------------
        # ------------------------------------keyboard--------------------
        #----------------------------------------------------------------------
        # click mouse: 3rd col is button_pressed and 4th is button_hold_time
        table = 'press_keyboard'
        useful_cols = [0,2,3,4,5]
        col_names = ['ts','cum_keys', 'cum_press_dur', 'cum_backspaces', 'cum_backspaces_dur']
       
        cond_df = pd.DataFrame(data[pp_idx][table][cond][:,useful_cols], columns = col_names)
        key_df=pd.DataFrame()
        key_df['ts'] = cond_df['ts']
        key_df['keyPress'] = cond_df['cum_keys'].diff()
        key_df['press_dur'] = cond_df['cum_press_dur'].diff()
        key_df['backsp'] = cond_df['cum_backspaces'].diff()
        key_df['backsp_dur'] = cond_df['cum_backspaces_dur'].diff()
        key_df['pause_dur'] = key_df['ts'].diff()
        
        # making it index in order to resample/group in timebins
        key_df = key_df.set_index('ts', drop=True)
        #converting unix into datetime
        key_df.index = pd.to_datetime(key_df.index,unit='s')
    
        
        #resampling to 1min, droping cols and renaming
        out_key = key_df.resample('1T').agg({'keyPress':'count', 'press_dur':'mean', \
                                             'backsp':'count', 'backsp_dur':'mean', \
                                                 'pause_dur':'mean'})
        out_key['pause_rate'] = 100 * out_key['pause_dur']/60
        
