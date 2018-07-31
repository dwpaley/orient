import numpy as np
import randpts
import argparse
import re
import pdb

atomRE = re.compile(
        r'([A-Za-z]\S*\s+\d+)\s+' #atom name and sfac number
        r'([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+).*') #x, y, z
shelxWords = ['ABIN', 'ACTA', 'AFIX', 'ANIS', 'ANSC', 'ANSR', 'BASF', 
        'BIND', 'BLOC', 'BOND', 'BUMP', 'CELL', 'CGLS', 'CHIV', 'CONF', 
        'CONN', 'DAMP', 'DANG', 'DEFS', 'DELU', 'DFIX', 'DISP', 'EADP', 
        'END', 'EQIV', 'EXTI', 'EXYZ', 'FEND', 'FLAT', 'FMAP', 'FRAG', 
        'FREE', 'FVAR', 'GRID', 'HFIX', 'HKLF', 'HTAB', 'ISOR', 'LATT', 
        'LAUE', 'LIST', 'L.S.', 'MERG', 'MORE', 'MOVE', 'MPLA', 'NCSY', 
        'NEUT', 'OMIT', 'PART', 'PLAN', 'PRIG', 'REM', 'RESI', 'RIGU', 
        'RTAB', 'SADI', 'SAME', 'SFAC', 'SHEL', 'SIMU', 'SIZE', 'SPEC', 
        'STIR', 'SUMP', 'SWAT', 'SYMM', 'TEMP', 'TITL', 'TWIN', 'TWST', 
        'UNIT', 'WGHT', 'WIGL', 'WPDB', 'XNPD', 'ZERR'] 

def parse_instructions(line):
    '''
    Parses a line such as '!!orient 0 0 0 --shift=2 --trials=7200 --frag=17'
    and returns a Namespace of all the arguments.
    '''
    parser=argparse.ArgumentParser()
    parser.add_argument('x', type=float, default=None)
    parser.add_argument('y', type=float, default=None)
    parser.add_argument('z', type=float, default=None) 
    parser.add_argument('-t', '--trials', default=100, type=int)
    parser.add_argument('-s', '--shift', default=0, type=float)
    parser.add_argument('-f', '--frag', type=int, default=17)
    parser.add_argument('-u', '--uiso', type=float, default=0.05)
    parser.add_argument('-a', '--afix', default='6')
    args = parser.parse_args(line.split()[1:])
    return args


def make_frag(lines):
    '''
    takes all the lines in a FRAG block, including FRAG and FEND, as a list
    of newline-terminated strings. Changes the FRAG number to 99; adds three
    dummy atoms: one at the centroid and two 1A away at mutual right angles;
    and returns the new FRAG block as a list of strings.
    '''

    xyzArray = np.zeros(shape=(len(lines)-2, 3))
    for i in range(len(lines)-2):
        xyzArray[i] = lines[i+1].split()[2:5]
    cent = np.mean(xyzArray, axis=0)
    dum1 = cent + [1,0,0]
    dum2 = cent + [0,1,0]

    outLines = ['FRAG 99\n']
    for at in [cent, dum1, dum2]:
        outLines.append('C 1 {:.5f} {:.5f} {:.5f}\n'.format(*at))
    outLines += lines[1:-1]
    outLines.append('FEND\n')

    return outLines

def proc_frag(line, inFile):
    '''
    Takes a line containing the keyword FRAG that was just read from inFile.
    Reads further lines from inFile, writing them to outFile, until it reaches
    FEND. Saves the whole FRAG...FEND block to a dictionary fragDict.
    '''
    fragNumber = int(line.split()[1])
    fragLines = []
    while True:
        fragLines.append(line)
        if line.lower().startswith('fend'):
            break 
        line = inFile.readline()
    return fragNumber, fragLines


def proc_orient(line, inFile, fragDict):
    '''
    This is called when a line containing '!!orient' is read from inFile.
    It continues reading inFile until reaching the line '!!oend'. It parses the
    arguments on the !!orient line, adds lines for the dummy atoms used to 
    orient the fragment, and then stores the rest of the lines in the !!orient
    block. If the centroid coordinates were not given, it calculates them from
    the atoms it reads. It returns a template with placeholders for the dummy
    atoms and a Namespace containing the !!orient arguments.
    '''

    # Process the !!orient line. Find the correct FRAG block from fragDict and
    # add dummy atoms to it. Store this modified FRAG block.
    orientArgs = parse_instructions(line)
    fragLines = make_frag(fragDict[orientArgs.frag])

    dummyAtoms = ['afix 99{}\n'.format(orientArgs.afix),
            'REM !! To remove the dummy atoms while preserving the rest of\n'
            'REM !! the model, simply refine this model in ShelXL and delete\n'
            'REM !! the lines from here through "PERP 1 ..." from the \n'
            'REM !! resulting .res file.\n'
            'part -1 10.0 !!ornt\n',
            'cent 1 cent_xyz 10 10.02 !!ornt\n',
            'pivt 1 pivt_xyz 10 10.02 !!ornt\n',
            'perp 1 perp_xyz 10 10.02 !!ornt\n']

    # Read and process lines until !!oend. Atoms are saved to atomMatchList and 
    # their coordinates are changed to 0 0 0. All other lines are unchanged.
    # All lines are written to the list orientLines. 
    atomMatchList, orientLines = [], []
    while True:
        atomMatch = atomRE.match(line)
        if atomMatch and not line[0].upper() in shelxWords: 
            atomMatchList.append(atomMatch)
            line = atomMatch.group(1) + ' 0 0 0 11 {}\n'.format(orientArgs.uiso)
        if line.lower().startswith('!!oend'):
            orientLines.append('afix 0\n')
            break
        orientLines.append(line)
        line = inFile.readline()

    # If the centroid was given on the !!orient line, then we name it here;
    # otherwise calculate it from the atoms within the orient...oend block.
    # If the centroid is on 0,0,0 then we nudge it slightly so that ShelXL
    # treats it as a real position.
    if orientArgs.x is not None: 
        cent = np.array([orientArgs.x, orientArgs.y, orientArgs.z])
    else:
        xyzArray = np.zeros(shape=(len(atomMatchList), 3))
        for i in range(len(atomMatchList)):
            xyzArray[i] = [atomMatchList[i].group(j) for j in range(2, 5)]
        cent = np.mean(xyzArray, axis=0)
    if np.linalg.norm(cent) < 0.001: cent += [.001, .001, .001]
    orientArgs.cent = cent


    outLines = fragLines + dummyAtoms + orientLines 
    return outLines, orientArgs
    

def proc_file(fileName):
    '''
    Reads an ins file and prepares an orient template with placeholders to
    randomize the orient fragment. Returns the template and the run parameters
    from the !!orient line.
    '''

    inFile = open(fileName + '.ins')
    outFile = open(fileName + '_or.ins', 'w') 
    fragDict = dict()
    template = []

    line = inFile.readline()
    while line:
        if line.lower().startswith('frag'):
            fragNumber, fragLines = proc_frag(line, inFile)
            template += fragLines
            fragDict[fragNumber] = fragLines
        elif line.lower().startswith('!!orient'):
            orientLines, orientArgs = proc_orient(line, inFile, fragDict)
            template += orientLines
        else:
            template.append(line)
        line = inFile.readline() 

    inFile.close()
    return template, orientArgs

