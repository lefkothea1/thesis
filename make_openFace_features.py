# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 18:30:28 2023

@author: lefko
just to develop a function that calculates look straight, left and right from openface gaze data
and other engineered features from openface outputs
function created here will be applied in read_n_aggregate_openface_output!!!!!!!!!!!DONT USE THIS
"""
import os
import pandas as pd

dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\openFace\\OpenFace_2.2.0_win_x64\\OpenFace_2.2.0_win_x64\\processed\\thesis_data\\'
os.chdir(dir1)

filename = 'pp02_neutral.csv'

df2 = pd.read_csv(filename) #dtype={'user_id': int}

name = 'ppNr'
cond = 'NorS'

def make_gaze_direction_features(df2, name, condition, saving_dir):
    
    gaze_angle_cols = ['gaze_angle_x', 'gaze_angle_y']
    
    df = df2.copy()
    
    fig = df[gaze_angle_cols].plot(kind='kde').get_figure() #2 plot distribution
    fig.savefig(saving_dir +str(name)+'_'+ condition +'_gazeAngleDistrib.png') 
    
    #if both angles closeto 0 (<0.1), then pp is looking straight
    df['gazeCenter'] = (df['gaze_angle_x'] < 0.15) & (df['gaze_angle_y'] < 0.15)
    df['gazeCenter'] = df['gazeCenter'].astype(int) #changing T/F to 1/0
    
    #positive angle_x means looking right, negative left
    #making two new columns that have the values of the angle, depending where pp was looking 
    #px (if -0.5-> gazeLeft = 0.5 (k gazeRight=0))
    df['gazeLeft'] = df['gaze_angle_x'].apply(lambda x: x if x > 0 else 0)
    df['gazeRight'] = df['gaze_angle_x'].apply(lambda x: abs(x) if x < 0 else 0)
    #angle_y negative when looking up, positive when down
    df['gazeDown'] = df['gaze_angle_y'].apply(lambda x: x if x > 0 else 0)
    df['gazeUp'] = df['gaze_angle_y'].apply(lambda x: abs(x) if x < 0 else 0)
    
    return df
    


# if u wanted 1 in new col when switching direction (from left to right):
# df['new_column'] = (df['specific_col'].shift(1) > 0) & (df['specific_col'] < 0)
# df['new_column'] = df['new_column'].astype(int)

# new_cols = ['gazeCenter', 'gazeRight','gazeLeft','gazeUp','gazeDown']
# df[new_cols].plot(kind='kde')

# maybe u want to return only new cols or df with cols appended...