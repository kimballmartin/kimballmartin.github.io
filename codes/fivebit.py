############################################################
##
## python 3 code for applied modern algebra (spring 2020)
## kimball martin
## 
##
## this is some helper code for some of the lab 4.  this code is not 
## necessarily meant to be the most efficient or elegant possible, but it 
## is meant to be easy to understand given what we did in class.  
## please notify me of any bugs/typos spotted.
############################################################


############################################################
##
## for lab 4
##
############################################################

# our 5-bit encoding scheme -- letters A-Z correspond to number 0-25
# and 0-5 correspond to the numerical codes 26-31
code = [chr(65+i) for i in range(26)] + [str(i) for i in range(6)]

# given an alphabetic string s (or semi-numeric--digits 0-5 are also allowed)
# return the encoding as a string of bits
# if the string includes other characters, they will be ignored
def encode(s):
  bits = []
  for x in s:
    for i in range(32):
      if code[i] == x:
        for j in range(5):	# append the j-th "bit" of i for j < 5
          bits.append(((1 << j) & i) >> j) 
        break
  return bits

# given a list of bits as encoded with the encode function, 
# return the decoded string (i.e., do the inverse to encode)
def decode(bits):
  s = ''
  for i in range(len(bits)//5):
    num = 0		# this will be the numerical value for a 5-bit block
    for j in range(5):
      num += (1 << j)*bits[5*i+j]
    s += code[num]
  return s


############################################################
##
## some code from lab 3
##
############################################################


############################################################
# returns only the alphabetic part of a string
# i.e., strips spaces, punctuation, numbers, etc.
############################################################
def onlyalpha(s):
    t = ''
    for x in s:
        if x.isalpha():
            t = t + x
    return t


############################################################
# perform frequency count on string s
# return result as list of length 26 whose i-th element is
# the number of times the i-th letter appears
############################################################
def freq_count(s):
    su = s.upper()
    count = []
    for i in range(65,91):
        freq = 0
        for x in su:
            if x == chr(i):
                freq = freq+1
        count.append(freq)
    return count

############################################################
# compute frequency distribution for string s
# this is the the vector of frequency counts divided by 
# the length of the sring
############################################################
def freq_dist(s):
    freq = freq_count(s)
    c = 1/sum(freq)
    for i in range(len(freq)):
        freq[i] = freq[i]*c
    return freq


############################################################
# letters in the English alphabet
############################################################
# upper-case letters, e.g., Letter[1] = 'B'
Letter = [chr(i) for i in range(65,91)]

# lower-case letters, e.g., letter[1] = 'b'
letter = [chr(i) for i in range(97,123)]


############################################################
# frequencies of letters in English plaintext
############################################################

EF = [.08167, .01492, .02782, .04253, .12702, .02228, .02015, .06094, .06966, \
.00153, .00772, .04025, .02406, .06749, .07507, .01929, .00095, .05987, \
.06327, .09056, .02758, .00978, .02360, .00150, .01974, .00074 ]

############################################################
# sample text for encryption, taken from
# https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology
############################################################

text = 'THENATIONALINSTITUTEOFSTANDARDSANDTECHNOLOGYNISTISAPHYSICALSCIENCESLABORATORYANDANONREGULATORYAGENCYOFTHEUNITEDSTATESDEPARTMENTOFCOMMERCEITSMISSIONISTOPROMOTEINNOVATIONANDINDUSTRIALCOMPETITIVENESSNISTSACTIVITIESAREORGANIZEDINTOLABORATORYPROGRAMSTHATINCLUDENANOSCALESCIENCEANDTECHNOLOGYENGINEERINGINFORMATIONTECHNOLOGYNEUTRONRESEARCHMATERIALMEASUREMENTANDPHYSICALMEASUREMENTITWASFORMERLYKNOWNASTHENATIONALBUREAUOFSTANDARDS'
