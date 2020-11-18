#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 17:52:54 2018

@author: Luiz Guilherme de M. Ventura
"""

import os
import glob
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]



p = input("Enter the path to the directory with the files: ")
#if p[-1] == '\"' or p[-1] == '\'':
#    p = p[:-1]
#    p = p + '/' + p[0] # insert a / if it is missing
#else:
#    p = p + '/'
p = p + '/'
p = p.replace('\'', '')
p = p.replace('\"','')
ext = input("Enter the file extension (like .wav) ")
listFiles = glob.glob(p + '*' + ext)

s = input("Enter the name prefix with a # where the numeration is: ")
l = input("How long is the number string? ")
n = input("How many files in total? ")
print("So, your files are in the form: {",)
for i in range(3):
    print(s.replace('#','%.{}d'.format(l) % (i+1)) + ext + ', ',)
print("}")
cfrm = input("Confirm? [y/n]: ")

listFiles.sort(key=natural_keys)

if cfrm == 'y':
    nt = input("first note [e.g. c#2]: ")
    nv = int(input("number of velocities: "))
    i = 1
    for file in listFiles:
        os.rename(file, p + str(nt) + s.replace('#', '') + str(i) + ext)
        print(file + ' -> ' + p + str(nt) + s.replace('#', '') + str(i) + ext)
        if i == nv:#int(nv):
            nt = input("next note [e.g. c#2]: ")
            nv = int(input("number of velocities: "))
            i = 1
        else:
            i += 1
