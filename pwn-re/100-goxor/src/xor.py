#!/usr/bin/python3

'''
Make the flag for goxor.
'''

import sys

flagFile = open("flag", "r").readline()

print ("challenge := []byte{", end='')

cnt = 0

length = len(flagFile)
for char in flagFile:
    print (ord(char) ^ 0x7f, end='')
    cnt +=1
    if cnt is not length:
        print (",", end='')

print ("}")
