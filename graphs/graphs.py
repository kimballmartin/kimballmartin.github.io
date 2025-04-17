##################################################
##
## Python 2.7 Code for Graph Theory (Spring 2014)
## Kimball Martin
## 
##
## Notes: This is sample code for some of the examples from
## class.  This code is not necessarily meant to be the most efficient
## or elegant possible, but in what I think is the simplest way to understand
## given what we did in class.  Please notify me of any bugs/typos spotted.
##
##
##################################################


##################################################
##
## From Section 1.2
##
##################################################

V = [ 1, 2, 3 ]
E = [ [1, 2], [2, 1], [2, 3], [3, 2] ]
G = [V, E]

##########
### Given a graph G=[V,E], return the set of neighbors of a vertex u
### in G.

def VE_neighbors(G, u):
    neigh = set()		# start with an empty set neigh
    E = G[1]			# let E be the edge set
    for e in E:
        if e[0] == u:		# for each edge of the form (u,v)
            neigh.add(e[1])	# add v to the set neigh
    return neigh

       ###
##########

VE_neighbors(G, 1)
VE_neighbors(G, 2)

##########
### Givea an n-by-n adjacency matrix A and an index 0 <= i < n
### return the list of neighbors of vertex i
            
def neighbors(A, i):
    n = len(A)			# let n be the size (number of rows) of A 
    neigh = []			# start with an empty set neigh
    for j in range(n):	
        if A[i][j] == 1:	# for each index 0 <= j < n
            neigh.append(j)	# append j to the list neigh if the i-th 
    return neigh		#     row has a 1 in the j-th position

# Note: I set rowi = A[i] for ease of reading.  One could avoid this
#	and just use the code "if A[i][j] !=0:" on line 6

       ###
##########

A = [ [ 0, 1, 1, 1 ], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 0, 0] ]

courses = { 4383 : "Cryptography", 4673 : "Graph Theory", \
5383 : "Cryptography", 5673 : "Graph Theory" }

G = { "purple" : { "purple", "monkey" }, \
"monkey" : {"purple", "dishwasher"}, \
"dishwasher" : { "monkey" } }

##################################################
##
## From Section 1.3
##
##################################################

##########
### Given a graph as an adjacency matrix, find the degree of vertex i
###

def deg(A,i):
    d = 0		       # initialize the degree d to be 0
    for j in range(len(A)):    # for j = 0, 1, 2, ..., n-1
        d = d+A[i][j]	       # add A[i,j] to d
    return d

       ###
##########

A = [ [ 0, 1, 1, 1 ], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 0, 0] ]
deg(A,0)
deg(A,1)
sum(A[0])
sum(A[1])

##################################################
##
## Lab 3
##
##################################################


###############
# Problem 3
###############

# generates the adjacency matrix for the complete graph K_n

def EmptyGraph(n):
    mat = []
    for i in range(n):
        rowi = []
        for j in range(n):      # create row i element by element
            rowi.append(0)
        mat.append(rowi)
    return mat


###############
# Problem 4
###############

# generates the adjacency matrix for the complete graph K_n

def CompleteGraph(n):
    mat = []
    for i in range(n):
        rowi = []
        for j in range(n):      # create row i element by element
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
    if n == 1:                  # the below algorithm doesn't work for n=1
        return [[ 0 ]]
    for i in range(n):
        rowi = []
        for j in range(n):      # create row i element by element
            if j == (i-1)%n or j == (i+1)%n:
                rowi.append(1)
            else:
                rowi.append(0)
        mat.append(rowi)
    return mat

#################################################
##
## Additional Graph Constructors
##
##################################################

############
# generates an adjacency matrix for the directed cycle graph of order n

def DiCycleGraph(n):
    mat = []
    if n == 1:                  # the below algorithm doesn't work for n=1
        return [[ 0 ]]
    for i in range(n):
        rowi = []
        for j in range(n):      # create row i element by element
            if j == (i+1)%n:
                rowi.append(1)
            else:
                rowi.append(0)
        mat.append(rowi)
    return mat

##############
# Given two adjacency matrices A and B, compute their "graph sum" or
# "union."  That is return the adjacency matrix
#  [ A  0 ]
#  [ 0  B ]

def graphsum(A, B):
    mat = []
    m, n = len(A), len(B)
    for i in range(m):		# first construct the [ A  0 ] part
        rowi = []
        for j in range(m):	# this puts in the A columns
            rowi.append(A[i][j])
        for j in range(n):	# this puts in the 0 columns
            rowi.append(0)
        mat.append(rowi)
    for i in range(n):		# now construct the [ 0  B ] rows
        rowi = []
        for j in range(m):	# put in the 0 columns
            rowi.append(0)
        for j in range(n):	# put in the B columns
            rowi.append(B[i][j])
        mat.append(rowi)
    return mat

##############
# Given a square matrix A, make a copy of A and return it
# We will use this to do things to A in other function without modifying
# the original A (if you modify a list or matrix within a function,
# the original list or matrix will be modified)

def matcopy(A):
    B = []
    n = len(A)
    for x in range(n):
        rowx = []
        for y in range(n):
            rowx.append(A[x][y])
        B.append(rowx)
    return B

##############
# Given an adjacency matrix A, add an undirected edge (i, j)
# The matrix is unmodified if (i,j) is already an edge
# This function does not modify the original A

def add_edge(A,i,j):
    B = matcopy(A)
    B[i][j] = 1
    B[j][i] = 1
    return B

##############
# Given an adjacency matrix A, remove an undirected edge (i, j)
# The matrix is unmodified if (i,j) is not already an edge
# This function does not modify the original A

def remove_edge(A,i,j):
    B = matcopy(A)
    B[i][j] = 0
    B[j][i] = 0
    return B

##############
# Given an adjacency matrix A, add an undirected edge (i, j)
# The matrix is unmodified if (i,j) is already an edge
# This function does not modify the original A

def add_diedge(A,i,j):
    B = matcopy(A)
    B[i][j] = 1
    return B

##############
# Given an adjacency matrix A, remove an undirected edge (i, j)
# The matrix is unmodified if (i,j) is not already an edge
# This function does not modify the original A

def remove_diedge(A,i,j):
    B = matcopy(A)
    B[i][j] = 0
    return B

#################################################
##
## From Section 1.5
##
##################################################

##########
### Given a graph as an adjacency matrix and a vertex i, find all vertices
### in the connected component, organized by distance from i
### I.e., return the spheres of radius r centered at i

def spheres(A, i):
    sph = [ { i } ]
    visited = { i }
    newvert = { i }
    while len(newvert) > 0:
        new = set()
        for j in newvert:
            neigh = neighbors(A,j)
            for k in neigh:
                if k not in visited:
                    new.add(k)
        newvert = new
        if len(newvert) > 0:
            sph.append(newvert)
            visited = visited.union(new)
    return sph

       ###
##########
