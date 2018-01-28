import sklearn
import numpy as np
import subprocess
import wave
import copy
import sys
import os
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

label_names = np.array(["clap","music","speech"])
feature_names = np.array(["mean","stddev","frac_silence","mean_freq","std_freq","mod_freq"])
feature_names = np.array(["stddev","frac_silence","mean_freq","std_freq","mod_freq"])

classif = {0:"clap",1:"music",2:"speech"}


labels = np.array([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2])
train_features = []

def gen_aud_from_vid(video_filename,audio_filename):

    try:
        process = subprocess.Popen(["ffmpeg", "-i",video_filename,"-vn",audio_filename],
        stdin = subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.stdin.write("y")

    except IOError:
        command = "ffmpeg -i "+video_filename+" -vn "+audio_filename
        subprocess.call(command, shell=True)
    time.sleep(1)


def analyze_audio_file(audio_filename):
    spf = wave.open(audio_filename,'r')
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    fs = spf.getframerate()
    Time=np.linspace(0, len(signal)/fs, num=len(signal))

    aud_feats = []
    aud_feats.append(np.std(signal))
    silence_thresh = np.mean(signal)/1.
    cop = copy.deepcopy(signal)
    cop[np.where(signal<silence_thresh)] = 1
    cop[np.where(signal>=silence_thresh)] = 0
    aud_feats.append(sum(cop)/float(len(cop)))


    dt = Time[1]-Time[0]
    ft_freq = np.fft.fftfreq(Time.shape[-1])*dt
    ft_sig = np.abs(np.fft.fft(signal))

    aud_feats.append(sum(ft_freq*ft_sig))

    aud_feats.append(sum(ft_freq*ft_sig**2))

    aud_feats.append(ft_freq[np.where(ft_sig==max(ft_sig))][0])


    return np.array(aud_feats)

def train_model(path_to_training_vids,vn, an):
    print "Training model..."
    for i, name in enumerate(vn):

        gen_aud_from_vid(path_to_training_vids+vn[i],path_to_training_vids+an[i])
        train_features.append(analyze_audio_file(path_to_training_vids+an[i]))

    # Split our data
    train, test, train_labels, test_labels = train_test_split(train_features,labels,test_size=0)

    # Initialize our classifier
    gnb = RandomForestClassifier()

    # Train our classifier

    model = gnb.fit(train, train_labels)
    print "Done training"
    print
    return gnb


def test_files(path_to_training_vids,training_videos,training_audio, testing_videos,testing_audio):
    test_features = []
    gnb = train_model(path_to_training_vids,training_videos, training_audio)
    print "Analyzing files..."

    for i, name in enumerate(testing_audio):

        gen_aud_from_vid(testing_videos[i],testing_audio[i])

        test_features.append(analyze_audio_file(testing_audio[i]))

    preds = gnb.predict(test_features)

    for i,pred in enumerate(preds):
        print "File: ", testing_videos[i]
        print "Classification: ",classif[pred]
        print

        if pred == 0:
            os.rename(testing_videos[i], "clap/"+testing_videos[i])
        if pred == 1:
            os.rename(testing_videos[i], "music/"+testing_videos[i])
        if pred == 2:
            os.rename(testing_videos[i], "speech/"+testing_videos[i])

        os.remove(testing_audio[i])

    return preds
