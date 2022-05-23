#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 22:19:39 2020

@author: luiz
"""

from midiutil import MIDIFile
import music21 as mus

notes = []
for iOctv in range(1,8):
    for iNote in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        note = mus.pitch.Pitch(iNote)
        note.octave = iOctv
        notes.append(note)

max_dur = 25
min_dur = 3
def duration_decay(i):
    return int(max_dur - (max_dur - min_dur)*(i/len(notes)))
dur_list = []

degrees  = [n.midi for n in notes]#[60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number

# inserting some extra notes manually:
degrees.insert(0,23)
degrees.insert(0,21)

track    = 0
channel  = 0
time     = 1
pause    = 2    # In beats
#duration = 1    # In beats
tempo    = 60   # In BPM
vel   = 75  # 0-127, as per the MIDI standard

#%% Generating midi file

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
    dur_list.append(duration_decay(i))
    start = 0
    for d in dur_list[:i]:
        start = start + d + pause
    MyMIDI.addNote(track, channel, pitch, start, dur_list[-1], vel)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
    
#%% Generate audio file from midi manually! Then replace the links and run this
from pydub import AudioSegment
import numpy as np
from os import path

audioPath = r"/media/luiz/Volume/Dokumente/Musik/Projekte/stwb_major-scale_v33.wav"
outputPath = r"/media/luiz/Volume/Dokumente/Musik/Projekte/temp"

audio = AudioSegment.from_wav(audioPath)
durations_ms = np.array([])
pause_ms = pause * 60/tempo * 1000
pause_ms = pause_ms - 1 # fine tuning, not sure why it's needed
for i, pitch in enumerate(degrees):
    duration_ms = duration_decay(i) * 60/tempo * 1000
    durations_ms = np.append(durations_ms, duration_ms)
    
for i, pitch in enumerate(degrees):
    t0 = i*pause_ms + np.sum(durations_ms[:i])
    t1 = i*pause_ms + np.sum(durations_ms[:i+1])
    
    if i > 0:
        t0 = t0 - 500 # start a bit earlier, to avoid cutting sound
    
    fileName = "normal_pitch" + str(pitch) + "_v" + str(1) + ".wav"
    filePath = path.join(outputPath, fileName)
    
    audioSegment = audio[t0:t1]
    audioSegment.export(filePath, format="wav")
    
