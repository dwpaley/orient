#!/usr/local/bin/python3

import proc_file, metric, randpts
from subprocess import Popen, PIPE
from shutil import copyfile
from sys import argv

def main(fileName):
    trMat = metric.make_inv_cart_mat(fileName)
    CLtext = ['shelxl', fileName.rstrip('.ins') + '_orient']
    best, n = 1, 0

    while 1:
        v1, v3 = randpts.makeVectors()
        proc_file.proc_file(fileName, v1, v3, trMat)
        p = Popen(CLtext, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        r1 = float(stdout.split('\n')[-11][7:13])
        if r1 < best:
            best = r1
            copyfile(fileName.rstrip('.ins') + '_orient.ins',
                    fileName + '.o{}'.format(n))
            n += 1
        print('Current R1={}\nBest R1={}\n'.format(r1, best))

main(argv[1])







