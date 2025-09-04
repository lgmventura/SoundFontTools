#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu, 4 Sep 2025 21:04:00

@author: luiz
"""

from sfzCreatorClass import SfzCreator, Sample
from os import path

sfz_path = '/home/luiz/Documents/InstrumentosVirtuais/VSCO 1 Percussion/VSCO1 - suspended cymbal.sfz'
dirname, filename = path.split(sfz_path)

sfz = SfzCreator()
sfz.loadSfzFile(sfz_path)
sfz.setVolumeToNormalize(0.9)
sfz.OutFile = sfz_path.replace('.sfz', '_normalized.sfz')
sfz.genSfz()