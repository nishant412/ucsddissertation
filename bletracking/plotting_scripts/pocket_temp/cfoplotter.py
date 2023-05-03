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

with open('cfo.csv','r') as cfofile:
    csvreader = csv.reader(cfofile,delimiter=',')
    for row in csvreader:
        cfoval = float(row[0])/1000
        #iqval = float(row[1])
        if math.isnan(cfoval):
            cfo.append(0.0)
        else:
            cfo.append(cfoval)
        #if math.isnan(iqval):
            #iq.append(0.0)
        #else:
            #iq.append(iqval)

with open('iq.csv','r') as iqfile:
    csvreader = csv.reader(iqfile,delimiter=',')
    for row in csvreader:
        iqval = float(row[0])
        if math.isnan(iqval):
            iq.append(0.0)
        else:
            iq.append(iqval)

cfo_t = np.array(cfo)
iq_t = np.array(iq)

for i in range(0,len(cfo_t)):
    if (i>0):
        if(cfo_t[i] == 0.0 or (cfo_t[i]-cfo_t[i-1] > 2.0)):
            cfo_t[i] = cfo_t[i-1]
        if(iq_t[i] == 0.0):
            iq_t[i] = iq_t[i-1]

with open('times_overlap.csv','r') as timefile:
    csvreader = csv.reader(timefile,delimiter=',')
    for row in csvreader:
        timeval = int(row[0])
        timevals.append(timeval*0.625/60000)

for i in range(len(timevals)):
    if (timevals[i] > 1.0) :
        cfo_x.append(timevals[i] - 1.0)
        iq_x.append(timevals[i] - 1.0)

timelen = len(cfo_t) - len(cfo_x)

cfo_n = cfo_t[timelen:]
iq_n = iq_t[timelen:]

kernel=repeat(1.0/64, 64)
iq_conv = convolve(iq_n, kernel, 'valid')

last_temp = 0.0
with open('temp17','r') as tempfile:
    csvreader = csv.reader(tempfile,delimiter=',')
    for row in csvreader:
        temp.append(float(row[0])/1000.0)
        last_temp = float(row[0])/1000.0

temp.append(last_temp)

for i in range(len(temp)):
    #if i < 106:
    temp_x.append(i*10/60.0)

'''
with open('room_temp','rb') as tempfile:
    csvreader = csv.reader(tempfile,delimiter=',')
    for row in csvreader:
        room_temp.append(float(row[0]))

for i in range(len(room_temp)):
    #if i < 106:
    room_temp_x.append(i*30/60.0)
#temp = temp[0:90]
'''
'''
with open('iq_offset','rb') as iqfile:
    csvreader = csv.reader(iqfile,delimiter=',')
    for row in csvreader:
        iqval = float(row[0])
        if math.isnan(iqval):
            iq.append(0.0)
        else:
            iq.append(iqval)
iq_n = np.array(iq)
'''
'''
print x 
print y
del x[18]
del y[18]
kernel = repeat(1.0/WINDOW, WINDOW)
y_conv = convolve(array(y), kernel, 'valid')
print len(x)
print len(y_conv)
'''

'''
fig,ax = plt.subplots(figsize=(6,3))
#fig.suptitle(r'Game',fontsize=16)
#ax.axvline(242.39599999971688,linestyle='--',color='0.5',linewidth=1.0,label='Dispenser opened')
#ax.text(245.39599999971688,-45,'Dispenser opened',rotation=90,fontsize=13)
#ax.axvline(0.0,-45,linestyle='--',color='0.50',linewidth=0.35,label='Enter gas station')
#ax.text(3.0,-50,'Enter station',rotation=90,fontsize=13)
#ax.set_xticks([0,50,100,150,200,250,300])
#ax.set_xticklabels(['0','50','100','150','200','250','300'])
#ax.set_xlim(0,300)
#ax.set_yticks([-80,-70,-60,-50,-40])
#ax.set_yticklabels(['-80','-70','-60','-50','-40'])
#ax.set_ylim(-80,-40)
#ax.tick_params(axis='both', which='major',direction='out', labelsize=16,pad=-5.0)
ax.tick_params(top='off',right='off')
ax.set_xlim(0,15)
#ax.set_ylim(ax.get_ylim()[::-1])
ax.set_ylim(7,-7)
ax.set_xlabel(r'Time(sec)$\longrightarrow$',fontsize=16)
ax.set_ylabel(r'$\longleftarrow$CFO(KHz)',fontsize=16,)
ax.xaxis.labelpad = 10
ax.yaxis.labelpad = 10
#ax.grid(linewidth=0.5)
#line1 = ax.plot(cfo_x,np.ma.masked_where(cfo_n == 0.0, cfo_n), color='#2c7fb8',linewidth=1.0,label='CFO')
line1 = ax.plot(cfo_x,np.ma.masked_where(cfo_n == 0.0, cfo_n), color='#ff0000',linewidth=2.0,label='CFO')

ax2 = ax.twinx()
ax2.tick_params(top='off',left='off')
ax2.set_ylim(20,50)
ax2.set_ylabel(r'Temperature (\textdegree C)$\longrightarrow$',fontsize=16)
ax2.yaxis.labelpad = 10
#line2 = ax2.plot(temp_x,temp, color='#581845',linewidth=1.0,linestyle='--',label=r'PMIC Temp')
line2 = ax2.plot(temp_x,temp, color='#581845',linewidth=1.0,linestyle='--',label=r'PMIC Temp')

line3 = ax2.plot(room_temp_x,room_temp, color='#ff0000',linewidth=1.0,linestyle='--',label=r'Room Temp')

lns = line1+line2+line3
labs = [l.get_label() for l in lns]
ax.legend(lns,labs,loc='upper left',frameon=False)
fig.set_dpi(300)
fig.savefig('cfo_plot.pdf',bbox_inches ='tight')

fig1,ax1 = plt.subplots(figsize=(6,3))
ax1.tick_params(top='off',right='off')
ax1.set_xlim(0,15)
#ax1.set_ylim(ax1.get_ylim()[::-1])
ax1.set_ylim(0.06,-0.06)
ax1.set_xlabel(r'Time(min)$\longrightarrow$',fontsize=16)
ax1.set_ylabel(r'$\longleftarrow$I/Q Offset',fontsize=16)
ax1.xaxis.labelpad = 10
ax1.yaxis.labelpad = 10
#ax.grid(linewidth=0.5)
line4=ax1.plot(iq_x,np.ma.masked_where(iq_n == 0.0, iq_n), color='#2c7fb8',linewidth=1.0,label=r'IQoffset')
#line4=ax1.plot(iq_x[63:],iq_conv, color='#2c7fb8',linewidth=1.0,label=r'IQoffset')

ax3 = ax1.twinx()
ax3.tick_params(top='off',left='off')
ax3.set_ylim(20,45)
ax3.set_ylabel(r'Temperature(C)$\longrightarrow$',fontsize=16)
ax3.yaxis.labelpad = 10
line5=ax3.plot(temp_x,temp, color='#581845',linewidth=1.0,linestyle='--',label='PMIC Temp')
line6 = ax3.plot(room_temp_x,room_temp, color='#ff0000',linewidth=1.0,linestyle='--',label=r'Room Temp')

lns = line4+line5+line6
labs = [l.get_label() for l in lns]
ax1.legend(lns,labs,loc='upper left',frameon=False)

fig1.set_dpi(300)
fig1.savefig('iq_plot.pdf',bbox_inches ='tight')
'''

#fig,ax = plt.subplots(figsize=(6,3))
fig,(ax,ax3) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3,1]},figsize=(6,5))
fmt = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.2f}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt)
ax3.yaxis.set_major_formatter(fmt)
ax3.xaxis.set_major_formatter(fmt)

ax.tick_params(top='off',right='off')
ax.tick_params(axis='both',labelsize=12)
ax3.tick_params(axis='both',labelsize=12)
ax.set_xlim(0,15)
#ax.set_ylim(ax.get_ylim()[::-1])
ax.set_ylim(-6,6)
ax.set_xlabel(r'Time(min)',fontsize=16)
ax.set_ylabel(r'CFO(KHz)',fontsize=16,color='#ff0000')
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
#ax.grid(linewidth=0.5)
#line1 = ax.plot(cfo_x,np.ma.masked_where(cfo_n == 0.0, cfo_n), color='#2c7fb8',linewidth=1.0,label='CFO')
line1 = ax.plot(cfo_x,np.ma.masked_where(cfo_n == 0.0, cfo_n), color='#ff0000',linewidth=2.0,label='CFO')
ax.axes.xaxis.set_visible(False)

ax2 = ax.twinx()
ax2.yaxis.set_major_formatter(fmt1)
ax2.tick_params(top='off',left='off')
ax2.tick_params(axis='both',labelsize=12)
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
#ax.legend(lns,labs,loc='upper right',frameon=False,fontsize=12)
ax.axvline(x = 8.5,color='#581845',linewidth=1.0,linestyle='--')
ax.axvline(x = 1.15,color='#581845',linewidth=1.0,linestyle='--')

trans = ax.get_xaxis_transform()
ax.annotate(r'Put in pocket',xy=(1.15,1.125),xycoords=trans,ha='center',va='top',fontsize=13)
ax.plot([1.15,1.15],[1.0,1.05],transform=trans,color='#581845',linewidth=1.0,linestyle='--',clip_on=False)
ax.annotate(r'Put on table',xy=(8.15,1.125),xycoords=trans,ha='center',va='top',fontsize=13)
ax.plot([8.5,8.5],[1.0,1.05],transform=trans,color='#581845',linewidth=1.0,linestyle='--',clip_on=False)
#ax.text(12.1,5,r'Stop',fontsize=12)
#ax.text(12.1,5.75,r'Game',fontsize=12)

ax3.set_xlim(0,15)
ax3.set_ylim(26,42)
ax3.plot(temp_x,temp,linewidth=2.0,label=r'PMIC temperature',color='#581845')
ax3.set_xlabel(r'Time(min)',fontsize=16)
ax3.set_ylabel(r'Temp($^{\circ}$C)',fontsize=16)
ax3.axvline(x = 8.5,color='#581845',linewidth=1.0,linestyle='--')
ax3.axvline(x = 1.15,color='#581845',linewidth=1.0,linestyle='--')

#ax.text(0.2,5,r'Start',fontsize=12)
#ax.text(0.2,5.75,r'Game',fontsize=12)
#ax.text(12.5,-1.0,r'Playing',rotation=90)
fig.subplots_adjust(hspace=0.05)
fig.set_dpi(300)
fig.savefig('cfo_plot.pdf',bbox_inches ='tight')

