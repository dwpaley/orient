basic notes on orient:

Usage:

Call with

$ orient <name> ntrial [maxshift]

where the working directory contains <name>.ins and <name>.hkl; ntrial is the
number of trials to run, and maxshift is a random translational shift for the 
search fragment up to the given # in angstroms (defaults to 0).


The following setup is required first: 

Make a frag file beginning with the following 3 dummy atoms:
Atom 1 is at the centroid of the fragment
Atom 2 should either (1) be 1 A away from Atom 1; or (2) should be collocated
 with a real pivot atom that will define a rotation axis CENT-PIVT for a 2d  
 rotation search.
Atom 3 should be 1 A away from Atom 1, such that ang(Atom 3-Atom 1-Atom 2) 
 = 90 deg.
The remaining atoms are the real fragment in any order.


Enter the search fragment created above between the tags frag 17/fend as normal. 
Next, find the centroid of the molecule to orient in the structure. Consider its 
coordinates to be x y z. Determine the correct part # (n) and sof for the
fragment you will be orienting. 
Then enter the following lines:

resi junk 999
afix 176
part n 10.0
CENT 1 x y z 10.0 10.02
dum1 1 XXXX
dum2 1 YYYY
part n sof
C1 1 0 0 0
C2 1 0 0 0
.
.
.
Cn 1 0 0 0 
part 0
afix 0
resi 0



Alternatively, for a rotation around an axis, use this format, ensuring that 
CENT and PIVT correspond to the atoms defined as Atom 1 and Atom 2 above.

resi junk 999
afix 176
part n 10.0
CENT 1 x y z 10.0 10.02
PIVT 1 x y z 10.0 10.02
dum2 1 YYYY
part n sof
C1 1 0 0 0 
C2 1 0 0 0
.
.
.
Cn 1 0 0 0
part 0
afix 0
resi 0



Set a cgls refinement with a small number of cycles; 10 typically works well.
3d rotation searches seem to converge in <100 trials and 2d rotation searches 
seem to converge in <20 trials. More trials will be needed if you use the 
random translational shift option (maybe up to about 500-1000?)

