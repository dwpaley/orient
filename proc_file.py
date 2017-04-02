import numpy as np

def proc_file(fileName, v1, v2, trMat):
    inFile = open(fileName, 'r')
    outFile = open(fileName.rstrip('.ins') + '_orient.ins', 'w')
    for line in inFile.readlines():
        if line[0:4] == 'CENT':
            cent = np.array([float(x) for x in line.split()[2:5]])
            dum1 = cent + np.dot(trMat, v1)
            dum2 = cent + np.dot(trMat, v2)
        if 'XXXX' in line:
            line = (line[:line.find('XXXX')] + 
                    ' {:.4f} {:.4f} {:.4f} 10.0 10.01\n'.format(
                    *dum1))
        if 'YYYY' in line:
            line = (line[:line.find('YYYY')] +
                ' {:.4f} {:.4f} {:.4f} 10.0 10.01\n'.format(
                    *dum2))
        outFile.write(line)
    inFile.close()
    outFile.close()

