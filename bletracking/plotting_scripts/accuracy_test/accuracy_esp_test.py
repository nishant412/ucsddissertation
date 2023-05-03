import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#from matplotlib import rc
import matplotlib.ticker
import numpy as np

plt.rcParams.update({"text.usetex":True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})

acc_esp = pd.read_csv('accuracy_no_test_snr0to15_2.csv',header=None).values
acc_esp = acc_esp[0:,1:]
#matplotlib.rcParams['pdf.fonttype'] = 42
#matplotlib.rc("text", usetex="false")
fig,ax = plt.subplots(figsize=(6,4))

fmt = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt1)

ax.tick_params(axis='both', which='major',direction='out', labelsize=12)
ax.tick_params(top='off',right='off')
ax.set_xlabel(r'\# of packets used for test',fontsize=16)
ax.set_ylabel('Accuracy',fontsize=16)
#ax.xaxis.labelpad = 10
#ax.yaxis.labelpad = 10
mac_esp = np.array([2,4,6,8,10,15,20,30,40])
ax.set_ylim(0,102)
ax.set_xlim(0,mac_esp[-1]+0.5)
ax.grid(linewidth=0.5)
ax.set_yticks([0,20,40,60,80,100])
ax.set_yticklabels(['0\%','20\%','40\%','60\%','80\%','100\%'])
ax.plot(mac_esp,acc_esp[0:,0]*100,linewidth=2.0,color='k')
ax.plot(mac_esp,acc_esp[0:,1]*100,'-.',linewidth=2.0,color='#09bc8a') #9e7b9b #9649cb #09bc8a #3f784c #c200fb 
ax.plot(mac_esp,acc_esp[0:,2]*100,'--',linewidth=2.0,color='#ff0000')
ax.plot(mac_esp,acc_esp[0:,3]*100,':',linewidth=2.0,color='#2c7fb8')
ax.scatter(mac_esp,acc_esp[0:,0]*100,linewidth=2.0,marker='s',color='k')
ax.scatter(mac_esp,acc_esp[0:,1]*100,linewidth=2.0,color='#09bc8a')
ax.scatter(mac_esp,acc_esp[0:,2]*100,linewidth=2.0,marker='*',color='#ff0000')
ax.scatter(mac_esp,acc_esp[0:,3]*100,linewidth=2.0,marker='X',color='#2c7fb8')

ax.set_yticks([0,20,40,60,80,100])
ax.set_yticklabels(['0\%','20\%','40\%','60\%','80\%','100\%'])

ax.legend(['10','15','20','25'],fontsize=12,title = "Test SNR",frameon=False,loc='lower right')
ax.get_legend().get_title().set_fontsize('13')
fig.set_dpi(300)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
fig.savefig('accuracy_esp_test2.pdf',bbox_inches ='tight')
