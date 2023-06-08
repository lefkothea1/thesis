# -*- coding: utf-8 -*-
"""
Created on Wed May  3 18:34:52 2023

@author: lefko

    
#outpout dill: data[pp_idx_in_folder][db_table][0]--> neutral
#             data[pp_idx_in_folder][db_table][1]--> stress
#             data[pp_idx_in_folder][db_table][2]--> combined


excluded db of pp8 ,some bug makes the stress array empty
"""
import numpy
#data = numpy.loadtxt("D:/Downloads/press_keyboard.csv", skiprows=1, delimiter=',', quotechar='"')
#keys = data[:,1]
#keys = ''.join([chr(int(c)) for c in data[:,1]])
#print(keys)


import sqlite3
from matplotlib import pyplot
import dill
import time
import os

dir1 = 'D:\\arxeia\\AI_VU\\THESIS_internship\\3-experimental\\data\\perSensor\\pp_db'
os.chdir(dir1)
 

load_data = False
# load_data = True
data_file_name = 'data_1683723067_W0pp6.dill'

 
if load_data:
      with open(data_file_name, 'rb') as f:
            data = dill.load(f)
else:
      file_list = [
            "pp2_1681199666.db",
            "pp3_1681211632.db",
            "pp4_1681222920.db",
            "pp5_766128782097970.db",
            "pp6_611326455666529.db",
            "pp7_599918311050588.db",
            # "pp8_922633815604365.db",#sth wrong with pp_idx6, stress data is empty
            "pp9_329099058570807.db",
            "pp11_145332461910408.db",
            "pp12_214191945255252.db",
            "pp13_134978789766445.db",
            "pp15_583687315866200.db",
            "pp16_678555598080922.db",
            "pp17_862277712727918.db",
            'pp18_010737528168533.db',
            'pp19_241334338585163.db',
            'pp20_854221747854308.db',
            'pp22_855738491523635.db',
            'pp23_151893617532019.db',
            'pp24_519859160092726.db',
            'pp25_563356877779437.db',
            'pp26_838539782019845.db'
      ]


      start_condition_time_1 = [
            1681201375.05938,
            1681212435.11465,
            1681223563.22855,
            1681373610.96539,
            1681373610.96539,
            1681386023.20309,
            # 1681386023.203090,
            1681720296.33971,
            1681731162.04832,
            1681978278.26150,
            1681978278.26150,
            1682410489.32556,
            1682422360.93932,
            1682422360.93932,#pp17
            1683533693.85086,
            1683545667.09950,
            1683545667.09950,
            1683643353.42956,               
            1683643353.42956,
            1683804645.35396,
            1683816564.40850,
            1683816564.40850

            
      ]

      end_condition_time_1 = [
            1681204075.05938,
            1681215135.114650,
            1681226263.228550,
            1681376310.965390,
            1681376310.965390,
            1681388723.203090,
            # 1681388723.203090,
            1681722996.33971,
            1681733862.04832,
            1681980978.26150,
            1681980978.26150,
            1682413189.32556,
            1682425060.93932,
            1682425060.93932,#pp17
            1683536393.850860,
            1683548367.099500,
            1683548367.099500,
            1683646053.429560,
            1683646053.429560,
            1683807345.353960,
            1683819264.408500,
            1683819264.408500
      ]

      start_condition_time_2 = [
            1681204705.64030,
            1681215479.86938, 
            1681226918.26452,
            1681376983.52251,
            1681376980.14483,
            1681389219.97856,
            # 1681376980.14483,
            1681723583.43346,
            1681734093.22135,
            1681981758.03373,
            1681981754.27047,
            1682413743.42901,
            1682426196.02803,
            1682426194.79324, #pp17
            1683536867.48762,
            1683548962.24024,
            1683548971.70138,
            1683646699.07074,
            1683646699.48218,
            1683807273.62899,
            1683819671.34145,
            1683819670.87299            
      ]

      end_condition_time_2 = [
            1681207405.64030,
            1681218179.86938,
            1681229618.26452,
            1681379683.52251,
            1681379680.14483,
            1681391919.97856,
            # 1681379680.14483,
            1681726283.43346,
            1681736793.22135,
            1681984458.03373,
            1681984454.27047,
            1682416443.42901,
            1682428896.02803,
            1682428894.79324, #pp17
            1683539567.48762,
            1683551662.24024,
            1683551671.70138,
            1683649399.07074,
            1683649399.48218,
            1683809973.62899,
            1683822371.34145,
            1683822370.87299            
]

 
      participant_numbers = range(len(file_list))
      table_names = ["click_mouse", "press_keyboard", "move_mouse", "scroll_mouse"]
 
      data = {}
      for participant_number in participant_numbers:
            file_name = file_list[participant_number]
            con = sqlite3.connect(file_name)
            cur = con.cursor()


            data[participant_number] = {}
            for table_name in table_names:
                  query = "SELECT * FROM %s" % table_name
                  result = cur.execute(query)
                  all_data = numpy.asarray(result.fetchall())
                  condition_1_selection = (all_data[:,0]>start_condition_time_1[participant_number]) & (all_data[:,0]<=end_condition_time_1[participant_number])
                  condition_2_selection = (all_data[:,0]>start_condition_time_2[participant_number]) & (all_data[:,0]<=end_condition_time_2[participant_number])
                  data[participant_number][table_name] = {}
                  data[participant_number][table_name][0] = all_data[condition_1_selection]
                  data[participant_number][table_name][1] = all_data[condition_2_selection]
                  data[participant_number][table_name][2] = numpy.concatenate((data[participant_number][table_name][0], data[participant_number][table_name][1]))

            cur.close()
            con.close()

 
#output dill: data[pp_idx_in_folder][db_table][0]--> neutral
#             data[pp_idx_in_folder][db_table][1]--> stress
#             data[pp_idx_in_folder][db_table][2]--> combined

      #plot_data_x = [x[1] for x in data['move_mouse']]
      #plot_data_y = [x[2] for x in data['move_mouse']]
      #pyplot.plot(plot_data_x, plot_data_y)
      #pyplot.show()

      with open('ALLdata_%d_W0pp8.dill' % time.time(), 'wb') as f:
            dill.dump(data, f)

 

# DO ANALYSIS WITH data
test = 1

# for i in range(len(start_condition_time_2)):   

#     print(end_condition_time_2[i] - start_condition_time_2[i])