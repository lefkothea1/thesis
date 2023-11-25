# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 16:08:23 2023

@author: lefko
RMSSD


this script combines all ppolar data per pp and calculates rmssd per pp. outputs summary over all pps
"""
from datetime import datetime, timedelta
import glob
import pandas as pd
import numpy as np

dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\polar\\perBlock_excl10minsFromStart_5minEnd\\allPPs_stress`\\'

out_file = dir1 + 'stress_RR.xlsx'


all_data = pd.DataFrame()


#collecting all PPs data for 1 condition
for file_name in glob.glob(dir1 + '*.csv'):
    print(file_name)
    name = file_name.split('\\')[-1][:4] #gets pp#_ WONT WORK FOR PP>10!
    x = pd.read_csv(file_name, low_memory=False)
    x.columns = name + x.columns #addig prefix
    all_data = pd.concat([all_data,x],axis=1)

    
df_rr = all_data[[col for col in all_data.columns if 'RR' in col]]
df_time = all_data[[col for col in all_data.columns if 'time' in col]]

#calculating RR successive differences  ----leaving out the first alnd last 2 min
rr_rmssd = df_rr.diff(axis=0)
#squaring the differences
for col in rr_rmssd.columns:
    rr_rmssd[col] = rr_rmssd[col]**2
#taking the root mean of average of squared differences
rmssd_array = np.sqrt(rr_rmssd.mean(axis=0))

with pd.ExcelWriter(out_file) as writer:
    df_rr.to_excel(writer, index=False, sheet_name='RR')

    rmssd_array.to_excel(writer,  sheet_name='RMSSD')
    df_time.to_excel(writer, index=False, sheet_name='time')

