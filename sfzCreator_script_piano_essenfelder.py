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
fp = '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/Essenfelder/kp_pedaloff'

sfz1 = sfz_creator([], '/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/Essenfelder_vertical.sfz')
v1 = 80
v2 = 108
v3 = 127
# v4 = 88
# v5 = 100
# v6 = 114
# v7 = 127


sfz1.VelMap = {'v2':v1 , 'v3': v2, 'v4': v3}#, 'v4': v4, 'v5': v5, 'v6': v6, 'v7': v7}

#sfz1.getSamplesFromFolder(fp, pmidi = 'C(\d+)')
#sfz1.getSamplesFromFolder(fp, pitch = '_([A-G]#?\d)_', vel='_([a-z]+)_')
sfz1.getSamplesFromFolder(fp, pmidi = 'pitch(\d+)', vel='_(v\d)', group=0)


sfz1.autoSpreadKeys('higher')

sfz1.autoSpreadVelocities('lower')

sfz1.setForAll('Ampeg_release', 0.4)

#sfz1.setForAll('Cutoff', 200)
sfz1.setForAllIf('Cutoff', 3000, 'Vel', '==', v1)
sfz1.setForAllIf('Cutoff', 1800, 'Vel', '==', v2)
sfz1.setForAllIf('Cutoff', 800, 'Vel', '==', v3)
# sfz1.setForAllIf('Cutoff', 180, 'Vel', '==', v4)
# sfz1.setForAllIf('Cutoff', 150, 'Vel', '==', v5)
# sfz1.setForAllIf('Cutoff', 120, 'Vel', '==', v6)
# sfz1.setForAllIf('Cutoff', 100, 'Vel', '==', v7)

sfz1.setForAllIf('Volume', 1, 'Vel', '==', v1)
sfz1.setForAllIf('Volume', 1, 'Vel', '==', v2)
sfz1.setForAllIf('Volume', 1, 'Vel', '==', v3)
# sfz1.setForAllIf('Volume', 1, 'Vel', '==', v4)
# sfz1.setForAllIf('Volume', 0, 'Vel', '==', v5)
# sfz1.setForAllIf('Volume', -1, 'Vel', '==', v6)
# sfz1.setForAllIf('Volume', -2, 'Vel', '==', v7)

# sfz1.setForAllIf('Amp_veltrack', 94, 'Vel', '==', v1)
# sfz1.setForAllIf('Amp_veltrack', 96, 'Vel', '==', v2)

sfz1.setForAll('Fil_veltrack', 8000)

sfz1.transpose(20)

#sfz1.genSfz()

# sfz2 with releases
from copy import copy
sfz2 = copy(sfz1)

fp_rel = r"/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/Essenfelder/releases"

sfz2.OutFile = r'/media/luiz/Volume/Dokumente/Musik/Projekte/SoundFonts/Essenfelder_vertical_rel.sfz'

sfz2.getSamplesFromFolder(fp_rel, pmidi = 'pitch(\d+)', group=1)
sfz2.autoSpreadKeys('higher', group=1)

sfz2.setForAll('Volume', -8, group=1)
sfz2.setForAll('Ampeg_release', 1.2, group=1)
sfz2.setForAll('Ampeg_start', 40, group=1)
sfz2.setForAll('Ampeg_attack', 0.3, group=1)
sfz2.setForAll('Trigger', 'release', group=1)

sfz2.setForAllRegexpFileName('Lorand', 0.000, 'rr1', group=1)
sfz2.setForAllRegexpFileName('Hirand', 0.500, 'rr1', group=1)
sfz2.setForAllRegexpFileName('Lorand', 0.500, 'rr2', group=1)
sfz2.setForAllRegexpFileName('Hirand', 1.000, 'rr2', group=1)

sfz2.transpose(20, group=1)

sfz2.genSfz()

# TODO: finish
