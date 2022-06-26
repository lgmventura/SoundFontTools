#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rename sample files

Created on Sat Jun 25 13:54:04 2022

@author: luiz
"""

import music21 as m21
import os
import re

folderPath = '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/University of Iowa/Percussion/Vibraphone/sus'


files = os.listdir(folderPath)


# Note number to note pitch
def renameNoteMidiPitchToName(files):
    iF = 0
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f)))) # IMPORTANT: all files in the folder must be labeled with a number to work
    for fname in files:
        if fname.endswith('.wav'):
            p = m21.pitch.Pitch(int(re.findall('p(\d+)', fname)[0]))
            print(p.nameWithOctave)
            #os.rename(os.path.join(folderPath, fname), os.path.join(folderPath, 'sus_' + p.nameWithOctave + '_v2.wav'))
            iF = iF + 1
        
# note pitch to note number
def renameNameToMidiPitch(files):
    for fname in files:
        iF = 0
        if fname.endswith('.wav'):
            p = m21.pitch.Pitch(re.findall('_([A-G]b?#?\d)', fname)[0])
            print(p.midi)
            #os.rename(os.path.join(folderPath, fname), os.path.join(folderPath, 'sus_' + str(p.midi) + '_v3.wav'))
            iF = iF + 1
            
renameNameToMidiPitch(files)