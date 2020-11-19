#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 23:33:36 2020

@author: luiz
"""
import copy
import music21 as mus # install this. With pip: pip install music21 / with anaconda: conda install -c iainsgillis music21
import re # regexp
from os import listdir
from os.path import isfile, join, relpath, dirname
import numpy as np

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
    Cutoff             = None
    Fil_veltrack       = None
    
    # non-opcodes:
    Vel                = None
    
    # methods:
    def get_pkeycenter(self):
        return self.Pkeycenter
    def get_vel(self):
        return self.Vel

class sfz_creator:
    Samples = None # list of dictionaries with sample name, file name and properties
    SfzStrL = [] # list of strings, one per line
    OutFile = None # output file path
    
    VelMap  = None # dict mapping velocities
    PkcList = []
    
    def __init__(self, samples, outFile):
        self.Samples = samples
        self.OutFile = outFile
    
    def genSfz(self): # generates sfz file from property "samples" (list of samples)
        self.writeHeader()
        for sample in self.Samples:
            self.writeSampleBlock(sample)
        with open(self.OutFile, 'w') as ofile:
            ofile.write('\n'.join(self.SfzStrL))
        print('SFZ file successfully generated')
            
    def writeHeader(self):
        self.SfzStrL.append('// Header lines')
        self.SfzStrL.append('') # empty line
        
    def writeSampleBlock(self, sample): # writes a region from a sample
        self.SfzStrL.append('<region>')
        self.SfzStrL.append('sample=' + sample.Fname)
        self.SfzStrL.append('pitch_keycenter=' + str(sample.Pkeycenter))
        self.SfzStrL.append('lokey=' + str(sample.Lokey))
        self.SfzStrL.append('hikey=' + str(sample.Hikey))
        if sample.Lovel != None:
            self.SfzStrL.append('lovel=' + str(sample.Lovel))
        if sample.Hivel != None:
            self.SfzStrL.append('hivel=' + str(sample.Hivel))
        
        if sample.Ampeg_release != None:
            self.SfzStrL.append('ampeg_release=' + str(sample.Ampeg_release))
        if sample.Amp_veltrack != None:
            self.SfzStrL.append('amp_veltrack=' + str(sample.Amp_veltrack))
        if sample.Cutoff != None:
            self.SfzStrL.append('cutoff=' + str(sample.Cutoff))
        if sample.Fil_veltrack != None:
            self.SfzStrL.append('fil_veltrack=' + str(sample.Fil_veltrack))
            
        self.SfzStrL.append('') # empty line
        
    def getSamplesFromFolder(self, folderPath, **kwargs):
        """
        

        Parameters
        ----------
        folderPath : string
            This should be the directory path in which the samples are to be
            found.
        **kwargs : key-value pairs
            Each key is a sample property that shall be checked in the file
            names. The corresponding value is a regexp template to find the
            property. Examples:
                pmidi='C(\d+)' # will look for a midi pitch that matches this
                    template.
                pitch='_([A-G]#?\d)_' # will look for pitches like
                    A#4 matching this.
                vel='v(\d+)' # will look for velocities in a sequence (1,2,3)
                velval = 'v(\d+)' # will look for velocity values
                    (e.g. 64, 90, 120)
                

        Returns
        -------
        None.

        """

        
        
        samFiles = listdir(folderPath)
        for samFile in samFiles:
            if samFile[-4:] != '.wav':
                continue # skip non wave files
            sam = sample()
            if self.OutFile == None:
                sam.Fname = join(folderPath, samFile)
            else:
                sam.Fname = join(relpath(folderPath, dirname(self.OutFile)), samFile)
            # create a pitch object:
            p = mus.pitch.Pitch()
            
            for key, value in kwargs.items(): # value is a regex template and key is a property
                if key == 'pitch':
                    pitchNameWithOctave = re.findall(value, samFile)
                    if len(pitchNameWithOctave) == 0:
                        print('Pitch not found for: ' + samFile)
                    elif len(pitchNameWithOctave) > 1:
                        print('More than one pitch match for: ' + samFile)
                    else:
                        p.nameWithOctave = pitchNameWithOctave[0]
                        sam.Pkeycenter = p.midi # assign midi pitch value to property
                if key == 'pmidi':
                    pitchMidiValue = re.findall(value, samFile)
                    if len(pitchMidiValue) == 0:
                        print('Pitch not found for: ' + samFile)
                    elif len(pitchMidiValue) > 1:
                        print('More than one pitch match for: ' + samFile)
                    else:
                        p.midi = int(pitchMidiValue[0])
                        sam.Pkeycenter = p.midi # assign midi pitch value to property
                if key == 'velval':
                    vel = re.findall(value, samFile)
                    if len(vel) == 0:
                        print('Velocity not found for: ' + samFile)
                    elif len(vel) > 1:
                        print('More than one velocity match for: ' + samFile)
                    else:
                        sam.Vel = int(vel[0]) # assign note velocity to property
                if key == 'vel':
                    vel = re.findall(value, samFile)
                    if len(vel) == 0:
                        print('Velocity not found for: ' + samFile)
                    elif len(vel) > 1:
                        print('More than one velocity match for: ' + samFile)
                    else:
                        sam.Vel = self.VelMap[vel[0]] # assign mapped note velocity to property
                        
            self.Samples.append(sam)
            self.PkcList.append(p.midi)
        
    def autoSpreadKeys(self, spreadDirection): # lower keys, closest keys, higher keys
        self.Samples.sort(key=sample.get_pkeycenter) # sorting samples according to pitch keycenter
        self.PkcList.sort() # pitch keycenter list
        for iSam in range(len(self.Samples)): # run through list
            currP = self.Samples[iSam].Pkeycenter # currP = current pitch
            if spreadDirection == 'lower':
                if self.PkcList.index(currP) == 0: # if it's the lowest pitch keycentre
                    self.Samples[iSam].Lokey = 0
                    self.Samples[iSam].Hikey = currP
                else:
                    self.Samples[iSam].Lokey = self.PkcList[self.PkcList.index(currP)-1] + 1 # find first occurrence and go back one position. Add 1 to start next region without superposition.
                    self.Samples[iSam].Hikey = currP
            elif spreadDirection == 'higher':
                if self.PkcList[::-1].index(currP) == 0:
                    self.Samples[iSam].Lokey = currP
                    self.Samples[iSam].Hikey = 127
                else:
                    self.Samples[iSam].Lokey = currP
                    self.Samples[iSam].Hikey = self.PkcList[::-1][self.PkcList[::-1].index(currP)-1] - 1 # find last occurrence and go back one position (reversed list). Subtract 1 to finish before starting next region, without superposition.
            
        
    def autoSpreadVelocities(self, spreadDirection): # lower vel, closest vel, higher vel
        self.Samples.sort(key=sample.get_vel)
        self.Samples.sort(key=sample.get_pkeycenter) # sorting samples according to pitch keycenter
        self.PkcList.sort() # pitch keycenter list
        pkc_array = np.array(self.PkcList)
        for iSam in range(len(self.Samples)): # run through list
            currSam = self.Samples[iSam]
            currP = self.Samples[iSam].Pkeycenter # currP = current pitch
            sameP = np.where(pkc_array == currP)
            samples_same_p = np.array(self.Samples)[sameP]
            vels = [x.Vel for x in samples_same_p]
            vels.sort()
            vels.insert(0, 0)
           # samples_same_p.tolist.sort(key=sample.Vel)
            currIdx = samples_same_p.tolist().index(currSam)
            if spreadDirection == 'lower':
                self.Samples[iSam].Lovel = vels[currIdx]
                self.Samples[iSam].Hivel = vels[currIdx+1]
                
        # todo - better approach: run thorough all pitches (0 to 127) and for every sub-region, do an independent spread. Connect them!
        
    def setForAll(self, prop, val):
        for iSam in range(len(self.Samples)):
            setattr(self.Samples[iSam], prop, val)
        
# Test (delete all this after testing):
#fp = '/media/luiz/Volume/Downloads/SoundFonts/SteinwayD274/Samples/Bright'
fp = '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/PTQ_SteinwayD_H'

sfz1 = sfz_creator([], '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/Steinway_D_HB.sfz')

sfz1.VelMap = {'v2': 50, 'v4': 100, 'loud': 127}

#sfz1.getSamplesFromFolder(fp, pmidi = 'C(\d+)')
#sfz1.getSamplesFromFolder(fp, pitch = '_([A-G]#?\d)_', vel='_([a-z]+)_')
sfz1.getSamplesFromFolder(fp, pmidi = 'pitch(\d+)', vel='_(v\d)_')


sfz1.autoSpreadKeys('higher')

sfz1.autoSpreadVelocities('lower')

sfz1.setForAll('Ampeg_release', 0.6)

sfz1.setForAll('Cutoff', 200)

sfz1.setForAll('Fil_veltrack', 8000)

sfz1.genSfz()
