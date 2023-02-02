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
fp = '/media/luiz/Volume/Downloads/SoundFonts/OrchideaSOL2020_release/OrchideaSOL2020/PluckedStrings/Guitar/ordinario'

sfz1 = sfz_creator([], '/media/luiz/Volume/Downloads/SoundFonts/OSOL Guitar rand (2).sfz')
v1 = 60
v2 = 99
v3 = 127


sfz1.VelMap = {'pp':v1 , 'mf': v2, 'ff': v3}

#sfz1.getSamplesFromFolder(fp, pmidi = 'C(\d+)')
#sfz1.getSamplesFromFolder(fp, pitch = '_([A-G]#?\d)_', vel='_([a-z]+)_')
sfz1.getSamplesFromFolder(fp, pitch = '-([A-G]#?\d)-', vel='-(pp|mf|ff)-')


sfz1.autoSpreadKeys('higher')

sfz1.autoSpreadVelocities('lower')

sfz1.setForAll('Ampeg_release', 0.8)

#sfz1.setForAll('Cutoff', 200)
sfz1.setForAllIf('Cutoff', 1800, 'Vel', '==', v1)
sfz1.setForAllIf('Cutoff', 600, 'Vel', '==', v2)
sfz1.setForAllIf('Cutoff', 200, 'Vel', '==', v3)

sfz1.setForAllIf('Volume', 10, 'Vel', '==', v1)
sfz1.setForAllIf('Volume', 4, 'Vel', '==', v2)
sfz1.setForAllIf('Volume', -2, 'Vel', '==', v3)

sfz1.setForAllIf('Amp_veltrack', 94, 'Vel', '==', v1)
sfz1.setForAllIf('Amp_veltrack', 96, 'Vel', '==', v2)

sfz1.setForAll('Fil_veltrack', 8000)

sfz1.genSfz()
