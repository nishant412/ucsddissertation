import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#from matplotlib import rc
import matplotlib.ticker

#matplotlib.rcParams['pdf.fonttype'] = 42
#matplotlib.rc("text", usetex="true")
#prop = font_manager.FontProperties(fname='/System/Library/Fonts/Helvetica.ttc')
plt.rcParams.update({"text.usetex":True,"font.family": "sans-serif","font.sans-serif": ["Helvetica"]})


feature = pd.read_csv('fpr_fnr_temp_thresh3.csv',header=None).values
fig = plt.figure(figsize=(6,4))
#fig.subplots_adjust(bottom=02)
#ax2 = ax.twiny()

ax = fig.add_axes([0.1, 0.17, 0.85, 0.85])

bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
width, height = bbox.width, bbox.height

ax1 = fig.add_axes([0.1409,0.1,0.1207,0.17])

#l = len(feature[0,:])
#ax2.plot(feature[2,:]/1000,(feature[0,:]),color='b',linewidth=2.0)

fmt = matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
fmt1 = matplotlib.ticker.StrMethodFormatter("{x:,.2f}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt1)
#ax1.yaxis.set_major_formatter(fmt1)

#fmt = matplotlib.ticker.StrMethodFormatter("{x}")
#ax1.xaxis.set_major_formatter(fmt)
ax1.yaxis.set_major_formatter(fmt1)
ax.plot(feature[2,:]/1000,(feature[0,:]),linewidth=2.0)
ax.set_xticks([1.6,4.8,8,16,24,32,40])
ax.set_xticklabels(['1','3','5','10','15','20','25'])
#ax.set_xlabel("Low-quality\n\n\nCrystal Oscillator Temperature $\Delta$ ($^\circ$C)",fontsize=12,labelpad=1)
ax.set_xlabel(r"\qquad\qquad\qquad{\fontsize{13pt}{3em}\selectfont \textbf{Low-quality crystal}}",labelpad=1)#\newline\newline\newline{\qquad\qquad\fontsize{16pt}{3em}\selectfont Temperature $\Delta$ ($^\circ$C)}",multialignment='center',labelpad=1)
#ax.set_yticks([0,2,4,6,8,10,12])
#ax.set_yticklabels(['0%','2%','4%','6%','8%','10%','12%'])
ax.set_xlim(-0.5,40.0)
ax.set_ylim(0.0,0.12)
ax.grid(True,which='major',axis='both',linewidth=0.5)
ax.tick_params(axis='y',right=False)
ax.tick_params(axis='x',direction='in')
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_ylabel(r'FPR',fontsize=16)
ax.tick_params(axis='both',labelsize=12)
ax.set_yticks([0.0,0.02,0.04,0.06,0.08,0.10,0.12])
ax.set_yticklabels(['0\%','2\%','4\%','6\%','8\%','10\%','12\%'])
#ax.set_yticklabels(ax.get_yticklabels(),fontsize=12)
ax.text(0.30,-0.25,r'Temperature $\Delta$ ($^\circ$C)',fontsize=16,transform=ax.transAxes)

ax1.set_xticks([0,0.54,1.0])
ax1.set_xticklabels(['5','15','25'],fontsize=12,color='#ff0000')
ax1.set_xlabel(r"\textbf{High-quality crystal}",fontsize=13,color='#ff0000',labelpad=1)
ax1.spines["top"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.set_yticks([])
ax1.patch.set_visible(False)
ax1.tick_params(axis='x',direction='in',color='#ff0000')
ax1.spines["bottom"].set_color('#ff0000')
'''
ax2.set_xlim(-0.5,40)
ax2.xaxis.set_ticks_position("bottom")
ax2.xaxis.set_label_position("bottom")
ax2.set_frame_on(True)
ax2.patch.set_visible(False)
ax2.grid(True,which='major',axis='x',linestyle=':')

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["bottom"].set_position(("axes",-0.3))
ax2.spines["bottom"].set_visible(True)
ax2.spines["bottom"].set_color('red')
ax2.spines["left"].set_visible(True)

ax2.set_xticks([1.44,4.32,7.2])
ax2.set_xticklabels(['5','15','25'],fontsize=14,color='red')
#ax2.set_xlim(0,7.5)
ax2.set_xlabel("High-quality crystal temperature($^\circ$C)",fontsize=14,color='red')
ax2.tick_params(color='red')
ax2.tick_params(axis='y',right=False)
'''
'''
ax.tick_params(axis='both', which='major',direction='out', labelsize=18)
ax.tick_params(top='off',right='off')
ax.tick_params(axis='x', length = 10)
ax2.tick_params(axis='x', length = 10)
#ax.set_xlabel('Temperature ($^\circ$C) - 8 minute cutting accuracy',fontsize=20)
ax.set_ylabel('FPR',fontsize=18)
ax.xaxis.labelpad = 10
ax.yaxis.labelpad = 10
ax.grid(linewidth=0.5)

#ax2.xaxis.set_label_coords(-0.1,-0.1)
ax2.xaxis.set_ticks_position('bottom')

ax2.tick_params(axis='both', which='major',direction='out', labelsize=18)
ax2.tick_params(top='off',right='off')

ax2.tick_params(axis = 'x', colors = 'red')
#ax2.set_xlabel('Temperature ($^\circ$C) - 0 minute cutting accuracy',fontsize=20)
ax2.xaxis.labelpad = 10
#ax2.grid(color = 'r', linestyle=':',linewidth=0.5)
ax2.set_ylim([0,0.2])
#ax.set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
#ax.legend(["iPhone","ESP32-Combo Chipset","TI-BLE only Chipset"],fontsize=16,frameon=False)
fig.set_dpi(300)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines["bottom"].set_position(("axes",-0.15))
ax.set_ylim([0,0.12])
'''

fig.set_dpi(300)
fig.savefig('fpr_temp_thresh_new.pdf',bbox_inches ='tight')
