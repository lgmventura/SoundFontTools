#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 23:33:36 2020

@author: luiz
"""


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
        self.SfzStrL.append('sample=' + sample['fname'])
        self.SfzStrL.append('lokey=' + str(sample['lokey']))
        self.SfzStrL.append('hikey=' + str(sample['hikey']))
        self.SfzStrL.append('lovel=' + str(sample['lovel']))
        self.SfzStrL.append('hivel=' + str(sample['hivel']))
        self.SfzStrL.append('pitch_keycenter=' + str(sample['pitch_keycenter']))
        if sample['ampeg_release'] != None:
            self.SfzStrL.append('ampeg_release=' + str(sample['ampeg_release']))
        if sample['amp_veltrack'] != None:
            self.SfzStrL.append('amp_veltrack=' + str(sample['amp_veltrack']))
            
        self.SfzStrL.append('') # empty line
        
samp1 = dict()
samp1['fname'] = '/media/luiz/Volume/Downloads/SoundFonts/Cello SFZ/Samples/Ens-Cello-Leg83_a1.wav'
samp1['lokey'] = 2
samp1['hikey'] = 3
samp1['lovel'] = 0
samp1['hivel'] = 20
samp1['pitch_keycenter'] = 64
samp1['ampeg_release'] = 0.6
samp1['amp_veltrack'] = None

samp2 = samp1.copy()
samp2['pitch_keycenter'] = 68
samp2['hikey'] = 10

sfz1 = sfz_creator([samp1, samp2], '/media/luiz/Volume/Downloads/SoundFonts/sfzPythonTest.sfz')
sfz1.genSfz()