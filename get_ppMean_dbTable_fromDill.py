# -*- coding: utf-8 -*-
"""
Created on Wed May 10 12:45:47 2023

@author: lefko

#outpout dill: data[pp_idx_in_folder][db_table][0]--> neutral
#             data[pp_idx_in_folder][db_table][1]--> stress
#             data[pp_idx_in_folder][db_table][2]--> combined

useful col indexes of each table (ts is always col0):
click mouse table: 3rd col is button_pressed and 4th is button_hold_time
move_mouse table: 3rd col is total_mouse_move_distance and 4th is total_mouse_move_time
press_keyboard: 2nd-total_keys, 3rd-total_press_keyboard_time, 4th-total_backspaces, 5th:
scroll_mouse: 5th- total_mouse_scroll_distance, 6th-total mousescrol time
"""
import os
import dill
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

#could also save it
def plot_mean_bar_indiv_lines(cond1_array, cond2_array, title, ylabel):
    for i in range(len(cond1_array)):
        plt.plot([0,1], [cond1_array[i], cond2_array[i]], 'o-', label=('pp_idx_'+str(i)))
    
    # Add the mean values to the plot as bars, with stdev as error
    error = [np.std(cond1_array), np.std(cond2_array)]
    plt.bar([0, 1], [np.nanmean(cond1_array), np.nanmean(cond2_array)], yerr=error, color='gray', alpha=0.5, edgecolor='black', linewidth=1.5, capsize=10)

    # Add labels and title
    plt.xlabel('Conditions')
    plt.xticks(ticks=[0,1], labels=['neutral','stress'])
    plt.ylabel(ylabel)
    plt.title(title)

    # Add legend and show the plot
    # plt.legend()
    plt.tight_layout()
    plt.show()

#dir_out includes the last/
# def analyse_move_mouse_table_from_dill(data, table, saving_dir): #-------------------------------------------------------------------------

#     useful_cols = [3,4]
#     col_names = ['cum_move_dist', 'cum_move_time']
    
#     #will hold the mean time and distance the mouse was moved per PP and per condition
#     time_neutral=[] ; dist_neutral=[] ; tot_dist_neutral=[] ; tot_time_neutral=[]
#     time_stress=[] ; dist_stress=[] ; tot_dist_stress=[] ; tot_time_stress=[]
    
    
#     for cond in [0,1]: 
#         for pp_idx in range(len(data)):
           
#             cond_df = pd.DataFrame(data[pp_idx][table][cond][:, 3:5], columns = col_names)
#             #adding cols with duration and distance of every mouse move (not cummulative)
#             cond_df['dist_diff'] = cond_df['cum_move_dist'].diff()
#             cond_df['time_diff'] = cond_df['cum_move_time'].diff()
            
#             if cond == 0: #neutral
#                 time_neutral.append(cond_df['time_diff'].mean())
#                 dist_neutral.append(cond_df['dist_diff'].mean())
#                 tot_dist_neutral.append(cond_df['dist_diff'].sum())
#                 tot_time_neutral.append(cond_df['time_diff'].sum())
                
#             if cond == 1: #stress
#                 time_stress.append(cond_df['time_diff'].mean())
#                 dist_stress.append(cond_df['dist_diff'].mean())
#                 tot_dist_stress.append(cond_df['dist_diff'].sum())
#                 tot_time_stress.append(cond_df['time_diff'].sum())
    
    
#     plot_mean_bar_indiv_lines(time_neutral, time_stress, 'move_mouse: Mean duration of every mouse move', 'move_duration (s)')
#     plot_mean_bar_indiv_lines(dist_neutral, dist_stress, 'move_mouse: Mean distance of every mouse move', 'move_distance')
#     plot_mean_bar_indiv_lines(tot_time_neutral, tot_time_stress, 'move_mouse: total duration of all mouse moves', 'move_duration (s)')
#     plot_mean_bar_indiv_lines(tot_dist_neutral, tot_dist_stress, 'move_mouse: total distance of all mouse moves', 'move_distance')
    
#     #outputting result in csv 
#     out_df=pd.DataFrame()
#     out_df['mouse_move_time_diff_Neutral'] = time_neutral
#     out_df['mouse_move_dist_diff_Neutral'] = dist_neutral
#     out_df['mouse_move_total_time_Neutral'] = tot_time_neutral
#     out_df['mouse_move_total_dist_Neutral'] = tot_dist_neutral
#     out_df['mouse_move_time_diff_Stress'] = time_stress
#     out_df['mouse_move_dist_diff_Stress'] = dist_stress
#     out_df['mouse_move_total_time_Stress'] = tot_time_stress
#     out_df['mouse_move_total_dist_Stress'] = tot_dist_stress
#     out_df.to_csv(saving_dir + 'mouse_move_table_PPmeans.csv')

#it will create output folder on dir up from dir_in
def make_output_folder(name):
    now = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    dir_out = dir_in+ name + now +'/'
    os.makedirs(dir_out)
    print('created folder'+str(dir_out))
    return dir_out     

#dir_out includes the last/
def analyse_press_keyboard_table_from_dill(data, table, dir_out):
    useful_cols = [2,3,4,5]
    col_names = ['cum_keys', 'cum_press_dur', 'cum_backspaces', 'cum_backspaces_dur']
    
    
    tot_keys_neutral=[] ; press_dur_neutral=[] ; tot_backs_neutral=[] ; back_dur_neutral=[]
    tot_keys_stress=[] ; press_dur_stress=[] ; tot_backs_stress=[] ; back_dur_stress=[]
    
    for cond in [0,1]: 
        for pp_idx in range(len(data)):
            
            cond_df = pd.DataFrame(data[pp_idx][table][cond][:, 2:6], columns = col_names)
            
            cond_df2 = cond_df.diff()
            cond_df2.columns= ['key', 'press_dur','backspace', 'backspace_dur']
            
            if cond == 0: 
                tot_keys_neutral.append(cond_df2['key'].sum())
                tot_backs_neutral.append(cond_df2['backspace'].sum())
                press_dur_neutral.append(cond_df2['press_dur'].mean())
                back_dur_neutral.append(cond_df2['backspace_dur'].mean())
            if cond == 1: 
                tot_keys_stress.append(cond_df2['key'].sum())
                tot_backs_stress.append(cond_df2['backspace'].sum())
                press_dur_stress.append(cond_df2['press_dur'].mean())
                back_dur_stress.append(cond_df2['backspace_dur'].mean())
    #afterwe have the total keyCount per pp, i can create their typing spped as wpm:
    wpm_neutral = [(x / 5)/45 for x in tot_keys_neutral]
    wpm_stress = [(x / 5)/45 for x in tot_keys_stress]
    plot_mean_bar_indiv_lines(tot_keys_neutral, tot_keys_stress, 'keyboard: total keys pressed', 'key count')
    plot_mean_bar_indiv_lines( wpm_neutral, wpm_stress, 'keyboard: typing speed as WPM', 'WPM')
    plot_mean_bar_indiv_lines(tot_backs_neutral, tot_backs_stress, 'keyboard: total backspace count', 'backspace count')
    plot_mean_bar_indiv_lines(press_dur_neutral, press_dur_stress, 'keyboard: mean key press duration', 'duration (s)')
    plot_mean_bar_indiv_lines(back_dur_neutral, back_dur_stress, 'keyboard: mean backspace press duration', 'duration (s)')
                
    
    #outputting result in csv 
    out_df = pd.DataFrame()
    out_df['total_keys_pressed_neutral'] = tot_keys_neutral
    # out_df['total_keyRatio_neutral(keys/min)'] = tot_keys_neutral/45
    out_df['total_backspaces_neutral'] = tot_backs_neutral
    out_df['press_duration_neutral'] = press_dur_neutral
    out_df['backspace_duration_neutral'] = back_dur_neutral
    out_df['WPM_neutral'] = wpm_neutral
    out_df['total_keys_pressed_stress'] = tot_keys_stress
    # out_df['total_keyRatio_stress(keys/min)'] = tot_keys_stress/45
    out_df['total_backspaces_stress'] = tot_backs_stress
    out_df['press_duration_stress'] = press_dur_stress
    out_df['backspace_duration_stress'] = back_dur_stress
    out_df['WPM_stress'] = wpm_stress
    out_df.to_csv(dir_out + 'keyboard_table_PPmeans.csv')

#dir_out includes the last/
def analyse_scroll_mouse_table_from_dill(data, table, saving_dir): #-------------------------------------------------------------------------
    
    useful_cols = [5,6]
    col_names = ['cum_scroll_dist', 'cum_scroll_time']
    
    #will hold the mean time  the mouse was scrolld per PP and per condition (distance is useless)
    time_neutral=[] ;  tot_dist_neutral=[] ; tot_time_neutral=[] ; count_neutral=[] #; dist_neutral=[]
    time_stress=[] ;  tot_dist_stress=[] ; tot_time_stress=[]; count_stress=[] #;dist_stress=[] 
    
    
    for cond in [0,1]: 
        for pp_idx in range(len(data)):
           
            cond_df = pd.DataFrame(data[pp_idx][table][cond][:, 5:], columns = col_names)
            #adding cols with duration and distance of every mouse scroll (not cummulative)
            cond_df['dist_diff'] = cond_df['cum_scroll_dist'].diff()
            cond_df['time_diff'] = cond_df['cum_scroll_time'].diff()
            
            if cond == 0: #neutral
                time_neutral.append(cond_df['time_diff'].mean())
                # dist_neutral.append(cond_df['dist_diff'].mean())
                tot_dist_neutral.append(cond_df['dist_diff'].sum())
                tot_time_neutral.append(cond_df['time_diff'].sum())
                count_neutral.append(len(cond_df))
                
            if cond == 1: #stress
                time_stress.append(cond_df['time_diff'].mean())
                # dist_stress.append(cond_df['dist_diff'].mean())
                tot_dist_stress.append(cond_df['dist_diff'].sum())
                tot_time_stress.append(cond_df['time_diff'].sum())
                count_stress.append(len(cond_df))
    
    
    plot_mean_bar_indiv_lines(time_neutral, time_stress, 'scroll_mouse: Mean duration of every mouse scroll', 'scroll_duration (s)')
    # plot_mean_bar_indiv_lines(dist_neutral, dist_stress, 'scroll_mouse: Mean distance of every mouse scroll', 'scroll_distance')
    plot_mean_bar_indiv_lines(tot_time_neutral, tot_time_stress, 'scroll_mouse: total duration of all mouse scrolls', 'scroll_duration (s)')
    plot_mean_bar_indiv_lines(tot_dist_neutral, tot_dist_stress, 'scroll_mouse: total distance of all mouse scrolls', 'scroll_distance (pixels)')
    plot_mean_bar_indiv_lines(count_neutral, count_stress, 'scroll_mouse: scroll count', 'count')
    
    #outputting result in csv 
    out_df=pd.DataFrame()
    out_df['mean_scroll_duration_neutral']= time_neutral
    out_df['total_scroll_duration_neutral']=tot_time_neutral
    out_df['total_scroll_distance_neutral']= tot_dist_neutral
    out_df['total_scroll_count_neutral'] = count_neutral
    out_df['mean_scroll_duration_stress']= time_stress
    out_df['total_scroll_duration_stress']=tot_time_stress
    out_df['total_scroll_distance_stress']= tot_dist_stress
    out_df['total_scroll_count_stress'] = count_stress
    out_df.to_csv(dir_out + 'scroll_table_PPmeans.csv')

#dir_out includes the last/
def analyse_click_table_from_dill(data, table, dir_out):
    #click mouse: 3rd col is button_pressed and 4th is button_hold_time
    
    
    useful_cols = [3,4]
    col_names = ['button', 'duration']
    
    #get_click_counts_n_duration_perPP()---------------------------------------------------------------
    neutral_0s_count = [] ; neutral_1s_count = [] #stores count per pp
    stress_0s_count = [] ; stress_1s_count = [] #stores count per pp    
    click_dur_neutral = [] ; click_dur_stress = [] #to store click duration per pp (of both keys)
    
    for cond in [0,1]: 
        for pp_idx in range(len(data)):
           
            cond_df = pd.DataFrame(data[pp_idx][table][cond][:, 3:5], columns = col_names) #df[df['button']==0]['duration']
            
            if cond == 0: #neutral:
                neutral_0s_count.append(cond_df['button'].value_counts()[0])
                neutral_1s_count.append(cond_df['button'].value_counts().get(1, default=0))
                
                click_dur_neutral.append(cond_df['duration'].mean())
                
            if cond == 1: #stress
                stress_0s_count.append(cond_df['button'].value_counts()[0])
                stress_1s_count.append(cond_df['button'].value_counts().get(1, default=0))
                
                click_dur_stress.append(cond_df['duration'].mean())
     
                
                #also maybe save plots?
    plot_mean_bar_indiv_lines(neutral_0s_count, stress_0s_count, 'mouse_click: 0s count in neutral and stress', 'click_count')
    plot_mean_bar_indiv_lines(neutral_1s_count, stress_1s_count, 'mouse_click: 1s count in neutral and stress', 'click_count')
    
    plot_mean_bar_indiv_lines(click_dur_neutral, click_dur_stress, 'mouse_click: click durations in neutral and stress' ,'click_duration(s)')
    
    #outputting result in csv 
    out_df=pd.DataFrame()
    out_df['click0_count_neutral'] = neutral_0s_count
    out_df['click1_count_neutral'] = neutral_1s_count
    out_df['click_duration_neutral(s)'] = click_dur_neutral
    out_df['click0_count_stress'] = stress_0s_count
    out_df['click1_count_stress'] = stress_1s_count
    out_df['click_duration_stress(s)'] = click_dur_stress
    # out_df['click0_ratio_Neutral (clicks/45min)'] = neutral_0s_count/45
    # out_df['click1_ratio_Neutral (clicks/45min)'] = neutral_1s_count/45
    
    out_df.to_csv(dir_out + 'clickMouse_table_PPmeans.csv')
    
#dir_out includes the last/
def analyse_move_mouse_table_from_dill(data, table, saving_dir): #-------------------------------------------------------------------------

    useful_cols = [3,4]
    col_names = ['cum_move_dist', 'cum_move_time']
    
    #will hold the mean time and distance the mouse was moved per PP and per condition
    time_neutral=[] ; dist_neutral=[] ; tot_dist_neutral=[] ; tot_time_neutral=[]
    time_stress=[] ; dist_stress=[] ; tot_dist_stress=[] ; tot_time_stress=[]
    speed_neutral=[] ; speed_stress = []
    
    for cond in [0,1]: 
        for pp_idx in range(len(data)):
           
            cond_df = pd.DataFrame(data[pp_idx][table][cond][:, 3:5], columns = col_names)
            #adding cols with duration and distance of every mouse move (not cummulative)
            cond_df['dist_diff'] = cond_df['cum_move_dist'].diff()
            cond_df['time_diff'] = cond_df['cum_move_time'].diff()
            
            if cond == 0: #neutral
                time_neutral.append(cond_df['time_diff'].mean())
                dist_neutral.append(cond_df['dist_diff'].mean())
                tot_dist_neutral.append(cond_df['dist_diff'].sum())
                tot_time_neutral.append(cond_df['time_diff'].sum())
                speed_neutral.append( (cond_df['dist_diff']/cond_df['time_diff']).mean() )
                
            if cond == 1: #stress
                time_stress.append(cond_df['time_diff'].mean())
                dist_stress.append(cond_df['dist_diff'].mean())
                tot_dist_stress.append(cond_df['dist_diff'].sum())
                tot_time_stress.append(cond_df['time_diff'].sum())
                speed_stress.append( (cond_df['dist_diff']/cond_df['time_diff']).mean() )
    
    
    plot_mean_bar_indiv_lines(time_neutral, time_stress, 'move_mouse: Mean duration of every mouse move', 'move_duration (s)')
    plot_mean_bar_indiv_lines(dist_neutral, dist_stress, 'move_mouse: Mean distance of every mouse move', 'move_distance(pixels')
    plot_mean_bar_indiv_lines(tot_time_neutral, tot_time_stress, 'move_mouse: total duration of all mouse moves', 'move_duration (s)')
    plot_mean_bar_indiv_lines(tot_dist_neutral, tot_dist_stress, 'move_mouse: total distance of all mouse moves', 'move_distance(pixels)')
    plot_mean_bar_indiv_lines(speed_neutral, speed_stress, 'move_mouse: mean speed of every mouse move', 'pixel/sec')
    
    #outputting result in csv 
    out_df=pd.DataFrame()
    out_df['mouse_move_time_diff_Neutral'] = time_neutral
    out_df['mouse_move_dist_diff_Neutral'] = dist_neutral
    out_df['mouse_move_total_time_Neutral'] = tot_time_neutral
    out_df['mouse_move_total_dist_Neutral'] = tot_dist_neutral
    out_df['mouse_move_time_diff_Stress'] = time_stress
    out_df['mouse_move_dist_diff_Stress'] = dist_stress
    out_df['mouse_move_total_time_Stress'] = tot_time_stress
    out_df['mouse_move_total_dist_Stress'] = tot_dist_stress
    out_df['mouse_move_speed_Neutral(pixel/sec)'] = speed_neutral
    out_df['mouse_move_speed_Stress'] = speed_stress
    out_df.to_csv(saving_dir + 'mouse_move_table_PPmeans.csv')



dir_in = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\pp_db'
os.chdir(dir_in)

#dir_out includes the last/
dir_out = make_output_folder('_ppMean_output')


 

data_file_name = 'ALLdata_1685716514_W0pp8.dill'

# df = pd.read_pickle(data_file_name) 

with open(data_file_name, 'rb') as f:
      data = dill.load(f)
      
# pp_idx = range(len(data)) #its the dictionary size
table_names = ["click_mouse", "press_keyboard", "move_mouse", "scroll_mouse"]



#---------------------------------------------------------------------------------------------------
analyse_click_table_from_dill(data, "click_mouse", dir_out)


analyse_move_mouse_table_from_dill(data, "move_mouse", dir_out)

analyse_press_keyboard_table_from_dill(data, 'press_keyboard', dir_out)
#

analyse_scroll_mouse_table_from_dill(data, 'scroll_mouse', dir_out)
