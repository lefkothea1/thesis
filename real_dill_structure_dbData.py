# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:07:44 2023

@author: lefko
UNDONE! not sre if useful also
trying to restructure the dill file to a csv table with cols:
    pp#, condition, [table:click_mouse (incl ts)], [tabel2].. etc
    
    so far i made it only for the same table, different pps n conditions (when new table gets concated to total data it is NaN)
"""
import os
import dill
import pandas as pd


dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\pp_db'
os.chdir(dir1)
 

data_file_name = 'data_1683723426_W0pp8.dill'

# df = pd.read_pickle(data_file_name) 

with open(data_file_name, 'rb') as f:
      data = dill.load(f)
      
# pp_idx = range(len(data)) #its the dictionary size
table_names = ["click_mouse", "press_keyboard", "move_mouse", "scroll_mouse"]

total_df = pd.DataFrame()
# # for pp_idx in range(len(data)):
# for pp_idx in range(2): #2test
#     # for table in table_names:
#     for table in table_names[0:1]: #2test
#         #------------------------------------combining conditions S and Ntot-----------------
#         temp_n = pd.DataFrame(data[pp_idx][table][0])
#         temp_n = temp_n.add_prefix(table)
#         temp_n['cond'] = 'N'
#         temp_n['pp_idx'] = pp_idx
#         total_df = pd.concat([total_df, temp_n], ignore_index=True)
#         temp_s = pd.DataFrame(data[pp_idx][table][1])
#         temp_s = temp_s.add_prefix(table)
#         temp_s['cond'] = 'S'
#         temp_s['pp_idx'] = pp_idx
#         total_df = pd.concat([total_df, temp_s], ignore_index=True)
#     #------------------------------------combining tables, end up with NAN-----------------



for table in table_names[0:1]: #2test
    for pp_idx in range(5): #2test
        #------------------------------------combining conditions and pps WITHIN a table-----------------
        temp_n = pd.DataFrame(data[pp_idx][table][0])
        temp_n = temp_n.add_prefix(table)
        temp_n['cond'] = 'N'
        temp_n['pp_idx'] = pp_idx
        total_df = pd.concat([total_df, temp_n], ignore_index=True)
        temp_s = pd.DataFrame(data[pp_idx][table][1])
        temp_s = temp_s.add_prefix(table)
        temp_s['cond'] = 'S'
        temp_s['pp_idx'] = pp_idx
        total_df = pd.concat([total_df, temp_s], ignore_index=True)
    #------------------------------------combining tables-----------------
        

