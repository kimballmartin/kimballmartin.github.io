##################################################
##
## For Lab 9
##
##################################################

# Hamming matrix
H = [ [1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1] ]

# Generator matrix
G = [ [1, 1, 1, 0, 0, 0, 0], [1, 0, 0, 1, 1, 0, 0], [0, 1, 0, 1, 0, 1, 0],
[1, 1, 0, 1, 0, 0, 1] ]

# Decoding matrix
R = [ [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0,0, 1, 0], [0, 0, 0, 1] ]

# test string (from Hamming's "You and your research" talk)
s = '''One of the characteristics of successful scientists is having courage. Once you get your courage up and believe that you can do important problems, then you can. If you think you can't, almost surely you are not going to. Courage is one of the things that Shannon had supremely. You have only to think of his major theorem. He wants to create a method of coding, but he doesn't know what to do so he makes a random code. Then he is stuck. And then he asks the impossible question, "What would the average random code do?" He then proves that the average code is arbitrarily good, and that therefore there must be at least one good code. Who but a man of infinite courage could have dared to think those thoughts? That is the characteristic of great scientists; they have courage. They will go forward under incredible circumstances; they think and continue to think.'''

# transpose a matrix
def transpose(A):
    B = []
    m = len(A)  # number of rows
    n = len(A[0])   # number of columns
    for j in range(n):
        rowj = []
        for i in range(m):
            rowj.append(A[i][j])
        B.append(rowj)
    return B

# matrix multiplication mod p (regular multiplication if n = 0)
def matmult(A, B, p = 0):
    C = []
    m = len(A) # number of rows
    n = len(B[0]) # number of columns
    l = len(B)
    if l != len(A[0]):
        return "Matrix sizes not compatible"
    for i in range(m):
        rowi = []
        for j in range(n):
            sum = 0
            for k in range(l):
                sum = sum + A[i][k]*B[k][j]
            if p != 0:
                sum = sum % p
            rowi.append(sum)
        C.append(rowi)
    return C

onverts a string into k-bit blocks
# if the string is not exactly divisible into k-bit blocks, return error
# (one could add padding and "parity check" to avoid this, but I'm being lazy)
def strtobits(s,k):
    bits = []
    if len(s)*8 % k != 0:
        return "String cannot be divided perfectly.  Please add dummy characters."
    for c in s:
        x = ord(c)
        for i in range(8):
            bits.append((x >> (7-i)) %2)
    blocks = []
    for i in xrange(len(bits)/k):
        block = bits[k*i:k*i+k]
        blocks.append(block)
    return blocks

# converts a list of bit blocks back into a string
def bitstostr(blocks):
    s = ''
    i, x = 0, 0
    for block in blocks:
        for bit in block:
            x = x + (bit << (7-i))
            i = i + 1
            if i % 8 == 0:
                s = s + chr(x)
                i, x = 0, 0
    return s

# apply noise to blocks with uniform error probability p
def noise(blocks, p):
    from random import random
    k = len(blocks[0])
    newblocks = []
    for i in xrange(len(blocks)):
        block = []
        for j in xrange(k):
            if random() < p:
                block.append((blocks[i][j] + 1) % 2)
            else:
                block.append(blocks[i][j])
        newblocks.append(block)
    return newblocks
