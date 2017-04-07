import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.pyplot import specgram
from scipy import signal

save_path='/Users/William/Desktop/Desktop/Projects/heart-sounds/ParseAudio/SetA/'

csvname='normal__201108011112.csv'

fname=save_path+csvname

df=pd.read_csv(fname,delimiter=',')

data=df.values

data=np.reshape(data,len(data))

maxdata=max(abs(data))

data=[x/maxdata for x in data]

rate=int(df.columns.values[0])
Nf=rate/2
wch=195/(Nf)

b, a = signal.butter(2,wch,btype='lowpass', analog=False)

datafilt=signal.filtfilt(b,a,data)

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



