import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#from matplotlib import rc
import matplotlib.ticker
import numpy as np

plt.rcParams.update({"text.usetex":True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})

#confusion_mat_binary = pd.read_csv('/Users/hadigivehchian/Desktop/CFO_data/ESP_Data_Raw/results_mobisys/field/confusion_mat_binary.csv',header=None).values
#confusion_mat_dev = pd.read_csv('/Users/hadigivehchian/Desktop/CFO_data/ESP_Data_Raw/results_mobisys/field/confusion_mat_dev.csv',header=None).values
#count_mat_g = pd.read_csv('/Users/hadigivehchian/Desktop/CFO_data/ESP_Data_Raw/results_mobisys/field/count_mat_g.csv',header=None).values
fpr_mat_g = pd.read_csv('fpr_mat_g.csv',header=None).values
a,b = np.histogram(fpr_mat_g.T,1000)
c = np.cumsum(a)
#matplotlib.rc("text", usetex="false")

fig,ax = plt.subplots(figsize=(6,4))

fmt = matplotlib.ticker.StrMethodFormatter("{x}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.2f}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt1)

ax.tick_params(axis='both', which='major',direction='out', labelsize=12)
ax.tick_params(top='off',right='off')
ax.set_xlabel('FPR',fontsize=16)
ax.set_ylabel('CDF',fontsize=16)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
ax.grid(linewidth=0.5)
#c = ax.hist(fpr_mat_g.T, bins = b, normed=True, cumulative=True, histtype='step', color='blue',linewidth=2.0)
ax.plot(np.concatenate(([0],b,[0.12])),np.concatenate(([0],c,c[-1,None],c[-1,None]),axis=0)/c[-1],color='#2c7fb8',linewidth=2.0)
ax.set_xlim(-0.005,0.12)
ax.set_ylim(-0.05,1.025)
ax.set_xticks([0.0,0.02,0.04,0.06,0.08,0.10,0.12])
ax.set_xticklabels([r'0\%',r'2\%',r'4\%',r'6\%',r'8\%',r'10\%',r'12\%'])
fig.set_dpi(300)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
fig.savefig('fpr_cdf.pdf',bbox_inches ='tight')
