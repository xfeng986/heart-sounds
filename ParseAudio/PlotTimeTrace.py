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

#This can be modified to loop through as subset of the csv files if you want to view more than one

csvname='extrahls__201101241433.csv'

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

windowsize=2*int(np.floor(rate*.040/2))+1

windowstep=2*int(np.floor(rate*0.020/2))+1

totalsteps=int(np.floor((len(datafilt)-windowsize)/windowstep))
print(windowsize)
print(totalsteps)
fftwinmat=[]
steplist=[]
#for i in range(0,10):
for i in range(0,totalsteps):
    windata=data[(0+windowstep*i):(windowsize+windowstep*i)]
    #steplist=np.append(steplist,((windowsize+windowstep*i)/2)/rate)
    #windata=datafilt[(0+windowstep*i):(windowsize+windowstep*i)]
    #plt.plot(unfiltwindata,color='k')
    #plt.plot(windata,color='r')
    #plt.show()
    #plt.close()
    window=np.exp(-np.power(range(-int(np.floor(windowsize/2)),int(np.floor(windowsize/2)+1)),2)/(2*(windowsize*0.5)**2))
    windata=np.multiply(windata,window)
    #plt.plot(windata,color='k')
    #plt.show()
    #plt.close()
    
    
    fftwin=abs(np.fft.rfft(windata))
    #plt.plot(fftwin)
    #plt.show()
    #plt.close()
    #plt.plot(fftwin[0:2*195])
    #plt.show()
    #plt.close()
    fftlittlemat=np.matrix.transpose(np.matrix(fftwin[0:20]))
    fftwinmat=np.append(fftwinmat,fftlittlemat)
    fftfreq=np.fft.fftfreq(int(windowsize),1/rate)
    fftfreq=fftfreq[0:len(fftwin)]
#freqlist=fftfreq[0:60]


#plt.plot()
#plt.show()
#plt.close()

    #plt.plot(fftfreq,fftwin)
    #plt.xlim(0,2*195)
    #plt.show()
    #plt.close()
#plt.show()
#plt.close()


fftwinmat=np.reshape(fftwinmat,(totalsteps,20))


mat=np.matrix.transpose(np.matrix(fftwinmat))

plt.plot(mat[:,90])
plt.show()
plt.close()

mat=mat[::-1]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.imshow(mat, interpolation='nearest', cmap=plt.cm.ocean)
#plt.xticks([])
plt.yticks([])
#plt.xticks(range(totalsteps),steplist,fontsize=12)
#plt.yticks(range(60),freqlist,fontsize=12)
plt.colorbar()
plt.show()


#plot timeseries and spectrogram
plt.subplot(2,1,1)
plt.plot(datafilt)
plt.ylabel('Amplitude')
plt.ylim(-1,1)
plt.subplot(2,1,2)
#plt.imshow(mat, interpolation='nearest', cmap=plt.cm.ocean)
#plt.colorbar()
specgram(datafilt,Fs=2)
plt.xlabel('Time in Sampling Units')
plt.ylabel('Frequency')
plt.ylim(0,1)
plt.show()
plt.close()

#print(len(datafilt))


