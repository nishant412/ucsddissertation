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
import math
import re
#matplotlib.rc("font", family="Helvetica Neue")
#matplotlib.rcParams['pdf.fonttype'] = 42
#matplotlib.rc("text", usetex="true")
plt.rcParams.update({"text.usetex": True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})


WINDOW = 5
cfo_x = []
cfo = []
iq_x = []
iq = []
temp_x = []
temp = []
timevals = []
room_temp = []
room_temp_x = []
phone_dict = {}
heights = []
tickvals = []

with open('snr_vals.csv','r') as snrfile:
    snr_reader=csv.reader(snrfile,delimiter=',')
    for row in snr_reader:
        if row[3] in phone_dict:
            phone_dict[row[3]].append(float(row[1]))
        else:
            phone_dict[row[3]] = []
            phone_dict[row[3]].append(float(row[1]))


#print phone_dict.keys()
for phone in phone_dict:
    snr_avg = sum(phone_dict[phone])/len(phone_dict[phone])
    tickvals.append(phone)
    heights.append(snr_avg)
    
#for i in range(snr_avg):
sort_tickvals = [x for _, x in sorted(zip(heights,tickvals),reverse=True)]
sort_heights = heights.sort(reverse=True)

print (heights)
#print sort_tickvals

for tick in sort_tickvals:
    if re.search(r'iPhone 8',tick):
        tick +="\niOS 14"
    if tick=='Pixel 5':
        tick +='\nAndroid 11'
    if tick=='Pixel 2':
        tick += '\nAndroid 11'
    if tick=='Pixel 1':
        tick += '\nAndroid 10'
    if tick=='Moto G6':
        tick += '\nAndroid 9'

print (sort_tickvals)
#fig,(ax,ax3) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3,1]},figsize=(6,5))
fig,ax = plt.subplots(figsize=(6,3))
fmt = matplotlib.ticker.StrMethodFormatter("{x:,.3f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
ax.xaxis.set_major_formatter(fmt1)
ax.yaxis.set_major_formatter(fmt1)
ax.tick_params(top='off',right='off')
ax.tick_params(axis='both',labelsize=12)
#ax.set_xlim(0,15)
#ax.set_ylim(ax.get_ylim()[::-1])
ax.set_ylim(0,40)
#ax.set_xlabel(r'Time(min)',fontsize=16)
ax.set_ylabel(r'SNR(dB)',fontsize=16,color='#581845')
#ax.axes.xaxis.set_visible(False)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
#ax.grid(linewidth=0.5)
#line1 = ax.plot(cfo_x,np.ma.masked_where(cfo_n == 0.0, cfo_n), color='#2c7fb8',linewidth=1.0,label='CFO')
#line1 = ax.plot(cfo_x,np.ma.masked_where(cfo_n == 0.0, cfo_n), color='#ff0000',linewidth=2.0,label='CFO')
ax.bar(range(len(sort_tickvals)),heights,color='#5d6d7e')
ax.set_xticks(range(len(tickvals)))
ax.set_xticklabels([r'iPhone 8'+'\n'+r'iOS 14',r'Moto G6'+'\n'+r'Android 9',r'Pixel 5'+'\n'+r'Android 11',r'Pixel 2'+'\n'+r'Android 11',r'Pixel 1'+'\n'+r'Android 10'],fontsize=12)

'''
ax2 = ax.twinx()
ax2.tick_params(top='off',left='off',bottom='off')
ax2.set_ylim(-0.06,0.06)
ax2.set_xlabel(r'Time(min)',fontsize=16)
ax2.set_ylabel(r'I/Q Offset',fontsize=16,color='#2c7fb8')
#ax2.xaxis.labelpad = 10
#ax2.yaxis.labelpad = 10
#ax.grid(linewidth=0.5)
line2=ax2.plot(iq_x,np.ma.masked_where(iq_n == 0.0, iq_n), color='#2c7fb8',linewidth=1.0,label=r'IQoffset')
#line4=ax1.plot(iq_x[63:],iq_conv, color='#2c7fb8',linewidth=1.0,label=r'IQoffset')
ax2.axes.xaxis.set_visible(False)

lns = line1+line2
labs = [l.get_label() for l in lns]
#ax.legend(lns,labs,loc='upper left',frameon=False,fontsize=12)
ax.axvline(x = 12,color='#581845',linewidth=1.0,linestyle='--')
ax.axvline(x = 0.1,color='#581845',linewidth=1.0,linestyle='--')

trans = ax.get_xaxis_transform()
ax.annotate(r'Start Game',xy=(0.1,1.125),xycoords=trans,ha='center',va='top',fontsize=12)
ax.plot([0.1,0.1],[1.0,1.05],transform=trans,color='#581845',linewidth=1.0,linestyle='--',clip_on=False)
ax.annotate(r'Stop Game',xy=(12.0,1.125),xycoords=trans,ha='center',va='top',fontsize=12)
ax.plot([12.0,12.0],[1.0,1.05],transform=trans,color='#581845',linewidth=1.0,linestyle='--',clip_on=False)
#ax.text(12.1,5,r'Stop',fontsize=12)
#ax.text(12.1,5.75,r'Game',fontsize=12)

#ax.text(0.2,5,r'Start',fontsize=12)
#ax.text(0.2,5.75,r'Game',fontsize=12)
#ax.text(12.5,-1.0,r'Playing',rotation=90)
ax3.set_xlim(0,15)
ax3.set_ylim(26,42)
ax3.plot(temp_x,temp,linewidth=2.0,label=r'PMIC temperature',color='#581845')
ax3.set_xlabel(r'Time(min)',fontsize=16)
ax3.set_ylabel(r'Temp($^{\circ}$C)',fontsize=16)
ax3.axvline(x = 12,color='#581845',linewidth=1.0,linestyle='--')
ax3.axvline(x = 0.1,color='#581845',linewidth=1.0,linestyle='--')
'''
#fig.subplots_adjust(hspace=0.05)
# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
fig.set_dpi(300)
fig.savefig('bar_plot.pdf',bbox_inches ='tight')

