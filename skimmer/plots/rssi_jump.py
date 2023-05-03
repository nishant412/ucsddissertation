import matplotlib
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter,AutoMinorLocator
from matplotlib.patches import Rectangle
from matplotlib import rc
from sys import argv,stdin
from numpy import convolve, repeat, array
#matplotlib.rc("font", family="Helvetica Neue")
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rc("text", usetex="false")


WINDOW = 5
x = []
y = []
with open('rssi_jump.csv','rb') as csvfile:
	csvreader =csv.reader(csvfile,delimiter=',')
	for row in csvreader:
		x.append(float(row[0]))
		y.append(int(row[1]))

print x 
print y
del x[18]
del y[18]
kernel = repeat(1.0/WINDOW, WINDOW)
y_conv = convolve(array(y), kernel, 'valid')

print len(x)
print len(y_conv)
fig,ax = plt.subplots(figsize=(8,3))
ax.axvline(242.39599999971688,linestyle='--',color='0.5',linewidth=1.0,label='Dispenser opened')
ax.text(245.39599999971688,-45,'Dispenser opened',rotation=90,fontsize=13)
ax.axvline(0.0,-45,linestyle='--',color='0.50',linewidth=0.35,label='Enter gas station')
ax.text(3.0,-50,'Enter station',rotation=90,fontsize=13)
ax.set_xticks([0,50,100,150,200,250,300])
ax.set_xticklabels(['0','50','100','150','200','250','300'])
ax.set_xlim(0,300)
ax.set_yticks([-80,-70,-60,-50,-40])
ax.set_yticklabels(['-80','-70','-60','-50','-40'])
ax.set_ylim(-80,-40)
ax.tick_params(axis='both', which='major',direction='out', labelsize=16,pad=-5.0)
ax.tick_params(top='off',right='off')
ax.set_xlabel('Time (seconds)',fontsize=16)
ax.set_ylabel('RSSI',fontsize=16)
ax.xaxis.labelpad = 10
ax.yaxis.labelpad = 10
ax.grid(linewidth=0.5)
ax.plot(x[0:24],y_conv, color='#2c7fb8',linewidth=2.0)
fig.set_dpi(300)
fig.savefig('rssi_jump.pdf',bbox_inches ='tight')
