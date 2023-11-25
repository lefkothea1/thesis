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
      

table_names = ["click_mouse", "press_keyboard", "move_mouse", "scroll_mouse"]




for pp_idx in range(len(data)):
    # print('ppindx: '+str(pp_idx))
    for cond in [0,1]: 
        #----------------------------------------------------------------------
        # ------------------------------------mouse scroll--------------------
        #----------------------------------------------------------------------
        table = 'scroll_mouse'
        useful_cols = [0,5,6]
        col_names = ['ts', 'cum_scroll_dist', 'cum_scroll_time']
        
        cond_df = pd.DataFrame(data[pp_idx][table][cond][:,useful_cols], columns = col_names)
        #adding cols with duration and distance of every mouse scroll (not cummulative)
        scroll_df=pd.DataFrame()
        scroll_df['ts'] = cond_df['ts']
        # scroll_df['scroll_dist'] = cond_df['cum_scroll_dist'].diff() #always 14
        scroll_df['scroll_dur'] = cond_df['cum_scroll_time'].diff()
        
