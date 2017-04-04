import numpy as np
import randpts

def proc_file(fileName, matrices):
    cartMat, invCartMat = matrices
    v1 = randpts.makeRand() #v1 is a cartesian unit vector
    inFile = open(fileName, 'r')
    outFile = open(fileName.rstrip('.ins') + '_orient.ins', 'w')
    for line in inFile.readlines():
        if line[0:4] == 'CENT':
            cent = np.array([float(x) for x in line.split()[2:5]])
            #cent is an xyz point 
            pivt = cent + np.dot(invCartMat, v1)
            #pivt is an xyz point. generated here as random and 1A away from
            #cent. can reset later to an arbitrary xyz point as long as the 
            #search fragment is setup to match.
        if line[0:4] == 'PIVT':
            pivt = np.array([float(x) for x in line.split()[2:5]])
        if 'XXXX' in line:
            line = line.replace('XXXX',' {:.4f} {:.4f} {:.4f} 10.0 10.01\n'
                    .format(*pivt))
        if 'YYYY' in line:
            v1 = np.dot(cartMat, (pivt - cent))
            v2 = randpts.makePerp(v1)
            dum2 = cent + np.dot(invCartMat, v2)
            line = line.replace('YYYY',' {:.4f} {:.4f} {:.4f} 10.0 10.01\n'
                    .format(*dum2))
        outFile.write(line)
    inFile.close()
    outFile.close()

