#!/usr/bin/env python3
#
# Helper for keys
# Copyright (C) 2022 Phil Champagne, bookofsatoshi.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#
# This allows the creation of a mnemonic based on the BIP39 dictionary
# from any arbitrary words. It should be used with caution. 
# A minimum of 12 words should be provided, but more can be supplied.
# For example, you could use all the words from a paragraph of a book 
# (minus punctuation) to which you could add a specific word of you choice.
# Anything goes and go as wild as you can.
# The purpose is for you to have the ability to recreate your wallet entirely 
# from memory using a set of words you could get from a known source or 
# from a set you are familiar with. However, it is recommended you take 
# note of the mnemonic generated using the BIP39 dictionary as another
# backup. 
#

import os
import sys
import hashlib
import base64
import binascii

numargs = len(sys.argv)
cmdargs = str(sys.argv)

if numargs < 12:
    print("Missing arguments. Need at least 12 words, but more is better")
    print("You must provide at least 12 words")
    sys.exit(1)

words = ""
i = 1

while True:
    words += str(sys.argv[i])
    i += 1
    if i >= numargs:
        break;
    words += " "

print("words supplied: %s" % (words))


hash_obj = hashlib.sha256(str(words).encode('utf-8'))
seed1 = hash_obj.hexdigest()

print("seed=")
print(str(seed1))

seedstr = str(seed1).strip()
data = binascii.unhexlify(seedstr)

h = hashlib.sha256(data).hexdigest()
b = bin(int(binascii.hexlify(data),16))[2:].zfill(len(data)*8) + \
    bin(int(h,16))[2:].zfill(256)[: len(data)* 8//32]

with open("wordlist/english.txt", "r") as f:
    wordlist = [w.strip() for w in f.readlines()]


dseedwords = ""
seedwords = []
perline = 0
counter = 1
for i in range(len(b)//11):
    indx = int(b[11*i:11*(i+1)],2)
    seedwords.append(wordlist[indx])
    dseedwords += str(counter) + ". " + wordlist[indx]
    counter += 1
    perline += 1
    if(counter <= 24):
        if(perline >= 4):
            dseedwords += "\n"
            perline = 0
        else:
            dseedwords += "  "

print("===========================")
print("========= RESULT ==========")
print("===========================")
print("seed used:")
print(seed1)
print("Orginal phrase used was: ")
print(words)
print("===========================")
print("===========================")
print("mnemonic words to use to generate your wallet:")
print("---")
print(dseedwords)
print("---")
print("===========================")
