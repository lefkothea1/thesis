# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 15:47:38 2023

@author: lefko
"""
import pandas as pd
import os
from scipy.stats import ttest_rel, wilcoxon

dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\questionnaire_stat'
os.chdir(dir1)

df = pd.read_csv('question_data4stat.csv')

neutral =df['neutral_time']
stress = df['stress_time']
 
t_stat, p_value = wilcoxon(neutral, stress)
print('wilcoxon for HOW MUCH TIME PRESSURE DID U EXPERIENCE')
print("T-statistic value: ", t_stat)  
print("P-Value: ", p_value)
if p_value<= 0.05:
    print('ABOVE IS SIGNIFICANT!!')
    
neutral =df['neutral_stress']
stress = df['stress_stress']
 
t_stat, p_value = wilcoxon(neutral, stress)
print('wilcoxon result for HOW MUCH STRESS DID U EXPERIENCE')
print("T-statistic value: ", t_stat)  
print("P-Value: ", p_value)
if p_value<= 0.05:
    print('ABOVE IS SIGNIFICANT!!')