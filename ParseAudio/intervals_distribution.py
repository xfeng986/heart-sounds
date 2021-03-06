import pandas as pd
import numpy as np
import matplotlib
#I use TkAgg as this helps speed up plotting tremendously on Mac OS. You may want to change to GTKAgg on a Windows OS.                                         
matplotlib.use('TkAgg')
#matplotlib.use('GTKAgg')                                                       
import matplotlib.pyplot as plt
from matplotlib import colors

file_path='/Users/William/Desktop/Desktop/Projects/heart-sounds/ParseAudio/SetA/'

lines=open(file_path+'set_a_timing.csv').read().splitlines()


S1=np.zeros(int(len(lines)/2))
S2=np.zeros(int(len(lines)/2))

S2mS1=np.zeros(int(len(lines)/2))

S1mS2=np.zeros(int(len(lines)/2)-1)

S1mS1=np.zeros(int(len(lines)/2)-1)

S2mS2=np.zeros(int(len(lines)/2)-1)

frate=[]

fdata=[]

fcount=0

maxcyc=[0]

testmaxcyc=0

for i in range(1,int(len(lines))):
    fname,cycid,Sid,Sval=lines[i].split(',')

    fname=fname.replace('wav','csv')

    fname=fname.replace('set_a/','')

    fname=file_path+fname

    df=pd.read_csv(fname,delimiter=',')

    rate=int(df.columns.values[0])
    
    if str(Sid)=='S1':
        S1[int((i+1)/2)-1]=int(Sval)/rate
    elif str(Sid)=='S2':
        S2[int((i-2)/2)]=int(Sval)/rate

for j in range(0,int(len(S1)-1)):
    
    S2mS1[j]=S2[j]-S1[j]

    S1mS2[j]=S1[j+1]-S2[j]

    S1mS1[j]=(S1[j+1]-S1[j])

    S2mS2[j]=S2[j+1]-S2[j]

S1mS2=S1mS2[S1mS2>=0]

S2mS1=S2mS1[S2mS1>=0]

S1mS1=S1mS1[S1mS1>=0]

S2mS2=S2mS2[S2mS2>=0]

n = 100
x = np.random.standard_normal(n)
y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)

#print(S1mS1.std())
#print(x)
#print(y)
#print(S1mS1)
opacity=0.75
bins = np.linspace(0, 2, 100)
plt.hexbin(S1mS1,S2mS2)
plt.show()
plt.hist(S1mS2,bins)
plt.hist(S2mS1,bins,alpha=opacity)
plt.show()
plt.hist(S1mS1,bins)
plt.hist(S2mS2,bins,alpha=opacity)
plt.show()



