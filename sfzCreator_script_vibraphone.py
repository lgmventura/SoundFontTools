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
fp = '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/University of Iowa/Percussion/Vibraphone/sus'

sfz1 = sfz_creator([], '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/Uniowa Vibraphone.sfz')
#v1 = 40 # the pp samples have too much noise
v2 = 85
v3 = 127


sfz1.VelMap = {'v2': v2, 'v3': v3}

#sfz1.getSamplesFromFolder(fp, pmidi = 'C(\d+)')
#sfz1.getSamplesFromFolder(fp, pitch = '_([A-G]#?\d)_', vel='_([a-z]+)_')
sfz1.getSamplesFromFolder(fp, pmidi = 'p(\d+)', vel='_(v\d)')


sfz1.autoSpreadKeys('higher')

sfz1.autoSpreadVelocities('lower')

sfz1.setForAll('Ampeg_release', 1.0)

#sfz1.setForAll('Cutoff', 200)
sfz1.setForAllIf('Cutoff', 700, 'Vel', '==', v2)
sfz1.setForAllIf('Cutoff', 200, 'Vel', '==', v3)

# sfz1.setForAllIf('Volume', 1, 'Vel', '==', v1)
# sfz1.setForAllIf('Volume', 2, 'Vel', '==', v2)
# sfz1.setForAllIf('Volume', 5, 'Vel', '==', v3)

#sfz1.setForAllIf('Amp_veltrack', 94, 'Vel', '==', v1)
sfz1.setForAllIf('Amp_veltrack', 96, 'Vel', '==', v2)

sfz1.setForAll('Fil_veltrack', 8000)

sfz1.genSfz()
