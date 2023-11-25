# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:04:28 2023

@author: lefko
doing statistics on typing behavior metrics
"""

import os
import pandas as pd
from scipy.stats import ttest_rel


dir_in = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\pp_db_ppMeanAnalysis_outputFINAL'
os.chdir(dir_in)
#------------------------------------------------------------------------------------------
click_filename = 'clickMouse_table_PPmeans.csv'

dfclick = pd.read_csv(click_filename)

pairs = [['click0_count_neutral','click0_count_stress'],\
         ['click1_count_neutral','click1_count_stress'],\
        ['click_duration_neutral(s)','click_duration_stress(s)'],\
        ['LclickRate_neutral', 'LclickRate_stress'],\
        ['RclickRate_neutral', 'RclickRate_stress']]
    
for pair in pairs:
# pair=pairs[0] #make into loop
    neutral =dfclick[pair[0]]
    stress = dfclick[pair[1]]
    
    t_stat, p_value = ttest_rel(neutral, stress)
    print('one sided paired t-test result for '+ str(pair[0].split('_')[:-1]))
    print("T-statistic value: ", t_stat)  
    print("P-Value: ", p_value)
    if p_value<= 0.05:
        print('ABOVE IS SIGNIFICANT!!')
    
 #------------------------------------------------------------------------------------------            
dfkey = pd.read_csv('keyboard_table_PPmeans.csv') 

pairs = [\
         ['total_keys_pressed_neutral','total_keys_pressed_stress'],\
        ['total_backspaces_neutral', 'total_backspaces_stress'],\
        ['press_duration_neutral', 'press_duration_stress'],
        ['backspace_duration_neutral','backspace_duration_stress'],\
            ['WPM_neutral', 'WPM_stress'],['pause_dur_neutral','pause_dur_stress'],\
                ['pause_rate_neutral','pause_rate_stress'],\
            ['keyRate_neutral', 'keyRate_stress'],\
            ['errorKeyRate_neutral', 'errorKeyRate_stress'] ]

for pair in pairs:
# pair=pairs[0] #make into loop
    neutral =dfkey[pair[0]]
    stress = dfkey[pair[1]]
    
    t_stat, p_value = ttest_rel(neutral, stress, nan_policy='omit')
    print('one sided paired t-test result for '+ str(pair[0].split('_')[:-1]))
    print("T-statistic value: ", t_stat)  
    print("P-Value: ", p_value)
    if p_value<= 0.05:
        print('ABOVE IS SIGNIFICANT!!')
#------------------------------------------------------------------------------------------
dfmove = pd.read_csv('mouse_move_table_PPmeans.csv')
pairs = [['mouse_move_time_diff_Neutral','mouse_move_time_diff_Stress'],\
         ['mouse_move_dist_diff_Neutral','mouse_move_dist_diff_Stress'],\
        ['mouse_move_total_time_Neutral','mouse_move_total_time_Stress'],\
        ['mouse_move_total_dist_Neutral','mouse_move_total_dist_Stress'],\
        ['mouse_move_speed_Neutral(pixel/sec)','mouse_move_speed_Stress']]
    
for pair in pairs:
# pair=pairs[0] #make into loop
    neutral =dfmove[pair[0]]
    stress = dfmove[pair[1]]
    
    t_stat, p_value = ttest_rel(neutral, stress)
    print('one sided paired t-test result for '+ str(pair[0].split('_')[:-1]))
    print("T-statistic value: ", t_stat)  
    print("P-Value: ", p_value)
    if p_value<= 0.05:
        print('ABOVE IS SIGNIFICANT!!')
    
#------------------------------------------------------------------------------------------
dfscroll = pd.read_csv('scroll_table_PPmeans.csv')
pairs = [['mean_scroll_duration_neutral', 'mean_scroll_duration_stress'],\
         ['total_scroll_duration_neutral', 'total_scroll_duration_stress'],\
        ['total_scroll_distance_neutral', 'total_scroll_distance_stress'],\
        ['total_scroll_count_neutral','total_scroll_count_stress']]
    
for pair in pairs:
# pair=pairs[0] #make into loop
    neutral =dfscroll[pair[0]]
    stress = dfscroll[pair[1]]
    
    t_stat, p_value = ttest_rel(neutral, stress)
    print('one sided paired t-test result for '+ str(pair[0].split('_')[:-1]))
    print("T-statistic value: ", t_stat)  
    print("P-Value: ", p_value)
    if p_value<= 0.05:
        print('ABOVE IS SIGNIFICANT!!')
        
        
