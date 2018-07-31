Orient uses a Monte Carlo approach to fit a molecular fragment, defined in a
FRAG instruction, on a site with a known centroid. Typically, several dozen or
hundred random orientations of the molecule on the site are tested. The 
orientation that gives the best R1 is saved.


Orient is called with

$ orient <name> 

where the working directory contains <name>.ins and <name>.hkl.

The ins file is a standard ShelXL format file but should contain the following:

-A FRAG fragment in orthogonal coordinates (as obtained from the Idealized
Molecular Geometry Library, 
http://xray.chem.wisc.edu/Projects/IdealizedMolecularGeometry.html, or generated
by Olex2).

-A block of atoms to which the orient fragment will be fitted. You are 
responsible for setting the part and occupancy of these atoms and any other
settings, such as RESI name, that you wish to include. The occupancy must be
set on a PART line. The coordinates may be filled with zeroes.

-Surrounding these atoms, add instructions for the Orient run. Start with:

!!orient x y z [--shift=0] [--trials=100] [--frag=17] [--uiso=.05] [--afix=6]

and end with:

!!oend

The arguments x, y, and z give the centroid of the orient fragment. They are not
mandatory; if they are not included, the centroid will be taken from the atoms
you supply between !!orient and !!oend.

The optional arguments are the following: shift is a random translational shift 
of n angstroms (default 0) in case the centroid is not known accurately. 
Trials is the number of random orientations to test. Frag is the number of the 
FRAG fragment that will be oriented. (This may be changed in case you are using
other FRAG fragments at the same time.) Uiso is the isotropic adp for each atom
in the search fragment and may be set to a free variable, i.e. -u21, to set a 
group isotropic ADP. Afix is the /n/ component of the AFIX code that will be
used for the search fragment. The default, 6, gives a rigid-body refinement, 
but 0 may be useful for a flexible fragment (maybe with restraints).

The number of trials needed depends on the size of the search fragment, the
point symmetry of the fragment, and the point symmetry of its crystallographic
site. In a very difficult scenario, with a molecule in point group C1 on a
general position and assuming a molecular "radius" of 4 A, it may require about
2000 trials to reach a 90% chance of a successful orientation. This number may
be scaled directly by the symmetry of the molecule, the symmetry of the site,
and the third power of the molecular radius. Thus, for toluene (point group C2v,
"radius" ~2 A) on an inversion center, we might expect 90% success in about 30
trials. However, the convergence of the orientation depends on the details of 
the molecule and site.

Set a cgls refinement with a small number of cycles; 10 typically works well.
Besides the centroid coordinates, it is often fine to omit the other run
parameters and use the defaults.

The following lines, when added to an ins file and called with $ orient <name>,
will run 30 trials to orient a toluene molecule on xyz = 0.5 0.5 0.5.

FRAG 17
C1  1	 1.198402 -0.033739  3.629224
C2  1	 1.201835 -0.000101  2.122450
C3  1	 0.001012 -0.000301  1.398484
C4  1	 0.000813 -0.000261  0.002140
C5  1	 1.208427  0.001721 -0.699221
C6  1	 2.412741  0.006115  0.007778
C7  1	 2.406015  0.006056  1.404106
FEND

!!orient .5 .5 .5 -t30 -f17 -s0
resi TOL 21
part -1 10.5
c1 1 0 0 0
c2 1 0 0 0
c3 1 0 0 0
c4 1 0 0 0
c5 1 0 0 0
c6 1 0 0 0
c7 1 0 0 0
part 0
resi 0
!!oend


Daniel W. Paley, Columbia Nano Initiative (Columbia University), 2018. 
Contact the author at dwp2111@columbia.edu.

This program is licensed under the GNU General Public License and is free for
anyone to use, copy, or modify. It may not be incorporated into proprietary
software. The full license is included in the file license.txt.
