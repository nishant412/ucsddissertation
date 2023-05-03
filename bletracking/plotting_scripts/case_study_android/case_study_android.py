import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#from matplotlib import rc
import matplotlib.ticker
import numpy as np

plt.rcParams.update({"text.usetex":True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})


gt = pd.read_csv('groundtruth_android_2.csv').values;

det = pd.read_csv('detected_android_2.csv').values;

no_dev = pd.read_csv('no_dev_android.csv').values;

gt = gt[:,1:]

det = det[:,1:]
fig,ax = plt.subplots(figsize=(6,2))

fmt = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.2f}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt)

ax.tick_params(axis='x', which='major',direction='out', labelsize=12)
ax.tick_params(top='off',right='off')
ax.set_xlabel('Time (Minutes)',fontsize=16)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
ax.grid(linewidth=0.5)

i = 0
j=0
ax.plot([1/6*i,1/6*(i+1)],[1.5+j,1.5+j],'#ff0000')
ax.plot([1/6*i,1/6*(i+1)],[0.5+j,0.5+j],'#2c7fb8')
#ax.legend(['Detected','Groundtruth'],fontsize=16,frameon=False,loc=(0.02,0.34))

for i in range(1,len(gt)):
    if gt[i] == 1:
        for j in np.arange(0,0.2,0.02):
            ax.plot([1/6*i,1/6*(i+1)],[0.5+j,0.5+j],'#2c7fb8')
    if det[i] == 1:
        for j in np.arange(0,0.2,0.02):
            ax.plot([1/6*i,1/6*(i+1)],[1.5+j,1.5+j],'#ff0000')

ax.set_yticks([])
#ax.set_yticklabels(["","",""])
ax.set_xlim([0,60])
ax.set_ylim([0,2.25])
ax.text(0.3,0.8,r'Detected',transform=ax.transAxes,color='#ff0000',fontsize=13)
ax.text(0.3,0.35,r'Groundtruth',transform=ax.transAxes,color='#2c7fb8',fontsize=13)
fig.set_dpi(300)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
fig.savefig('case_study_android2.pdf',bbox_inches ='tight')


#matplotlib.rc("text", usetex="false")
fig1,ax1 = plt.subplots(figsize=(6,2))

fmt = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.2f}")
ax1.xaxis.set_major_formatter(fmt)
ax1.yaxis.set_major_formatter(fmt)

ax1.tick_params(axis='both', which='major',direction='out', labelsize=12)
ax1.tick_params(top='off',right='off')
ax1.set_xlabel(r'Time (Minutes)',fontsize=16)
ax1.set_ylabel(r'\# of devices',fontsize=16)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
ax1.grid(linewidth=0.5)
ax1.plot(1/6*np.arange(1,360)-1/12,no_dev,color='#2c7fb8')

ax1.set_xlim(0,60)
fig1.set_dpi(300)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')
fig1.savefig('case_study_android_devno2.pdf',bbox_inches ='tight')
