# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:53:11 2023

@author: lefko/teo
"""
from datetime import datetime, timedelta
import csv
import os
import pandas as pd

def create_csv_between_times(start_time_str, end_time_str, input_file, output_file):
    """
    Creates a new CSV file containing the intervals and times between two time points.
    
    Parameters:
    start_time_str (str): A string representing the start time in the format "hh:mm:ss".
    end_time_str (str): A string representing the end time in the format "hh:mm:ss".
    input_file (str): The name of the input CSV file.
    output_file (str): The name of the output CSV file.
    """
    
    # Convert the start and end times to datetime objects
    title_date = datetime.strptime(input_file.split(".")[0], '%Y-%m-%d %H-%M-%S')
    start_time = datetime.strptime(start_time_str, '%H-%M-%S')
    start_time = title_date.replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second)
    end_time = datetime.strptime(end_time_str, '%H-%M-%S')
    end_time = title_date.replace(hour=end_time.hour, minute=end_time.minute, second=end_time.second)
    
    # Read the input CSV file
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        
    # Convert each interval to its corresponding time with the cumulative date
    cumulative_date = title_date
    new_data = []
    for i in range(len(data)):
        ms = int(data[i][0])
        interval_date = cumulative_date + timedelta(milliseconds=ms)
        if start_time <= interval_date <= end_time:
            new_data.append([data[i][0], interval_date.strftime('%Y-%m-%d %H-%M-%S.%f')])
        cumulative_date = interval_date
    
    # Write the results to a new CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_data)
        
        
        
        
dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\day1_11-April-23\\pp2\\polar\\pp2_pt12023-04-11 10-30-43 - Copy_renamed'
os.chdir(dir1)

# Input and output file names
input_file = '2023-04-11 10-30-43.txt'
output_file = input_file


# Read the input CSV file
with open(input_file, 'r') as f:
    reader = csv.reader(f)
    data = [row for row in reader]


    
    
# Get the title date from the input file name
title_date = datetime.strptime(input_file.split(".")[0], '%Y-%m-%d %H-%M-%S')

# Convert each interval to its corresponding time with the cumulative date
cumulative_date = title_date
for i in range(len(data)):
    ms = int(data[i][0])
    interval_date = cumulative_date + timedelta(milliseconds=ms)
    data[i].append(interval_date.strftime('%Y-%m-%d %H:%M:%S.%f'))
    cumulative_date = interval_date

# Write the results to a new CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)



create_csv_between_times('10-30-43', '11-30-43', csv_file, activity_name)