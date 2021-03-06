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
from scipy.fftpack import idct
from scipy import signal

#Set path where csv files of concern are                                                                                
file_path='/Users/William/Desktop/Desktop/Projects/heart-sounds/ParseAudio/SetA/'

#This can be modified to loop through as subset of the csv files if you want to view more than one                      

csvname='murmur__201102052338.csv'

#append path to csv to the csv file name                                                                                
fname=file_path+csvname

#This will be the parameter that passes to window duration. I'm setting it to 40ms here.
windowduration=0.05

#This will be the amount by which the window shifts for each step in the spectrogram. I'm setting it to 50% overlap at each step
windowshift=0.5*windowduration

#Set the maximum frequency in Hz  desired for the spectrogram analysis. Should be less than the minimum Nyquist frequency of 2000Hz
maxfreq=350

#Set the number of mel filter banks to use
melbanks=20

def importdata(filename):
    #Create a Pandas dataframe from the csv note the column header will be the sample rate when using this approach         
    df=pd.read_csv(filename,delimiter=',')

    #Extract data values into an array                                                                                      
    data=df.values

    #Reshape into a 1D array                                                                                                
    data=np.reshape(data,len(data))

    #Get the column header which is the rate in order to do low pass filtering                                              
    rate=int(df.columns.values[0])
    
    return(rate,data)

def spectrogram(rate,data):
    
    #set windowsize in sample units
    windowsize=2*int(np.floor(rate*windowduration/2))+1

    #set window shift in sample units
    windowstep=2*int(np.floor(rate*windowshift/2))+1
    
    #figure out how many shifts are possible
    totalsteps=int(np.floor((len(data)-windowsize)/windowstep))

    #Using a gaussian window for now. Plan to modify later
    window=np.exp(-np.power(range(-int(np.floor(windowsize/2)),int(np.floor(windowsize/2)+1)),2)/(2*(windowsize*0.5)**2))
    
    fftwinmat=[]

    #Calculate windowed data and fourier transform

    #Do it separately the first time to get the frequency bin associated with the maximum spectrogram frequency desired
    windata=data[(0):(windowsize)]

    windata=np.multiply(windata,window)
    
    windata=np.append(windata,np.zeros(len(data)-(windowsize)))
    
    fftfreq=np.fft.fftfreq(len(data),1/rate)
    
    freqbin=(np.abs(fftfreq-maxfreq)).argmin()

    fftfreq=fftfreq[0:freqbin+1]

    fftwin=abs(np.fft.rfft(windata))
    fftlittlemat=np.matrix.transpose(np.matrix(fftwin[0:freqbin+1]))
    fftwinmat=np.append(fftwinmat,fftlittlemat)
    
    for i in range(1,totalsteps):
        
        windata=data[(0+windowstep*i):(windowsize+windowstep*i)]
        
        windata=np.multiply(windata,window)
        
        windata=np.append(windata,np.zeros(len(data)-(windowstep*i+windowsize)))

        if i>0:
            windata=np.append(np.zeros(windowstep*i),windata)

        fftwin=abs(np.fft.rfft(windata))
        fftlittlemat=np.matrix.transpose(np.matrix(fftwin[0:freqbin+1]))
        fftwinmat=np.append(fftwinmat,fftlittlemat)
                
    fftwinmat=np.reshape(fftwinmat,(totalsteps,freqbin+1))

    mat=np.matrix.transpose(np.matrix(fftwinmat))

    mat=mat[::-1]

    return(mat,fftfreq,totalsteps,freqbin)

def filter_bank(numbanks,freqlist,maxbin,numsteps):
    
    filtbank=[] 
    
    filthold=[]
    #Calculate the upper and lower frequencies on mel scale
    lowmel=1125.0*np.log(1.0+freqlist[0]/700.0)
    upmel=1125.0*np.log(1.0+freqlist[maxbin]/700.0)
    
    
    #Calculate location of filter bank peaks and nodes
    melbankpos=np.linspace(lowmel,upmel,numbanks+2,endpoint=True)
    
    
    #Invert bank positions to normal frequency
    normbankpos=700.0*(np.expm1(np.multiply(1.0/1125.0,melbankpos)))

    
    #Get closest frequency bin to bank position
    normidx=[(np.abs(freqlist-x)).argmin() for x in normbankpos]
    
    
    #Calculate filterbank as a matrix so I can multiply into spectrogram matrix.
    for i in range(0,numbanks):
        
        slopeup=1.0/(normidx[i+1]-normidx[i])

        slopedown=1.0/(normidx[i+1]-normidx[i+2])

        bankup=[slopeup*(x-normidx[i]) for x in range(normidx[i],normidx[i+1]+1)]

        bankdown=[slopedown*(x-normidx[i+2]) for x in range(normidx[i+1]+1,normidx[i+2]+1)]

        
        if i>0:
        
            filthold=np.append(np.zeros(normidx[i]),filthold)
        
        filthold=np.append(filthold,bankup)
        
        filthold=np.append(filthold,bankdown)
              
        if i<numbanks:
        
            filthold=np.append(filthold,np.zeros((maxbin-normidx[i+2])))
                    
        filtbank.append([filthold[::-1]])
        
        plt.plot(filthold)

        filthold=[]
        
        
    plt.show()
    plt.close()

    filtbank=np.asarray(filtbank)
        
    filtmat=np.matrix(filtbank)

    

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.imshow(filtmat, aspect=0.25*numsteps/30, interpolation='nearest',extent=[0,numsteps,numbanks,0], cmap=plt.cm.jet)
    
    #plt.axis([0,steps,20,0])                                                                                                                                      
    #labels=[int(freqlist[2999]),int(freqlist[2499]),int(freqlist[1999]),int(freqlist[1499]),int(freqlist[999]),int(freqlist[499]),int(freqlist[0])]              
    
    #plt.axis('scaled')                                                                                                                                           
    #plt.xticks(range(totalsteps),steplist,fontsize=12)                                                                                                           
    #plt.yticks(range(60),freqlist,fontsize=12)                                                                                                                   
    #plt.colorbar()                                                                                                                                               
    plt.show()
    plt.close()

    return(filtmat)
   
def mel_filtering(filtmat,specmat,numsteps):

    melbindata=np.dot(filtmat,specmat)

    dctmelmat=melbindata[::-1]

    """melbindata=np.log(melbindata[::-1])

    melbindata=np.asarray(melbindata)
    
    #print(melbindata[:,100])
    #melbindata=idct(melbindata,axis=0)
    
    dctmelbin=[]

    for i in range(0,numsteps):

        melfft=np.fft.ifft(melbindata[:,i])
        
        melfft=np.square(abs(melfft[4:30]))
        
        plt.plot(melfft)

        dctmelbin.append(melfft.transpose())
    
    dctmelbin=np.asarray(dctmelbin)

    plt.show()
    plt.close()
    dctmelmat=np.matrix(dctmelbin)
    
    dctmelmat=dctmelbin.transpose()

    dctmelmat=dctmelmat[::-1]"""
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.imshow(dctmelmat,aspect=0.25*numsteps/melbanks ,interpolation='nearest', cmap=plt.cm.jet)
    plt.show()
    plt.close()


rat,dat=importdata(fname)

specdat,flist,steps,mbin=spectrogram(rat,dat)

#plt.plot(freqlist)
#plt.show()
#plt.close()

index=np.linspace(0,mbin,num=5,endpoint=True)
index=[int(x) for x in index]

flab=[int(flist[x]) for x in index]
flab=flab[::-1]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.imshow(specdat, aspect=0.25*steps/mbin, interpolation='nearest',extent=[0,steps,mbin,0], cmap=plt.cm.jet)
plt.yticks(index)                                                                                                         
#plt.axis([0,steps,20,0])
#labels=[int(freqlist[2999]),int(freqlist[2499]),int(freqlist[1999]),int(freqlist[1499]),int(freqlist[999]),int(freqlist[499]),int(freqlist[0])]
ax.set_yticklabels(flab)
plt.xticks([])
#plt.axis('scaled')
#plt.xticks(range(totalsteps),steplist,fontsize=12)                                                                     
#plt.yticks(range(60),freqlist,fontsize=12)                                                                             
#plt.colorbar()
plt.show()
plt.close()

filters=filter_bank(melbanks,flist,mbin,steps)

mel_filtering(filters,specdat,steps)
