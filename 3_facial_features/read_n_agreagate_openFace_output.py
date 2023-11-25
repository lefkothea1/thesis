# -*- coding: utf-8 -*-
"""
Created on Tue May 30 16:12:48 2023

@author: lefko
combining and editing openFace output of each pp:
--reads in every openFace output
--drops rows where tracking wasnt sucessful
--droppin un needed columns
--averaging every 30 rows (1sec) of only numerical cols
---adding col with pp# and condition (N/s)


"""
import glob
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

# pass in only numerical columns!
def avg_n_rows_df (df, n):    
    
    # Calculate the number of groups
    num_groups = len(df) // n
    
    # Create an empty dataframe to store the averaged values
    df_averaged = pd.DataFrame()
    
    # Iterate through each group and calculate the mean of the rows
    for i in range(num_groups):
        start = i * n
        end = start + n
    
        # Calculate the mean of each column within the group
        group_mean = df.iloc[start:end].mean()
        #for timestamp and frame cols, dont calc the mean but take the max (1sec increments)
        group_mean['timestamp']= df['timestamp'].iloc[start:end].max()
        group_mean['frame']= df['frame'].iloc[start:end].max()
    
        # Append the mean values to the averaged dataframe, keeping original column order
        df_averaged = df_averaged.append(group_mean, ignore_index=True)[df.columns.tolist()]
    return df_averaged

#it will create output folder on dir up from dir_in
def make_output_folder(folder_name):
    now = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    dir_out = dir_in + folder_name + now +'/'
    os.makedirs(dir_out)
    print('created folder'+str(dir_out))
    return dir_out 


def make_gaze_direction_features(df2, name, condition, saving_dir):
    
    gaze_angle_cols = ['gaze_angle_x', 'gaze_angle_y']
    
    df = df2.copy()
    
    # fig = df[gaze_angle_cols].plot(kind='kde', title= name +'_'+ condition).get_figure() #2 plot distribution
    # fig.savefig(saving_dir +str(name)+'_'+ condition +'_gazeAngleDistrib.png') 
    
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

dir_in = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\openFace_out\\retrying_problematic\\'

dir_out = make_output_folder('aggr1min_processed_OpenFace_pp6-7')
# dir_out = make_output_folder('aggr1sec_processed_OpenFace')

aggr_win = 30*60 #1min
# aggr_win = 30 #1sec


all_data = pd.DataFrame()



#collecting all csv (pp) files in dir_in
for file_name in glob.glob(dir_in + '*.csv'):
    
    print(file_name)
    
    name = file_name.split('\\')[-1].split('_')[0] # will split filename by _ and keep the 1st part (which should be pp#)
    x = pd.read_csv(file_name, sep=',')
    
    
    useful_cols = ['timestamp','frame', 'success', 'confidence',\
                   'AU01_r', 'AU02_r', 'AU04_r', 'AU05_r', 'AU06_r', \
                    'AU07_r','AU09_r', 'AU10_r', 'AU12_r', 'AU14_r', \
                    'AU15_r', 'AU17_r', 'AU20_r', 'AU23_r', 'AU25_r',\
                    'AU26_r', 'AU45_r', 'AU45_c', 'AU28_c', 'pose_Tx',\
                    'pose_Ty','pose_Tz' ,\
                    'gazeCenter','gazeUp', 'gazeDown', 'gazeRight', 'gazeLeft']
        
    if "B1" in file_name:
        cond = 'N'
    elif "B2" in file_name:
        cond='S'
    else:
        print('cant find condition for file '+str(file_name))

    #ENGINEER FEATURES HERE!!!--------------------------------------------------------------------------------------
    
    x = make_gaze_direction_features(x, name, cond, dir_out)
    
    
    
        
    temp = x[useful_cols].copy()
    #should average every 30 rows -->1 sec time resolution
    temp = avg_n_rows_df(temp, aggr_win)
    
    #renaming
    temp.rename(columns = {'AU01_r':'AU1_InnerBrowRaiser', 'AU02_r':'AU2_OuterBrowRaiser',\
                 'AU04_r': 'AU4_BrowLowerer','AU05_r': 'AU5_UpperLipRaiser', \
                'AU06_r': 'AU6_CheekRaiser', 'AU07_r': 'AU7_LidTightener', \
                'AU09_r': 'AU9_NoseWringler', 'AU10_r': 'AU10_UpperLipRaiser',\
                'AU12_r': "AU12_LipCornerPuller", 'AU14_r':'AU14_Dimpler',\
                'AU15_r': "AU15_LipCornerDepressonr", 'AU17_r':'AU17_ChinRaiser',\
                'AU20_r': "AU20_LipStretcher", 'AU23_r':'AU23_LipTightener',\
                'AU25_r': "AU25_LipsPart", 'AU26_r':'AU26_JawDrop', 
                'AU45_r': "AU45_BlinkInt", 'AU45_c': 'AUc45_BlinkRate',\
                'AU28_c': 'AUc28_LipSuck',\
                'pose_Tx': 'headOrient_x', 'pose_Ty': 'headOrient_y', \
                'pose_Tz': 'headOrient_z', 'timestamp':'ts(sec)'}, inplace = True)
    #adding pp number col
    temp.insert(0, 'pp_id', name)
    #adding condition col
    temp.insert(1, 'condition', cond)
    
    
    
    temp.to_csv(dir_out + name +'_'+ cond + '.csv', index=False)
    



# all_data.to_csv('all_face_data.csv')