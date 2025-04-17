# Sage 9+ code for computing traces of Fricke involutions W_N on newspaces
# S_k(N)^new as in my paper
# Root number bias for newforms
# Kimball Martin

# Code updated June 2022

# There are 4 different functions to compute using different formulas
# in this paper:

# trWnewdirect(N,k)
# trWnew(N,k)
# trWnew2(N,k)
# trWnew3(N,k)

# return  h'(D) 
def hprime(D):
  D0 = fundamental_discriminant(D)
  F = ZZ(sqrt(D/D0))
  h0 = len(BinaryQF_reduced_representatives(D0))
  if D0 == -4:
    h0 = 1/2
  if D0 == -3:
    h0 = 1/3
  gamma = sum([moebius(t)*kronecker_symbol(D0,t)/t for t in divisors(F)])*F
  return h0*gamma

# return Hurwitz class number
def H(D):
  if D == 0:
    return -1/12
  D0 = fundamental_discriminant(D)
  F = ZZ(sqrt(D/D0))
  return sum([hprime(ZZ(D/f^2)) for f in divisors(F)])

# returns root number of newform f
def rootno(f):
  k = f.weight()
  N = f.level()
  w = (-1)^(k/2)
  for p in prime_divisors(N):
    w = w*f.atkin_lehner_eigenvalue(p)
  return ZZ(w)

# returns the trace of the Fricke involution 
# W_n = \prod_{p<infty} W_p on S^new_k(N)
# by directly computing root numbers of each newform
def trWnewdirect(N,k):
  F = Newforms(N,k,names='a')
  return (-1)^(k/2)*sum([rootno(f)*f.hecke_eigenvalue_field().degree() for f in F])

# test alternative formula for H(D)
def H2(D):
  if D == 0:
    return -1/12
  D0 = fundamental_discriminant(D)
  F = ZZ(sqrt(D/D0))
  s = sum([moebius(t)*kronecker_symbol(D0,t)*sigma(F/t) for t in divisors(F)])
  return s*hprime(D0)

# INPUT: N
# OUTPUT: (N1, N2) where N = N1 * N2^2, N1 sqfree
def decompose(N):
  N1 = 1
  for p in prime_divisors(N):
    if valuation(N,p)%2 == 1:
      N1 = N1*p
  N2 = ZZ(sqrt(N/N1))
  return (N1, N2)

def trWold(N,k):
  if k == 2:
    delta = 1
  else:
    delta = 0
  if N == 1: 
    return CuspForms(1,k).dimension()
  if N == 2:
    if k%8 == 0:
      return 1 
    if k%8 == 2:
      return delta - 1
    return 0
  if N == 3:
    if k%12 == 4 or k%12 == 10:
      return 0
    return (-1)^(k/2)*(1 - delta)
  if N == 4:
    if k%4 == 2:
      return delta - 1
    return 0
  (N1, N2) = decompose(N)
  if is_fundamental_discriminant(-N1):
    if N2%2 == 1:
      return (-1)^(k/2)*(3-kronecker_symbol(-N1,2))*hprime(-N)/2 + delta
    else:
      return (-1)^(k/2)*hprime(-N) + delta
  return (-1)^(k/2)*hprime(-4*N)/2 + delta

# compute trace of W_N on newspace using (3.1)
def trWnew(N,k):
  (N1, N2) = decompose(N)
  return sum([moebius(Q) * trWold(N1*(N2/Q)^2,k) for Q in divisors(N2)])

def c(D,n): 
  return sum([euler_phi(n/t)*moebius(t)*kronecker_symbol(D,t) for t in divisors(n)])

def cprime(N):
  (N1, N2) = decompose(N)
  D = -fundamental_discriminant(-N1)
  if N1%8 == 3 and N2%4 == 2:
    return c(-D,N2)/2 # - c(-D,odd_part(N2))
  return c(-D,N2)

def xi0(N,k):
  (N1, N2) = decompose(N)
  D = -fundamental_discriminant(-N1)
  if N1 == 1:
    if is_squarefree(N2):
      if N2%2 == 1:
        return moebius(N2)*(trWold(1,k)-(-1)^(k/2)*1/4)
      return moebius(N2)*(trWold(1,k)-trWold(4,k)+(-1)^(k/2)*1/4)
    if N2%2 == 0:
      if is_squarefree(ZZ(N2/2)):
        return moebius(ZZ(N2/2))*(trWold(4,k)-(-1)^(k/2)*1/2)
  if N1 == 2:
    if is_squarefree(N2):
      return moebius(N2)*(trWold(2,k)-(-1)^(k/2)*1/2)
  if N1 == 3:
    if is_squarefree(N2):
      return moebius(N2)*(trWold(3,k)-(-1)^(k/2)*2/3)
  return 0

def bN(N):
  (N1, N2) = decompose(N)
  D = -fundamental_discriminant(-N1)
  if N1%4 == 2 or N1%4 == 1:
    kappa = 1/2
  else:
    if N2%2 == 0:
      kappa = 1
    else:
      kappa = (3 - kronecker_symbol(-N1,2))/2
  return kappa

# test out expression in Sec 3.4
def trWnew2(N,k):
  (N1, N2) = decompose(N)
  D = -fundamental_discriminant(-N1)
  delta = 0
  if k == 2:
    if N2 == 1:
      delta = 1
    if N1 == 1:
      if is_squarefree(N2) and N2%2 == 1:
        delta = delta - moebius(N2)
      if N2%4 == 0:
        if is_squarefree(ZZ(N2/2)):
          delta = delta - moebius(N2/2)
    if (N1 == 2 or N1 == 3) and is_squarefree(N2):
      delta = delta - moebius(N2)
  return (-1)^(k/2)*bN(N)*cprime(N)*hprime(-D) + xi0(N,k) + delta


# test statement of Prop 3.2 
def trWnew3(N,k):
  (N1, N2) = decompose(N)
  D = -fundamental_discriminant(-N1)
  delta = 0
  if k == 2 and N2 == 1:
     delta = 1
  if is_squarefree(N2):
    if N1 == 1:
      if N2%2 == 1:
        k1 = 0
        if k%12 == 2:
          k1 = 1

        return (-1)^(k/2)*(c(-4,N2)-moebius(N2))/4 + moebius(N2)*(floor(k/12) - k1) + delta
      else:
        k1 = 0
        if k%12 == 6 or k%12 == 10:
          k1 = 1
        return (-1)^(k/2)*(c(-4,N2)+moebius(N2))/4 + moebius(N2)*(floor(k/12) + k1) + delta
    if N1 == 2:
      k2 = 1
      if k%8 == 4 or k%8 == 6:
        k2 = -1
      return (-1)^(k/2)*(c(-8,N2)+k2*moebius(N2))/2 + delta
    if N1 == 3:
      k3 = 1
      if k%12 == 4 or k%12 == 10:
        k3 = -2
      return (-1)^(k/2)*(bN(N)*cprime(N)+k3*moebius(N2))/3 + delta
  if N1 == 1 and N2%4 == 0:
    if is_squarefree(N2/2):
      return (-1)^(k/2)*c(-4,N2)/4 - moebius(N2/2)/2

  return (-1)^(k/2)*bN(N)*cprime(N)*hprime(-D) + delta
