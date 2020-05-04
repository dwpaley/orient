#!/usr/local/bin/python3

import proc_file, metric, write_ins
from subprocess import getoutput
from shutil import move, copyfile
from sys import argv
from re import compile as re_compile
from tempfile import NamedTemporaryFile



banner = '''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

                                    Orient 

                              Daniel W. Paley
                            dwp2111@columbia.edu

||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''

failBanner = '''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

ShelXL refinement failed with the output shown above.
Please modify your ins file and run again.
'''

startText = '''
Fragment: \t\t\t{frag}
Centroid xyz: \t\t\t{x:.3f} {y:.3f} {z:.3f}
Trials: \t\t\t{trials}
Max. translation:\t\t{shift} A
Uiso for oriented fragment: \t{uiso}
Afix code for fragment: \t{frag}{afix}

ctrl-C to end at any time

Any key to start
'''



def cleanup(fileName, CLtext):
    '''
    clean up by copying best to name_or.ins, refining one more time, 
    then deleting the dummy atoms from the res file
    '''

    move(fileName + '_best', fileName + '_or.ins')
    getoutput(CLtext)
    res = fileName + '_or.res'
    with NamedTemporaryFile(mode='w', delete=False) as tmp, \
            open(res) as f:
        for line in f.readlines():
            if not (line.startswith('!!ornt') or
                    line.startswith('CENT') or
                    line.startswith('PIVT') or
                    line.startswith('PERP') or
                    '!!' in line):

                tmp.write(line)
    move(tmp.name, res) 
    print('\nOutput is written to {}'.format(res))


def main(fileName):
    copyfile(fileName + '.hkl', fileName + '_or.hkl')
    CLtext = 'shelxl {}_or'.format(fileName)
    r1SearchExp = re_compile(r'R1 = +([0-9.]+) +for')

    matrices = metric.make_matrices(fileName + '.ins') 
    template, orientArgs = proc_file.proc_file(fileName)
    
    input(startText.format(**vars(orientArgs)))

    best, n = 1, 0 
    try:
        for tr in range(orientArgs.trials):
            write_ins.write_ins(template, orientArgs, matrices, fileName)
            shelxlOut = getoutput(CLtext)
            try:
                r1 = float(r1SearchExp.search(shelxlOut).group(1))
            except AttributeError:
                r1 = 1
            if r1 < best:
                n += 1
                best = r1
                copyfile(fileName + '_or.ins', fileName + '_best')
            print('Trial {}\nCurrent R1={}\nBest R1={}\n'
                    .format(tr + 1, r1, best))
    except KeyboardInterrupt:
        pass

    if r1 == 1:
        print(getoutput(CLtext))
        print(failBanner)
    else:
        cleanup(fileName, CLtext)


if __name__ == '__main__':
    print(banner)
    if len(argv) == 1:
        print('\nUsage:\n\n\t$ orient <name> \n\nto process <name>.ins. For '
                'full documentation: \n\n\t$ orient --help')
    elif '--help' in sys.argv:
        import README
        print(README.text)
    else:
        main(argv[1])







