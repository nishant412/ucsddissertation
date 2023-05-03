#!/usr/bin/python

import sys

l = []
for line in sys.stdin:
	if (len(line.rstrip()) == 0): continue
	x = float(line)
	l.append(x)

l.sort()
print l[0], 0.0
for idx in range(0,len(l)):
	if (idx == (len(l)-1)):
		print l[idx],(idx+1)/float(len(l))
	else:
		if (l[idx] != l[idx+1]):
			print l[idx],(idx+1)/float(len(l))
			print l[idx+1],(idx+1)/float(len(l))
