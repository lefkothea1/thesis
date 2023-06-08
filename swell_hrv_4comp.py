# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:32:57 2023

@author: lefko
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#when using condition istead of block, output is a list of lists. inner lists have tuples, 1 per each condition. tuple 1[0[]:condition name, and tuple1[1]:df with data]
def split_perPP_perCond(df):
    ### separated the data in base of person and blok [P=Person][B=Condition][1=data]
    split_df = []
    pp_df = list(df.groupby("Condition"))
    #pp_df is a list of tuples. pp_df[0] is the first tuple
    #pp_df[0][0]: PP1(str) and pp_df[0][1]: data (df)
    for pp in pp_df:
        split_df.append(list(pp[1].groupby("PP"))) #each blok has R and one more contition
    return split_df
#when splitting first per condition and then for PP: split[0]=I ,split[1]: N , split[2]=T
#and in the idder list  there are 25 tuples, one per pp!

dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\SWELL_data\\1676295645105-The_SWELL_Knowledge_Work_\\3 - Feature dataset\\per sensor\\'
#dir1 = 'swell_data'
os.chdir(dir1)
filename = 'D - Physiology features (HR_HRV_SCL - final).csv'

df_raw = pd.read_csv(filename, usecols=['PP', 'Condition', 'RMSSD'])

#droppin R rows
df2 = df_raw.loc[df_raw["Condition"] !='R']
print(df_raw.shape)

#removing the 999s
df2 = df2.replace(999, 'NaN')
df2 = df2.dropna()

print(df_raw.shape)


split = split_perPP_perCond(df2)

i_ppAvg =[] ; n_ppAvg=[] ; t_ppAvg=[]
#split[0]=I ,split[1]: N , split[2]=T
for cond_idx in range(len(split)):
    for pp_idx in range(len(split[cond_idx])):
        # split[cond_idx][pp_idx][1]["RMSSD"].astype('float').mean() #1is the df in the innest tuple, [0] is the pp#
        
        # appends [pp name and the mean of their df]
        if cond_idx == 0:
            i_ppAvg.append([split[cond_idx][pp_idx][0], split[cond_idx][pp_idx][1]["RMSSD"].astype('float').mean()])
        elif cond_idx ==1:
            n_ppAvg.append([split[cond_idx][pp_idx][0], split[cond_idx][pp_idx][1]["RMSSD"].astype('float').mean()])
        elif cond_idx == 2:
            t_ppAvg.append([split[cond_idx][pp_idx][0], split[cond_idx][pp_idx][1]["RMSSD"].astype('float').mean()])
        
inter_perPPavg = pd.DataFrame(i_ppAvg, columns=['pp','rmssd'])
inter_perPPavg.to_csv('I-meanRMSSD_perPP.csv')
neutral_perPPavg = pd.DataFrame(n_ppAvg, columns=['pp','rmssd'])
neutral_perPPavg.to_csv('N-meanRMSSD_perPP.csv')
timePres_perPPavg = pd.DataFrame(t_ppAvg, columns=['pp','rmssd'])
timePres_perPPavg.to_csv('T-meanRMSSD_perPP.csv')
    

()

