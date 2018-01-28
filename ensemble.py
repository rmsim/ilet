import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import copy
import subprocess
import re
import sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from split_by_audio import *
from classify_audio import *

# files to analyze
video_filename = "comptest.mov"
audio_filename = "comptest.wav"
path_to_training_vids = "training_files/"
low, high = 4, 6
start_dist = 150
step = 50

#first split the files
print "Starting splitting analysis"
split_movie_names = optimum_num_segments(video_filename,audio_filename,(low,high),start_dist,step)


#then classify
print
print "Starting classification analysis"
# for testing
video_names = ["clap1.mov","clap2.mov","clap3.mov","clap4.mov","clap5.mov","clap6.mov","clap7.mov","clap8.mov","clap9.mov","clap10.mov",
                    "music1.mov","music2.mov","music3.mov","music4.mov","music5.mov","music6.mov","music7.mov","music8.mov","music9.mov","music10.mov",
                    "speech1.mov","speech2.mov","speech3.mov","speech4.mov","speech5.mov","speech6.mov","speech7.mov","speech8.mov","speech9.mov","speech10.mov"]

audio_names = ["1.wav","2.wav","3.wav","4.wav","5.wav","6.wav","7.wav","8.wav",
    "9.wav","10.wav","11.wav","12.wav","13.wav","14.wav","15.wav","16.wav","17.wav","18.wav",
    "19.wav","20.wav","21.wav","22.wav","23.wav","24.wav","25.wav","26.wav","27.wav","28.wav","29.wav","30.wav"]

test_vid = split_movie_names
test_aud = []
for i in test_vid:
    test_aud.append(i[:-4]+".wav")

test_files(path_to_training_vids,video_names,audio_names,test_vid,test_aud)

print "Done with analysis"
