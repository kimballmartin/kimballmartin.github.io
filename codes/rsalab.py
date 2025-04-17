##################################################
##
## python 3 code for applied modern algebra (spring 2020)
## lab 6 (rsa)
## kimball martin
## 
##
## note: this is helper code for lab 6. this code is not 
## necessarily meant to be the most efficient or elegant 
## possible, but in what I think is the simplest way to 
## understand given what we've done in class.  please 
##  notify me of any bugs/typos.
##
##################################################


# converts a string into an integer
# note: i assume the intial character is not null (chr(0))
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

# my rsa public key for task 2
n2 = 2428830267196161313981
e2 = 65537

# my message and digital signature for task 2
m2 = 'Kimball'
sig2 = 1594206331031372105728
