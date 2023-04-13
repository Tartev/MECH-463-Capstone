#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 23:21:58 2023

@author: vincenttarte
"""
import random
import math as math 
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from itertools import count
import numpy as np
import matplotlib.pyplot as plt
import scipy as scpy
from scipy.signal import bessel, filtfilt
import pandas as pd
import moviepy.editor as mp
#%matplotlib qt

# Load data and set parameters

filename = "Vincent_2P.csv"

start = 700 
stop = 10700

data = pd.read_csv(filename)

gyroscope_values = data["Shimmer_6835_Gyro_Z_CAL"]

#gyroscope_values = gyroscope_values[start:stop]

time_stamp = data["time_stamp"]

#time_stamp = time_stamp[start:stop]

fs = 120.482  # Sampling rate

fc = 10  # Cut-off frequency

Tgiven = 25/1000  # Time window for IC detection (in ms)

window = int(Tgiven /0.0083) #define window between MS an IC 

window2 = int(300/(1000*0.0083)) #define a time window between IC an TO 

# Filter data

b, a = bessel(2, fc/(fs/2), btype='low')  # 2nd order Bessel filter

filtered_data = filtfilt(b, a, gyroscope_values)

#filtered_data = gyroscope_values
# Initialize variables

MSW = 0
IC = 0
TO = 0 

#List of candidate point

MSW_marker = []
IC_marker = []
TO_marker = []
MSt_marker = []

#Boolean value for MS, IC and TO detection

MSW_var = 0 

hold_TO = 1 

hold_IC = 0 

hold_MSt = 0 


#define thresholds

MS_threshold = 100 

IC_threshold =  0 

TO_threshold =  -40

IC_window = 30

TO_window = 70


for i in range(2, len(filtered_data)):
    
    #compute threshold and moving averages
    
    if len(MSW_marker)>=3:
        
        MS_threshold = sum(filtered_data[MSW_marker[-3:-1]])*1/6
        
    if len(IC_marker)>=3:
        
        IC_threshold = sum(filtered_data[IC_marker[-3:-1]])*1/20
        
    if len(TO_marker)>=3:
        
        TO_threshold = sum(filtered_data[TO_marker[-3:-1]])*0.5/3
        
        
    if len(MSW_marker)>=2:
        
        
        Gait_length = MSW_marker[-1] - MSW_marker[-2]
        
        TO_window = int(0.5 * Gait_length)
        
        IC_window = int(0.3 * Gait_length)
       
    
    # Compute difference between consecutive samples
    
    Dn = filtered_data[i] - filtered_data[i-1]
    
    Dn_min1 = filtered_data[i-1] - filtered_data[i-2]

    # Search for MSW
    append = 0 
    
    
    if Dn_min1 > 0 and Dn < 0 and filtered_data[i] > MS_threshold and MSW_var == 0 and hold_TO ==1: 
        
        MSW = i
        
        MSW_marker.append(i)
        
        MSW_var = 1 

        hold_TO = 0 

        hold_IC = 0 

        hold_MSt = 0 
        
    elif Dn > 0 and Dn_min1 < 0 :
            
        if MSW_var == 1 and filtered_data[i] < IC_threshold:
            
            for j in range(i, MSW+IC_window):
                
                if filtered_data[j] > filtered_data[j-1]:
                    
                    IC = j
                    
                    if filtered_data[j+1] > filtered_data[j]:
                        
                    
                        if filtered_data[j+1] - filtered_data[IC] < 20:
                            
                            IC = j
                            
                            IC_marker.append(j)
                            
                            append = append + 1
                            
                            MSW_var = 0 

                            hold_TO = 0 

                            hold_IC = 1 

                            hold_MSt = 0  
                            
                            if append == 1:
                                
                                #MSW_var = 0
                                
                                continue
                        
                            else:
                            
                                IC_marker.pop()
                                
                                #MSW_var = 0
                            
                                
                                break
                            
    #Search for Mid Stance (MSt)    

    if Dn_min1 > 0 and Dn < 0 and filtered_data[i] < 0 and hold_IC == 1 and filtered_data[i]>-50 and hold_MSt == 0 and i > IC_marker[-1]+5:
        
        
        MSt_marker.append(i)
        
        MSW_var = 0 

        hold_TO = 0 

        hold_IC = 0 

        hold_MSt = 1                     
            
    # Search for TO                    

    if i > MSW+TO_window and filtered_data[i] < TO_threshold and i < len(filtered_data)-2 and hold_MSt ==1:
        
        TO = i
        
        if filtered_data[TO] > filtered_data[i+1]:
            
            TO = i + 1
          
            if filtered_data[TO] < filtered_data[TO+1]:
                
                TO_marker.append(TO)
                
                MSW_var = 0 

                hold_TO = 1 

                hold_IC = 0 

                hold_MSt = 0
                
            else: 
                
                MSW_var = 0 
                
                IC = 0
           
              
# Plot data
time_stamp = time_stamp/fs
plt.plot(time_stamp, filtered_data, label='Filtered Data')
s=10
# Add labels for MSW, IC and TO

plt.scatter(time_stamp[MSW_marker], filtered_data[MSW_marker],\
            c='r', marker='^', label='MS',s=s)

plt.scatter(time_stamp[IC_marker], filtered_data[IC_marker],\
            c='g', marker='x', label='IC',s=s)

plt.scatter(time_stamp[TO_marker], filtered_data[TO_marker],\
            c='k', marker='o', label='TO',s=s)
    
plt.scatter(time_stamp[MSt_marker], filtered_data[MSt_marker],\
            color = 'b',marker='o',label = 'MSt',s=s)

plt.xlabel('time (s)')

lenght = len(time_stamp)

#plt.xticks(np.arange(time_stamp[0],time_stamp[lenght-1]),10)

plt.ylabel('Medio-lateral angular velocity (deg/s)')
#plt.axvline(x=1,linestyle = '--', color = 'r', label = 'stairs up')
#plt.axvline(x=11,linestyle = ':', color = 'r', label = 'stairs down')

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

#plt.axis([11000/fs,12500/fs, -300,400])

print(len(TO_marker))
print(TO_marker)
#print(MSW_marker)
#print(len(IC_marker))
#print(IC_marker)

#print(len(MSW_marker))
#print(IC_marker)

fig = plt.figure(figsize=(6,4))
axes = fig.add_subplot(1,1,1)
plt.title("Dynamic Axes")
start = 650
end = 1000
y1 = filtered_data[start:end]
t = range(int(len(y1)))


y2 = np.ones_like(y1)
y3 = np.ones_like(y1)
k=0

for i in range(len(y1)):
    
    if i + start > TO_marker[k]:
        
        k = k+1
    
    if i == TO_marker[k]-start:
        
        y2[i] = y1[i] 
        
        k = k+1
        
        
    else: 
        
        y2[i] = np.nan
        
k=0

for i in range(len(y1)):
    
    if i + start > IC_marker[k]:
        
        k = k+1
    
    if i == IC_marker[k]-start:
        
        y3[i] = y1[i] 
        
        k = k+1
        
        
    else: 
        
        y3[i] = np.nan
    
        
x, y, yy,yyy = [], [], [], []

print(len(y1))
print(len(y2))

s = 10

status = 'black'

def animate(i):
    
    global status
    
    x.append(t[i])
    y.append((y1[i]))
    yy.append((y2[i]))
    yyy.append((y3[i]))
    plt.xlim(i-60,i+5)
    axes.set_ylim(-300, 400)
    
    if np.isnan(y2[i]) == False: 
        
        print('y2')
        
        status = "green"
        
        plt.axvline(x=i,linestyle = '--', color = 'r')
        plt.text(i+5,200,'FES ON')
        
    if np.isnan(y3[i]) == False: 
        
        print('y3')
        
        plt.axvline(x=i,linestyle = '--', color = 'r')
        plt.text(i+5,200,'FES OFF')
        
        status = "black"
       
    plt.plot(x,y, scaley=True, scalex=True, color = status)
    #plt.scatter(x,y, color = status)
    plt.plot(x,yy, scaley=True, scalex=True, color="g", marker = 'X',ms=s)
    plt.plot(x,yyy, scaley=True, scalex=True, color="r", marker = 'X',ms=s)
    
    

anim = FuncAnimation(fig, animate, interval=100, frames = range(len(t)))
plt.ylabel('Medio-lateral angular velocity (deg/s)')
plt.xlabel('time')

f = r"/Users/vincenttarte/Desktop/Capstone Algorithm developpement for variable gait/animation.gif"
writergif = animation.PillowWriter(fps=24) 
anim.save(f, writer=writergif, dpi = 100)

'''
clip = mp.VideoFileClip("animation.gif")
clip.write_videofile("myvideo.mp4")
'''







