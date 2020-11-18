#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created at 17:34:43 on Mon, the 3rd of June of 2019
SFZ loop tool
@author: Luiz Guilherme de M. Ventura
"""

import os
import glob
import re
from scipy.io.wavfile import read as wvrd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal # for low-pass filter
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
        i1 = num_vel # for test, will be updated
        if k % int(num_seq) == 0:
            i2 = 1
            cfrm2 = simpledialog.askstring("Input", file[-12:] + " was identified as " + current_pitch + " seq " + str(i2))
            if cfrm2 == '':
                nt = current_pitch
            else:
                nt = cfrm2
        #os.rename(file, p + str(nt) + s.replace('#', '') + str(i) + ext)
        os.rename(file, p + s.replace('$0', nt).replace('$1', str(i1)).replace('$2', str(i2)) + ext)
        print(file + ' -> ' + p + s.replace('$0', nt).replace('$1', str(i1)).replace('$2', str(i2)) + ext)
        i2 += 1

def find_loop_samples(waveData, threshold = 0.4):
    sampleRate = waveData[0]
    dt = 1.0/sampleRate
    wv_left = waveData[1][:,0]
    wv_left = wv_left/np.max(wv_left) # normalization
    wv_right = waveData[1][:,1]
    wv_right = wv_right/np.max(wv_right) # normalization
    wv_left_d = (wv_left[1:] - wv_left[:-1])/dt # derivative
    wv_right_d = (wv_right[1:] - wv_right[:-1])/dt # derivative
    wv_left_energy = wv_left**2
    wv_right_energy = wv_right**2
    
    # First job: find the region where we want the loop. Not in the silence, but where the mean signal energy is
    # greater than a threshold:
    b, a = signal.butter(8, 0.125)
    wv_left_energy_lpf = signal.filtfilt(b, a, wv_left_energy, padlen=150)
    try:
        lp_start = np.where(wv_left_energy_lpf > 0.4)[0][0] # first element where the wave is greater than the threshold
        lp_end = np.where(wv_left_energy_lpf > 0.4)[0][-1] # last element where the wave is greater than the threshold
        
        # Now it's time to correct the loops. The first thing I will do is reduce a bit the size to avoid be too much close to the
        # begin or to the end. But I have to do it proportionaly to the length of the wave file.
        lp_start = lp_start + int(len(wv_left)*0.05) # value hard-coded here.
        lp_end = lp_end - int(len(wv_left)*0.05) # value hard-coded here.
        
        # Now, one of the most important steps and though to do by hand: take samples with same amplitude both at the beginning
        # and at the end. Let's find amplitude 0 or very close to it. And to get an even better result, let's try to take a derivative
        # of same signal (ideally, we should search a derivative close to each other, for start and end. TODO).
        # Both things have to be checked in both channels, so the requirements shouldn't be so strict.
        amp0_left = np.where(wv_left_energy[lp_start:lp_end] < 0.001) + lp_start # amplitude threshold hard-coded here
        amp0_right = np.where(wv_right_energy[lp_start:lp_end] < 0.001) + lp_start # amplitude threshold hard-coded here
        # For speed and memory optimization, we looked only from lp_start to lp_end. So, the lp_start had to be added!!!
        amp0_both = np.intersect1d(amp0_left, amp0_right)
        lp_start = amp0_both[0]
        lp_end = amp0_both[-1]
        
        derPos_left = np.where(wv_left_d[lp_start:lp_end] > 0) + lp_start # already only considering the region where amplitude is also nearly 0
        derPos_right = np.where(wv_right_d[lp_start:lp_end] > 0) + lp_start # already only considering the region where amplitude is also nearly 0
        derPos_both = np.intersect1d(derPos_left, derPos_right) # in the end, these conditions look in fact so strict =O
        
        # Now, we are hopefully ready to take the final loop start and loop end.
        lp_start = derPos_both[0]
        lp_end = derPos_both[-1]
    except:
        print('Warning: could not find loop samples for last file. Using the whole length!')
        lp_start = 1
        lp_end = len(wv_left - 1)
    
    return lp_start, lp_end

def rewrite_sfz_file(loop_starts, loop_ends, sfz_text_original, path_sfz, name_suffix = '_autoLoop'):
#    remaining_text = sfz_text_original
#    for k in range(len(loop_starts)):
#        pos_l = remaining_text.find('loop_start')
#        endline = remaining_text[pos_l:].find('\n')
#        sfz_text_original[pos_l:endline] = 'loop_start=' + str(loop_starts[k])
#        remaining_text = remaining_text[pos_l+10:]
#        
#    for k in range(len(loop_ends)):
#        pos_l = remaining_text.find('loop_end')
#        endline = remaining_text[pos_l:].find('\n')
#        sfz_text_original[pos_l:endline] = 'loop_end=' + str(loop_ends[k])
#        remaining_text = remaining_text[pos_l+10:]
    text_lines = sfz_text_original.split('\n')
    ks = 0;
    ke = 0;
    for k, line in enumerate(text_lines):
        if line[:10] == 'loop_start':
            text_lines[k] = 'loop_start=' + str(int(loop_starts[ks]))
            ks = ks + 1
        elif line[:8] == 'loop_end':
            text_lines[k] = 'loop_end=' + str(int(loop_ends[ke]))
            ke = ke + 1
#        else:
#            text_lines[k] = text_lines[k]
    
    #print(text_lines)
    with open(path_sfz[:-4] + name_suffix + '.sfz','w') as sfz_file_out:
        sfz_file_out.writelines('\n'.join(text_lines))

def on_loop_button_click(entries): # this will only affect samples which already have the tag loop_start
    e = []
    field = []
    for k, entry in enumerate(entries):
        field.append(entry[0])
        e.append(entry[1].get())
    path_sfz = e[5]
    #sfz_file = open(path_sfz)
    with open(path_sfz,'r') as sfz_file:
        text = sfz_file.read()
    remaining_text = text # start to iterate through the text
    pos_l = 0
    #while pos_l != -1: # when str.find() doesn't find anything, it returns -1
    loop_starts = np.array([])
    loop_ends = np.array([])
    while True: #for k in range(4):
        pos_l = remaining_text.find('loop_start') # pos_l is the position of the first character of the next loop_start
        #aux_text = remaining_text[pos_l:pos_l-500:-1] # search for the tag 'sample' backwards. This line is only for limitting the search to last n characters
        #pos_s = pos_l - aux_text.find('elpmas') # sample backwards
        if pos_l == -1:
            break
        aux_text = remaining_text[:pos_l]
        pos_s = aux_text.rfind('sample') # position of the first char of 'sample' in the aux_text, looking backwards
        endline = aux_text[pos_s:].find('\n')
        sfz_folder = path_sfz[:path_sfz.rfind('/')]
        sample_file_path = sfz_folder + '/' + aux_text[pos_s+7:pos_s + endline]  # adding the sample file name given in the sfz file with the rest of the folder
        sample_file_path = '/'.join(sample_file_path.split('\\'))
        #print(sample_file_path)
        remaining_text = remaining_text[pos_l+10:]
        
        wv = wvrd(sample_file_path)
        loop_sample_start, loop_sample_end = find_loop_samples(wv)
        #print('Start:' + str(loop_sample_start))
        #print('End:' + str(loop_sample_end))
        
        loop_starts = np.append(loop_starts, loop_sample_start)
        loop_ends = np.append(loop_ends, loop_sample_end)
        
    rewrite_sfz_file(loop_starts, loop_ends, text, path_sfz, '_loop')
    print('Done!')
    

from tkinter import *
fields = 'Path to file', 'Extension (e.g. .wav)', 'Form', 'No. velocities', 'No. sequences'
fields2 = 'Path to sfz file', # we are working with vectors of strings. If there is only one string, a comma at the end is needed,
# otherwise, it will iterate over characters within the string instead of iterating over strings inside the vector.

std_entries = '', '.wav', '$0_v$1_r$2', '', '', ''


def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text)) 

def set_std(entries):
    for k, entry in enumerate(entries):
        entry[1].insert(0, std_entries[k])

def makeform(root, fields, fields2):
   entries = []
   for k, field in enumerate(fields):
#      row = Frame(root)
      lab = Label(master = root, width=20, text=field, anchor='w')
      ent = Entry(master = root)
#      row.grid(row=0, column=0, padx='5', pady='5', sticky='ew')
      lab.grid(row=2*k, column=0, padx='5', pady='5', sticky='ew')
      ent.grid(row=2*k+1, column=0, padx='5', pady='5', sticky='ew')
      entries.append((field, ent))
   for k, field in enumerate(fields2):
#      row = Frame(root)
      lab = Label(master = root, width=20, text=field, anchor='w')
      ent = Entry(master = root)
#      row.pack(side=TOP, fill=X, padx=5, pady=5, column=1)
      lab.grid(row=2*k, column=1, padx='5', pady='5', sticky='ew')
      ent.grid(row=2*k+1, column=1, padx='5', pady='5', sticky='ew')
      entries.append((field, ent))
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields, fields2)
   set_std(ents)
   root.bind('<Return>', (lambda event, e=ents: on_rename_button_click(e)))   
   b1 = Button(root, text='Rename',
          command=(lambda e=ents: on_rename_button_click(e)))
   b1.grid( column=0, padx='5', pady='5', sticky='ew') # row not defined, going to pack after all rows
   b2 = Button(root, text='Quit', command=root.destroy)
   b2.grid( column=0, padx='5', pady='5', sticky='ew') # row not defined, going to pack after all rows
   
   b3 = Button(root, text='Redefine loops', command=(lambda e=ents: on_loop_button_click(e)))
   b3.grid( column=1, padx='5', pady='5', sticky='ew') # row not defined, going to pack after all rows
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
