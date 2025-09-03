#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove leading or trailing silence from audio samples
adapted from: https://stackoverflow.com/questions/29547218/remove-silence-at-the-beginning-and-at-the-end-of-wave-files-with-pydub

Created on Sun May 29 23:47:57 2022

@author: luiz
"""

from pydub import AudioSegment
from os import path, listdir

folderPath = r"/media/luiz/HDp1/Gravações/SF/Essenfelder_v2/pedal_on"
outputFolder = r"processed" # folder must exist!

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=5):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def removeLeadingSilence(wavFilePath, silence_threshold=-50.0, chunk_size=5, offset=0):
    sound = AudioSegment.from_file(wavFilePath, format="wav")

    start_trim = detect_leading_silence(sound, silence_threshold=silence_threshold, chunk_size=chunk_size)

    duration = len(sound)
    start_trim_offset = start_trim + offset
    trimmed_sound = sound[start_trim_offset:duration]
    
    return trimmed_sound

def removeTrailingSilence(wavFilePath, silence_threshold=-50.0, chunk_size=5, offset=0):
    sound = AudioSegment.from_file(wavFilePath, format="wav")

    end_trim = detect_leading_silence(sound.reverse(), silence_threshold=silence_threshold, chunk_size=chunk_size)

    duration = len(sound)
    end_trim_offset = end_trim + offset
    trimmed_sound = sound[0:duration-end_trim_offset]
    
    return trimmed_sound

def removeLeadingTrailingSilence(wavFilePath, silence_threshold=-50.0, chunk_size=5, offset_lead=0, offset_trail=0):
    sound = AudioSegment.from_file(wavFilePath, format="wav")

    start_trim = detect_leading_silence(sound, silence_threshold=silence_threshold, chunk_size=chunk_size)
    end_trim = detect_leading_silence(sound.reverse(), silence_threshold=silence_threshold, chunk_size=chunk_size)
    
    duration = len(sound)
    start_trim_offset = start_trim + offset_lead
    end_trim_offset = end_trim + offset_trail
    trimmed_sound = sound[start_trim_offset:duration-end_trim_offset]
    
    return trimmed_sound
    
samFiles = listdir(folderPath)
for samFile in samFiles:
    if samFile[-4:] != '.wav':
        continue # skip non wave files
    audioProcessed = removeLeadingSilence(path.join(folderPath, samFile), offset=-20, silence_threshold=-40, chunk_size=5)
    outputFile = path.join(folderPath, outputFolder, samFile)
    audioProcessed.export(outputFile, format="wav")
