import numpy as np
from math import cos, radians, acos, sin, sqrt

def make_inv_cart_mat(fileName):
    '''This makes the inverse of the Cartesian basis transformation described
    on Shmueli p. 235'''
    with open(fileName, 'r') as inFile:
        inst = ''
        while inst.lower() != 'cell':
            line = inFile.readline()
            inst = line.split()[0] if line.split() else ''
    a, b, c, al, be, ga = [float(x) for x in line.split()[2:8]]
    cal, cbe, cga = [cos(radians(angle)) for angle in (al, be, ga)]

    gij = np.array([[a**2, a*b*cga, a*c*cbe],
                    [b*a*cga, b**2, b*c*cal],
                    [c*a*cbe, c*b*cal, c**2]])
    gInv = np.linalg.inv(gij)
    ast, bst, cst = [sqrt(gInv[i][i]) for i in range(3)]
    alst = acos(gInv[1][2]/bst/cst)
    best = acos(gInv[0][2]/ast/cst)
    gast = acos(gInv[0][1]/ast/bst)

    cartMat = np.array([[a, b*cga,              c*cbe],
                        [0, b*sin(radians(ga)), -c*sin(radians(be))*cos(alst)],
                        [0, 0,                  1/cst]])
    invCartMat = np.linalg.inv(cartMat)

    return invCartMat

