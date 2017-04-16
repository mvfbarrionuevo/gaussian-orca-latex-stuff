#!/usr/bin/python

import sys, os, getopt

def usage():
	print "I see you need some help, may I suggest you to call me as follow:.\n"
	print '    1) To calculate 'u'f\u207A(r) (electrophilicity):\n'
	print '      1.1) ./fukuisurf.py -p anion.cube,natural.cube\n\n'
	print '    2) To calculate 'u'f\u207B(r) (nucleophilicity):\n'
	print '      2.1) ./fukuisurf.py -m natural.cube,cation.cube\n\n'
	print '    3) To calculate 'u'f\u2070(r) (suceptibility to radical attack):\n'
	print '      3.1) ./fukuisurf.py -r anion.cube,cation.cube\n\n'
	print 'Please, follow the definition that:\n'
	print '   I) Natural = no electron perturbation;\n'
	print '  II) Cation  = electron perturbation by removal of 1 electron;\n'
	print ' III) Anion   = electron perturbation by adding of 1 electron;\n\n' 
	print "Have a nice one.\n"
	return True

def read_lines(files):
	read_lines = []
	with open(files) as lines_to_read:
		read_lines = lines_to_read.readlines()
	lines_to_read.close()
	return read_lines

def read_ele(list_ele, start, end):
	list_lines = []
	elemts = []
	for i in range(int(start),int(end)):
	   list_lines.append(list_ele[i].split())
	for i in list_lines:
	  for ele in i:
		elemts.append(ele)
	return elemts

def match_verify(first,second):
	itemsf = []
	itemss = []
	itemsf = read_ele(first, 2, 6)
	itemss = read_ele(second, 2, 6)
	for i in range(16):
		if not itemsf[i] == itemss[i]:
		  print "Line element "+itemsf[i]+" don't match with line element "+itemss[i]+".\n"
		  sys.exit(2)
	number_of_atoms = itemsf[0]
	return number_of_atoms

def list_columns(obj, cols=4, columnwise=True, gap=4):
    """
    Print the given list in evenly-spaced columns.

    Parameters
    ----------
    obj : list
        The list to be printed.
    cols : int
        The number of columns in which the list should be printed.
    columnwise : bool, default=True
        If True, the items in the list will be printed column-wise.
        If False the items in the list will be printed row-wise.
    gap : int
        The number of spaces that should separate the longest column
        item/s from the next column. This is the effective spacing
        between columns based on the maximum len() of the list items.
    """

    sobj = [str(item) for item in obj]
    if cols > len(sobj): cols = len(sobj)
    max_len = max([len(item) for item in sobj])
    if columnwise: cols = int(math.ceil(float(len(sobj)) / float(cols)))
    plist = [sobj[i: i+cols] for i in range(0, len(sobj), cols)]
    if columnwise:
        if not len(plist[-1]) == cols:
            plist[-1].extend(['']*(len(sobj) - len(plist[-1])))
        plist = zip(*plist)
    printer = '\n   '.join([
        ''.join([c.ljust(max_len + gap) for c in p])
        for p in plist])
    return printer

def do_fplus(number_of_atoms,anion,natural):
	lines = 0
    	for line in anion:
          lines += 1
	start = int(number_of_atoms)+6
	itemsf = read_ele(anion, start, lines)
	itemss = read_ele(natural, start, lines)
	new_itemsf = []
	new_itemss = []
	for item in itemsf:
		new_itemsf.append(float(item))
	for item in itemss:
		new_itemss.append(float(item))
	result = [a - b for a, b in zip(new_itemsf, new_itemss)]
	printer = list_columns(result, columnwise=False, cols=6, gap=3)
	with open("fplus_surface.cube", "a") as fplus:
		fplus.write('Cube file for f+(r) (electrophilicity) surface\nCreated by Manoel Barrionuevo 2017\n')
		for i in range(int(number_of_atoms)+4):
		  fplus.write(anion[i+2])
		fplus.write('   '+printer)
	fplus.close()
	return True

def do_fminus(number_of_atoms,natural,cation):
	lines = 0
    	for line in cation:
          lines += 1
	start = int(number_of_atoms)+6
	itemsf = read_ele(natural, start, lines)
	itemss = read_ele(cation, start, lines)
	new_itemsf = []
	new_itemss = []
	for item in itemsf:
		new_itemsf.append(float(item))
	for item in itemss:
		new_itemss.append(float(item))
	result = [a - b for a, b in zip(new_itemsf, new_itemss)]
	printer = list_columns(result, columnwise=False, cols=6, gap=3)
	with open("fminus_surface.cube", "a") as fplus:
		fplus.write('Cube file for f-(r) (nucleophilicity) surface\nCreated by Manoel Barrionuevo 2017\n')
		for i in range(int(number_of_atoms)+4):
		  fplus.write(natural[i+2])
		fplus.write('   '+printer)
	fplus.close()
	return True

def do_frad(number_of_atoms,anion,cation):
	lines = 0
    	for line in anion:
          lines += 1
	start = int(number_of_atoms)+6
	itemsf = read_ele(anion, start, lines)
	itemss = read_ele(cation, start, lines)
	new_itemsf = []
	new_itemss = []
	for item in itemsf:
		new_itemsf.append(float(item))
	for item in itemss:
		new_itemss.append(float(item))
	result = [(a - b)/2 for a, b in zip(new_itemsf, new_itemss)]
	printer = list_columns(result, columnwise=False, cols=6, gap=3)
	with open("fzero_surface.cube", "a") as fplus:
		fplus.write('Cube file for f0(r) (radical attack suceptibility) surface\nCreated by Manoel Barrionuevo 2017\n')
		for i in range(int(number_of_atoms)+4):
		  fplus.write(anion[i+2])
		fplus.write('   '+printer)
	fplus.close()
	return True

def fplus(files):
	print "You have chosen "+files[0]+" as anion and "+files[1]+" as natural.\n"
	print 'Orbital surface for 'u'f\u207A(r) calculation is going to be performed according to equation:\n'
	print '    'u'f\u207A(r) = rho(r)(N+1) - rho(r)(N)\n'
	anion = read_lines(files[0])
	natural = read_lines(files[1])
	number_of_atoms = match_verify(anion,natural)
	do_fplus(number_of_atoms,anion,natural)
	return True
	
def fminus(files):
	print "You have chosen "+files[0]+" as natural and "+files[1]+" as cation.\n"
	print 'Orbital surface for 'u'f\u207B(r) calculation is going to be performed according to equation:\n'
	print '    'u'f\u207B(r) = rho(r)(N) - rho(r)(N-1)\n'
	natural = read_lines(files[0])
	cation = read_lines(files[1])
	number_of_atoms = match_verify(natural,cation)
	do_fminus(number_of_atoms,natural,cation)
	return True

def fzero(files):
	print "You have chosen "+files[0]+" as anion and "+files[1]+" as cation.\n"
	print 'Orbital surface for 'u'f\u2070(r) calculation is going to be performed according to equation:\n'
	print '    'u'f\u2070(r) = [rho(r)(N+1) - rho(r)(N-1)]/2\n'
	anion = read_lines(files[0])
	cation = read_lines(files[1])
	number_of_atoms = match_verify(anion,cation)
	do_frad(number_of_atoms,anion,cation)
	return True

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hp:m:r:")
      if not opts:
	print "No options supplied.\n"
	usage()
	sys.exit(2)
   except getopt.GetoptError, msg:
      print '\nError: %s\n' % msg
      usage()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt == '-p':
	print 'You want to calculate 'u'f\u207A(r) (electrophilicity).'
        files = arg.split(",")
	fplus(files)
      elif opt == '-m':
	print 'You want to calculate 'u'f\u207B(r) (nucleophilicity).'
        files = arg.split(",")
	fminus(files)
      elif opt == '-r':
	print 'You want to calculate 'u'f\u2070(r) (radical suceptibility attack).'
        files = arg.split(",")
	fzero(files)
   print "\nThat's it, hope you now can plot it into PyMol. Have fun!\n"

if __name__ == "__main__":
   main(sys.argv[1:])
