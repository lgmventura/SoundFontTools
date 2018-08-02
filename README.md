# SoundFontTools

This software is free and OpenSource. Distributed under GNU public license.

What is this?

Until now, just a simple Python code to rename intruments' sample files to the form loaded by Sfzed for creating regions automatically. Sfzed.exe is a Windows free tool to create and edit SFZ files.
E.g.:
c1_vel1.wav, c1_vel2.wav, c1_vel3.wav, c#1_vel1.wav, c#1_vel2.wav, c#1_vel3.wav, ...
The current version 0.2 should be executed on the terminal without any argument. It will ask for the folder, name radical (prefix, in the example above, _vel. In this case, you should enter #_vel) and file extension. The program tries to recognize pitch, but not velocity yet. The pitch recognition is still not working so well, especially if the sample is short, so it asks you for confirmation. It still can be a lot improved, is though much faster than renaming files manually. ;)

I intend to extend this repository with new useful tools to create SFZ, SF2, Sf3 SoundFonts.
