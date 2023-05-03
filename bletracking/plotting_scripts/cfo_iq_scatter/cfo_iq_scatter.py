import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#from matplotlib import rc
import matplotlib.ticker
import numpy as np

plt.rcParams.update({"text.usetex":True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})

feature = pd.read_csv('iphone_esp_ti_features_2.csv',header=None).values
#label = pd.read_csv('iphone_esp_ti_labels.csv',header=None).values

fig,ax = plt.subplots(figsize=(6,4))

fmt = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.2f}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt1)

ax.scatter(feature[0:8,1]/1000,feature[0:8,2],s = 100,marker='X',color='#2c7fb8',linewidth=2)
ax.scatter(feature[8:28,1]/1000,feature[8:28,2],s = 100,facecolors='none', edgecolors='#ff0000',linewidth=2)
ax.scatter(feature[28:48,1]/1000,feature[28:48,2],s = 200, marker='+',color='#09bc8a',linewidth=2)
ax.scatter(feature[48,1]/1000,feature[48:,2],s = 100,facecolors='none', edgecolors='#ff0000',linewidth=2)
ax.tick_params(axis='both', which='major',direction='out', labelsize=12)
ax.tick_params(top='off',right='off')
ax.set_xlabel('CFO (KHz)',fontsize=16)
ax.set_ylabel('IQ Offset Magnitude',fontsize=16)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
ax.grid(linewidth=0.5)
#ax.set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
ax.legend(["iPhone","ESP32-Combo Chipset","TI-BLE only Chipset"],fontsize=12,frameon=False)
fig.set_dpi(300)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylim([0,0.07])
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
fig.savefig('cfoiq_iphone_esp_ti2.pdf',bbox_inches ='tight')
