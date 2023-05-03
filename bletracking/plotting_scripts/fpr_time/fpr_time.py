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

dev_list = np.concatenate((range(0,8),range(9,13),range(14,19)))
fpr_targets = fpr_targets[:,dev_list]
test_dev_targets = test_dev_targets[:,dev_list]

fig,ax = plt.subplots(figsize=(6,4))

fmt = matplotlib.ticker.StrMethodFormatter("{x}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
ax.xaxis.set_major_formatter(fmt1)
ax.yaxis.set_major_formatter(fmt)

ax.tick_params(axis='x', which='major',direction='out', labelsize=12)
ax.tick_params(top='off',right='off')
ax.set_xlabel('Time (Seconds)',fontsize=16)
ax.set_ylabel('Device Label',fontsize=16)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
ax.grid(linewidth=0.5)
a = np.squeeze(np.array([fpr_targets>0])*0.5)
a_sort = np.array(np.argsort(np.mean(a,axis=0))[::-1])
max_time = 289

for j in range(0,17):
    i = a_sort[j]#dev_list[j]
    if np.sum(test_dev_targets[:,i],axis=0)>0:
        b = np.reshape(np.reshape(np.concatenate((np.array(range(0,max_time))+0.01, np.array(range(1,max_time+1))-0.01)),(2,max_time)).T,(1,max_time*2))
        c = np.reshape(np.concatenate((a[:,i:i+1],a[:,i:i+1]),axis=1),(1,max_time*2))+j+1
        ax.plot(np.squeeze(b),np.squeeze(c), color='#2c7fb8')
ax.set_yticks(range(1,18))
ax.set_yticklabels(a_sort+1)
ax.set_xlim(0,300)
fig.set_dpi(300)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
fig.savefig('fpr_time_10sec_sort2.pdf',bbox_inches ='tight')
