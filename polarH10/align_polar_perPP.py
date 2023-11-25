# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:38:21 2023

@author: lefko
reads in the condition_trimmed_RR excel file
for each pp created average RR within a sec (1000ms)
outputs a concated table with the RRs of all pps (binned) in sheetRR 
includes their time column in sheet time

"""
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt

#should plot 2conditions per pp, NOT all pps in each condition which is what it is currently doing
#idea: make another script only for plotting this, from loading both neutral and stress files
def plot_RR_fromDf(df_rr, cond):
    for col in df_rr.columns[1:]:
        plt.plot(df_rr['time(sec)'],df_rr[col],label=col, linewidth=1, alpha=0.7)
        plt.legend()
        plt.title('PP RRs '+str(cond))
        
dir_in = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\polar\\perBlock_excl10minsFromStart_5minEnd\\allPPs_stress\\'
os.chdir(dir_in)
condition='stress'
dir_out = dir_in + 'allPPs_RR_aligned_stress.xlsx'
# filename='PP02_neutral_HRVtrimed.csv'
# name='pp02_'
# # df = pd.read_excel(filename, engine='openpyxl')
# df = pd.read_csv(filename, index_col='time')
# df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H-%M-%S.%f')

# #resampling/ binning time to 1sec
# binned_df =  df['RR'].resample('1S').mean()
# #storing it to out_df
# out_df = binned_df.reset_index()


all_data = pd.DataFrame()

# collecting all PPs data for 1 condition
for file_name in glob.glob(dir_in + '*.csv'):
    print(file_name)
    name = file_name.split('\\')[-1][:5] #gets pp#_ make sure pp1 is pp01 in filename
    df = pd.read_csv(file_name, low_memory=False, index_col='time')
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H-%M-%S.%f')
    #resampling/ binning time to 1sec
    binned_df =  df['RR'].resample('1S').mean()
    #storing it to out_df
    out_df = binned_df.reset_index()
    out_df.columns = name + out_df.columns #addig prefix
    all_data = pd.concat([all_data,out_df],axis=1)
    
df_rr = all_data[[col for col in all_data.columns if 'RR' in col]]
#adding a time_elapsed column
df_rr.insert(0,'time(sec)', range(df_rr.shape[0]))

plot_RR_fromDf(df_rr, condition)

df_time = all_data[[col for col in all_data.columns if 'time' in col]]

with pd.ExcelWriter(dir_out) as writer:
    df_rr.to_excel(writer, index=False, sheet_name='RR')
    df_time.to_excel(writer, index=False, sheet_name='time')

