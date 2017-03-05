#!/usr/bin/python
#################################################################
# List-pocket-residues.py - created by Manoel Barrionuevo - 2016#
#################################################################
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

import sys, time, os, shutil
import pymol
from pymol import cmd, stored
pymol.finish_launching()

#################################################################

p = sys.argv[1]

def pdb_listing(p):
        # Creating list of present pdbs
        dirs = os.listdir(p)
        lista = []
        for files in dirs:
           if files.endswith(".pdb"):
              lista.append(files)
        lista.sort()
        return lista

# Calling pdb_listing to get a list of pdb files to work with

pdbs = []
pdbs = pdb_listing(p)

# Getting list of residues for each pocket in each pdb

index=0
for index in range(len(pdbs)):
        pymol.cmd.load(pdbs[index])
        pymol.cmd.remove("chain B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+X+Y+Z")
        pymol.cmd.remove("solvent")
        pymol.cmd.select("zincos", "symbol ZN")
        pymol.cmd.select("pocket", "all within 7.5 of zincos")
        stored.list = []
        pymol.cmd.iterate("(n. ca & pocket)","stored.list.append(resi)")
        print pdbs[index]
        print stored.list
        pymol.cmd.remove("all")
        pymol.cmd.delete("all")

# Get out!
pymol.cmd.quit()

# Ends everything

print " "
print "Great, everything ran smoothly. Have a good one! :D"
print " "
quit()
