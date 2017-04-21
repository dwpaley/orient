#!/usr/local/bin/python3

import proc_file, metric
from subprocess import Popen, PIPE
from shutil import copyfile
from sys import argv

def main(fileName, ntrial):
    copyfile(fileName + '.hkl', fileName + '_orient.hkl')
    matrices = metric.make_matrices(fileName + '.ins')
    CLtext = ['shelxl', fileName + '_orient']
    best, n = 1, 0

    for tr in range(ntrial):
        proc_file.proc_file(fileName, matrices)
        p = Popen(CLtext, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        r1 = float(stdout.split('\n')[-11][7:13])
        if r1 < best:
            best = r1
            copyfile(fileName + '_orient.ins', fileName + '.o{}'.format(n))
            n += 1
        print('Trial {}\nCurrent R1={}\nBest R1={}\n'.format(tr + 1, r1, best))

main(argv[1], int(argv[2]))







