# Some Sage 8 code to do calculations with definite quaternion algebras over 
# Q and compute (trivial weight) quaternionic modular forms and prime level N
# 
# Author: Kimball Martin
# Updated: May 2020
#
# The following code is not intended to optimize efficiency.
# The main functions are eigenbasis(N) and cuspbasis(N) which will compute
# quaternionic modular eigenforms phi as vectors of values
# (phi(x_1), ..., phi(x_h)) 
# for a "nice" ordering of x_1, ..., x_h, with respect to the permumation 
# sigma_N described in my in my congruence mod 2 paper (Can J 2018) or my 
# paper on zeroes of # quaternionic modular forms with Jordan Wiebe (JNT 2020).
# Namely, x_1, ..., x_t will be fixed points of sigma_N, and subsequent
# elements will appear in pairs (x_m, x_{m+1}) which are transposed
#
# The point of this ordering means that all eigenforms with root number -1
# will have zeroes in their first t entries, and for subsequent pairs 
# (x_m, x_{m+1}) transposed by sigma_N, we will have 
# phi(x_{m+1}) = w_phi phi(x_m), where w_phi is the root number of phi
#
# Note: imposing this ordering is rather slow (it takes more than
# a couple of seconds for N > 300), so if you want to compute examples for
# larger N, you should modify this code to not force the ordering
# (my Magma code allows you the option to impose or not impose such an
# ordering, but I didn't include this option in the following Sage functions) 

# compute the class number of definite quaternion algebra over Q
# of discrimant D
def quatclassno(D):
   pd = prime_divisors(D)
   x, y, z = 1, 3, 4
   for p in pd:
       x = x*(p-1)
       y = y*(1-legendre_symbol(-4,p))
       z = z*(1-legendre_symbol(-3,p))
   return (x+y+z)/12

# return True/False according to whether Q(sqrt(d)) embeds in the definite
# rational algebra of discriminant N 
# ASSUMES: d is the discriminant of Q(sqrt(d))
def hasembedding(N,d):
  if d >= 0:
    return False
  for p in prime_divisors(N):
    if kronecker_symbol(d,p) == 1:
      return False
  return True

# given a vector of algebraic integers, scale so all elements are integral
def intmult(v):
  m = 1
  for x in v:
    m = lcm(m,x.denominator())
  return [m*x for x in v]

# given an integer matrix T, and a factor m of the charpoly occuring with
# multiplicity one, return the
# eivenvector associated to a root of m
def eigenvec(T,m):
  K.<a> = NumberField(m)
  A = Matrix(K,T) - identity_matrix(T.ncols())*a
  kr = A.transpose().kernel()
  return kr.basis()[0]

# given an n-by-n permutation matrix of order 2, return a vector of length n
# consisting of +1's, 0's, and -1's such that the fixed points of W are 
# 0's and W interchanges +1 and -1's
def Wrep(W):
  n = W.ncols()
  v = []
  for i in xrange(n):
    j = 0
    while W[i][j] != 1:
      j += 1
    if j == i:
      v.append(0)
    if j > i:
      v.append(1)
    if j < i:
      v.append(-1)
  return v

# given an n-by-n permutation matrix of order 2, return the associated
# permutation as a list, so w[i]=j means W sends i to j
def Wperm(W):
  n = W.ncols()
  w = []
  for i in xrange(n):
    j = 0
    while W[i][j] != 1:
      j += 1
    w.append(j)
  return w

# given a Hecke operator T = Tp permutation of order 2 W, return T with 
# with respect to a permuted basis e_0, ..., e_{n-1} such that 
# (i) W fixes e_0,..., e_r and permutes e_{r+2i}, e_{r+2i-1}
# (ii) any columns with column sum < p+1 occur at the beginning
def changebasis(T,W):
  n = T.nrows()
  k = sum(T.row(0))
  w = Wperm(W)

  neword = []				# specify prelim order of new basis
  for i in xrange(n):
    if w[i] == i:
      neword.append(i)
  for i in xrange(n):
    if w[i] > i:
      neword.append(i)
      neword.append(w[i])
  U = matrix(n,{})
  for i in xrange(n):
    U.add_to_entry(neword[i],i,1)

  T = U.transpose()*T*U
  front = []				# impose property (ii)
  for i in xrange(n):
    if sum(T.column(i)) < k:
      front.append(i)
  for i in xrange(len(front)):		
    T.swap_rows(i,front[i])
    T.swap_columns(i,front[i])
  return T

# return a basis of Hecke eigenvectors for quaternionic modular forms
# of weight 2 and prime level N
# QMFs are given as tuples
# (eigenvector in Q(a), minpoly of a, level N, root number, # fixed points of W)
# here we order the entries in the eigenvectors so that the fixed points of
# W come first (this is slow for large N)
def eigenbasis(N):
    B = BrandtModule(N)
    qmfs = []
    for p in primes(100):
      T = B.hecke_matrix(p)
      f = T.charpoly()
      fact = list(f.factor())
      norepfact = True
      for x in fact:
        if x[1] > 1:
          norepfact = False
      if norepfact:
        W = B.hecke_matrix(N)
        r = Wrep(W).count(0)
        T = changebasis(T,W)
        W = changebasis(W,W)
        for x in fact:
          ev = intmult(eigenvec(T,x[0]))
          phi = column_matrix(ev)
          aN = -1
          if W*phi == phi:
            aN = 1
          qmfs.append((ev, x[0], N, aN,r))
        return qmfs
    return "No T_p has distinct eigenvalues for p < 100"

# return a basis of Hecke eigenvectors for quaternionic cusp forms
# of weight 2 and prime level N
def cuspbasis(N):
  qmfs = eigenbasis(N)
  return qmfs[1:]

# return the degree d quaternionic eigencuspforms of weight 2 and prime level N
def degdforms(N, d):
    B = BrandtModule(N)
    qmfs = []
    for p in primes(100):
      T = B.hecke_matrix(p)
      f = T.charpoly()
      fact = list(f.factor())
      norepfact = True
      for x in fact:
        if x[1] > 1:
          norepfact = False
      if norepfact:
        count = [x[0].degree() for x in fact].count(d) 
        if count > 0:
          if d > 1 or count > 1:
            W = B.hecke_matrix(N)
            w = Wrep(W)
            for x in fact:
              if x[0].degree() == d:
                ev = intmult(eigenvec(T,x[0]))
                if d == 1:
                  if len(ev) == ev.count(1):
                    continue
                phi = column_matrix(ev)
                aN = -1
                if W*phi == phi:
                  aN = 1
                qmfs.append((ev, x[0],N, aN,w))
        return qmfs
    return "No T_p has distinct eigenvalues for p < 100"

# return the integral Hecke cusp eigenforms (attached to ECs) for prime
# levels up to X
def ecforms(X):
  ec = dict()
  for N in primes(11,X+1):
    S = degdforms(N,1)
    if len(S) > 0:
      ec[N] = S
  return ec
