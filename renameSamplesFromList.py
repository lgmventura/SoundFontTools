#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 00:06:37 2020

@author: luiz
"""

import os
import music21 as mus
import re

folderPath = '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/PTQ_SteinwayD_H/tmp'

notes = []
for iOctv in range(1,8):
    for iNote in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        note = mus.pitch.Pitch(iNote)
        note.octave = iOctv
        notes.append(note)

notes.insert(0,mus.pitch.Pitch(midi=23))
notes.insert(0,mus.pitch.Pitch(midi=21))

iF = 0
files = os.listdir(folderPath)
files.sort(key=lambda f: int(''.join(filter(str.isdigit, f)))) # IMPORTANT: all files in the folder must be labeled with a number to work
#print(files)
for fname in files:
    if fname.endswith('.wav'):
        nmidistr = str(notes[iF].midi)
        #print(nmidistr)
        os.rename(os.path.join(folderPath, fname), os.path.join(folderPath, 'kp_v2_pitch' + nmidistr + '.wav'))
        iF = iF + 1