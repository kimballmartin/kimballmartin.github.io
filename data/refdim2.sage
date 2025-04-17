# Sage 9 code to do calculations related to Yamauchi's trace formula,
# my paper on refined dimension formulas (JNT, 2018),
# and my paper on zeroes of quaternionic modular forms with Jordan Wiebe
# (JNT, 2020)
#
# Author: Kimball Martin
# Updated: Aug 2020
#
# The main functions of interest are:
#
# Snewdim(N,k) - computes the dimension of the newspace of level Gamma0(N)
# 	and weight k for a SQUAREFREE level N
#
# refdim(N,i,k=2) - computes the dimension of the Atkin-Lehner eigenspace
#	of the space above with given Atkin-Lehner signs at each prime 
#	dividing N.  here these Atkin-Lehner signs are specified as an 
#	integer 0 <= i <= 2^w-1, where w is the number of prime factors of N
#	representing a sign pattern.  here 0 gives the sign pattern of all -1's
#	and 2^w-1 gives the sign pattern of all +1's.  in general, call
#	signpat(w,i) to see the sign pattern associated to i

# function r(D,n) from Skoruppa-Zagier
def r(D,n):
    count = 0
    for x in range(2*n):
        if (x*x-D)%(4*n) == 0:
            count = count + 1
    return count

# return the class number h(d) (assuming d is a fundamental discriminant)
def classno(d):
    return len(BinaryQF_reduced_representatives(d))

# return  h'(D) (assuming D < 0 is a fundamental discriminant)
def hprime(D):
  if D == -4:
    return 1/2
  if D == -3:
    return 1/3
  return len(BinaryQF_reduced_representatives(D))

# given a squarefree N, return disc Q(sqrt(-N))

def delta(N):
  if N % 4 == 3:
    return -N
  return -4*N

def b(M1, M2):
  j = M1 % 8
  i = M2 % 2
  if i == 1:
    if j == 3:
      return 4
    if j == 7:
      return 2
    return 1
  if j == 3:
    return -2
  if j == 7:
    return 0
  return -1


def c(N0, N2):
  if N0 % 4 !=3:
    return 1
  if N2 % 2 == 1:
    return 3 - kronecker_symbol(N0,2)
  if N2 % 2 == 0:
    return 5 - kronecker_symbol(N0,2)

def p2(k):
  j = k % 8
  if j == 0 or j == 6:
    return -1
  return 1

def p3(k):
  j = k % 12
  if j == 0 or j == 8:
    return -1
  if j == 2 or j == 6:
    return 1
  if j == 4:
    return 2
  return -2

# compute the trace of W_M on S_k(N), assuming M > 1 and N squarefree
# by default take k=2
def tr0(N, M, k=2):
  if M == 1:
    return Snewdim(N,k)
  D = delta(M)
  h = classno(D)
  M2 = int(N/M)
  M2odd = M2
  j = 0
  if M2odd % 2 == 0:
    M2odd = int(M2/2)
    j = 1
  pset = prime_factors(M2odd)
  prod1 = 1
  for p in pset:
    prod1 = prod1 * (kronecker_symbol(D,p) - 1)
  tr = (-1)^(k/2) * prod1 * b(M, M2) * h / 2 
  w = len(prime_factors(M2))
  if M == 2:
    prod2 = 1
    for p in pset:
      prod2 = prod2 * (kronecker_symbol(-4,p) - 1)
    tr = tr - (-1)^j * p2(k) * prod2 / 2
  if M == 3:  			# note need to adjust h(-3) to h'(-3) here
    tr = tr/3 - (-1)^j*(j+1)/3 * p3(k) * prod1
  if k == 2:
    tr = tr + (-1)^w
  return tr

# compute the class number of a definite quaternion algebra/Q with discriminant
# N; returns 0 if N is not valid discriminant
def hB(N):
  if not(is_squarefree(N)) or len(prime_divisors(N)) % 2 != 1:
    return 0
  s2 = 1/4
  s3 = 1/3
  for p in prime_divisors(N):
    s2 = s2 * (1 - kronecker_symbol(-4,p))
    s3 = s3 * (1 - kronecker_symbol(-3,p))
  return euler_phi(N)/12 + s2 + s3

# compute the type number of a definite quaternion algebra/Q with discriminant
# N; returns 0 if N is not valid discriminant
def tB(N):
  if hB(N) == 0:
    return 0
  e = len(prime_divisors(N))
  s2 = s3 = s4 = 0
  if N % 3 == 0:
    s3 = 1
  if N % 2 == 0:
    s3 = s3/2
    s2 = s4 = 1/2
  for p in prime_divisors(N):
    s2 = s2 * (1 - kronecker_symbol(-4,p))
    s3 = s3 * (1 - kronecker_symbol(-3,p))
    s4 = s4 * (1 - kronecker_symbol(-2,p))
  return (hB(N)+s2+s3+s4)/(2^e) 

# the following functions are to work with sign patterns of length w,
# which we often view as integers between 0 and 2^w-1.

# given an integer n, return the sign pattern of length w corresponding to n
def signpat(w,n):
  pat = []
  for j in range(w):
    pat.append(2*int((n & (2^j))/2^j)-1)
  return pat

# given a sign pattern eps = (pm 1, pm 1, ..., pm 1), return the
# corresponding integer
def signpatint(eps):
  n = 0
  for j in range(len(eps)):
    n += 2^j*int((eps[j]+1)/2)
  return n

# to generate all sign patterns for N (squarefree)
def allsignpats(N):
  w = len(prime_divisors(N))
  l = []
  for i in range(2^w):
    l.append(signpat(w,i))
  return l

def signpateval(chi,N,d):
  P = prime_divisors(N)
  P.sort()
  chidict = dict()
  for i in range(len(P)):
    chidict[P[i]] = chi[i]
  prod = 1
  for p in prime_divisors(d):
    prod = prod*chidict[p]
  return prod

# for N odd sqfree with an odd number of prime factors, compute
# dim M^+N(O) - dim M^chi(O)
# for Prop 3.7 of paper with Jordan Wiebe
def wt2bias(N, chi):
  s = 0
  for d in divisors(N):
    if d > 1:
      prod = 1
      for p in prime_divisors(N/d):
        prod = prod * (1-kronecker_symbol(delta(d),p))
      s += (1-signpateval(chi,N,d))*hprime(delta(d))*b(d,N/d)*prod
  s = s/2
  if N%3 == 0:
    prod = 1/3
    for p in prime_divisors(N/3):
      prod = prod * (1-kronecker_symbol(-3,p))
    s += (1-signpateval(chi,N,3))*prod
  return s/2^(len(prime_divisors(N)))

# negate a sign pattern v
def negate(v):
  return [-x for x in v]

# for the set of N in between N1 and N2 for which wt2bias works, find the set 
# sign patterns not +_N which have the same dimension as +_N
def biasedpat(N1,N2):
  l = []
  count = 0
  countadm = 0
  for N in range(N1,N2+1):
    if N%2 == 1:
      if is_squarefree(N):
        w = len(prime_divisors(N))
        if w%2 == 1 and w > 1:
          countadm += 1
          flag = False
          for i in range(1,2^w):
            chi = negate(signpat(w,i))
            a = wt2bias(N,chi)
            if a == 0:
              l.append((N,chi))
              flag = True
          if flag:
            count += 1
  print("Number of admissible levels with non-trivial biased pattern:  ", count)
  print("Number of admissible levels:  ", countadm)
  return l

# for squarefree N, compute the dimension of the newspace of S_k(N)
def Snewdim(N,k):
  d = (k-1)*euler_phi(N)/12
  c1 = ((1-k)/4+floor(k/4))
  c2 = ((1-k)/3+floor(k/3))
  for p in prime_divisors(N):
    c1 = c1*(kronecker_symbol(-4,p)-1) 
    c2 = c2*(kronecker_symbol(p,3)-1)
  d += c1 + c2
  if k == 2:
    d += moebius(N)
  return d

# for squarefree N compute dimension of AL newspace with given sign pattern
# input sign pattern as number i between 0 and 2^w(N)-1
def refdim(N,i,k=2):
  s = 0
  w = len(prime_divisors(N))
  chi = signpat(w,i)
  for d in divisors(N):
      s = s + signpateval(chi,N,d) * tr0(N, d, k)
  return s/(2^w)
