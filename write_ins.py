import randpts
from numpy import dot
from numpy.random import rand

def write_ins(template, args, matrices, fileName):
    '''
    Takes a template, fills in coordinates for the dummy atoms, and writes
    an ins file ready for ShelXL refinement.
    '''
    with open(fileName+'_or.ins', 'w') as outFile:
        cartMat, invCartMat = matrices #transform to and from a Cartesian basis
        v1, v2 = randpts.makeVectors() #these are perp., cartesian, unit vectors
        shift = dot(invCartMat, 
            (args.shift * randpts.makeRand() * rand()))
        cent = args.cent + shift
        pivt = cent + dot(invCartMat, v1)
        perp = cent + dot(invCartMat, v2)
        
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

