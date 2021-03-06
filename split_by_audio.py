import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import copy
import subprocess
import re
import time


thresh = 1. # change this depending on your silence theshold
cutoff=.000001 # change depending on how much hgih frequency noise to get rid of


def plot_raw_sound(signal,Time,fs):

    plt.figure()
    plt.title('Signal Wave...')
    plt.plot(Time,signal)
    plt.ylabel("relative db")
    plt.xlabel("time (s)")
    plt.savefig("raw sound")

def whiten(signal,timeseries,cutoff):
    '''removes higher freq noise and plots'''
    dt = timeseries[1]-timeseries[0]
    ft_freq = np.fft.fftfreq(timeseries.shape[-1])*dt
    ft_sig = np.fft.fft(signal)
    ft_sig[np.where(np.abs(ft_freq)>cutoff)]=0
    inv = np.abs(np.fft.ifft(ft_sig))
    invt = np.linspace(0,len(inv),len(inv))*dt
    #plt.figure()
    #plt.plot(invt,inv)
    #plt.title('Signal Wave FFT')
    #plt.ylabel("relative db")
    #plt.xlabel("time (s)")
    #plt.savefig("whitened sound")
    return invt,inv

def split_sound(ft_time,ft_sig,thresh,dist):
    '''uses amplitude changes to split the sound file'''
    silence_thresh = np.mean(ft_sig)
    silence = copy.deepcopy(ft_sig)

    silence[np.where(ft_sig<silence_thresh)]=1
    silence[np.where(ft_sig>=silence_thresh)]=0
    diffy = np.diff(silence)
    for i in range(len(diffy/dist)-1):
        seg = diffy[i*dist:(i+1)*dist]
        if 1 in seg and -1 in seg:
            diffy[i*dist:(i+1)*dist] = 0
    ind_split =  np.where(diffy!=0)[0]
    return ind_split

def plot_split_time(time_split,sig_split):
    plt.figure()
    colors = ["r","k","b","g","c"]
    for i in range(len(time_split)):
        plt.plot(time_split[i],sig_split[i],color = colors[i%5])
    plt.savefig("split sig")
    return i

def split_video(video_filename,time_split,signal,ind_split,tot_seconds):
    break_points = []
    for i in range(len(time_split)):
        break_points.append(time_split[i][0])
    if 0 not in break_points:
        break_points = np.append(0.,break_points)
    if 1 not in break_points:
        break_points = np.append(break_points,1.)
    split_movie_names = []
    for i in range(len(break_points[:-1])):
        start_time = str(break_points[i])
        end_time = str(break_points[i+1])
        name = video_filename[:-4]+str(i)+".mov"
        split_movie_names.append(name)

        try:
                process = subprocess.Popen(["ffmpeg","-i",video_filename,"-ss",start_time,"-t",end_time,name], stdin = subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                process.stdin.write("y")

        except IOError:
                "ffmpeg -i "+video_filename+" -ss "+start_time+" -t "+end_time+" seg"+str(i)+".mov"
                subprocess.call(command, shell=True)
        time.sleep(1)




    return split_movie_names

def optimum_num_segments(video_filename,audio_filename,target_num,start_dist,step):

    process = subprocess.Popen(["ffmpeg", "-i",video_filename,"-vn",audio_filename], stdin = subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.stdin.write("y")

    process = subprocess.Popen(['ffmpeg',  '-i', video_filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
    tot_seconds = 3600*float(matches['hours'])+float(60*matches['minutes'])+float(matches['seconds'])

    spf = wave.open(audio_filename,'r')

    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    fs = spf.getframerate()

    Time=np.linspace(0, len(signal)/fs, num=len(signal))

    #plot_raw_sound(signal,Time,fs)


    #If Stereo
    if spf.getnchannels() == 2:
        print 'Just mono files'
        sys.exit(0)


    ft_time, ft_sig = whiten(signal,Time,cutoff)
    (low,high) = target_num

    print "Target # pieces between: ", low, high
    print


    num_pieces = 0
    while num_pieces+1 not in range(low,high+1):
        start_dist += step
        print "Trying distance: ", start_dist


        ind_split = split_sound(ft_time,ft_sig,thresh,dist=start_dist)
        num_pieces = len(ind_split)
        print "Number of pieces: ", num_pieces+1
        if num_pieces+1 in range(low,high+1):
            print "Target number achieved!"
        else:
            print "Increasing distance by 50..."
        print
    time_split = np.split(ft_time,ind_split)
    sig_split = np.split(ft_sig,ind_split)

    num_pieces = plot_split_time(time_split,sig_split)

    split_movie_names = split_video(video_filename,time_split,signal,ind_split,tot_seconds)
    return split_movie_names
