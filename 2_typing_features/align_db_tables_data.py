# -*- coding: utf-8 -*-
"""
Created on Tue May 16 15:04:19 2023

@author: lefko
WORKS FOR combo of all tables 
also engineers features for typing behavior
reads in the typing behavior from dill
restructures it, per table, by using1min bins 
exports excel (1file per pp) with each condition in a new sheet. includes ts as index

also plots mean speed of mouse and typing per pp

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





for pp_idx in range(len(data)):
    print('ppindx: '+str(pp_idx))
    for cond in [0,1]: 
        #----------------------------------------------------------------------
        # ------------------------------------CLICK MOUSE--------------------
        #----------------------------------------------------------------------
        # click mouse: 3rd col is button_pressed and 4th is button_hold_time
        table = 'click_mouse'
        useful_cols = [0,3,4]
        col_names = ['ts','button', 'duration']
       
        click_df = pd.DataFrame(data[pp_idx][table][cond][:,useful_cols], columns = col_names) #df[df['button']==0]['duration']
        
        
        
        # making it index in order to resample/group in timebins
        click_df = click_df.set_index('ts', drop=True)
        #converting unix into datetime
        click_df.index = pd.to_datetime(click_df.index,unit='s')
        
        #adding needed cols before resampling
        #kind of count for right clicks (button=1) and left clicks (button=0)
        click_df['Lclick'] = click_df['button'].apply(lambda x: 1 if x== 0 else 0)
        click_df['Rclick'] = click_df['button'].apply(lambda x: 1 if x== 1 else 0)
        
        
        
        #resampling to 1min, keeping the mean of duration nd the count for R and L clicks (as clickrate)
        out_click = click_df.resample('1T').agg({'duration':'mean', 'Rclick':'sum', 'Lclick':'sum'})
        out_click.rename(columns={'duration':'click_dur'})
        # -------------------------------------------------------------------------------------------------
        # -----------------------------------MOVE MOUSE--------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------
        
        move_df = pd.DataFrame(data[pp_idx]["move_mouse"][cond][:,[0,3,4]], columns = ['ts','cum_move_dist', 'cum_move_time'])
        #adding cols with duration and distance of every mouse move (not cummulative)
        move_df['dist_diff'] = move_df['cum_move_dist'].diff()
        move_df['time_diff'] = move_df['cum_move_time'].diff()
        # making it index in order to resample/group in timebins
        move_df = move_df.set_index('ts', drop=True)
        #converting unix into datetime
        move_df.index = pd.to_datetime(move_df.index,unit='s')
        
        #adding needed cols before resampling
        move_df['speed'] = move_df['dist_diff']/move_df['time_diff']
        
        #resampling to 1min, droping cols and renaming
        out_move = move_df.resample('1T').mean()
        out_move = out_move.drop(['cum_move_dist', 'cum_move_time'], axis=1)
        out_move = out_move.rename(columns={'dist_diff':'move_dist', 'time_diff':'move_duration','speed':'move_speed'})
        #----------------------------------------------------------------------
        # ------------------------------------mouse scroll--------------------
        #----------------------------------------------------------------------
        
        cond_df = pd.DataFrame(data[pp_idx]['scroll_mouse'][cond][:,[0,5,6]], columns = ['ts', 'cum_scroll_dist', 'cum_scroll_time'])
        #adding cols with duration and distance of every mouse scroll (not cummulative)
        scroll_df=pd.DataFrame()
        scroll_df['ts'] = cond_df['ts']
        # scroll_df['scroll_dist'] = cond_df['cum_scroll_dist'].diff() #always 14
        scroll_df['scroll_dur'] = cond_df['cum_scroll_time'].diff()
        
        #resampling
        scroll_df = scroll_df.set_index('ts',drop=True)
        scroll_df.index = pd.to_datetime(scroll_df.index, unit = 's')
        scroll_out = scroll_df.resample('1T').mean()
        
        #----------------------------------------------------------------------
        # ------------------------------------Combining 3/4 mouse tables--------------------
        #----------------------------------------------------------------------
        allMouse_out = pd.concat([out_click, out_move, scroll_out],axis=1)
        
 #----------------------------------------------------------------------
 #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        # ------------------------------------keyboard--------------------
        #----------------------------------------------------------------------
        
        
        # useful_cols = [0,2,3,4,5]
        # col_names = ['ts','cum_keys', 'cum_press_dur', 'cum_backspaces', 'cum_backspaces_dur']
       
        cond_df = pd.DataFrame(data[pp_idx]['press_keyboard'][cond][:,[0,2,3,4,5]], \
                               columns = ['ts','cum_keys', 'cum_press_dur', 'cum_backspaces', 'cum_backspaces_dur'])
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
        key_out = key_df.resample('1T').agg({'keyPress':'count', 'press_dur':'mean', \
                                             'backsp':'count', 'backsp_dur':'mean', \
                                                 'pause_dur':'mean'})
        key_out['pause_rate'] = 100 * key_out['pause_dur']/60


         #----------------------------------------------------------------------
         # ------------------------------------Combining ALL tables--------------------
         #----------------------------------------------------------------------
        combo_out = pd.concat([allMouse_out, key_out], axis= 1)
        print(combo_out.head())
        
        
        #----------------------------------------------------------------------
        # ------------------------------------sending them all to excel--------------------
        #----------------------------------------------------------------------
        
        # write the 2 cond in two excel sheets, one file per pp-------------------------------------
        name = 'allTables_ppIndex_'+str(pp_idx)
        
        if cond==0:
            condition = 'neutral'
            fileOut = dir_out+ name +'.xlsx' 
            with pd.ExcelWriter(fileOut, datetime_format="YYYY-MM-DD HH:MM:SS") as writer:
                combo_out.to_excel(writer, index=True, sheet_name=condition)
        elif cond ==1:
            condition='stress'
            fileOut = dir_out+ name +'.xlsx' 
            #opens the excel file and writes in there
            with pd.ExcelWriter(fileOut, engine='openpyxl',datetime_format="YYYY-MM-DD HH:MM:SS", mode='a') as writer:
                combo_out.to_excel(writer, index=True, sheet_name=condition)
                

        
        
    
