import numpy as np
import randpts

def proc_file(fileName, matrices, translateScale=0):
    cartMat, invCartMat = matrices
    v1 = randpts.makeRand() #v1 is a cartesian unit vector
    inFile = open(fileName + '.ins', 'r')
    outFile = open(fileName + '_orient.ins', 'w')

    lineCounter = 0



    for line in inFile.readlines():

        # This applies a random shift to the search fragment (achieved by
        # shifting the 3 dummy atoms away from the centroid of the frag)
        if lineCounter > 0: 
            lineList = line.split()
            for i in range(2,5): 
                lineList[i] = float(lineList[i])
            line = '{} {} {:.6f} {:.6f} {:.6f}\n'.format(
                    lineList[0], lineList[1], *(lineList[2:5] + tVector))
            lineCounter -= 1
        if line[0:4].upper() == 'FRAG':
            lineCounter = 3
            tVector = randpts.makeRand() * translateScale * np.random.rand()

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

