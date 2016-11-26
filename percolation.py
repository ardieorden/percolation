import numpy as np
import matplotlib.pyplot as plt

def percolation(p,L):
    """
    Simulate percolation and label contiguous clusters using the
    Hoshen-Kopelman algorithm
    
    Parameters
    ----------
    p : float
        Cluster concentration
    L : int
        Lattice length
    
    Returns
    -------
    hk : array
        Percolation cluster labeled using Hoshen-Kopelman algorithm
    meanmass : float
        Average cluster mass of the finite clusters in the 'hk' array
    """
    
    """
    Creates a Boolean grid representing whether a site is occupied
    (i.e. True) or vacant (i.e. False)
    """
    grid = np.random.rand(L,L) < p
    
    """Container for cluster labels"""
    hk = np.zeros((L,L))
    
    """Label each occupied site with a different number"""
    label = 1
    for i in xrange(L):
        for j in np.arange(L):
            if grid[i][j] == True:
                hk[i][j] = label
                label += 1
    
    """Container indicating which labels are adjacent to one another"""
    adjacent = []
    
    """Identify labels which are bottom adjacent"""
    i = 0
    for j in xrange(L-1):
        if grid[i][j] == True and grid[i][j+1] == True:
            adjacent.append([ hk[i][j], hk[i][j+1] ])
    
    """Identify labels which are right adjacent"""
    j = 0
    for i in xrange(L-1):
        if grid[i][j] == True and grid[i+1][j] == True:
            adjacent.append([ hk[i][j], hk[i+1][j] ])
    
    for i in xrange(1,L):
        for j in xrange(1,L):
            """Identify labels which are left adjacent"""
            if grid[i][j] == True and grid[i-1][j] == True:
                adjacent.append([ hk[i][j], hk[i-1][j] ])
            """Identify labels which are top adjacent"""
            if grid[i][j] == True and grid[i][j-1] == True:
                adjacent.append([ hk[i][j], hk[i][j-1] ])
    
    """Converts 'adjacent' from a Python list into a NumPy array"""
    adjacent = np.array(adjacent)
    
    """Relabel adjacent sites with the smallest label"""
    for i in xrange(len(adjacent)):
        for j in adjacent[i]:
            min_label = min(adjacent[i])
            hk = hk - (hk == j)*j + (hk == j)*min_label
            adjacent = adjacent - (adjacent == j)*j + (adjacent == j)*min_label
    
    """
    Containers indicating which cluster labels are on the
    top, bottom, right and left borders
    """
    t = []
    b = []
    r = []
    l = []
    i = 0
    for j in xrange(L):
        if grid[i][j] == True:
            t.append(hk[i][j])
    i = L-1
    for j in xrange(L):
        if grid[i][j] == True:
            b.append(hk[i][j])
    j = 0
    for i in xrange(L):
        if grid[i][j] == True:
            l.append(hk[i][j])
    j = L-1
    for i in xrange(L):
        if grid[i][j] == True:
            r.append(hk[i][j])
    
    """Converts 't', 'b', 'r' and 'l' from a Python list into a NumPy array"""
    t = np.unique(t)
    b = np.unique(b)
    r = np.unique(r)
    l = np.unique(l)
    
    """
    Counts the number of clusters but does not count infinite clusters
    (i.e. infinite clusters extend from top to bottom or left to right)
    """
    notcounted = []
    for i in t:
        for j in b:
            if i == j:
                notcounted.append(i)
    for i in r:
        for j in l:
            if i == j:
                notcounted.append(i)
    notcounted = np.unique(notcounted)
    clusters = list(np.unique(adjacent))
    for i in notcounted:
        clusters.remove(i)
    
    """Compute the total cluster mass"""
    totalmass = 0.0
    for i in clusters:
        totalmass += np.sum(hk == i)
    
    """Calculate the mean cluster mass """
    try:
        meanmass = totalmass / len(clusters)
    except:
        meanmass = 0

    return [hk, meanmass]

"""Definition of variables"""
L = 30
all_p = np.linspace(0, 1, 100)
all_mass = []
for i in xrange(100):
    mass = percolation(all_p[i], L)[1]
    all_mass.append(mass)

"""Plot the mean cluster mass as a function of the cluster concentration p"""
plt.plot(all_p, all_mass)
plt.xlabel('$p$')
plt.ylabel('$<s>$')
plt.legend(loc=2)
plt.savefig('meanmassvsp.png', dpi=600)
plt.show()

"""Use the result to determine the critical concentration"""
critical_p = all_p[all_mass.index(max(all_mass))]
print critical_p