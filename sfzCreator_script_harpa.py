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
fp = '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/PTQ_ConcertHarp'

sfz1 = sfz_creator([], '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/ConcertHarp1.sfz')
v1 = 40
v2 = 85
v3 = 127


sfz1.VelMap = {'v1':v1 , 'v2': v2, 'v3': v3}

#sfz1.getSamplesFromFolder(fp, pmidi = 'C(\d+)')
#sfz1.getSamplesFromFolder(fp, pitch = '_([A-G]#?\d)_', vel='_([a-z]+)_')
sfz1.getSamplesFromFolder(fp, pmidi = 'pitch(\d+)', vel='_(v\d)_')


sfz1.autoSpreadKeys('higher')

sfz1.autoSpreadVelocities('lower')

sfz1.setForAll('Ampeg_release', 1.0)

#sfz1.setForAll('Cutoff', 200)
sfz1.setForAllIf('Cutoff', 1200, 'Vel', '==', v1)
sfz1.setForAllIf('Cutoff', 400, 'Vel', '==', v2)
sfz1.setForAllIf('Cutoff', 100, 'Vel', '==', v3)

# sfz1.setForAllIf('Volume', 1, 'Vel', '==', v1)
# sfz1.setForAllIf('Volume', 2, 'Vel', '==', v2)
# sfz1.setForAllIf('Volume', 5, 'Vel', '==', v3)

sfz1.setForAllIf('Amp_veltrack', 94, 'Vel', '==', v1)
sfz1.setForAllIf('Amp_veltrack', 96, 'Vel', '==', v2)

sfz1.setForAll('Fil_veltrack', 8000)

sfz1.genSfz()
