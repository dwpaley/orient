import randpts
import numpy as np

def write_ins(template, args, matrices, fileName):
    '''
    Takes a template, fills in coordinates for the dummy atoms, and writes
    an ins file ready for ShelXL refinement.
    '''
    with open(fileName+'_or.ins', 'w') as outFile:
        cartMat, invCartMat = matrices #transform to and from a Cartesian basis
        v1, v2 = randpts.makeVectors() #these are perp., cartesian, unit vectors
        shift = np.dot(invCartMat, 
            (args.shift * randpts.makeRand() * np.random.rand()))
        cent = args.cent + shift
        pivt = cent + np.dot(invCartMat, v1)
        perp = cent + np.dot(invCartMat, v2)
        
        for line in template:
            if 'cent_xyz' in line:
                line = line.replace(
                        'cent_xyz', '{:.5f} {:.5f} {:.5f}'.format(*cent)) 
            if 'pivt_xyz' in line:
                line = line.replace(
                        'pivt_xyz', '{:.5f} {:.5f} {:.5f}'.format(*pivt)) 
            if 'perp_xyz' in line:
                line = line.replace(
                        'perp_xyz', '{:.5f} {:.5f} {:.5f}'.format(*perp)) 
            outFile.write(line)

