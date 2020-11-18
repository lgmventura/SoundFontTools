#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 17:52:54 2018

@author: Luiz Guilherme de M. Ventura
"""

import os
import glob
import re
from scipy.io.wavfile import read as wvrd
import numpy as np
import matplotlib.pyplot as plt
try:
    import tkinter as tk  # for python 3
    from tkinter import messagebox
    from tkinter import simpledialog
except:
    import Tkinter as tk  # for python 2

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

from math import log2, pow

# https://www.johndcook.com/blog/2016/02/10/musical-pitch-notation/
A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
def pitch(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def freq_wav(wv):
    srate = wv[0]
    dt = 1.0/srate
    wv_left = wv[1][:,0]
    wv_right = wv[1][:,1]
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
##-----------------------------

def on_rename_button_click(entries):
    e = []
    field = []
    for k, entry in enumerate(entries):
        field.append(entry[0])
        e.append(entry[1].get())
    p = e[0] + '/'
    ext = e[1]
    s = e[2]
    num_vel = e[3]
    num_seq = e[4]
    listFiles = glob.glob(p + '*' + ext)
    listFiles.sort(key=natural_keys)
    fetch(entries)
    
    for k, file in enumerate(listFiles):
        wv = wvrd(file)
        
        f_1harmonic = freq_wav(wv)
        
        current_pitch = pitch(f_1harmonic)
        if k % (int(num_seq)*int(num_vel)) == 0:
            i1 = 1 # vel
            i2 = 1 # seq
            cfrm2 = simpledialog.askstring("Input", file[-12:] + " was identified as " + current_pitch + " seq " + str(i2))
            if cfrm2 == '':
                nt = current_pitch
            else:
                nt = cfrm2
        #os.rename(file, p + str(nt) + s.replace('#', '') + str(i) + ext)
        print('num vel: ' + str(num_vel) + ' num seq: ' + str(num_seq) + " i1: " + str(i1) + ' i2: ' + str(i2))
        os.rename(file, p + s.replace('$0', nt).replace('$1', str(i1)).replace('$2', str(i2)) + ext)
        print(file + ' -> ' + p + s.replace('$0', nt).replace('$1', str(i1)).replace('$2', str(i2)) + ext)
        i2 += 1
        if k % int(num_seq) == 0:
            i2 = 1 # restart i2
            i1 += 1 # next i1


from tkinter import *
fields = 'Path to file', 'Extension (e.g. .wav)', 'Form', 'No. velocities', 'No. sequences'
std_entries = '', '.wav', '$0_v$1_r$2', '', ''

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text)) 

def set_std(entries):
    for k, entry in enumerate(entries):
        entry[1].insert(0, std_entries[k])

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=20, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   set_std(ents)
   root.bind('<Return>', (lambda event, e=ents: on_rename_button_click(e)))   
   b1 = Button(root, text='Rename',
          command=(lambda e=ents: on_rename_button_click(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Quit', command=root.destroy)
   b2.pack(side=LEFT, padx=5, pady=5)
   root.mainloop()


#p = input("Enter the path to the directory with the files: ")
##if p[-1] == '\"' or p[-1] == '\'':
##    p = p[:-1]
##    p = p + '/' + p[0] # insert a / if it is missing
##else:
##    p = p + '/'
#p = p + '/'
#p = p.replace('\'', '')
#p = p.replace('\"','')
#ext = input("Enter the file extension (like .wav) ")
#listFiles = glob.glob(p + '*' + ext)
#
#s = input("Enter the name prefix with a # where the numeration is: ")
##l = input("How long is the number string? ")
###n = input("How many files in total? ")
##print("So, your files are in the form: {",)
##for i in range(3):
##    print(s.replace('#','%.{}d'.format(l) % (i+1)) + ext + ', ',)
##print("}")
##cfrm = input("Confirm? [y/n]: ")
#num_seq = input("Is there a fixed number of sequences? If so, how many? ")
#
#listFiles.sort(key=natural_keys)
#
#if cfrm == 'y':
#    i = 1
#    last_pitch = ''
#    for k, file in enumerate(listFiles):
#        wv = wvrd(file)
#        wv_left = wv[1][:,0]
#        wv_right = wv[1][:,1]
#        
#        f_1harmonic = freq_wav(wv_left)
#        
#        current_pitch = pitch(f_1harmonic)
#        if num_seq == 'n':
#            if last_pitch != current_pitch:
#                #i = 1
#                cfrm2 = input(file[-12:] + " was identified as " + current_pitch + " seq " + str(i) + ". Proceed? [y/n]")
#                if cfrm2 == 'y':
#                    i = 1
#            else:
#                i += 1
#                cfrm2 = input(file[-12:] + " was identified as " + current_pitch + " and last pitch was the same, so seq = " + str(i) + ". Proceed? [y/n]")
#            if cfrm2 == 'y':
#                os.rename(file, p + current_pitch + s.replace('#', '') + str(i) + ext)
#                print(file + ' -> ' + p + current_pitch + s.replace('#', '') + str(i) + ext)
#                last_pitch = current_pitch
#            else:
#                nt = input("So, which note should it be? ")
#                if last_pitch == nt:
#                    i += 1
#                    print("seq proceeding the count: " + str(i))
#                    current_pitch = nt # so that it uses the actual pitch corrected by user for the count
#                else:
#                    i = int(input("seq: "))
#                os.rename(file, p + str(nt) + s.replace('#', '') + str(i) + ext)
#                print(file + ' -> ' + p + str(nt) + s.replace('#', '') + str(i) + ext)
#                last_pitch = current_pitch
#        elif isInt(num_seq):
#            if k % int(num_seq) == 0:
#                i = 1
#                cfrm2 = input(file[-12:] + " was identified as " + current_pitch + " seq " + str(i) + ". Proceed? [y/n]")
#                if cfrm2 == 'y':
#                    nt = current_pitch
#                else:
#                    nt = input("So, which note should it be? ")
#            os.rename(file, p + str(nt) + s.replace('#', '') + str(i) + ext)
#            print(file + ' -> ' + p + str(nt) + s.replace('#', '') + str(i) + ext)
#            i += 1
#        else:
#            print("Not valid…")
