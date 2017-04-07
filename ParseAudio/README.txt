The folders SetA and SetB contain files with the amplitude versus time of heartbeat recordings as csv files (comma delimited) with the first entry being the sample rate.
SetA file names begin with one of the following: 
artifact (contains excess noise and heartbeats may not be able to be extracted) 
Aunlabelledtest (this is test data to characterize as one of the four other categories) 
extrahls (extra heart sounds)
normal (normal heartbeat)
murmur (the recording exhibits a heart murmur)

IMPORTANT!
The first entry of each of these csv is the sample rate. 

In the SetA folder are the files set_a.csv and set_a_timing.csv

set_a.csv has columns with: 
dataset label (a for SetA or b for SetB) 
fname (audio file names)
label (artifact, extrahls, normal, murmur, or blank for unlabeled)
sublabel (in SetB, some recordings are noisy, and may be sublabeled as noisynormal, noisymurmur etc.) 

set_a_timing.csv has columns with:
fname 
cycle (anywhere from 1 to 19: the heartbeat cycle that the time observation refers to. But note that in some cases cycles have been skipped.)
sound (either S1 for systole or S2 for diastole sound)
location (time location in number of audio samples)

The SetB folder has similar and self explanatory structure.

See https://www.kaggle.com/kinguistics/heartbeat-sounds for detailed descriptions. 
