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

for filename in os.listdir(save_path):
    
    if filename.startswith('normal'):
        csvname=filename

        #append path to csv to the csv file name
        fname=file_path+csvname

        #Create a Pandas dataframe from the csv note the column header will be the sample rate when using this approach
        df=pd.read_csv(fname,delimiter=',')

        #Extract data values into an array
        data=df.values

        #Reshape into a 1D array
        data=np.reshape(data,len(data))

        #Get the column header which is the rate in order to do low pass filtering
        rate=int(df.columns.values[0])
        Nf=rate/2
        wch=195/(Nf)

        #Use a butterworth low pass filter
        b, a = signal.butter(2,wch,btype='lowpass', analog=False)

        #Do symmetric low pass filtering so that there is no phase offset!
        datafilt=signal.filtfilt(b,a,data)
        
        maxdatafilt=max(abs(datafilt))

        #Normalize filtered data
        datafilt=[x/maxdatafilt for x in datafilt]
        
        #plot timeseries and spectrogram
        plt.subplot(2,1,1)
        plt.plot(datafilt)
        plt.ylabel('Amplitude')
        plt.ylim(-1,1)
        plt.subplot(2,1,2)
        specgram(datafilt,Fs=1)
        plt.xlabel('Time in Sampling Units')
        plt.ylabel('Frequency')
        plt.ylim(0,0.5)
        plt.show()
        plt.close()



