#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 23:33:36 2020

@author: luiz
"""
import copy

class sample:
    # opcodes:
    Fname              = None
    Pkeycenter         = None
    Lokey              = None
    Hikey              = None
    Lovel              = None
    Hivel              = None
    Ampeg_release      = None
    Amp_veltrack       = None
    

class sfz_creator:
    Samples = None # list of dictionaries with sample name, file name and properties
    SfzStrL = [] # list of strings, one per line
    OutFile = None # output file path
    
    def __init__(self, samples, outFile):
        self.Samples = samples
        self.OutFile = outFile
    
    def genSfz(self):
        for sample in self.Samples:
            self.writeSampleBlock(sample)
        with open(self.OutFile, 'w') as ofile:
            ofile.write('\n'.join(self.SfzStrL))
        print('SFZ file successfully generated')
            
    def writeSampleBlock(self, sample):
        self.SfzStrL.append('<region>')
        self.SfzStrL.append('sample=' + sample.Fname)
        self.SfzStrL.append('lokey=' + str(sample.Lokey))
        self.SfzStrL.append('hikey=' + str(sample.Hikey))
        self.SfzStrL.append('lovel=' + str(sample.Lovel))
        self.SfzStrL.append('hivel=' + str(sample.Hivel))
        self.SfzStrL.append('pitch_keycenter=' + str(sample.Pkeycenter))
        if sample.Ampeg_release != None:
            self.SfzStrL.append('ampeg_release=' + str(sample.Ampeg_release))
        if sample.Amp_veltrack != None:
            self.SfzStrL.append('amp_veltrack=' + str(sample.Amp_veltrack))
            
        self.SfzStrL.append('') # empty line
        
# Test:
samp1 = sample()
samp1.Fname = '/media/luiz/Volume/Downloads/SoundFonts/Cello SFZ/Samples/Ens-Cello-Leg83_a1.wav'
samp1.Lokey = 2
samp1.Hikey = 3
samp1.Lovel = 0
samp1.Hivel = 20
samp1.Pkeycenter = 64
samp1.Ampeg_release = 0.6

samp2 = copy.deepcopy(samp1)
samp2.Pkeycenter = 68
samp2.Hikey = 10

sfz1 = sfz_creator([samp1, samp2], '/media/luiz/Volume/Downloads/SoundFonts/sfzPythonTest.sfz')
sfz1.genSfz()