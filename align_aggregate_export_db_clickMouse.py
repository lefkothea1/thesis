# -*- coding: utf-8 -*-
"""
Created on Tue May 16 15:04:19 2023

@author: lefko
WORKS FOR CLICK MOUSE TABLE
DONT USE THIS SCRIPT, USE THE 'ALIGN DB TABLES DATA-'. IT INCLUDES MOVE MOUSE AND CLICK MOUSE TABLES
reads in the typing behavior from dill
restructures it, per table, by using1sec bins (now done click mouse only)
exports excel (1file per pp) with each condition in a new sheet. includes ts as index

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


data_file_name = 'data_1683723426_W0pp8.dill'



with open(data_file_name, 'rb') as f:
      data = dill.load(f)
      
# pp_idx = range(len(data)) #its the dictionary size
table_names = ["click_mouse", "press_keyboard", "move_mouse", "scroll_mouse"]


#def.......-----------------------------------------------------------------------------
# click mouse: 3rd col is button_pressed and 4th is button_hold_time
table = 'click_mouse'
useful_cols = [0,3,4]
col_names = ['ts','button', 'duration']



for pp_idx in range(len(data)):
    print('ppindx: '+str(pp_idx))
    for cond in [0,1]: 
        print('condition is : '+str(cond))
       
        cond_df = pd.DataFrame(data[pp_idx][table][cond][:,useful_cols], columns = col_names) #df[df['button']==0]['duration']
        
        
        
        # making it index in order to resample/group in timebins
        cond_df = cond_df.set_index('ts', drop=True)
        #converting unix into datetime
        cond_df.index = pd.to_datetime(cond_df.index,unit='s')
        
        #adding needed cols before resampling
        #kind of count for right clicks (button=1) and left clicks (button=0)
        cond_df['Lclick'] = cond_df['button'].apply(lambda x: 1 if x== 0 else 0)
        cond_df['Rclick'] = cond_df['button'].apply(lambda x: 1 if x== 1 else 0)
        
        #below works! just need to make cols separate for each button (click=1 to sum it over interval and duration_right click and left separately)
        # cond_df.resample('1S').mean()#1sec bins
        # cond_df = cond_df.resample('1T').mean()#1min bins
        
        #resampling to 1min, keeping the mean of duration nd the count for R and L clicks (as clickrate)
        outdf = cond_df.resample('1T').agg({'duration':'mean', 'Rclick':'sum', 'Lclick':'sum'})
        
        # write the 2 cond in two excel sheets, one file per pp--------------------
        name = 'clickMouse_ppIndex_'+str(pp_idx)
        
        if cond==0:
            condition = 'neutral'
            fileOut = dir_out+ name +'.xlsx' 
            with pd.ExcelWriter(fileOut, datetime_format="YYYY-MM-DD HH:MM:SS") as writer:
                outdf.to_excel(writer, index=True, sheet_name=condition)
        elif cond ==1:
            condition='stress'
            fileOut = dir_out+ name +'.xlsx' 
            wb = load_workbook(fileOut)
            writer = pd.ExcelWriter(fileOut, datetime_format="YYYY-MM-DD HH:MM:SS", engine = 'openpyxl')
            writer.book = wb
            outdf.to_excel(writer, index=True, sheet_name=condition)
            wb.save(fileOut)
# https://stackoverflow.com/questions/42370977/how-to-save-a-new-sheet-in-an-existing-excel-file-using-pandas
        
        
    
