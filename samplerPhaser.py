#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 01:08:30 2022

@author: luiz
"""

import re
from scipy.io.wavfile import read as wvrd
from scipy.io.wavfile import write as wvwr
import numpy as np
from os import path, listdir

def freq_wav(wv):
    srate = wv[0]
    dt = 1.0/srate
    wv_left = wv[1][:,0]
    wv_right = wv[1][:,1] # this way, it is required to be stereo
    wv_left_f = abs(np.fft.fft(wv_left))[0:int(len(wv_left)/2)]
    wv_left_fn = wv_left_f/np.max(wv_left_f)
    frq = wv_left_f/(len(wv_left)*dt)
    thr = 0.06 # threshold for first harmonic
    #f_1harmonic = np.argmax(wv_left_fn > 0.06)/(len(wv_left)*dt)
    f_1harmonic = np.argmax(wv_left_fn > thr)/(len(wv_left)*dt) # correction
    m_1harmonic = np.max(wv_left_fn > thr) # correction
    f_1harmonic_l = (np.argmax(wv_left_fn > thr) - 1)/(len(wv_left)*dt) # correction
    m_1harmonic_l = wv_left_fn[np.argmax(wv_left_fn > thr) - 1] # correction
    f_1harmonic_r = (np.argmax(wv_left_fn > thr) + 1)/(len(wv_left)*dt) # correction
    m_1harmonic_r = wv_left_fn[np.argmax(wv_left_fn > thr) + 1] # correction
    
    f_1harmonic = (f_1harmonic*m_1harmonic + f_1harmonic_l*m_1harmonic_l + f_1harmonic_r*m_1harmonic_r)/(m_1harmonic + m_1harmonic_l + m_1harmonic_r)
    return f_1harmonic

folderPath = '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/University of Iowa/Percussion/Vibraphone/sus'
outFolder = 'processed'

samFiles = listdir(folderPath)
for samFile in samFiles:
    if samFile[-4:] != '.wav':
        continue # skip non wave files
    wv = wvrd(path.join(folderPath, samFile))
    samplerate = wv[0]
    
    
    # now, we can get the approximate frequency of the first harmonic
    freq = freq_wav(wv)
    print(freq_wav(wv))
    
    # getting the period of the waveform
    period = 1/freq
    
    # creating a new wavfile delayed by approximately this period, to reduce the volume of the 1st harmonic
    numSamplesPeriod = wv[0] * period
    
    numZeros = int(numSamplesPeriod*0.46)
    zeros = np.zeros(numZeros)
    wv2data = np.full((wv[1].shape[0] + numZeros, 2), 0)
    
    # left channel
    wv2data[:,0] = np.hstack((wv[1][:,0], zeros)) + np.hstack((zeros, wv[1][:,0]))
    
    # right channel
    wv2data[:,1] = np.hstack((wv[1][:,1], zeros)) + np.hstack((zeros, wv[1][:,1]))
    
    wv2data = wv2data*0.4
    wvwr(path.join(folderPath, outFolder, samFile), samplerate, wv2data.astype(np.int16))
