#!/usr/bin/python
# Manoel Barrionuevo
# Plot calculate energy from gaussian optimization using *.log file generated by gaussian09

# Last updated : 06-03-2017

import matplotlib
import numpy as np
import sys, os, subprocess
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from math import pow
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

# ------------- GET INPUT FILE ------------- #	
if len(sys.argv) <= 1:
	name = raw_input("Please enter path to G09 output file: ")
else:
	name = sys.argv[1] 
# ------------------------------------------ #

# --------------- GREP ENERGY -------------- #	
os.system("grep -h 'SCF Done' "+name+" > "+name+".txt")
# ------------------------------------------ #


# ----------- GREP FUNCTION/BASIS ---------- #	

os.system("grep -h 'SCF Done' "+name+" | awk '{print $3}' | sed 's/E(R//g' | sed 's/)//g' | head -1 > "+name+".f")
ff = open(name+".f","r")
lines = ff.readlines()
ff.close()

func = []
for line in lines:
	t = line.split()
	func.append(t[0])
function = func[0].encode("ascii")

os.system("grep -o 'Standard basis:.*' "+name+" | sed 's/Standard basis://g' | head -1 > "+name+".b")
bb = open(name+".b","r")
lines = bb.readlines()
bb.close()

basi = []
for line in lines:
	t = line.split()
	basi.append(t[0])
basis = basi[0].encode("ascii")

# ------------------------------------------ #

# ---------------- GET DATA ---------------- #		
fo = open(name+".txt", "r")
lines = fo.readlines()
fo.close()

energy = []
point = []
scale = []
n = 0
for line in lines:
	t = line.split()
	n += 1	 
	point.append(n)
	energy.append(t[4])
scale.append(t[5]) 
escale = scale[0].encode("ascii")
# ------------------------------------------ #

# ------------- PLOTTING STUFF ------------- #			

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(point,energy, color='b',linestyle='-',marker='o',markersize='15',linewidth='1.2', antialiased=True)	
plt.title(r"Optimization by using "+str(function)+"/"+str(basis),fontsize=30, y=1.04)
plt.xlabel(r'Step', fontsize=30)
plt.ylabel(r'Energy ('+str(escale)+')', fontsize=30)
plt.tick_params(labelsize='30')
plt.xlim([min(point)-1,max(point)+1])
plt.xticks(np.arange(min(point),max(point)+1,1))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.grid(True)
plt.show()
# ------------------------------------------ #


# ------------- CLEANING STUFF ------------- #			
os.system("rm -rf "+name+".txt "+name+".f "+name+".b")
# ------------------------------------------ #
