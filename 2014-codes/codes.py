##################################################
##
## Python 2.7 Code for Applied Modern Algebra (Spring 2014)
## Kimball Martin
## 
##
## Notes: This is sample code for some of the examples from
## class.  This code is not necessarily meant to be the most efficient
## or elegant possible, but in what I think is the simplest way to understand
## given what we did in class.  Please notify me of any bugs/typos spotted.
##

##################################################


##################################################
##
## From Section 3.2
##
##################################################

def gcd(a,b,verb=False):
    c = max(a,b)
    d = min(a,b)
    if d == 0:
        return c
    if verb:
        print c, d
    while c%d != 0:
        c, d = d, c%d
	if verb:
            print c, d
    return d

##################################################
##
## From Lab 3
##
##################################################

def shift(s,k):
    s = s.upper()
    t = ''
    for x in s:
        j = (ord(x)-65+k)%26 + 65
        t = t + chr(j)
    return t


##################################################
##
## From Lab 4
##
##################################################

#####################
# returns only the alphabetic part of a string
# i.e., strips spaces, punctuation, numbers, etc.

def onlyalpha(s):
    t = ''
    for x in s:
        if x.isalpha():
            t = t + x
    return t


#####################
# slice 1 string into n string---if you write the string across in
# n columns, each string is one columns
# returns result as a list of strings

def slice(s, n):
    cols = []
    for i in range(n):
       cols.append('')
    for i in range(len(s)):
        cols[i%n] = cols[i%n] + s[i]
    return cols
 

#####################
# count number of letter coincidences of s with displacements of s
# by lengths up to N.  a high number of coincidences for Vigenere
# ciphertext indicates that length is the key length

def vig_keylength(s, N):
    coins = []
    for d in range(1,N+1):
        count = 0
        for i in range(len(s)-d):
            if s[i] == s[i+d]:
                count = count+1
        coins.append(count)
    for d in range(1,N+1):
        print d, "    ", coins[d-1]

#####################
# perform frequency count on string s

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

#####################
# compute frequency distribution for string s
# this is the the vector of frequency counts divided by total number of letters

def freq_dist(s):
    freq = freq_count(s)
    c = 1.0/sum(freq)
    for i in range(len(freq)):
        freq[i] = freq[i]*c
    return freq


#####################
# given a frequency count or distribution list, augment it with the letters
# A - Z.  if optional parameter sort is set to True, sort by frequency

def aug_freq(freq, sort = False):
    afreq = []
    for i in range(65,91):
        afreq.append([chr(i), freq[i-65]])
    if sort:
        afreq = sorted(afreq, key = lambda af: af[1], reverse=True)
    return afreq


#####################
# frequencies of letters in English plaintext

EF = [.08167, .01492, .02782, .04253, .12702, .02228, .02015, .06094, .06966, \
.00153, .00772, .04025, .02406, .06749, .07507, .01929, .00095, .05987, \
.06327, .09056, .02758, .00978, .02360, .00150, .01974, .00074 ]

#####################
# compute the dot product of 2 vectors (lists) v1 and v2
def dot(v1, v2):
    y = 0
    for i in range(len(v1)):
        y = y + v1[i]*v2[i]
    return y


#####################
# this function lets you try making substitutions to
# a ciphertext C
# usage >>>trysub('CIPHERTEXT', ['E=a', 'X=e'])
# optional parameter N sets number of characters per line to print

def trysub(c, subs, N=15):
    C = c.upper()	# force ciphertext C to be uppercase
    subl = []   	# this code turns the inputted substitution list into 
    for x in subs:
        subl.append((x[0], x[2]))
    subd = dict(subl)   # ... a Python dictionary
    t = '' 		# make a new string t that will be our substituted text
    for x in C:		# go through each character of ciphertext
        if x in subd:	# if x is in our substutition dictionary, make the sub
            t = t + subd[x]
        if x not in subd:	# otherwise just put a dash for unknown char
            if x.isupper():
                t = t + '-'
            else:	# but keep punctionation/spaces as is
                t = t + x
    nlines = len(C)/N + 1
    from sys import stdout
    for k in range(nlines):    # now print things out side by side
        for i in range(N):
            if k*N+i < len(C):
                stdout.write(C[k*N+i])
            else:
                stdout.write(' ')
        print '          ',
        for i in range(N):
            if k*N+i < len(t):
                stdout.write(t[k*N+i])
        print ''


#####################
# perform a random substitution cipher on a plaintext p

def randsub(p):
    s = p.upper()
    alpha = []
    perm = []
    for i in range(65,91):
        alpha.append(chr(i))
        perm.append(chr(i))
    from random import shuffle
    shuffle(perm)
    sub = []
    for i in range(26):
        sub.append((alpha[i], perm[i]))
    subd = dict(sub)
    t = ''
    for x in s:		# go through each character of ciphertext
        if x.isupper():	# if x is in our substutition dictionary, make the sub
            t = t + subd[x]
        else:
            t = t + x
    return t


#####################
# count repeated digrams in a string s
# optional argument minrep specifies the minimum number of times a digram
# should occur before including it

def digrams(s, minrep=2):
    digr = []                   # will be list of digrams with frequencies
    counted = []                # will be list of digrams already checked
    for i in range(len(s)-1):
        x = s[i]
        y = s[i+1]
        count = 1
        for j in range(i+1, len(s)-1):
            if s[j] == x and s[j+1] == y:
                count = count + 1
        if count >= minrep and x+y not in counted:
            digr.append([x+y, count])
            counted.append(x+y)
    digr = sorted(digr, key = lambda x: x[1], reverse=True)
    return digr

#####################
# count repeated trigrams in a string s
# optional argument minrep specifies the minimum number of times a trigram
# should occur before including it

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

C0a = 'UBPUELQADNTGEOVSKCSMILZQSFHYVTMWUCDEDSOUEMABEYEAQSQNSISSQYCEFCUMZJMARXFPQAWBPWQHRZLPXGXWSVQZDNTSZGLMNEXZHXELQTLLDXEMCSRCYCGOWIATPUCIXOWCZRNSWQPIZUHHPVMHRLDSRHKYQMDGWMJDKUBGZHGZHCDGMZOYOEESFIYHEMCSRCATPUYHFVHMPXATDFWWGQKLPPMHLIYWUGFUWPQRWBPWQQRHOWKNBAJQARXFPSRAFIYXUBXCYKUBWBTWIOBQPHQFLPPXTSQNSWKNBAJQARXFPSRAESEEWWQAELQGHNZJMZOLPPMHLIYWNSWQPIZUHHPVMHRLDSRHKMJDKUBGZHGZHIQQUTPCDJUBLNPPKUHHPVMHHXZZQFDJZPKBRGTEXFLHRSHSUUQMQZGNSMEDUINIEGWYCQUBDNPWMTWYCERWQCEIZIPVPVATVNPTEWHYGIZHXUWPKHKYCIIWOFMIZCPICIEMCSRMQGVYPLUZEYCXEGBTJKKHKYZVQAWBPWKNBAJQARXFPWATPUCIZCWOYMCIHZZVFVHSOIBSQXZRFVHWSSUQHIQKQBHLLXAFVUEIMQKMEIB'

C0b = 'MYTGRBSFBAONAGYTOLOGRBSFBAOJCPBOTAJBUBKPBRJSUUTMOANTKNOSGMALKMTNYKACPTBKZIBJMYTFAOJMRAMTOBRZAQOBGYJPXJMAMPMALKNAGYTOMYTJNYTUTIBJAKVTKMTZXSNYBORTJIYTBMJMLKTXPMXTBOJMYTKBUTLFRLOZGRBSFBAOIYLGOLULMTZMYTPJTLFMYTNAGYTOMYTMTNYKACPTTKNOSGMJGBAOJLFRTMMTOJZAQOBGYJAKJMTBZLFJAKQRTRTMMTOJBJAKMYTJAUGRTJPXJMAMPMALKNAGYTOBKZOBMYTOULOTNLUGRTDVAQTKTOTNAGYTOJSJMTUJMYTKAKPJTMYTGRBSFBAOAJMYPJJAQKAFANBKMRSYBOZTOMLXOTBWJAKNTMYTFOTCPTKNSBKBRSJAJPJTZFLOJAUGRTJPXJMAMPMALKNAGYTOJZLTJKLMILOWIAMYAMFOTCPTKNSBKBRSJAJNBKJMARRXTPKZTOMBWTKXPMLKMYTJADYPKZOTZGLJJAXRTZAQOBGYJOBMYTOMYBKMYTMITKMSJADGLJJAXRTULKLQOBGYJMYTFOTCPTKNSBKBRSJAJLFZAQOBGYJAJGLJJAXRTXPMNLKJAZTOBXRSULOTZAFFANPRMBKZAMQTKTOBRRSOTCPAOTJBUPNYRBOQTONAGYTOMTDMAKLOZTOMLXTPJTFPR'

C1 = 'GCBRIFXVQRSCOXSFVERIJTBRIUDECKGQWXKSCLDLWBWXOWNAKPDHIIFGDBRIJTAKRGCOXEFVVSRYLPOVWIPOXJTMCKGEQXKSCLDLWIMKTGIATMTQMBNSQJOVBDWYRLWMXSFVVSRYCIXKSATDLWBQMIYDKVEFVIXHQDCTYKIKKRLRIDGZTUGLWCBRIQSWCSAIAXMFVVKRYCWXKUDECKGQWXKFDVQRSCOXMFVBBIWHOYTACOXSFVVSRYCIXKLWMWMUTOYGDPVQAZPBKRGXAITDPKOXGQMVSFVQCXZTVSRYCIXKFXVQRSCOXSFV'

C2 = 'RBDRYRXDNJPRKAKRBJPIEXKYPVOYFOZIQUIAUFRXKRBDFDIZXRJERBDVFJZAIFDAZRURYJPURRBDHHONYOBUDXNYXXIHHOIBDUGJEOJNDGKQUPRDGRBDYFPUNDRJYPOXZGDRBDQJFGOYFOZIHDOUZIDRBDHHOFDEDFFDGRJRBDIYMNDNHDFIQUPGDFYPVUFJZPGRBDHZYXGYPVUIUOYFOZIYPAUFRYOZXUFHUFJPCJPRJJLIEXKYPVOYFOZIUERDFHUFFKRJJLQBJBUGHFJZVBRRBDNRJRBDHHORBDVFJZAUGGDGEXKYPVRJNULDYRIJZPGXDIIXYLDUPUORZUXOYFOZIUPGNJFDXYLDIJNDRBYPVEFJNQJFXGQUFYRBDVFJZAQUIOJNYPVZAQYRBRBDYFPUNDURURYNDQBDPRBDFJKUXVZUFGINDPIJPVIPJJAKCIRBDFDGHUFJPBUGHDDPURUADULNUPEFDGCJPFYOBRBJEDPRBDQQYVDFNUPEXKYPVUODLPJQPUIRBDFDGHUFJPOJNNUPGDGUISZUGFJPJEAXUPDILPJQPUIRBDEXKYPVOYFOZIRBDQJFGINJPRKAKRBJPQDFDUGGDGHDOUZIDRBDKOXUYNDGYRIJZPGDGXYLDUFDUXXKHUGRBDURFYOUXUVDPRRBDIJFRJEADFIJPQBJQJZXGBUCDHFJZVBRRBDNRJVDRBDFQYRBTJBPOXDDIDIZVVDIRYPVAKRBJPUIIJNDRBYPVIXYNKIXYRBDFKUPGDFYOYGXDIZVVDIRYPVNJPRKRBDKXURDFDMAXUYPDGRBURRBDPUNDNJPRKNUGDZIXUZVBHDOUZIDNJPRKRJZINDUPIXJFGNJPRVJNDFKJZFVFDURVDPDFUXJERBDIDOJPGQJFXGQUFRBDHHOBUGFDTDORDGIJNDJRBDFPUNDIAZREJFQUFGHKRBDVFJZAYPOXZGYPVQBYRBDFOUPUGURBDPJIDIBJQJQYRIOJXYPAXYPRUBJFIDUIAJJPUPGUHUIYPRBDRJUGDXDCURYPVNJNDPRUPGJQXIRFDROBYPVRYNDIDCDFUXJERBDIDRYRXDIQDFDXURDFZIDGEJFYPGYCYGZUXDAYIJGDI'

