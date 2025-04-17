############################################################
##
## python 3 code for applied modern algebra (spring 2020)
## kimball martin
## 
##
## this is some helper code for some of the labs.  this code is not 
## necessarily meant to be the most efficient or elegant possible, but it 
## is meant to be easy to understand given what we did in class.  
## please notify me of any bugs/typos spotted.
##
## note: this code was modified from earlier python 2 code
## so may still have some python 2 idiosyncracies
############################################################


############################################################
##
## for lab 3
##
############################################################


############################################################
# apply Caesar shift by k to the string s as in lab 2
############################################################
def shift(s,k):
    s = s.upper()
    t = ''
    for x in s:
        if x.isalpha():
            j = (ord(x)-65+k)%26 + 65
            t = t + chr(j)
        else:
            t = t + x
    return t


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
# slice 1 string into n strings---if you write the string 
# across in n columns, each string is one column
# returns result as a list of strings
############################################################
def slice(s, n):
    cols = []
    for i in range(n):
       cols.append('')
    for i in range(len(s)):
        cols[i%n] = cols[i%n] + s[i]
    return cols
 

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
# count repeated bigrams in a string s
# optional argument minrep specifies the minimum number of times a bigram
# should occur before including it
############################################################
def bigrams(s, minrep=2):
    bigr = []                   # will be list of bigrams with frequencies
    counted = []                # will be list of bigrams already checked
    for i in range(len(s)-1):
        x = s[i]
        y = s[i+1]
        count = 1
        for j in range(i+1, len(s)-1):
            if s[j] == x and s[j+1] == y:
                count = count + 1
        if count >= minrep and x+y not in counted:
            bigr.append([x+y, count])
            counted.append(x+y)
    bigr = sorted(bigr, key = lambda x: x[1], reverse=True)
    return bigr


############################################################
# count repeated trigrams in a string s
# optional argument minrep specifies the minimum number of times a trigram
# should occur before including it
############################################################
def trigrams(s, minrep=2):
    trigr = []                  # will be list of trigrams with frequencies
    counted = []                # will be list of trigrams already checked
    for i in range(len(s)-2):
        x = s[i]
        y = s[i+1]
        z = s[i+2]
        count = 1
        for j in range(i+1, len(s)-2):
            if s[j] == x and s[j+1] == y and s[j+2] == z:
                count = count + 1
        if count >= minrep and x+y+z not in counted:
            trigr.append([x+y+z, count])
            counted.append(x+y+z)
    trigr = sorted(trigr, key = lambda x: x[1], reverse=True)    
    return trigr


############################################################
# this function lets you try making substitutions to
# a ciphertext C
# usage >>>subst('CIPHERTEXT', {'E':'a', 'X':'e'})
# optional parameter N sets number of characters per line to print
# default N = 60
############################################################
def subst(c, sub, N=60):
    C = c.upper()	# force ciphertext C to be uppercase
    t = '' 		# make a new string t that will be our substituted text
    for x in C:		# go through each character of ciphertext
        if x in sub:	# if x is in our substutition dictionary, make the sub
            t = t + sub[x]
        if x not in sub:	# otherwise just put a dash for unknown char
            if x.isupper():
                t = t + '-'
            else:	# but keep punctionation/spaces as is
                t = t + x
    nlines = len(C)//N + 1
    from sys import stdout
    for k in range(nlines):    # now print things out side by side
        for i in range(N):
            if k*N+i < len(C):
                stdout.write(C[k*N+i])
            else:
                stdout.write(' ')
        print('          ',)
        for i in range(N):
            if k*N+i < len(t):
                stdout.write(t[k*N+i])
        print('')


############################################################
# some strings for lab 3/homework 5
# C32 - ciphertext for book problem 4.9.32
############################################################

loremipsum = 'LOREMIPSUMDOLORSITAMETCONSECTETURADIPISCINGELITSEDDOEIUSMODTEMPORINCIDIDUNTUTLABOREETDOLOREMAGNAALIQUAUTENIMADMINIMVENIAMQUISNOSTRUDEXERCITATIONULLAMCOLABORISNISIUTALIQUIPEXEACOMMODOCONSEQUATDUISAUTEIRUREDOLORINREPREHENDERITINVOLUPTATEVELITESSECILLUMDOLOREEUFUGIATNULLAPARIATUREXCEPTEURSINTOCCAECATCUPIDATATNONPROIDENTSUNTINCULPAQUIOFFICIADESERUNTMOLLITANIMIDESTLABORUM'

C1 = 'HCTEPLQFYNETZYMCPLVNLPDLCDHSTNSZFEAFEDACTYEDZCCPEFCYDJZFCNSZTNPLWWAZDDTMWPDSTQEVPJDLYOLDDZNTLEPONLPDLCDSTQEDZQESPDECTYRDHSTNSLCPZCOPCPOQCZXXZDEWJWTVPWJPYRWTDSAWLTYEPIEEZWPLDEWTVPWJMJXLVTYRFDPZQJZFCEPDEDSTQEDQFYNETZYEPDEESTDQFYNETZYZYESPTYNWFOPONTASEPCEPIENHSTNSHLDPYNCJAEPOHTESLNLPDLCNTASPC'

C2 = 'HTSLSWRXCKACEKPTZWWERXCSDLSBNOXKMMCCCWLREREEJLKMLHTGLRIADLDWMXGDNSFKPWHIKAXXCGPJWDERXOFGBIVELSFKXGDNSFNTPTSWFDERXOFGPHYIAGJKWYQRSFMLMUMSLRIKPTAUCWMBEUGXWGSEJKDERXSLAMWRDBWSNMQIIFUDQYIHWEKXGRADKMMCCCWJKXFTRLZKRYQRSFMLMUMSLRIKPTAUCAFXLWEKRWHCAWXXGUIUAXZCHTAYKXGDNKEKOCJSWGPHYIAKLKXGHTAUCMQROFUOVLTDOADLRWEMKOSDSALSSRRWEUGXXCMTGXERATRLSSRRNAFVNIAXSAGXQYZIFYSRRWEXSMIMUUFUOVRPIFLIMLPPHDIMLVSLSDMQIIUKDSYERGTVIKXTAKMSKBOFHBEAIIUWDSQIAJLGMRWAHGZYJPTAGXSPERGUOWQIOTWCXSSIWVZSNJLSLSSLHCSFLIBXVWJCIRDPAUCWSRHSKKPJEEGHVIJXVAFQMLPCGMXXPNOJWFIPNALGWGMBPGKSREPCJQCXYAIVWKPJNSLSDMQIIUAKRQROEHSPCSALSKFMJTLZOILIIJWZSNJLSLSSLPNGHOVYIIGFMEJAEVUORQJSLZSWKPYTWYVEPNAROHZNGGNOVLBEFLKPQIALACXGRADAXWRXTMLOWBTSUJSTRXVWKDERXSLAMWAPNTWEWCSTGKEQKPRAROXFTPGHEPYIIGFNERPNMEOVGRADVOWAGIHLYVQXNUDEHCBESFKRBHTSFNEPSDWNSERXOFXYVADNLAXYMJSVSDERNPWKVMITIFUYQCLHADOJPTQMWXGWPNVHOVATNLSQIYGEEGBISHEXMVMLIEJECSDSEKUBMZXNYUKXCVOJAMEJSALSVMITEVMMERXOF'

C32 = 'LKZB RMLK X JFAKFDEQ AOBXOV TEFIB F MLKABOBA TBXH XKA TBXOV LSBO JXKV X NRXFKQ XKA ZROFLRP SLIRJB LC CLODLQQBK ILOB TEFIB F KLAABA KBXOIV KXMMFKD PRAABKIV QEBOB ZXJB X QXMMFKD XP LC PLJB LKB DBKQIV OXMMFKD OXMMFKD XQ JV ZEXJYBO ALLO Q FP PLJB SFPFQBO F JRQQBOBA QXMMFKD XQ JV ZEXJYBO ALLO LKIV QEFP XKA KLQEFKD JLOB'
