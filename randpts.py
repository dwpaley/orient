from random import gauss
from numpy.linalg import norm
from numpy import array, cross

def makeVectors():
    '''return two unit vectors that are randomly distributed on a sphere
    with the condition that they are mutually perpendicular'''
    p1, p2 = [[gauss(0,1) for i in range(3)] for i in range(2)]
    p3 = cross(p1, p2)
    p1 = p1 / norm(p1)
    p3 = p3 / norm(p3)  #p1 and p3 are now random, perpendicular, unit vectors
    return p1, p3
