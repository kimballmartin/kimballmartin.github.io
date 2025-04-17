# Date: 2/09/09
# MATH 4383/5383: Simple coding theory routines for Python 2.x
# Author: Kimball Martin
#
# Usage: The "offically recommended" way to use this is to save this file in
# your working directory and call each function by preceeding each function
# name with "ecc."  E.g., if you want to use the corruptbmp function, call it
# by ecc.corruptbmp(...).  See the section on modules in python documentation.
# (The unrecommended way would be to cut and paste, in which case you don't
# need the "ecc." in front.)
#
# Please notify me of any bugs you may find and I will fix it as soon as
# possible (or if you fix it yourself please send me the fix).
#
# In what follows, c will be a character (string of length 1 byte).  In the
# computer, c is represented by a binary string of length 8, and we may speak
# of the p-th bit of c, where 0 <= p <= 7.
#
# Note: for reading from and writing to files, our data will be given in
# the form of strings (type str).  However, we will want to work with our data
# on the bit level (using what are called bitwise operators), for which
# we will need to convert characters/strings into integers/longs.  Note that
# a long integer can be any length in python.  You can convert from a 
# character (string of length 1) to an integer with ord() and back again with
# chr().  My functions strtolong() and longtostr() below convert between
# strings and long integers.  

# Load some modules we will need
import random
import sys

# For a character c, returns the p-th bit 
# Here p should be an integer between 0 and 7
def pthbit(c,p):
   n = ord(c)			# converts c to integer type
   return (n >> (7-p)) & 1

# This takes a character c and prints the binary representation for c
def binrep(c): 
   for p in range(8):		# for p from 0 to 7 do the following
      sys.stdout.write(str(pthbit(c,p)))   # print without leaving space	

# This returns the Hamming weight of the binary representation for a
# character c
def weight(c):
   w = 0
   for p in range(8):
      w = w + pthbit(c,p)
   return w

# Takes the bits of string s and returns it as a long integer (of arbitrary 
# length) l
def strtolong(s):
   l = long(0)
   for c in s:
      l = l << 8
      l = l + ord(c)
   return l

# The inverse of strtolong--input a long integer l and the number of bits n
# the string should be (a multiple of 8) and get out the string.  
# Very different from str(l,n)
def longtostr(l,n):
   s = ''
   m = n-8
   x = long(255) << m			# let x be all 1's in the highest
   while m >= 0:			# order byte
      s = s + chr((l & x) >> m)		# AND it with l to get the first char.
      x = x >> 8			# shift x to the next byte
      m = m - 8				# and repeat to the end
   return s

# Returns how many bits are in a string s
def numbits(s):
   return 8*len(s)

# This returns (as a character) one random byte of noise for a binary symmetric 
# channel with a probability of error of P (between 0 and 1) per bit
def charnoise(P):
   e = 0			# the error byte, as an integer, initally 0
   for p in range(8):
      if random.random() < P:	# with probability P
         e = e + (1 << p)	# make the p-th bit of e into a 1
   return chr(e)		# return the error byte e as a character

# Adds noise to a string s assuming a binary symmetric channel with bit error
# probablility P
def addbscnoise(s, P):
   b = numbits(s)		# b = number of bits in s
   l = strtolong(s)		# change string to long to to bit operations
   e = long(0)			# e error bit
   for i in range(0,b):		# for each bit
      if random.random() < P:
         e = long(1 << i)
         l = l ^ e		# add noise
   return longtostr(l,b)	# return noisy data as string

# Reads a bitmap file named fname, skips the header, adds noise according to the
# Binary Symmetric Channel with probability P, and outputs it as 'out.bmp'
def corruptbmp(inname,outname,P):
   f = open(inname,'rb')		# make the input file read-only
   g = open(outname,'wb')		# make the output file writeable
   s = f.read(55)			# read the 55-byte header
   g.write(s)				# write the header
   s = f.read()				# read the rest of the data
   t = addbscnoise(s, P)		# add noise to it
   g.write(t)				# write it out
   g.close()				# close the files
   f.close()
