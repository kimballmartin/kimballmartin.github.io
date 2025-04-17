##################################################
##
## Code for Math Capstone (Fall 2012)
## Kimball Martin
## 9/13/12
##
## Notes: This is sample code for some of the exercises given in Math
## Capstone.  This code is not necessarily meant to be the most efficient
## or elegant possible, but in what I think is the simplest way to understand
## given what we did in class.  Please notify me of any bugs spotted.
##
##
##################################################

##################################################
##
## From HW 1
##
##################################################


# a function which, given an adjacency matrix A, prints out the list of
# edges for the graph in "human format"

def print_edges(A):
    n = len(A)				# let n be the size of the matrix
    for i in range(n):
        for j in range(i+1,n):
            if A[i][j] == 1:
                print '{', i+1, ',', j+1, '}'


##################################################
##
## From HW 2
##
##################################################

# Given an adjacency matrix A, return the number of vertices for the 
# corresponding graph

def nvert(A):
    return len(A)

# Given an adjacency matrix A, return the number of edges for the 
# corresponding graph

def nedges(A):
    n = len(A)
    e = 0			# a variable which counts the number of edges
    for i in range(n):
        for j in range(i+1,n):
            if A[i][j] == 1:
                e = e + 1
    return e

# Given an adjacency matrix and a nonnegative integer k, return True if the
# graph is k-regular and False otherwise

def iskreg(A,k):
    n = len(A)
    for i in range(n):		# return false if the i-th vertex does not
        if A[i].count(1) != k:	# have degree k
            return False
    return True			# return True if no vertex fails this test

# Given an adjacency matrix, return True if the graph is regular and False 
# otherwise.  One just needs to check if it is k-regular, where k is the
# degree of the first (zeroth) vertex

def isreg(A):
    k = A[0].count(1)		# get the degree of the first vertex
    return iskreg(A,k)

##################################################
##
## From in class
##
##################################################


##################################################
# a recursive function to compute x^n mod m via repeated squaring
# here x, n and m are assumed to be nonnegative integers and m > 0
##################################################

def modexp(x,n,m):
    if n == 0:
        return 1
    if x == 0:
        return 0
    k = 0
    r = n
    while r > 1:		# let k = floor(log_2(n))
	r = r >> 1		# namely, replace n with floor(n/2) and count 
        k = k + 1		#    how many times you must do this to get to 1
    y = x
    for i in range(k): 		# let y = x^(2^k) % m via repeated squaring
        y = y * y % m
    return y * modexp(x,n - (1 << k), m) % m
