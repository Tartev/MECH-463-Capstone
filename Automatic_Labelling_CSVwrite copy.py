#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 21:18:21 2023

@author: vincenttarte
"""
import csv 
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import bessel, filtfilt
import pandas as pd
from scipy import signal

#%%

def closest_values(arr1, arr2):
    TO = []
    HS = []
    for value in arr1:
        closest_before = None
        closest_after = None
        for compare_value in arr2:
            if compare_value >= value:
                closest_after = compare_value
                break
            else:
                closest_before = compare_value
        if closest_before and closest_after != None:
            TO.append(closest_before)
            HS.append(closest_after)
    return np.array(TO), np.array(HS)



#%%

def add_string_to_csv_at_indices(filename, arr, row_indices_TO,row_indices_HS, string_value):
    with open(filename, 'r') as f_input, open('output.csv', 'w') as output_csv:
        
        swing = 0 
        
        reader = csv.reader(f_input,dialect = 'excel')
        writer = csv.writer(output_csv)
        
        # add the new column to the header
        
        
        # Iterate over the rows of the input CSV
        for i, row in enumerate(reader):
            
            # Skip the first two rows (the header rows)
            
            if i < 1:
                
                writer.writerow(row)
                
                continue
            
            if i in row_indices_TO:
                
                row.append(int(arr[np.where(row_indices_TO == i)]))
                swing = 1
                
            if i in row_indices_HS:
                
                row.append(int(arr[np.where(row_indices_HS == i)]))    
                swing = 0 
                
            elif swing == 1:
                
                row.append('1')
                
            else:
                
                row.append('0')
                
            # Modify the row and write it to the output CSV
    
            writer.writerow(row)
        
        

#%%

# Load data and set parameters

data = pd.read_csv("data_dev.csv")

gyroscope_values = data["Shimmer_6835_Gyro_Z_CAL"]

time_stamp = data["time_stamp"]


fs = 120.482  # Sampling rate

fc = 10  # Cut-off frequency


# Filter data

b, a = bessel(2, fc/(fs/2), btype='low')  # 2nd order Bessel filter

filtered_data = filtfilt(b, a, gyroscope_values)

#filtered_data = gyroscope_values

# Initialize variables

# Find peaks(max).
peak_indexes = signal.find_peaks(filtered_data, height = 100, distance = 40)
peak_indexes = peak_indexes[0]
 
# Find valleys(min).
valley_indexes = signal.argrelextrema(filtered_data, np.less, order = 1)
valley_indexes = valley_indexes[0]

#find mid-stance local maxima

MidStance_indexes = signal.argrelextrema(-filtered_data, np.less, order = 1)

MidStance_indexes = MidStance_indexes[0]

MidStance_index = []

index = 0

for i in range(0,len(MidStance_indexes)):
     
    if filtered_data[MidStance_indexes[i]] < 0:
        print('if')
        MidStance_index.append(MidStance_indexes[i])
    
    

TO, HS = closest_values(peak_indexes,valley_indexes)


arr = np.ones_like(TO)

string_value = 'Swing?'

time_stamp = (1/120.482)*time_stamp


# Plot data

plt.plot(time_stamp, filtered_data, label='Filtered Data')
plt.scatter(time_stamp[peak_indexes], filtered_data[peak_indexes],\
                        c='r', marker= 9, label='MS')
plt.scatter(time_stamp[TO], filtered_data[TO],color = 'green', marker='^', label = 'TO')
plt.scatter(time_stamp[HS], filtered_data[HS],color = 'm',marker='v',label = 'HS')
plt.scatter(time_stamp[MidStance_index], filtered_data[MidStance_index],color = 'b',marker='.',label = 'MSt')
#plt.plot(time_stamp, gyroscope_values, label=' Data')

#plt.xlabel('ticks (120.482Hz)')

plt.xlabel('time (s)')

len = len(time_stamp)

plt.xticks(np.arange(time_stamp[0],time_stamp[len-1], 1 ))


plt.ylabel('Medio-lateral angular velocity (deg/s)')

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

add_string_to_csv_at_indices('data_dev.csv', arr, TO, HS, string_value)

print(TO)
print(peak_indexes)
print(HS)

#pd.DataFrame(HS).to_clipboard()

