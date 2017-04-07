import scipy.io.wavfile
import numpy as np
import os.path

#Set the pat to where the .wav files you want to convert to .csv are stored
save_path='/Users/William/Desktop/Desktop/Projects/heart-sounds/ParseAudio/SetA'

# Loop over .wav files in the current directory"
for filename in os.listdir():
    if filename.endswith('.wav'): 
        
        #Get sampling rate and amplitude for .wav
        rate, data = scipy.io.wavfile.read(filename)
        
        #Put the sampling rate at the very beginning
        a = np.append([rate],data)
        
        #Make a list with all but the last entry so that we can have the last entry without a delimiter later
        b=a[:len(a)-1]

        csvname=filename.replace('wav','csv')

        completeName=os.path.join(save_path,csvname)

        file1 = open(completeName, "w")
        
        #put all values except the last into a comma separated list
        file1.writelines( list( "%s," % item for item in b ) )
        
        #add last entry without delimeter
        file1.writelines("%s" % a[len(a)-1])

        file1.close()



















