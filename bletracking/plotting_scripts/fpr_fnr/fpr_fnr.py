import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#from matplotlib import rc
import matplotlib.ticker
import numpy as np

plt.rcParams.update({"text.usetex":True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})


fpr_targets = pd.read_csv('fpr_10sec_allpreviouspack.csv',header=None).values
fnr_targets = pd.read_csv('fnr_10sec_allpreviouspack.csv',header=None).values
test_dev_targets = pd.read_csv('test_dev_10sec_allpreviouspack.csv',header=None).values

fig,ax = plt.subplots(figsize=(6,4))

fmt = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.2f}")
ax.xaxis.set_major_formatter(fmt1)
ax.yaxis.set_major_formatter(fmt1)

ax.tick_params(axis='both', which='major',direction='out', labelsize=12)
ax.tick_params(top='off',right='off')
ax.set_xlabel('FNR',fontsize=16)
ax.set_ylabel('FPR',fontsize=16)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
ax.grid(linewidth=0.5)
#c = ax.hist(fpr_mat_g.T, bins = b, normed=True, cumulative=True, histtype='step', color='blue',linewidth=2.0)
ax.scatter(np.mean(fnr_targets[:,np.sum(test_dev_targets,axis=0)>0]/test_dev_targets[:,np.sum(test_dev_targets,axis=0)>0],axis=0),np.mean(fpr_targets[:,np.sum(test_dev_targets,axis=0)>0]>0,axis=0),color='#2c7fb8',linewidth=2.0)
count = 0
for i, txt in enumerate(range(1,20)):
    if np.sum(test_dev_targets[:,i],axis=0)>0 and i<10:
        count = count+1
        ax.annotate(count, (np.mean(fnr_targets[:,i]/test_dev_targets[:,i],axis=0), np.mean(fpr_targets[:,i]>0,axis=0)+0.005),fontsize=12)
    elif np.sum(test_dev_targets[:,i],axis=0)>0 and i>9:
        count = count+1
        ax.annotate(count, (np.mean(fnr_targets[:,i]/test_dev_targets[:,i],axis=0)-0.003, np.mean(fpr_targets[:,i]>0,axis=0)+0.005),fontsize=12)
ax.set_yticks([0.0,0.02,0.04,0.06,0.08,0.10,0.12,0.14])
ax.set_yticklabels(['0\%','2\%','4\%','6\%','8\%','10\%','12\%','14\%'])
ax.set_xticks([0.0,0.02,0.04,0.06,0.08,0.10])
ax.set_xticklabels(['0\%','2\%','4\%','6\%','8\%','10\%'])

fig.set_dpi(300)
ax.set_xlim(-0.004,0.10)
ax.set_ylim(-0.006,0.14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
fig.savefig('fpr_fnr2.pdf',bbox_inches ='tight')
