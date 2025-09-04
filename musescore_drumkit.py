#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
drm file creator for musescore drumkit based on SFZ file.

Created on Wed 3rd Sep 19:19:27 2025

@author: luiz
"""

from sfzCreatorClass import Sample, SfzCreator

from typing import Iterable, Set

from lxml import etree

from dataclasses import dataclass, fields
import inspect

import numpy as np


musescore_version = '4.60'

def all_common_substrings(strings: Iterable[str], min_len: int = 1) -> Set[str]:
    """Return every substring that is present in *all* supplied strings."""
    strings = list(strings)
    if not strings:
        return set()

    # 1. candidates come from the shortest string
    shortest = min(strings, key=len)
    candidates = {
        shortest[i:j]
        for i in range(len(shortest))
        for j in range(i + min_len, len(shortest) + 1)
    }

    # 2. keep only those that occur in every other string
    for s in strings:
        candidates = {sub for sub in candidates if sub in s}
        if not candidates:          # early exit
            break
    return candidates


def maximal_common_substrings(strings: Iterable[str], min_len: int = 1) -> Set[str]:
    """Same as above, but drop substrings that are already part of a longer common one."""
    common = all_common_substrings(strings, min_len)
    # discard any substrings that are *inside* a longer common substring
    return {sub for sub in common
            if not any(other != sub and sub in other for other in common)}



@dataclass
class Drum():
    _pitch: int = None
    
    head: str = 'normal'
    line: int = 0
    voice: int = 0
    name: str = ''
    stem: int = 1
    shortcut: str = None
    panelRow: int = None
    panelColumn: int = None
    
    def to_lxml(self) -> etree._Element:
        """
        Return an lxml Element whose tag-names are the class-variable names
        and whose text content is the string representation of the values.
        """
        root = etree.Element(self.__class__.__name__)          # <MyClass> … </MyClass>
        for name, value in self.__dict__.items():
            # skip private / callable stuff
            if value is None:
                continue
            
            if not name.startswith('_') and not callable(value) and not inspect.isroutine(value):
                child = etree.SubElement(root, name)
                child.text = str(value)
            
        root.set('pitch', str(self._pitch))
        
        return root

@dataclass
class MusescoreDrumkit():
    percussionPanelColumns: int = None
    _Drums = []
    
    def to_lxml(self) -> etree._Element:
        
        root = etree.Element('museScore')
        root.set('version', musescore_version)
        
        # get elements (percussionPanelColumns)
        for name, value in self.__dict__.items():
            # skip private / callable stuff
            if value is None:
                continue
            
            if not name.startswith('_') and not callable(value) and not inspect.isroutine(value):
                child = etree.SubElement(root, name)
                child.text = str(value)
            
        for drum in self._Drums:
            child = drum.to_lxml()
            
            root.append(child)
        
        return root
    
    def to_file(self, output_filepath: str,
                incl_header=True,
                append_extension=True):
        if append_extension:
            if not output_filepath.endswith('.drm'):
                output_filepath = output_filepath + '.drm'
        
        root = self.to_lxml()
        et = etree.ElementTree(root)
        if incl_header:
            header = '<?xml version="1.0" encoding="UTF-8"?>\n'
            out_str = etree.tostring(root, pretty_print=True, encoding='unicode')
            with open(output_filepath, 'w') as out_file:
                out_file.write(header)
                out_file.write(out_str)
        else:
            et.write(output_filepath, pretty_print=True)

def sfz_class_to_drumkit_class(sfz_creator_obj: SfzCreator,
                               panelColumns: int = 8):
    # shorter alias
    sfz = sfz_creator_obj
    
    # get lists of lowkeys, hikeys and pitch keycentres
    lokeys = np.array([sample.Lokey for sample in sfz.Samples])
    hikeys = np.array([sample.Hikey for sample in sfz.Samples])
    pitch_keycentres = np.array([sample.Pkeycenter for sample in sfz.Samples])
    
    # list of drums
    drums = []
    
    # Getting filenames to identify common strings
    fnames = [sample.Fname for sample in sfz.Samples]
    
    # identitying which strings are in all filenames
    common_to_all = maximal_common_substrings(fnames)
    
    # removing common substrings
    # fnames_diff = fnames[:]  # copy
    fnames_diff = []
    for fname in fnames:
        for common_str in common_to_all:
            fname = fname.replace(common_str, '')
        fnames_diff.append(fname)
    
    
    # going through all midi notes and extracting which
    # ones have a sound in the SFZ
    idx_drum = 0
    for idx_midi_key in range(128):  # all 128 pitches, from 0 to 127
        samples_current_key = []
        
        idx_match_lokeys = idx_midi_key >= lokeys
        idx_match_hikeys = idx_midi_key <= hikeys
        idx_match_both = np.where(np.logical_and(
            idx_match_lokeys,
            idx_match_hikeys))[0]
        
        samples_match_lokey = [sfz.Samples[idx] for idx in idx_match_lokeys]
        samples_match_hikey = [sfz.Samples[idx] for idx in idx_match_hikeys]
        
        samples_match_both = [sfz.Samples[idx] for idx in idx_match_both]
        
        if len(samples_match_both) > 0:
            drum = Drum()
            
            drum._pitch = idx_midi_key
            
            drum_fnames = [fnames_diff[idx] for idx in idx_match_both]
            common_to_drum = maximal_common_substrings(drum_fnames)
            
            drum_name = ' '.join(common_to_drum).replace('_', ' ').strip()
            drum.name = drum_name
            
            drum.head = 'normal'  # hard-coded for now
            drum.line = 0  # hard-coded for now
            
            # this will be the horizontal position of the drum in the musescore Ui table selection
            drum.panelColumn = idx_drum%panelColumns  # mod, rest of division, to get the column
            
            # this will be the vertical position of the drum in the musescore Ui table selection
            drum.panelRow = idx_drum//panelColumns  # integer division to get the row
            
            drum.stem = 1  # hard-coded for now
            drum.voice = 0  # hard-coded for now
            
            drums.append(drum)
            
            idx_drum = idx_drum + 1
    
    musescore_drumkit = MusescoreDrumkit()
    musescore_drumkit.percussionPanelColumns = panelColumns
    musescore_drumkit._Drums = drums
    
    return musescore_drumkit

def sfz_to_musescore_drumkit_drm(sfz_fp: str, outfile: str = None, panelColumns=8):
    if outfile is None:
        outfile = sfz_fp.removesuffix('.sfz') + '.drm'
    
    sfz = SfzCreator()
    sfz.loadSfzFile(sfz_fp)
    drumkit = sfz_class_to_drumkit_class(sfz, panelColumns=panelColumns)
    drumkit.to_file(outfile)
    print(f'MuseScore Drumkit drm generated successfully, saved to {outfile}')


if __name__ == '__main__':  # tests - how to use
    # drum class examples
    dr = Drum()
    dr2 = Drum()
    
    dr._pitch = 50
    dr2._pitch = 60
    
    drm = MusescoreDrumkit()
    drm.percussionPanelColumns = 8

    drm._Drums = [dr, dr2]
    root = drm.to_lxml()
    print(etree.tostring(root, pretty_print=True, encoding='unicode'))
    
    
    # sfz class to drumkit class
    sfz = SfzCreator()
    sfz.loadSfzFile('my_sfz.sfz')
    musescore_drumkit = sfz_class_to_drumkit_class(sfz)
    
    # direct file conversion
    sfz_to_musescore_drumkit_drm('my_sfz.sfz', 'mu_drumkit.drm')
