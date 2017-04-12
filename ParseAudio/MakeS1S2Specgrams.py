"""The purpose of this code will be to open set_a_timing.csv and for each filename contained therein, and read in the appropriate csv. It will then windown a short interval around the S1 or S2 (say 250ms on each side of the labeled time) sound and fourier transform. I will then frequency bin into an equal number of bins by doing max pooling so that all of the outputs have the same dimensionality."""
import os
import pandas as pd
import numpy as np
import matplotlib
#I use TkAgg as this helps speed up plotting tremendously on Mac OS. You may want to change to GTKAgg on a Windows OS.                                         
matplotlib.use('TkAgg')
#matplotlib.use('GTKAgg')                                                       
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.pyplot import specgram
from scipy import signal

#Set path where csv files of concern are                                        
file_path='/Users/William/Desktop/Desktop/Projects/heart-sounds/ParseAudio/SetA/'

timing_file='set_a_timing.csv'

#Open timing file and split on carriage 
lines=open(file_path+timing_file).read().splitlines()

#Loop through all of the lines in the timing csv
for i in range(1,int(len(lines))):
#for i in range(1,3):
    #Get file name, and other parameters. 
    #The most important being Sid which will become our training/validation label and Sval which is the location about which we will window.
    fname,cycid,Sid,Sval=lines[i].split(',')

    #change wav to csv and remove set_a/ in fname
    fname=fname.replace('set_a/','')
    fname=fname.replace('wav','csv')



    #Create a Pandas dataframe from the csv note the column header will be the sample rate when using this approach                                        
    df=pd.read_csv(file_path+fname,delimiter=',')

    #Extract data values into an array                                      
    data=df.values

    #Reshape into a 1D array and get the rate                                                
    data=np.reshape(data,len(data))
    dataavg=np.mean(data)
    data=[x-dataavg for x in data]
    rate=int(df.columns.values[0])
    Nf=rate/2
    wch=195/(Nf)
    #Use a butterworth low pass filter                                                                              
    b, a = signal.butter(2,wch,btype='lowpass', analog=False)

    #Do symmetric low pass filtering so that there is no phase offset!                                              
    datafilt=signal.filtfilt(b,a,data)

    #Extract identity of sound and get data within a symmetrically placed approximately 200ms window about the sound
    if str(Sid)=='S1':
        S1=int(Sval)
        half_window=int(rate*0.001)
        soundclip=datafilt[S1-half_window:S1+half_window]
        
    elif str(Sid)=='S2':
        S2=int(Sval)
        half_window=int(rate*0.001)
        soundclip=datafilt[S2-half_window:S2+half_window]
        
                      
    t=np.arange(0/rate,(len(datafilt)+1)/rate,1/rate)
    #t=[x*1/rate for x in t]

    sp=np.fft.fft(soundclip)
    freq = np.fft.fftfreq(t.shape[-1])

    spabs=[abs(x) for x in sp]
    maxabs=max(spabs)
    spabs=[x/maxabs for x in spabs]

    spphi=np.arctan2(sp.imag,sp.real)

    spphi=np.unwrap(spphi)
    
    if str(Sid)=='S1':
        plt.subplot(2,1,1)
        plt.plot(spabs,color='r')
        plt.subplot(2,1,2)
        plt.plot(spphi,color='r')
    elif str(Sid)=='S2':
        plt.subplot(2,1,1)
        plt.plot(spabs,color='b')
        plt.subplot(2,1,2)
        plt.plot(spphi,color='b')

plt.show()
plt.close()


