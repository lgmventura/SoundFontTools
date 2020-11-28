#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script that uses the SFZ Creator Class to create an sfz from a folder containing samples

Created on Sat Nov 28 13:31:09 2020

@author: luiz
"""
from sfzCreatorClass import sfz_creator

# Test (delete all this after testing):
#fp = '/media/luiz/Volume/Downloads/SoundFonts/SteinwayD274/Samples/Bright'
fp = '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/PTQ_SteinwayD_H'

sfz1 = sfz_creator([], '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/Steinway_D_HB.sfz')

sfz1.VelMap = {'v1': 33, 'v2': 50, 'v3': 75, 'v4': 100, 'v5': 116, 'v6': 127}

#sfz1.getSamplesFromFolder(fp, pmidi = 'C(\d+)')
#sfz1.getSamplesFromFolder(fp, pitch = '_([A-G]#?\d)_', vel='_([a-z]+)_')
sfz1.getSamplesFromFolder(fp, pmidi = 'pitch(\d+)', vel='_(v\d)_')


sfz1.autoSpreadKeys('higher')

sfz1.autoSpreadVelocities('lower')

sfz1.setForAll('Ampeg_release', 1.0)

#sfz1.setForAll('Cutoff', 200)
sfz1.setForAllIf('Cutoff', 2000, 'Vel', '==', 33)
sfz1.setForAllIf('Cutoff', 1400, 'Vel', '==', 50)
sfz1.setForAllIf('Cutoff', 800, 'Vel', '==', 75)
sfz1.setForAllIf('Cutoff', 220, 'Vel', '==', 100)
sfz1.setForAllIf('Cutoff', 160, 'Vel', '==', 116)
sfz1.setForAllIf('Cutoff', 120, 'Vel', '==', 127)

sfz1.setForAllIf('Volume', 1, 'Vel', '==', 33)
sfz1.setForAllIf('Volume', 2, 'Vel', '==', 50)
sfz1.setForAllIf('Volume', 5, 'Vel', '==', 75)
sfz1.setForAllIf('Volume', 1, 'Vel', '==', 100)
sfz1.setForAllIf('Volume', 0, 'Vel', '==', 116)
sfz1.setForAllIf('Volume', -1, 'Vel', '==', 127)

sfz1.setForAllIf('Amp_veltrack', 94, 'Vel', '==', 33)
sfz1.setForAllIf('Amp_veltrack', 96, 'Vel', '==', 50)

sfz1.setForAll('Fil_veltrack', 8000)

sfz1.genSfz()
