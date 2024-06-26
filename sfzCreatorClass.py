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
from os.path import isfile, join, split, relpath, dirname
import numpy as np

from audio_db import getPeakAmpDB

class sample:
    # opcodes:
    Pkeycenter         = None
    Lokey              = None
    Hikey              = None
    Lovel              = None
    Hivel              = None
    Ampeg_start        = None
    Ampeg_attack       = None  # https://sfzformat.com/opcodes/ampeg_attack/
    Ampeg_release      = None
    Ampeg_hold         = None
    Ampeg_sustain      = None
    Ampeg_decay        = None
    Amp_veltrack       = None
    Cutoff             = None
    Fil_veltrack       = None
    Volume             = None
    Hirand             = None
    Lorand             = None
    Trigger            = None  # when to trigger the sample
    Offset             = None  # number of samples to skip at the beginning (start to play at)
    
    Locc64             = None  # sustain pedal
    Hicc64             = None  # sustain pedal
    
    # non-opcodes:
    Fname              = None
    FullFilePath       = None
    
    Vel                = None
    
    # grouping
    Group              = None
    
    # methods:
    def get_pkeycenter(self):
        return self.Pkeycenter
    def get_vel(self):
        return self.Vel

# def peakAmpDB(wave_file_path):
#     import wave
#     import struct
    
#     # Open the audio file
#     with wave.open(wave_file_path, 'r') as audio:
#         # Extract the raw audio data
#         raw_data = audio.readframes(audio.getnframes())
    
#     # Convert the raw audio data to a list of integers
#     samples = struct.unpack('{n}h'.format(n=audio.getnframes()), raw_data)
    
#     # Find the peak sample
#     peak = max(samples)
    
#     # Calculate the reference value based on the bit depth of the audio file
#     reference_value = 2**(audio.getsampwidth() * 8 - 1)
    
#     # Calculate the peak value in dBFS, using the maximum possible sample value as the reference value
#     peak_dB = 20 * np.log10(peak / reference_value)
    
#     print(peak_dB)

def doBinaryOperation(val1, val2, binaryOp):
    if binaryOp == '+':
        retVal = val1 + val2
    elif binaryOp == '*':
        retVal = val1 * val2
    return retVal

class sfz_creator:
    Samples = None # list of dictionaries with sample name, file name and properties
    SfzStrL = [] # list of strings, one per line
    OutFile = None # output file path
    
    VelMap  = None # dict mapping velocities
    PkcList = []
    
    def __init__(self, samples, outFile):
        self.Samples = samples
        self.OutFile = outFile
    
    def __add__(self, other):  # merging two sfz file objects
        self.Samples = self.Samples + other.Samples
        self.SfzStrL = self.SfzStrL + other.SfzStrL
        self.VelMap = self.VelMap | other.VelMap
        self.PkcList = self.PkcList + other.PkcList
        return self
    
    def genSfz(self): # generates sfz file from property "samples" (list of samples)
        self.SfzStrL = [] # clear list
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
        
        if sample.Ampeg_start != None:
            self.SfzStrL.append('ampeg_start=' + str(sample.Ampeg_start))
        if sample.Ampeg_attack != None:
            self.SfzStrL.append('ampeg_attack=' + str(sample.Ampeg_attack))
        if sample.Ampeg_release != None:
            self.SfzStrL.append('ampeg_release=' + str(sample.Ampeg_release))
        if sample.Ampeg_hold != None:
            self.SfzStrL.append('ampeg_hold=' + str(sample.Ampeg_hold))
        if sample.Ampeg_sustain != None:
            self.SfzStrL.append('ampeg_sustain=' + str(sample.Ampeg_sustain))
        if sample.Ampeg_decay != None:
            self.SfzStrL.append('ampeg_decay=' + str(sample.Ampeg_decay))
        if sample.Amp_veltrack != None:
            self.SfzStrL.append('amp_veltrack=' + str(sample.Amp_veltrack))
        if sample.Cutoff != None:
            self.SfzStrL.append('cutoff=' + str(sample.Cutoff))
        if sample.Fil_veltrack != None:
            self.SfzStrL.append('fil_veltrack=' + str(sample.Fil_veltrack))
        if sample.Volume != None:
            self.SfzStrL.append('volume=' + str(sample.Volume))
        if sample.Hirand != None:
            self.SfzStrL.append('hirand=' + str(sample.Hirand))
        if sample.Lorand != None:
            self.SfzStrL.append('lorand=' + str(sample.Lorand))
        if sample.Trigger != None:
            self.SfzStrL.append('trigger=' + str(sample.Trigger))
        if sample.Offset != None:
            self.SfzStrL.append('offset=' + str(sample.Offset))
        if sample.Locc64 != None:
            self.SfzStrL.append('locc64=' + str(sample.Locc64))
        if sample.Hicc64 != None:
            self.SfzStrL.append('hicc64=' + str(sample.Hicc64))
            
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
            
            sam.FullFilePath = join(folderPath, samFile)
            
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
                if key == 'group':
                    sam.Group = value
                        
            self.Samples.append(sam)
            self.PkcList.append(p.midi)
        
    def autoSpreadKeys(self, spreadDirection, group = None): # lower keys, closest keys, higher keys
        self.Samples.sort(key=sample.get_pkeycenter) # sorting samples according to pitch keycenter
        self.PkcList.sort() # pitch keycenter list
        for iSam in range(len(self.Samples)): # run through list
            currP = self.Samples[iSam].Pkeycenter # currP = current pitch
            if group == None or group == self.Samples[iSam].Group:
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
                elif spreadDirection == 'closest':
                    raise NotImplementedError('To be implemented.')
            
    def autoSpreadVelocities(self, spreadDirection, group = None): # lower vel, closest vel, higher vel
        self.Samples.sort(key=sample.get_vel)
        self.Samples.sort(key=sample.get_pkeycenter) # sorting samples according to pitch keycenter
        self.PkcList.sort() # pitch keycenter list
        pkc_array = np.array(self.PkcList)
        for iSam, currSam in enumerate(self.Samples): # run through list
            if group == None or group == currSam.Group:
                currP = self.Samples[iSam].Pkeycenter # currP = current pitch
                sameP = np.where(pkc_array == currP)
                samples_same_p = np.array(self.Samples)[sameP]
                vels = [x.Vel for x in samples_same_p]
                vels.sort()
                vels.insert(0, 0)
                # samples_same_p.tolist.sort(key=sample.Vel)
                try:
                    currIdx = samples_same_p.tolist().index(currSam)
                except ValueError as e:
                    print(f'Current sample keycentre: {currSam.Pkeycenter}')
                    print(f'Same pitch at: {sameP}')
                    print(f'Pitch keycentre array: {pkc_array}')
                    print(f'length of pitch keycentre list: {len(self.PkcList)}')
                    raise(e)
                if spreadDirection == 'lower':
                    self.Samples[iSam].Lovel = vels[currIdx] + 1
                    self.Samples[iSam].Hivel = vels[currIdx+1]
                elif spreadDirection == 'higher':
                    raise NotImplementedError('To be implemented.')
                elif spreadDirection == 'closest':
                    raise NotImplementedError('To be implemented.')
                    
        
    # TODO: correct this, which should do for the group separately:
    # def autoSpreadVelocities(self, spreadDirection, group = None): # lower vel, closest vel, higher vel
    #     self.Samples.sort(key=sample.get_pkeycenter) # sorting samples according to pitch keycenter
    #     self.PkcList.sort() # pitch keycenter list    
    #     # because we want to do only for the group, let us separate the group
    #     # first. If group is None, it will be the same as operating the whole
    #     # list of samples.
    #     sampleListGroup = []  # subset of samples of the given group
    #     PkcListGroup = []  # subset of pitch keycentres of the given group
    #     for idx, currSam in enumerate(self.Samples): # run through list
    #         if group is None or group == currSam.Group:  # copy all samples from group to this subset
    #             sampleListGroup.append(self.Samples[idx])
    #             PkcListGroup.append(self.PkcList[idx])
        
    #     sampleListGroup.sort(key=sample.get_vel)
    #     sampleListGroup.sort(key=sample.get_pkeycenter) # sorting samples according to pitch keycenter
    #     PkcListGroup.sort() # pitch keycenter list
    #     pkc_array = np.array(PkcListGroup)
    #     for idxG, currSamG in enumerate(sampleListGroup): # run through list
    #          currP = sampleListGroup[idxG].Pkeycenter # currP = current pitch
    #          sameP = np.where(pkc_array == currP)
    #          samples_same_p = np.array(sampleListGroup)[sameP] # same pitch
    #          vels = [x.Vel for x in samples_same_p]
    #          vels.sort()
    #          vels.insert(0, 0)
    #         # samples_same_p.tolist.sort(key=sample.Vel)
    #          currIdx = samples_same_p.tolist().index(currSamG)
    #          if spreadDirection == 'lower':
    #              sampleListGroup[idxG].Lovel = vels[currIdx] + 1
    #              sampleListGroup[idxG].Hivel = vels[currIdx+1]
    #          elif spreadDirection == 'higher':
    #              raise NotImplementedError('To be implemented.')
    #          elif spreadDirection == 'closest':
    #              raise NotImplementedError('To be implemented.')
                
    #     # todo - better approach: run thorough all pitches (0 to 127) and for every sub-region, do an independent spread. Connect them!
        
    #     # now going from the group list back to the global list self.Samples
    #     for idx in range(len(self.Samples)-1, -1, -1):  # run it backwards because we will pop elements out
    #         if self.Samples[idx].Group == group:
    #             self.Samples.pop(idx) # delete all samples of this group
    #             self.PkcList.pop(idx) # delete equally here
    #     self.Samples = self.Samples + sampleListGroup  # insert them back, but now with velocities spreaded in the group
    #     self.PkcList = self.PkcList + PkcListGroup  # insert back here too
        
        
        
    def setForAll(self, attribute: str, val, group = None):
        """
        

        Parameters
        ----------
        attribute : str
            attribute to set for all samples. E.g. 'Ampeg_release'
        val : int OR float
            value to set for attribute in all samples.

        Returns
        -------
        None.

        """
        for iSam in range(len(self.Samples)):
            if group == None or group == self.Samples[iSam].Group:
                setattr(self.Samples[iSam], attribute, val)
            
    def setForAllIf(self, attribute: str, val, comparison_attr: str, comparison_sign: str, comparison_value, group = None):
        """
        

        Parameters
        ----------
        attribute : str
            attribute to set for all samples that matches the condition.
            E.g. 'Cutoff'.
        val : TYPE
            Value to set for attribute in all samples that matches the
            condition.
        comparison_attr : str
            Attribute whose value is to be checked.
        comparison_sign : str
            '==', '!=', '<', '>', '<=' or '>='.
        comparison_value : TYPE
            Value to check in the comparison attribute.

        Raises
        ------
        AttributeError
            If comparison_sign is not valid.

        Returns
        -------
        None.

        """
        # Todo: make it more flexible with any possible set of conditions. Like [if a < b and c != d or e == f] -> this will need an interpreter for this. eval, exec?
        if comparison_sign == '==':
            for iSam in range(len(self.Samples)):
                if group == None or group == self.Samples[iSam].Group:
                    if getattr(self.Samples[iSam], comparison_attr) == comparison_value:
                        setattr(self.Samples[iSam], attribute, val)
        elif comparison_sign == '!=':
            for iSam in range(len(self.Samples)):
                if group == None or group == self.Samples[iSam].Group:
                    if getattr(self.Samples[iSam], comparison_attr) != comparison_value:
                        setattr(self.Samples[iSam], attribute, val)
        elif comparison_sign == '>=':
            for iSam in range(len(self.Samples)):
                if group == None or group == self.Samples[iSam].Group:
                    if getattr(self.Samples[iSam], comparison_attr) >= comparison_value:
                        setattr(self.Samples[iSam], attribute, val)
        elif comparison_sign == '<=':
            for iSam in range(len(self.Samples)):
                if group == None or group == self.Samples[iSam].Group:
                    if getattr(self.Samples[iSam], comparison_attr) <= comparison_value:
                        setattr(self.Samples[iSam], attribute, val)
        elif comparison_sign == '>':
            for iSam in range(len(self.Samples)):
                if group == None or group == self.Samples[iSam].Group:
                    if getattr(self.Samples[iSam], comparison_attr) > comparison_value:
                        setattr(self.Samples[iSam], attribute, val)
        elif comparison_sign == '<':
            for iSam in range(len(self.Samples)):
                if group == None or group == self.Samples[iSam].Group:
                    if getattr(self.Samples[iSam], comparison_attr) < comparison_value:
                        setattr(self.Samples[iSam], attribute, val)
        else:
            raise AttributeError('Invalid comparison sign: ' + comparison_sign)
    
    def setForAllRegexpFileName(self, attribute: str, val, re_template: str, group = None):
        for idx, sample in enumerate(self.Samples):
            match = re.findall(re_template, split(sample.Fname)[1]) # compare file name only, not path
            if len(match) > 0:
                if group == None or group == sample.Group:
                    setattr(self.Samples[idx], attribute, val)
    
    def operateOnAll(self, attribute: str, val, binaryOp: str, group = None):
        """
        Operate on all samples. If a group is given, it will restrict to that
        group. Usage:
            sfz.operateOnAllOpcodes("Volume", 2, "+") will increase the volume
            of all samples by 2.

        Parameters
        ----------
        attribute : str
            attribute to modified for all samples. E.g. 'Ampeg_release'
        val : int OR float
            value to operate with attribute in all samples.
        binaryOp: str
            Operator to use between current value of the attribute and val,
            resulting in the new value for the attribute.

        Returns
        -------
        None.

        """
        for iSam in range(len(self.Samples)):
            if group == None or group == self.Samples[iSam].Group:
                currVal = getattr(self.Samples[iSam], attribute)
                newVal = doBinaryOperation(currVal, val, binaryOp)
                setattr(self.Samples[iSam], attribute, newVal)
    
    # TODO: operateOnAllIf
    
    def operateOnAllRegexpFileName(self, attribute: str, val, binaryOp: str, re_template: str, group = None):
        for idx, sample in enumerate(self.Samples):
            match = re.findall(re_template, split(sample.Fname)[1]) # compare file name only, not path
            if len(match) > 0:
                if group == None or group == sample.Group:
                    currVal = getattr(self.Samples[idx], attribute)
                    newVal = doBinaryOperation(currVal, val, binaryOp)
                    setattr(self.Samples[idx], attribute, newVal)
    
    def setGroupRegexpFileName(self, re_template: str, newGroup: int, group = None):
        for idx, sample in enumerate(self.Samples):
            match = re.findall(re_template, split(sample.Fname)[1]) # compare file name only, not path
            if len(match) > 0:
                if group == None or group == sample.Group:
                    self.Samples[idx].Group = newGroup
    
    def changeGroup(self, currentGroup: int, newGroup: int):
        for idx, sample in enumerate(self.Samples):
            if currentGroup == sample.Group:
                self.Samples[idx].Group = newGroup
    
    def transpose(self, key_offset: int, group = None):
        for idx, sample in enumerate(self.Samples):
            if group == None or group == sample.Group:
                sample.Pkeycenter = sample.Pkeycenter + key_offset
                sample.Lokey = sample.Lokey + key_offset
                sample.Hikey = sample.Hikey + key_offset
                self.Samples[idx] = sample
                
    def changeHiVelIfVels(self, newHivel, ifHivel=None, ifLovel=None, group=None):  # useful when autospread velocities cannot do the job right because of multiple rr samples concurring for the same region
        for idx, sample in enumerate(self.Samples):
            if group == None or group == sample.Group:
                condHivel = False  # matches the condition ifHivel
                condLovel = False  # matches the condition ifLovel
                if ifHivel is None:
                    condHivel = True
                elif sample.Hivel == ifHivel:
                    condHivel = True
                if ifLovel is None:
                    condLovel = True
                elif sample.Lovel == ifLovel:
                    condLovel = True
                
                if condHivel and condLovel:
                    self.Samples[idx].Hivel = newHivel
                        
        
    def changeLoVelIfVels(self, newLovel, ifHivel=None, ifLovel=None, group=None):
        for idx, sample in enumerate(self.Samples):
            if group == None or group == sample.Group:
                condHivel = False  # matches the condition ifHivel
                condLovel = False  # matches the condition ifLovel
                if ifHivel is None:
                    condHivel = True
                elif sample.Hivel == ifHivel:
                    condHivel = True
                if ifLovel is None:
                    condLovel = True
                elif sample.Lovel == ifLovel:
                    condLovel = True
                
                if condHivel and condLovel:
                    self.Samples[idx].Lovel = newLovel


    # Methods that access the wav files
    def setVolumeToNormalize(self, multiplier: float = 1, group = None):
        for idx, sample in enumerate(self.Samples):
            if group == None or group == sample.Group:
                peakDB = getPeakAmpDB(sample.FullFilePath)
                self.Samples[idx].Volume = multiplier * (-peakDB)
            