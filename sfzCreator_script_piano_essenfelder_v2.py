#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script that uses the SFZ Creator Class to create an sfz from a folder containing samples

Created on 28/03/2024

I sampled the Essenfelder vertical piano again with professional microphones
closer to the strings. New samples were recorded too. The only problem is
that the piano is not very well tuned, but this also gives some charm.
The other only problem is that sometimes the v1 is as forte (or piano) as
v2. So the first only problem is not alone ;).

@author: luiz
"""
from sfzCreatorClass import sfz_creator

# Test (delete all this after testing):
#fp = '/media/luiz/Volume/Downloads/SoundFonts/SteinwayD274/Samples/Bright'
fp = '/media/luiz/HDp1/Gravações/SF/Essenfelder_v2/pedal_off'

sfz1 = sfz_creator([], '/media/luiz/HDp1/Gravações/SF/Essenfelder_v2/Essenfelder_vertical_v2.sfz')
v1 = 64
v2 = 80
v3 = 108
v4 = 127
# v5 = 100
# v6 = 114
# v7 = 127


sfz1.VelMap = {'v1':v1 , 'v2': v2, 'v3': v3, 'v4': v4}#, 'v5': v5, 'v6': v6, 'v7': v7}

#sfz1.getSamplesFromFolder(fp, pmidi = 'C(\d+)')
#sfz1.getSamplesFromFolder(fp, pitch = '_([A-G]#?\d)_', vel='_([a-z]+)_')
sfz1.getSamplesFromFolder(fp, pmidi = 'pitch(\d+)', vel='-(v\d)', group=0)


sfz1.autoSpreadKeys('higher')

sfz1.autoSpreadVelocities('lower')

sfz1.changeLoVelIfVels(newLovel=1, ifHivel=64, ifLovel=65)  # do the bugfix after autospreadVels because of multiple rr samples in the same region

# this below works now, but then the region v2 will be problematic, starting from 1
# sfz1.setGroupRegexpFileName('rr1', newGroup=1)
# sfz1.setGroupRegexpFileName('rr2', newGroup=2)

# sfz1.autoSpreadVelocities('lower', group=0)
# sfz1.autoSpreadVelocities('lower', group=1)
# sfz1.autoSpreadVelocities('lower', group=2)
# sfz1.changeGroup(1, newGroup=0)
# sfz1.changeGroup(2, newGroup=0)

sfz1.setForAll('Ampeg_release', 0.4)

#sfz1.setForAll('Cutoff', 200)
sfz1.setForAllIf('Cutoff', 3000, 'Vel', '==', v2)
sfz1.setForAllIf('Cutoff', 1800, 'Vel', '==', v3)
sfz1.setForAllIf('Cutoff', 800, 'Vel', '==', v4)
# sfz1.setForAllIf('Cutoff', 180, 'Vel', '==', v4)
# sfz1.setForAllIf('Cutoff', 150, 'Vel', '==', v5)
# sfz1.setForAllIf('Cutoff', 120, 'Vel', '==', v6)
# sfz1.setForAllIf('Cutoff', 100, 'Vel', '==', v7)

# sfz1.setForAllIf('Volume', 1, 'Vel', '==', v1)
# sfz1.setForAllIf('Volume', 1, 'Vel', '==', v2)
# sfz1.setForAllIf('Volume', 1, 'Vel', '==', v3)
# sfz1.setForAllIf('Volume', 1, 'Vel', '==', v4)
# sfz1.setForAllIf('Volume', 0, 'Vel', '==', v5)
# sfz1.setForAllIf('Volume', -1, 'Vel', '==', v6)
# sfz1.setForAllIf('Volume', -2, 'Vel', '==', v7)

sfz1.setVolumeToNormalize(group=0)

# Increase the volume for lower samples
sfz1.operateOnAll('Volume', -2, '+')
sfz1.operateOnAllRegexpFileName("Volume", 8, "+", 'pitch(?:01|02)')
sfz1.operateOnAllRegexpFileName("Volume", 7, "+", 'pitch(?:03|04)')
sfz1.operateOnAllRegexpFileName("Volume", 6, "+", 'pitch(?:05|06)')
sfz1.operateOnAllRegexpFileName("Volume", 4, "+", 'pitch(?:07|08|09)')
sfz1.operateOnAllRegexpFileName("Volume", 2, "+", 'pitch1[0-6]')
sfz1.operateOnAllRegexpFileName("Volume", 1, "+", '(?:pitch1[7-9]|pitch2[0-6])')

# sfz1.setForAllIf('Amp_veltrack', 94, 'Vel', '==', v1)
# sfz1.setForAllIf('Amp_veltrack', 96, 'Vel', '==', v2)

sfz1.setForAll('Fil_veltrack', 8000)

sfz1.transpose(20)

sfz1.setForAllRegexpFileName('Lorand', 0.000, 'rr1', group=0)
sfz1.setForAllRegexpFileName('Hirand', 0.500, 'rr1', group=0)
sfz1.setForAllRegexpFileName('Lorand', 0.500, 'rr2', group=0)
sfz1.setForAllRegexpFileName('Hirand', 1.000, 'rr2', group=0)


# Now, internal reverb from the piano, which remains
fp_internal_reverb = '/media/luiz/HDp1/Gravações/SF/Essenfelder_v2/staccato_internal_reverb'
sfz1.getSamplesFromFolder(fp_internal_reverb, pmidi = 'pitch(\d+)', group=2)

# spread keys from group 1 (which contains the release samples)
sfz1.autoSpreadKeys('higher', group=2)

# set other opcodes for this group
sfz1.setForAll('Volume', 8, group=2)
sfz1.setForAll('Ampeg_release', 12.0, group=2)
sfz1.setForAll('Offset', 8000, group=2)
sfz1.setForAll('Ampeg_attack', 0.6, group=2)

sfz1.transpose(20, group=2)


#sfz1.genSfz()

# sfz2 with releases
from copy import copy
sfz2 = copy(sfz1)

fp_rel = r"/media/luiz/HDp1/Gravações/SF/Essenfelder_v2/release"

sfz2.OutFile = r'/media/luiz/HDp1/Gravações/SF/Essenfelder_v2/Essenfelder_vertical_rel_v2.sfz'

# import release samples and set them to group 1
sfz2.getSamplesFromFolder(fp_rel, pmidi = 'pitch(\d+)', group=1)

# spread keys from group 1 (which contains the release samples)
sfz2.autoSpreadKeys('higher', group=1)

# set other opcodes for this group
# sfz2.setForAll('Volume', -8, group=1)
sfz2.setForAll('Volume', -2, group=1)
sfz2.setForAll('Ampeg_release', 1.2, group=1)
sfz2.setForAll('Ampeg_start', 40, group=1)
sfz2.setForAll('Ampeg_attack', 0.3, group=1)
sfz2.setForAll('Trigger', 'release', group=1)

# increase the volume to the lower key samples
# sfz2.setForAllRegexpFileName('Volume', 2, 'pitch(?:01|02|03|04)', group=1)
# sfz2.setForAllRegexpFileName('Volume', 1, 'pitch(?:05|06|07|08)', group=1)
# sfz2.setForAllRegexpFileName('Volume', 0, 'pitch(?:09|10|11)', group=1)
# sfz2.setForAllRegexpFileName('Volume', -1, 'pitch1[2-3]', group=1)
# sfz2.setForAllRegexpFileName('Volume', -2, 'pitch1[4-5]', group=1)
# sfz2.setForAllRegexpFileName('Volume', -3, 'pitch1[6-7]', group=1)
# sfz2.setForAllRegexpFileName('Volume', -4, 'pitch1[8-9]', group=1)
# sfz2.setForAllRegexpFileName('Volume', -5, 'pitch20', group=1)
# sfz2.setForAllRegexpFileName('Volume', -6, 'pitch2[1-2]', group=1)
# sfz2.setForAllRegexpFileName('Volume', -7, 'pitch2[3-6]', group=1)

sfz2.setForAllRegexpFileName('Lorand', 0.000, 'rr1', group=1)
sfz2.setForAllRegexpFileName('Hirand', 0.500, 'rr1', group=1)
sfz2.setForAllRegexpFileName('Lorand', 0.500, 'rr2', group=1)
sfz2.setForAllRegexpFileName('Hirand', 1.000, 'rr2', group=1)

sfz2.transpose(20, group=1)

sfz2.genSfz()

# TODO: finish
