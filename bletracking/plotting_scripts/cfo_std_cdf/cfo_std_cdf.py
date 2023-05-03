import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#from matplotlib import rc
import matplotlib.ticker
import numpy as np

cfo_base = pd.read_csv('cfo_std_baseline.csv').values

cfo = pd.read_csv('cfo_std.csv').values

fig,ax = plt.subplots(figsize=(6,4))

fmt = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.1f}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt1)


ax.tick_params(axis='both', which='major',direction='out', labelsize=12)
ax.tick_params(top='off',right='off')
ax.set_xlabel('Standard deviation of estimated CFO (KHz)',fontsize=16)
ax.set_ylabel('CDF',fontsize=16)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
ax.grid(linewidth=0.5)
#c = ax.hist(fpr_mat_g.T, bins = b, normed=True, cumulative=True, histtype='step', color='blue',linewidth=2.0)
#ax.plot(np.concatenate(([0],b,[0.12])),np.concatenate(([0],c,c[-1,None],c[-1,None]),axis=0)/c[-1],color='blue',linewidth=2.0)
a,b = np.histogram(cfo_base/1000,1000)
c = np.cumsum(a)
b[0] = 0
c[0] = 0
ax.plot(b[0:-1],c/c[-1],'b--')

a,b = np.histogram(cfo/1000,1000)
print (np.mean(cfo/1000))
c = np.cumsum(a)
b[0] = 0
c[0] = 0
ax.plot(b[0:-1],c/c[-1],'r')
ax.set_yticks([0,0.2,0.4,0.6,0.8,1])
ax.legend(["Existing Techniques","Proposed Technique"],fontsize=12,frameon=False)
fig.set_dpi(300)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
fig.savefig('CFO_comparison_ESP2.pdf',bbox_inches ='tight')
