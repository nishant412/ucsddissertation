import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import csv

no_skimmer = []
skimmer = []

with open("inoutdata_final.csv",'rb') as fd:
	for line in fd.readlines():
		line = line.rstrip('\r\n')
		row = line.split(',')
		no_skimmer.append(int(row[0]))
		if (row[1] != ''):
			skimmer.append(int(row[1]))

#print skimmer
#print no_skimmer

num_bins = 10
bin_vals = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210]

no_skimmer.sort()
x= []
y = []
x.append(no_skimmer[0])
y.append(0.0)
for idx in range(0,len(no_skimmer)):
	if(idx == (len(no_skimmer) - 1)):
		x.append(no_skimmer[idx])
		y.append((idx+1)/float(len(no_skimmer)))
	else:
		if(no_skimmer[idx] != no_skimmer[idx+1]):
			x.append(no_skimmer[idx])
			x.append(no_skimmer[idx+1])
			y.append((idx)/float(len(no_skimmer)))
			y.append((idx+1)/float(len(no_skimmer)))


fig,ax = plt.subplots(figsize=(8,3.5))
#ax.lines.Line2D(x,y,linewidth=1.0)
line = Line2D(x,y,linewidth=4.0,solid_capstyle='butt',solid_joinstyle = 'miter',drawstyle = 'steps')
ax.add_line(line)
#counts,bin_edges = np.histogram (no_skimmer,bins=bin_vals,normed=True)
#cdf = np.cumsum(counts)
#ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'No skimmer found')
'''
counts,bin_edges = np.histogram (skimmer,bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1], label = 'Skimmer found')
ax.legend(loc='right')
'''
xtics = [30*i for i in range(5)]
ytics = [0.1*i for i in range(11)]
ax.set_ylim(0,1.0)
#ax.grid(b=True, which='major', linestyle='-')
ax.set_xlabel('Inspection time (minutes at fuel station)',fontsize = 25)
ax.set_ylabel('CDF',fontsize=25)
ax.set_xlim(0,120)
ax.set_xticks(xtics)
ax.set_yticks(ytics)
plt.tick_params(axis='both', which='major', labelsize=20,pad = 10)
#plt.ylim(bottom=0,top=1)
#plt.xlim(0, max(skimmer)+20)

plt.savefig('cdf_timetaken_arizona.pdf',bbox_inches='tight')
#plt.show()

