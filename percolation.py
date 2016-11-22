import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

__author__ = 'A. Orden'
__name__ = '__main__'


"""Definition of variables"""
L = 6
p = 0.59725

def algorithm1():
    """Generate percolation structure"""
    
    lattice = np.zeros((L,L))
    
    """
    Loop through all (i,j), draw a random number r,
    if r < p then plot a point at the position (i,j)
    """
    for i in xrange(L):
        for j in xrange(L):
            r = np.random.random()
            if r < p:
                lattice[i][j] = 1
    
    plt.imshow(lattice, cmap=cm.gray)

def algorithm2():
    """Generate percolation structure using a direct growth process"""
    
    """Let 255 == undefined"""
    """Label all sites of a square lattice as undefined"""
    lattice = 255*np.ones((L,L))
    
    """Label corners as vacant in order to setup a border"""
    for i in xrange(L):
        lattice[0][i] = 0
        lattice[i][0] = 0
        lattice[L-1][i] = 0
        lattice[i][L-1] = 0
    
    """Occupy the center"""
    lattice[L/2][L/2] = 1
    
    """
    Define a list that will hold the positions of the 
    undefined sites adjacent to the cluster.
    """
    lis = [[L/2+1, L/2],
           [L/2, L/2+1],
           [L/2-1, L/2],
           [L/2, L/2-1]]
    """The list has a length PD = 4L."""
    PD = 4*L
    for i in xrange(4, PD):
        lis.append([None,None])
    
    """
    Define 'counter', a pure counting variable, whose value is incremented
    by 1 each time a new undefined boundary site of the cluster is generated.
    """
    global counter
    counter = 3
    
    """Label sites as occupied (i.e. 1) or vacant (i.e. 0)."""
    def definition(i,j):
        if lattice[i][j] != 255:
            return
        global counter
        r = np.random.random()
        if r < p:
            lattice[i][j] = 1
            if lattice[i][j+1] == 255:
                counter += 1
                lis[counter%PD][0] = i
                lis[counter%PD][1] = j+1
            if lattice[i][j-1] == 255:
                counter += 1
                lis[counter%PD][0] = i
                lis[counter%PD][1] = j-1
            if lattice[i+1][j] == 255:
                counter += 1
                lis[counter%PD][0] = i+1
                lis[counter%PD][1] = j
            if lattice[i-1][j] == 255:
                counter += 1
                lis[counter%PD][0] = i-1
                lis[counter%PD][1] = j
        else:
            lattice[i][j] = 0
    
    """Continue labelling sites until no undefined sites are left."""
    for _ in xrange(10000):
        for k in xrange(counter+1):
            i = lis[k%PD][0]
            j = lis[k%PD][1]
            definition(i,j)
    
    """If there is still an undefined site, plot in red and blue"""
    if 255 in lattice:
        plt.imshow(lattice)
    """If all sites are vacant or occupied, plot in black and white"""
    if 255 not in lattice:
        plt.imshow(lattice, cmap=cm.gray)

algorithm2()