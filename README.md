# YSFHasher
Adds characters to YSF Reflector names to create a specific hash

This Python program accepts a proposed YSF Reflector name and a desired YSF Reflector number. It fiddles with the last four
character positions to find a hash of the name that produces the desired number. The program is currently set to only use
capital alpha characters, but this can be changed.

There is some small probablility that a hash won't be found. In that case make a modification to the reflector name.

The program will run either from the command line or as cgi-bin.
