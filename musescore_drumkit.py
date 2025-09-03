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

def sfz_class_to_drumkit_class():
    pass

def sfz_to_musescore_drumkit_drm(sfz_fp: str, outfile: str = None):
    sfz_class_to_drumkit_class()


if __name__ == '__main__':
    # testing
    dr = Drum()
    dr2 = Drum()
    
    dr._pitch = 50
    dr2._pitch = 60
    
    drm = MusescoreDrumkit()
    drm.percussionPanelColumns = 8

    drm._Drums = [dr, dr2]
    root = drm.to_lxml()
    print(etree.tostring(root, pretty_print=True, encoding='unicode'))