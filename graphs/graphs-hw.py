##################################################
##
## Python 2.7 Code for Graph Theory Homework (Spring 2014)
## Kimball Martin
## 
##
## Notes: This is sample code for some of the exercises from
## class.  Generally I won't include examples of testing of the code.
## This code is not necessarily meant to be the most efficient
## or elegant possible, but in what I think is the simplest way to understand
## given what we did in class.  Please notify me of any bugs/typos spotted.
##
##
##################################################


##################################################
##
## Lab Homework 1
##
##################################################

###############
# Exercise 1
###############

def count_vec(n):
    v = []		# create an empty list v
    for i in range(n):	# for i = 0, 1, ..., n-1
        v.append(i+1)	# append i+1 to the list v
    return v

# Note: one can do this more simply without loops by simply returning
# range(1,n+1)

###############
# Exercise 2
###############

def scale_vec(v,c):
    newv = []			# create a new (empty) vector newv
    for x in v:			# go through each element of v
        newv.append(c*x)	# and add c times that element to newv
    return newv

# Note: you should not modify the elements of v directly in this code
# for example, don't do this:

def scale_vec_BAD(v,c):
    n = len(v)			# let n be the length of v
    i = 0
    while i < n:		# go through positions 0, 1, ..., n-1
        v[i] = c*v[i]		# of v and replace each element with c times
        i = i+1			# that element
    return v

# the problem is if you apply the latter function to

v = [1, 2, 3]
scale_vec_BAD(v,3)

# both the vector returned and the original vector v will be scaled by 3
# though there are some instances where you may want to change a list or
# matrix that you pass to a function, typically you don't want to

###############
# Exercise 3
###############

# This is essentially the same as scale_vec

def shift_vec(v,c):
    newv = []
    for x in v:
        newv.append(c+x)
    return newv

###############
# Exercise 4
###############

# Here is one way to do it

def count_mat(n):
    mat = []			# start with an empty list for our matrix
    v = count_vec(n)		# let v = [1, 2, ..., n], which is the first row
    for i in range(n):		# add n rows to mat, which are just shifts of
        mat.append(shift_vec(v, n*i))	# v by 0, n, 2n, ..., (n-1)n
    return mat

# Another way is to make use the range function to specify each row directly,
# you just need to be careful with the indices

def count_mat_ver2(n):
    mat = []
    for i in range(n):
        mat.append(range(i*n+1, (i+1)*n+1))
    return mat

##################################################
##
## Lab 3
##
##################################################


###############
# Problem 4
###############

# generates the adjacency matrix for the complete graph K_n

def CompleteGraph(n):
    mat = []
    for i in range(n):
        rowi = []
        for j in range(n):	# create row i element by element
            if i==j:
                rowi.append(0)
            else:
                rowi.append(1)
        mat.append(rowi)
    return mat


###############
# Problem 5
###############

# generates an adjacency matrix for the cycle graph C_n

def CycleGraph(n):
    mat = []
    if n == 1:			# the below algorithm doesn't work for n=1
        return [[ 0 ]]
    for i in range(n):
        rowi = []
        for j in range(n):	# create row i element by element
            if j == (i-1)%n or j == (i+1)%n:
                rowi.append(1)
            else:
                rowi.append(0)
        mat.append(rowi)
    return mat


###############
# Bonus
###############

# generates an adjacency matrix for the directed cycle graph of order n

def DiCycleGraph(n):
    mat = []
    if n == 1:			# the below algorithm doesn't work for n=1
        return [[ 0 ]]
    for i in range(n):
        rowi = []
        for j in range(n):	# create row i element by element
            if j == (i+1)%n:
                rowi.append(1)
            else:
                rowi.append(0)
        mat.append(rowi)
    return mat

