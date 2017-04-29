#!/usr/local/bin/python3

import proc_file, metric
from subprocess import getoutput
from shutil import copyfile
from sys import argv
from re import compile

def main(fileName, ntrial):
    copyfile(fileName + '.hkl', fileName + '_orient.hkl')
    matrices = metric.make_matrices(fileName + '.ins')

    CLtext = 'shelxl {}_orient'.format(fileName)
    r1SearchExp = compile(r'R1 = +([0-9.]+) +for')
    
    best, n = 1, 0

    for tr in range(ntrial):
        proc_file.proc_file(fileName, matrices)
        shelxlOut = getoutput(CLtext)
        r1 = float(r1SearchExp.search(shelxlOut).group(1))
        if r1 < best:
            best = r1
            copyfile(fileName + '_orient.ins', fileName + '.o{}'.format(n))
            n += 1
        print('Trial {}\nCurrent R1={}\nBest R1={}\n'.format(tr + 1, r1, best))

main(argv[1], int(argv[2]))







