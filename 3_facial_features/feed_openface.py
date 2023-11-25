# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:04:05 2023

@author: lefko
"""
import os

# Set the path to the OpenFace installation directory
openface_dir = 'D:\\arxeia\\AI_VU\\THESIS_internship\\openFace\\OpenFace_2.2.0_win_x64\\OpenFace_2.2.0_win_x64'

# Set the path to the input image or video
input_vid = 'pp02_neutral.mkv'  

# Set the output directory for the generated files
output_dir = 'G:\\lefs_cut_vids\\openFace_output'

# Set the command to run OpenFace based on the task you want to perform
command = 'FeatureExtraction.exe -f "{input_vid}" -out_dir "{output_dir}"'

os.chdir(openface_dir)
# Run the command
os.system(command)
