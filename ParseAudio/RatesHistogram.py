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

rate=[]

for filename in os.listdir(file_path):
    
    if not filename.startswith('set_a') and not filename.startswith('.'):
        csvname=filename

        #append path to csv to the csv file name
        fname=file_path+csvname

        #Create a Pandas dataframe from the csv note the column header will be the sample rate when using this approach
        df=pd.read_csv(fname,delimiter=',')
        
        #Get the column header which is the rate in order to do low pass filtering
        rateval=int(df.columns.values[0])
        
        rate=np.append(rate,rateval)
        


plt.plot(rate)
plt.show()
plt.close()

