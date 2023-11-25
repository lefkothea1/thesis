# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 14:20:17 2023

@author: lefko
OUTPUT WILL BE REWRITTEN - CAREFUL!!!!!!!!!!!!!!!!!

reads in aggregated per min opennface and db files (incl engineered feautres!!)
db excels are in one folder, all pps, with 1 sheet per condition
openface will be in 1 folder all the pps fr neutral, and in another folder all csv for stress

per pp:
    cond = neutral:
        read excel (db)
        read csv openface
        combine them
    cond = stress
        same as above
    concat 2cond(combo_neutral, combo_stress, axis=0
    export participant csv 
    
"""
import glob
import os
import pandas as pd
from openpyxl import load_workbook

def concat_1pp_typing_openface_1cond(db_file, face_file, cond):
    pp_db = db_file.split('_')[1][:-5]
    db_df = pd.read_excel(dir_db + db_file, sheet_name = cond, engine='openpyxl')
    
    #keeping only middle 30mins of typing behavior
    db_df = db_df.iloc[10:40].reset_index()
    print(len(db_df))
    
    
    pp_face = face_file.split('_')[0]
    face_df = pd.read_csv(dir_face + face_file)
    print(len(face_df))
    
    if pp_face == pp_db:
        pp_cond = pd.concat([face_df, db_df],axis = 1)
        print(pp_face +' ' +cond+ ' concated')
        return pp_cond, pp_face
    else:
        print('pp numbers dont match!')
        print(pp_face, pp_db)
        
        
#has all pps inside, typing behavior aggregated per minute
dir_db = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\pp_db_AggregatedFeat_output20230602_16-51-26\\'
dir_face = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\openFace_out\\retrying_problematic\\aggr1min_processed_OpenFace_pp6-720230616_14-03-32\\'

dir_out ='D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\allSensors_allPPs     \\'

db_filelist = ['allTables_pp02.xlsx','allTables_pp03.xlsx', 'allTables_pp04.xlsx',\
               'allTables_pp05.xlsx','allTables_pp09.xlsx', 'allTables_pp11.xlsx',\
                'allTables_pp12.xlsx','allTables_pp13.xlsx','allTables_pp15.xlsx',\
                'allTables_pp16.xlsx','allTables_pp17.xlsx','allTables_pp18.xlsx',\
                'allTables_pp19.xlsx','allTables_pp22.xlsx','allTables_pp23.xlsx',\
                'allTables_pp24.xlsx','allTables_pp25.xlsx','allTables_pp26.xlsx']

face_filelist_neutral = ['pp02_N.csv', 'pp03_N.csv','pp04_N.csv','pp05_N.csv',\
                         'pp09_N.csv', 'pp11_N.csv','pp12_N.csv','pp13_N.csv',\
                        'pp15_N.csv','pp16_N.csv','pp17_N.csv','pp18_N.csv',\
                        'pp19_N.csv','pp22_N.csv', 'pp23_N.csv','pp24_N.csv',\
                        'pp25_N.csv','pp26_N.csv']


face_filelist_stress = ['pp02_S.csv','pp03_S.csv','pp04_S.csv', 'pp05_S.csv',\
                        'pp09_S.csv','pp11_S.csv','pp12_S.csv','pp13_S.csv',\
                        'pp15_S.csv','pp16_S.csv','pp17_S.csv','pp18_S.csv',\
                        'pp19_S.csv','pp22_S.csv','pp23_S.csv','pp24_S.csv',\
                        'pp25_S.csv','pp26_S.csv']


if not len(db_filelist) == len(face_filelist_neutral) == len(face_filelist_stress):
    print('CHECK YOUR FILE LISTS, they dont match')

all_data=pd.DataFrame()
for i in range(len(db_filelist)):
    pp_neutral, ppNr = concat_1pp_typing_openface_1cond(db_filelist[i], face_filelist_neutral[i], 'neutral')
    # print(len(pp_neutral))
    pp_stress, ppNr = concat_1pp_typing_openface_1cond(db_filelist[i], face_filelist_stress[i], 'stress')
    # print(len(pp_stress))
    
    full_pp = pd.concat([pp_neutral, pp_stress], axis = 0)
    full_pp.to_csv(dir_out + ppNr + '_all1minData.csv', index = False)
    all_data = pd.concat([all_data, full_pp], axis=0) #gathering all conditions for all pps
all_data.to_csv(dir_out + 'all_data_pp9.csv', index = False)


    
    
