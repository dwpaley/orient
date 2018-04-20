#!/usr/local/bin/python3

import proc_file, metric
from subprocess import getoutput
import shutil as sh
from sys import argv
from re import compile
import tempfile

def main(fileName, ntrial, translateScale=0):
    sh.copyfile(fileName + '.hkl', fileName + '_orient.hkl')
    matrices = metric.make_matrices(fileName + '.ins')

    CLtext = 'shelxl {}_orient'.format(fileName)
    r1SearchExp = compile(r'R1 = +([0-9.]+) +for')
    
    best, n = 1, 0

    for tr in range(ntrial):
        proc_file.proc_file(fileName, matrices, translateScale)
        shelxlOut = getoutput(CLtext)
        try:
            r1 = float(r1SearchExp.search(shelxlOut).group(1))
        except AttributeError:
            r1 = 1
        if r1 < best:
            n += 1
            best = r1
            sh.copyfile(fileName + '_orient.ins', fileName + '.o{}'.format(n))
        print('Trial {}\nCurrent R1={}\nBest R1={}\n'.format(tr + 1, r1, best))

    # clean up by copying best to name_orient.ins, refining one more time, 
    # then deleting the dummy atoms from the res file
    sh.copyfile(fileName + '.o{}'.format(n), fileName + '_orient.ins')
    getoutput(CLtext)
    res = fileName + '_orient.res'
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp, \
            open(res) as f:
        for line in f.readlines():
            if not ('CENT' in line.upper() or 
                    'DUM' in line.upper() or
                    'PIVT' in line.upper()):
                tmp.write(line)
    sh.move(tmp.name, res)

    print('\nOutput is written to {}'.format(res))


if len(argv) == 3:
    main(argv[1], int(argv[2]))
if len(argv) == 4:
    main(argv[1], int(argv[2]), float(argv[3]))







