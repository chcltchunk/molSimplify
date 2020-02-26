# @file namegen.py
#  Generates filenames
#
#  Written by JP Janet for HJK Group
#
#  Dpt of Chemical Engineering, MIT

from .structgen import *
from molSimplify.Scripts.molSimplify_io import *
import argparse
import sys
import os
import shutil
import itertools
import random

# Generates name for complex given core and ligands
#  @param core mol3D of core
#  @param ligs List of ligand names
#  @param ligoc List of ligand occurrences
#  @param args Namespace of arguments
#  @return Complex name


def name_complex(core, ligs, ligoc, args):
    center = core.getAtom(0).symbol()
    name = center + '_'
    if args.oxstate:
        ox = str(args.oxstate)
    else:
        ox = "0"
    name += "_ " + str(ox)
    if args.spin:
        spin = str(args.spin)
    else:
        spin = "0"
    name += "_ " + str(spin)
    for i, lig in enumerate(ligs):
        names += '_' + str(lig[:3]) + '-' + str(ligoc[i])
    names += "_"+str(spin)
    return name
