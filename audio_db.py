#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat 23 Mar 2024 14:18:30 

@author: luiz
"""

from os import listdir, mkdir
from os.path import isfile, isdir, join, split, relpath, dirname
import numpy as np
from scipy.io.wavfile import read, write
import wave

def get_bit_depth(wave_file):
    with wave.open(wave_file, 'rb') as wf:
        return wf.getsampwidth() * 8
    
def getPeakAmpDB(wave_file_path):
    # https://gist.github.com/endolith/e8597a58bcd11a6462f33fa8eb75c43d?permalink_comment_id=3461842
    # bit_depth = get_bit_depth(wave_file_path)  # this retrieves 24 for 24-bit, but scipy converts to 32 bit and scales it, so we need to use scipy
    sample_rate, data = read(wave_file_path)
    bit_depth = data.dtype.itemsize * 8
    if np.issubdtype(data.dtype, np.unsignedinteger):  # uint8 wav
        maxAmp = np.max(data)/(2**bit_depth) - 2**bit_depth/2
        minAmp = np.min(data)/(2**bit_depth) - 2**bit_depth/2
    elif np.issubdtype(data.dtype, np.signedinteger):  # 16, 24, 32 bit
        maxAmp = np.max(data)/(2**bit_depth/2)
        minAmp = np.min(data)/(2**bit_depth/2)
    elif np.issubdtype(data.dtype, np.floating):  # 32 bit floating  - does it even make sense if we can exceed 1.0?
        maxAmp = np.max(data)
        minAmp = np.min(data)
    
    peak_amplitude = max(abs(maxAmp), abs(minAmp))
    
    peakDB = 20 * np.log10(peak_amplitude)
    #peakDB = max(20 * np.log10(maxAmp), 20 * np.log10(-minAmp))
    
    return peakDB

def adjust_volume(wave_file_path, raise_db, output_file_path):
    # bit_depth = get_bit_depth(wave_file_path)
    sample_rate, data = read(wave_file_path)
    bit_depth = data.dtype.itemsize * 8
    
    data = data.astype(np.float32)
    
    if bit_depth != 16:
        data = data/(2**bit_depth)
        data = data * 2**16
    
    # Calculate the scaling factor based on dB increase
    scale_factor = 10 ** (raise_db / 20)
    
    # Apply the scaling factor to the data
    scaled_data = data * scale_factor
    
    # Ensure that the values are within the valid range
    scaled_data = np.clip(scaled_data, -32768, 32767).astype(np.int16)
    
    write(output_file_path, sample_rate, scaled_data)

def normalize_file(wave_file_path, volume_db, output_file_path):
    current_db = getPeakAmpDB(wave_file_path)
    raise_db = volume_db - current_db
    adjust_volume(wave_file_path, raise_db, output_file_path)
    
def normalize_group(wave_file_paths, volume_db):
    """
    Normalizes volume of a group of files based on the highest volume
    of them all and applying the same volume change to all files.

    Parameters
    ----------
    wave_file_paths : TYPE
        List of file paths or a single folder.
    volume_db : TYPE
        DESCRIPTION.
    out_file_suffix : TYPE, optional
        DESCRIPTION. The default is '_normalized'.

    Returns
    -------
    None.

    """
    out_dir_name = 'normalized'
    
    if isdir(wave_file_paths):
        file_names = listdir(wave_file_paths)
        dir_content = list(map(join, [wave_file_paths] * len(file_names),
                               file_names))
    
        wave_file_paths = []
        for element in dir_content:
            if element.endswith('.wav'):
                wave_file_paths.append(element)
    
    current_db = -48  # minimum
    for wfpath in wave_file_paths:
        wf_db = getPeakAmpDB(wfpath)
        print(f'{wfpath}: {wf_db} dB')
        if wf_db > current_db:
            current_db = wf_db
    
    raise_db = volume_db - current_db
    print(f'Raising {raise_db} dB')
    for wfpath in wave_file_paths:
        dir_path, file_name = split(wfpath)
        if not isdir(join(dir_path, out_dir_name)):
            mkdir(join(dir_path, out_dir_name))
        output_file_path = join(dir_path, out_dir_name, file_name)
        adjust_volume(wfpath, raise_db, output_file_path)
        print(f'Adjusted volume of {wfpath}. Saved into {output_file_path}')
