# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 14:37:06 2023

@author: lefko
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



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
    
dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\pp_db_ppMeanAnalysis_outputFINAL'
os.chdir(dir1)

df = pd.read_csv('clickMouse_table_PPmeans.csv')
plot_mean_bar_indiv_lines(df['click0_count_neutral']/45, df['click0_count_stress']/45, 'mouse dynamics: Left Click rate', 'clicks/min')
plot_mean_bar_indiv_lines(df['click1_count_neutral']/45, df['click1_count_stress']/45, 'mouse dynamics: Right Click rate', 'clicks/min')
plot_mean_bar_indiv_lines(df['click_duration_neutral(s)'], df['click_duration_stress(s)'], 'mouse dynamics: click duration', 'sec')

df = pd.read_csv('keyboard_table_PPmeans.csv')
plot_mean_bar_indiv_lines(df['total_keys_pressed_neutral']/45, df['total_keys_pressed_stress']/45, 'Keyboard Dynamics: Key Press Rate', 'keys/sec')
plot_mean_bar_indiv_lines(df['total_backspaces_neutral']/45, df['total_backspaces_stress']/45, 'Keyboard Dynamics: Error Key Rate', 'keys/sec')
NOT PLOTTING press_duration_neutral and backspace duration  as it not accurate 
plot_mean_bar_indiv_lines(df['WPM_neutral'], df['WPM_stress'], 'Keyboard Dynamics: Words Per Minute', 'WPM') #not gonna show it gt idio me key rate
plot_mean_bar_indiv_lines(df['pause_rate_neutral'], df['pause_rate_stress'], 'Keyboard Dynamics: non- typing time (pause rate)', 'percentage') #plotting one of the pause features cause theyre dinetical

df = pd.read_csv('mouse_move_table_PPmeans.csv')
plot_mean_bar_indiv_lines(df['mouse_move_time_diff_Neutral'], df['mouse_move_time_diff_Stress'], 'Mouse Dynamics: Mean Move Duration', 'sec')
plot_mean_bar_indiv_lines(df['mouse_move_dist_diff_Neutral'], df['mouse_move_dist_diff_Stress'], 'Mouse Dynamics: Mean Move Distance', 'pixels')
plot_mean_bar_indiv_lines(df['mouse_move_speed_Neutral(pixel/sec)'], df['mouse_move_speed_Stress'], 'Mouse Dynamics: Mean Move Speed', 'pixels/sec')
plot_mean_bar_indiv_lines(df['mouse_move_total_time_Neutral'], df['mouse_move_total_time_Stress'], 'Mouse Dynamics: Total Mouse Move duration', 'sec')
plot_mean_bar_indiv_lines(df['mouse_move_total_dist_Neutral'], df['mouse_move_total_dist_Stress'], 'Mouse Dynamics: Total Mouse Move Distance', 'pixels')


df = pd.read_csv('scroll_table_PPmeans.csv')
plot_mean_bar_indiv_lines(df['mean_scroll_duration_neutral'], df['mean_scroll_duration_stress'], 'Mouse Dynamics: Mean Scroll Duration','sec')
