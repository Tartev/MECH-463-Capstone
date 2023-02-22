#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 16:02:46 2023

@author: vincenttarte
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:13:23 2023

@author: vincenttarte
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import bessel, filtfilt
import pandas as pd

# Load data and set parameters

data = pd.read_csv("data_dev.csv")

gyroscope_values = data["Shimmer_6835_Gyro_Z_CAL"]


time_stamp = data["time_stamp"]

time_stamp = (1/120.482)*time_stamp


fs = 120.482  # Sampling rate

fc = 10  # Cut-off frequency

Tgiven = 25/1000  # Time window for IC detection (in ms)

window = int(Tgiven /0.0083) #define window between MS an IC 

window2 = int(300/(1000*0.0083)) #define a time window between IC an TO 

# Filter data

#b, a = bessel(2, fc/(fs/2), btype='low')  # 2nd order Bessel filter

#filtered_data = filtfilt(b, a, gyroscope_values)

filtered_data = gyroscope_values
# Initialize variables


MSW = 0
IC = 0
TO = 0 



#List of candidate point

MSW_marker = []
IC_marker = []
TO_marker = []

#Boolean value for MS, IC and TO detection

MSW_var = 0 

hold_ms = 0 

hold_IC = 0 

# Loop through data

hold_TO = 0 

#define thresholds

MS_threshold = 100 

IC_threshold = 0

TO_threshold = -40

IC_window = 20

TO_window = 30

for i in range(2, len(filtered_data)):
    
    #compute threshold and moving averages
    
    if len(MSW_marker)>=3:
        
        MS_threshold = sum(filtered_data[MSW_marker[-3:-1]])*1/6
        
    if len(IC_marker)>=3:
        
        IC_threshold = sum(filtered_data[IC_marker[-3:-1]])*1/20
        
    if len(TO_marker)>=3:
        
        TO_threshold = sum(filtered_data[TO_marker[-3:-1]])*1/10
        
        
    # Compute difference between consecutive samples
    
    Dn = filtered_data[i] - filtered_data[i-1]
    
    Dn_min1 = filtered_data[i-1] - filtered_data[i-2]

    # Search for MSW
    append = 0 
    
    
    if Dn_min1 > 0 and Dn < 0 and filtered_data[i] > MS_threshold and hold_ms == 0: 
        #print(MS_threshold)
        MSW = i
        MSW_marker.append(i)
        
        MSW_var = 1 
        hold_ms = 1
      
        
    elif Dn > 0 and Dn_min1 < 0 :
            
        if MSW_var == 1 and filtered_data[i] < IC_threshold:
            
            #print(IC_threshold)
            
            for k in range(i, MSW + IC_window):

                if filtered_data[k] < filtered_data[k-1]:
                    
                    IC = k 
                    MSW_var = 0 
                    
                    if filtered_data[k+1] > filtered_data[k]:
                            
                        IC = k
                        IC_marker.append(k)
                        append = append + 1
                        
                        if append == 1:
                            
                            MSW_var = 0
                            continue
                    
                        else:
                        
                            IC_marker.pop()
                            MSW_var = 0
                            break
                   
    # Search for TO
  
    if i > MSW+TO_window and filtered_data[i] < TO_threshold and i < len(filtered_data)-2:
        
        TO = i
        
        print(TO_threshold)
        
        if filtered_data[TO] > filtered_data[i+1]:
            
            TO = i + 1
          
            if filtered_data[TO] < filtered_data[TO+1]:
                
                TO_marker.append(TO)
                
                hold_TO = hold_TO + 1
                
                if hold_TO == 2:
                
                    if filtered_data[TO_marker[-1]] < filtered_data[TO_marker[-2]]:
                        
                        TO_marker.pop(-2)
                        
                    hold_ms = 0 
                    IC = 0
                    hold_TO = 0
                        
                else: 
                    
                    hold_ms = 0 
                    IC = 0
                    
              
# Plot data

plt.plot(time_stamp, filtered_data, label='Filtered Data')

# Add labels for MSW, IC and TO

plt.scatter(time_stamp[MSW_marker], filtered_data[MSW_marker],\
            c='r', marker='^', label='MS')

plt.scatter(time_stamp[IC_marker], filtered_data[IC_marker],\
            c='g', marker=',', label='IC')

plt.scatter(time_stamp[TO_marker], filtered_data[TO_marker],\
            c='k', marker='o', label='TO')

plt.xlabel('time (s)')

len = len(time_stamp)

plt.xticks(np.arange(time_stamp[0],time_stamp[len-1], 0.5 ))

plt.ylabel('Medio-lateral angular velocity (deg/s)')

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

print(TO_marker)
print(MSW_marker)
print(IC_marker)





#%%

pd.DataFrame(IC_marker).to_clipboard()



