import sklearn
import numpy as np
import subprocess
import wave
import copy
import sys

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

label_names = np.array(["clap","music","speech"])
feature_names = np.array(["mean","stddev","frac_silence","mean_freq","std_freq","mod_freq"])
feature_names = np.array(["stddev","frac_silence","mean_freq","std_freq","mod_freq"])

classif = {0:"clap",1:"music",2:"speech"}

#mean pitch
labels = np.array([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2])
train_features = []

def gen_aud_from_vid(video_filename,audio_filename):
    process = subprocess.Popen(["ffmpeg", "-i",video_filename,"-vn",audio_filename], stdin = subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.stdin.write("y")
    process = subprocess.Popen(['ffmpeg',  '-i', video_filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()


def analyze_audio_file(audio_filename):
    spf = wave.open(audio_filename,'r')
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    fs = spf.getframerate()
    Time=np.linspace(0, len(signal)/fs, num=len(signal))

    aud_feats = []
    #aud_feats.append(np.mean(signal))
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


video_names = ["clap1.mov","clap2.mov","clap3.mov","clap4.mov","clap5.mov","clap6.mov","clap7.mov","clap8.mov","clap9.mov","clap10.mov",
                    "music1.mov","music2.mov","music3.mov","music4.mov","music5.mov","music6.mov","music7.mov","music8.mov","music9.mov","music10.mov",
                    "speech1.mov","speech2.mov","speech3.mov","speech4.mov","speech5.mov","speech6.mov","speech7.mov","speech8.mov","speech9.mov","speech10.mov"]

audio_names = ["1.wav","2.wav","3.wav","4.wav","5.wav","6.wav","7.wav","8.wav",
    "9.wav","10.wav","11.wav","12.wav","13.wav","14.wav","15.wav","16.wav","17.wav","18.wav",
    "19.wav","20.wav","21.wav","22.wav","23.wav","24.wav","25.wav","26.wav","27.wav","28.wav","29.wav","30.wav"]


def train_model(vn, an):
    print "Training model..."
    for i, name in enumerate(vn):

        gen_aud_from_vid(vn[i],an[i])
        train_features.append(analyze_audio_file(an[i]))

    # Split our data
    train, test, train_labels, test_labels = train_test_split(train_features,labels,test_size=0)

    # Initialize our classifier
    gnb = RandomForestClassifier()

    # Train our classifier

    model = gnb.fit(train, train_labels)
    print "Done training"
    print
    return gnb




test_vid = ["testc.mov"]
test_aud = ["testa.wav"]
test_features = []

def test_files(training_videos,training_audio, testing_videos,testing_audio):

    gnb = train_model(training_videos, training_audio)

    for i, name in enumerate(testing_audio):
        print "Analyzing files..."
        gen_aud_from_vid(testing_videos[i],testing_audio[i])
        test_features.append(analyze_audio_file(testing_audio[i]))

        preds = gnb.predict(test_features)

        for i,pred in enumerate(preds):
            print "File: ", testing_videos[i]
            print "Classification: ",classif[pred]
            print

        return preds


test_files(video_names,audio_names,
test_vid,test_aud)
