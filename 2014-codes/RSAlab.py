##################################################
##
## Python 2.7 Code for Applied Modern Algebra (Spring 2014)
## Lab 7 (RSA)
## Kimball Martin
## 
##
## Notes: This is sample code for some of the examples from
## class.  This code is not necessarily meant to be the most efficient
## or elegant possible, but in what I think is the simplest way to understand
## given what we did in class.  Please notify me of any bugs/typos spotted.
##

##################################################


# converts a string into an integer
# Note: I assume the intial character is not null (chr(0))
def strtoint(s):
   n = 0
   for x in s:
       n = n << 8
       n = n + ord(x)
   return n

# converts an integer into an string, inverse to strtoint
def inttostr(n):
   s = ''
   while n > 0:
       s = chr(n & 255) + s
       n = n >> 8 
   return s

# given an integer n, find the maximum length of strings
# we can work with mod n
def blocklen(n):
    m = 0
    n = n >> 8
    while n > 0:
        m = m + 1
        n = n >> 8
    return m

# my RSA public key
n = 2428830267196161313981L
e = 65537

# my message and digital signature
m = 'Kimball'
sig = 1594206331031372105728L
