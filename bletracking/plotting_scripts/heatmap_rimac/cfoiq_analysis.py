import csv
import re
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.image import NonUniformImage
import matplotlib.patches as patches
import matplotlib

#matplotlib.rcParams['pdf.fonttype'] = 42
#matplotlib.rc("text", usetex="true")
#matplotlib.rc(
plt.rcParams.update({"text.usetex": True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})

mac_master = {}

with open('rimac_times.csv','r') as csvfile:
	csvreader = csv.reader(csvfile,delimiter=',')
	for elmt in csvreader:
		if elmt[0] not in mac_master:
			mac_master[elmt[0]] = float(elmt[1])


cfo = []
iq = []
total_packets = 0

'''
with open('cfoiq_rimac2.csv','rb') as infile:
	csvreader=csv.reader(infile,delimiter=',')
	for row in csvreader:
		cfo.append(float(row[0])/1000.0)
		iq.append(float(row[1]))
		total_packets += int(row[2])

with open('cfoiq_rimac_2.csv','rb') as infile:
	csvreader=csv.reader(infile,delimiter=',')
	for row in csvreader:
		cfo.append(float(row[0])/1000.0)
		iq.append(float(row[1]))
		total_packets += int(row[2])
'''
mac_string = ''
with open('cfoiq_rimac_withmac_day1.csv','r') as infile:
	csvreader=csv.reader(infile,delimiter=',')
	for row in csvreader:
		for i in range (3,9):
			mac_string += '{:x}'.format(int(row[i]))
		
		if mac_string in mac_master:
			if (mac_master[mac_string] <= 180.0):
				cfo.append(float(row[0])/1000.0)
				iq.append(float(row[1]))
				total_packets += int(row[2])
		
		mac_string = ''

with open('cfoiq_rimac_withmac.csv','r') as infile:
	csvreader=csv.reader(infile,delimiter=',')
	for row in csvreader:
		for i in range (3,9):
			mac_string += '{:x}'.format(int(row[i]))
		
		if mac_string in mac_master:
			if (mac_master[mac_string] <= 180.0):
				cfo.append(float(row[0])/1000.0)
				iq.append(float(row[1]))
				total_packets += int(row[2])
		
		mac_string = ''

	
print ("total_packets:",total_packets)
print (max(cfo))
print (min(cfo))
print (max(iq))
print (min(iq))
print ("Number of MAC addresses", len(cfo))
#print sum(cfo)/float(len(cfo))
#print sum(iq)/float(len(iq))
print (np.mean(cfo))
print (np.mean(iq))
'''
fig,ax = plt.subplots(figsize=(100,20),dpi=100)
ax.scatter(cfo,iq,color='#116aaf',marker='x')
ax.set_xlim(-33.0,36.0)

ax.grid(True,'major','both',linestyle='-',color='#a6a6a6')
ax.grid(True,'minor','both',linestyle=':',color='#a6a6a6')
ax.minorticks_on()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks(np.arange(-33.0, 36.0, 1.0))
ax.tick_params(axis='both',which='both',direction='out',top='off',right='off')
ax.set_xlabel("CFO (KHz)",fontsize=18)
ax.set_ylabel("IQ offset",fontsize=18)
ax.xaxis.set_minor_locator(AutoMinorLocator(10))

fig.savefig("cfo_iq_scatter2.pdf",bbox_inches='tight')
'''
heatmap, xedges, yedges = np.histogram2d(cfo,iq,bins=50)
extent = [xedges[0],xedges[-1],yedges[0],yedges[-1]]

#np.set_printoptions(threshold=np.inf)
#print heatmap.shape
#print heatmap.size
mean_cfo = np.mean(cfo)
mean_iq = np.mean(iq)
mean_cfo_bin = 0
mean_iq_bin = 0
print (extent)
print ('xedges',xedges)
print ('yedges',yedges)
for i in range(0,len(xedges)):
	if (xedges[i] > mean_cfo):
		mean_cfo_bin = i
		break

for i in range(0,len(yedges)):
	if (yedges[i] > mean_iq):
		mean_iq_bin = i
		break

#print heatmap
#print "heatmap", heatmap[mean_cfo_bin][mean_iq_bin]
#print "heatmap.t", heatmap.T[mean_iq_bin][mean_cfo_bin]
print ("sum:",np.sum(heatmap.T))
print ("floor:",math.floor(np.sum(heatmap.T)*2/3))
#print "center_coords",(mean_cfo_bin,mean_iq_bin)

#fig.savefig(heatmap.T, extent=extent, origin='lower')
#print plt.colormaps()
print ("Mean bins", mean_cfo_bin, mean_iq_bin)
check_sum = 0.0 
 
for i in range(-9,10):
	for j in range(-9,10):
		check_sum += heatmap.T[mean_iq_bin+i][mean_cfo_bin+j]

print ("check_sum:",check_sum)


fig,ax = plt.subplots(figsize=(6,4))
histo_map = ax.imshow(heatmap.T,origin='lower',extent=extent,interpolation='nearest',aspect='auto',cmap=plt.get_cmap('gnuplot2_r'))
'''
histo_map = NonUniformImage(ax, interpolation='nearest',cmap=plt.get_cmap('gnuplot2_r'))
xcenters = (xedges[:-1] + xedges[1:]) / 2
ycenters = (yedges[:-1] + yedges[1:]) / 2
histo_map.set_data(xcenters, ycenters, heatmap.T)
ax.images.append(histo_map)
'''
#ax.set_aspect(1)
#c_x,c_y = ax.transData.transform((mean_cfo,mean_iq))
fmt = matplotlib.ticker.StrMethodFormatter("{x:,.3f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
ax.xaxis.set_major_formatter(fmt1)
ax.yaxis.set_major_formatter(fmt)

trans_point = (ax.transData + ax.transAxes.inverted()).transform((mean_cfo,mean_iq))

contour_33 = patches.Rectangle((xedges[22],yedges[15]), (xedges[-1]-xedges[0])/50*13,(yedges[-1]-yedges[0])/50*13, linestyle='dashed',linewidth=1.7,facecolor='none',edgecolor='k')
ax.add_patch(contour_33)
contour_66 = patches.Rectangle((xedges[18],yedges[11]), (xedges[-1]-xedges[0])/50*21,(yedges[-1]-yedges[0])/50*21, linestyle='dashed',linewidth=1.7,facecolor='none',edgecolor='k')
ax.add_patch(contour_66)
ax.text(xedges[22],yedges[28],r'36\%',fontsize=13,fontweight='semibold')
ax.text(xedges[18],yedges[33],r'66\%',fontsize=13,fontweight='semibold')
#theta = np.linspace(-np.pi,np.pi, 5)
#ax.plot(np.sin(theta),np.cos(theta))
ax.set_ylim(0.005,0.03)
ax.set_xlim(-36,36)
ax.tick_params(axis='both',labelsize=12)
cb = fig.colorbar(histo_map,ax=ax,ticks=[0.0,2.0,4.0,6.0,8.0,10.0,12.0])
cb.ax.yaxis.set_major_formatter(fmt1)
cb.set_label(label=r'\# of devices',fontsize=16)
cb.ax.tick_params(labelsize=12)
ax.set_xlabel(r'CFO (KHz)',fontsize=16)
ax.set_ylabel(r'I/Q offset magnitude',fontsize=16)
#plt.colormaps()
#plt.show()
#fig.artists.append(circle2)


fig.set_dpi(300)
fig.savefig("heatmap.pdf",bbox_inches='tight')

count1 = 0
count2 = 0

for elmt in heatmap:
	for elmt2 in elmt:
		if elmt2 == 1.0:
			count1 += 1
		if elmt2 == 2.0:
			count2 += 1

print ("Count1",count1)			 
print ("Count2",count2)			 

