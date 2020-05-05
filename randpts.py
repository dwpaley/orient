from random import gauss
from linalg import cross, norm


def makeRand():
    '''return a single unit vector randomly distributed on a sphere'''
    v1 = [gauss(0,1) for i in range(3)]
    return [x/norm(v1) for x in v1]

def makePerp(v1):
    '''return a random unit vector on a circle perpendicular to v1'''
    v2 = [gauss(0,1) for i in range(3)]
    v3 = cross(v1, v2)
    return [x/norm(v3) for x in v3]

def makeVectors():
    '''return two unit vectors that are randomly distributed on a sphere
    with the condition that they are mutually perpendicular'''
    p1, p2 = [[gauss(0,1) for i in range(3)] for j in range(2)]
    p3 = cross(p1, p2)
    norm1 = norm(p1)
    norm3 = norm(p3)
    p1 = [x/norm1 for x in p1]
    p3 = [x/norm3 for x in p3]
    return p1, p3
