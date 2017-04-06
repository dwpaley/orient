basic notes on orient:

Usage:
Make a frag file beginning with the following 3 dummy atoms:
Atom 1 is at the centroid of the fragment
Atom 2 should either (1) be 1 A away from Atom 1; or (2) should be collocated
 with a real pivot atom that will define a rotation axis CENT-PIVT for a 2d  
 rotation search.
Atom 3 should be 1 A away from Atom 1, such that ang(Atom 3-Atom 1-Atom 2) 
 = 90 deg.
The remaining atoms are the real fragment in any order.



Find the centroid of the molecule to orient in the structure. Enter the search
fragment between the tags frag 17/fend as normal. Then enter the following 
lines:

resi junk 999
afix 176
part n 10.0
CENT 1 x y z 10.0 10.02
dum1 1 XXXX
dum2 1 XXXX
part n sof
C1 1 0 0 0 sof .05
C2 1 0 0 0 sof .05
.
.
.
Cn 1 0 0 0 sof .05
resi 0
afix 0
part 0



Alternatively, for a rotation around an axis, use this format, ensuring that 
CENT and PIVT correspond to the atoms defined as Atom 1 and Atom 2 above.

resi junk 999
afix 176
part n 10.0
CENT 1 x y z 10.0 10.02
PIVT 1 x y z 10.0 10.02
dum2 1 XXXX
part n sof
C1 1 0 0 0 sof .05
C2 1 0 0 0 sof .05
.
.
.
Cn 1 0 0 0 sof .05
resi 0
afix 0
part 0



Set a cgls refinement with a small number of cycles; 10 typically works well.
Call the script with "orient structure.ins n" where n is the number of runs
you wish to perform. 3d rotation searches seem to converge in <100 trials and
2d rotation searches seem to converge in <20 trials.

Currently you will have to copy structure.hkl to structure_orient.hkl before
the refinement will run. 

Each refinement that produces a new best R1 factor will copy its ins file to 
structure.ins.onn where nn is the trial #. These can conveniently be copied to
structure_orient.ins and refined to see the result of a particular trial.


