# -*- coding: utf-8 -*-
"""
Created on Mon May  1 15:33:59 2023

@author: lefko
"""
import pandas as pd
import sqlite3
import os
#import sqlalchemy 


dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\pp_db\\pp2'
os.chdir(dir1)


try:
    conn = sqlite3.connect("1681199666.db")    
except Exception as e:
    print(e)

#Now in order to read in pandas dataframe we need to know table name
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(f"Table Name : {cursor.fetchall()}")

df = pd.read_sql_query('SELECT * FROM press_keyboard', conn)
conn.close()

print (df.head())