import pickle
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib import rc
#rc('text',usetex=True)
hitlist_match = []
with open('hitlist_matchlist','rb') as f:
	hitlist_match = pickle.load(f)
'''
for elmt in hitlist_match:
	name = elmt[1]
	if ((name != None) and (name != '') and (name != 'None') and (name[:5] != 'RNBT-') and (name[:5] != 'SP100') and (name[:4] != 'AP00') and (name != 'HC-05') and (name[:11] != 'POWERDRIVER') and (name[:5] != 'GENX_') and (name[:6] != 'Police') and (name[:2] != '11') and (name != 'BT66') and (name != 'Magnetic Speaker')):
		print elmt[0],elmt[1]
	#if name =='AP001648-3E8B':
		#print 'A',name[:4]
'''
hitmatch = {}
count1 = 0
count2 = 0
bar_vals = []
bar_keys = []
total_count = 0
for elmt in hitlist_match:
	name = elmt[1]
	#if ((name != None) and (name != '') and (name != 'None') and (name[:5] != 'RNBT-') and (name[:5] != 'SP100') and (name[:4] != 'AP00') and (name != 'HC-05') and (name[:11] != 'POWERDRIVER') and (name[:5] != 'GENX_') and (name[:6] != 'Police') and (name[:2] != '11') and (name != 'BT66') and (name != 'Magnetic Speaker')):
		#print elmt[0],elmt[1]
	#if name =='AP001648-3E8B':
		#print 'A',name[:4]
	if((name is not None) and (elmt[0][:8] == '00:06:66')):
		if((name[:5] == 'RNBT-') and (elmt[0] not in hitmatch)):
			count1 += 1
			hitmatch[elmt[0]] = 1
			#print elmt[0]
if(count1 > 0):
	bar_vals.append(count1)
	bar_keys.append('Default')
print 'RNBT-%',count1
count1 = 0
for elmt in hitlist_match:
	name = elmt[1]
	if((name is not None) and (elmt[0][:8] == '00:06:66')):
		if((name[:5] == 'SP100') and (elmt[0] not in hitmatch)):
			count1 += 1
			hitmatch[elmt[0]] = 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('"SP100*"')
print 'SP100%',count1
count1 = 0
for elmt in hitlist_match:
        name = elmt[1]
        if((name is not None) and (elmt[0][:8] == '00:06:66')):
                if((name[:4] == 'AP00') and (elmt[0] not in hitmatch)):
                        count1 += 1
                        hitmatch[elmt[0]] = 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('"AP00*"')
print 'AP00%',count1
count1 = 0
for elmt in hitlist_match:
        name = elmt[1]
        if((name is not None) and (elmt[0][:8] == '00:06:66')):
                if((name[:11] == 'POWERDRIVER') and (elmt[0] not in hitmatch)):
                        count1 += 1
                        hitmatch[elmt[0]] = 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('POWERDRIVER*')
print 'POWER\nDRIVER',count1
count1 = 0
for elmt in hitlist_match:
        name = elmt[1]
        if((name is not None) and (elmt[0][:8] == '00:06:66')):
                if((name[:5] == 'GENX_') and (elmt[0] not in hitmatch)):
                        count1 += 1
                        hitmatch[elmt[0]] = 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('"GENX*"')
print 'GENX_',count1

count1 = 0
for elmt in hitlist_match:
        name = elmt[1]
        if((name is not None) and (elmt[0][:8] == '00:06:66')):
                if((name[:6] == 'Police') and (elmt[0] not in hitmatch)):
                        count1 += 1
                        hitmatch[elmt[0]] = 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('"Police*"')
print 'Police%',count1

count1 = 0
for elmt in hitlist_match:
        name = elmt[1]
        if((name is not None) and (elmt[0][:8] == '00:06:66')):
                if((name[:2] == '11') and (elmt[0] not in hitmatch)):
                        count1 += 1
                        hitmatch[elmt[0]] = 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('"11*"')
print '11%',count1

count1 = 0
for elmt in hitlist_match:
        name = elmt[1]
        if((name is not None) and (elmt[0][:8] == '00:06:66')):
                if((name == 'BT66') and (elmt[0] not in hitmatch)):
                        count1 += 1
                        hitmatch[elmt[0]] = 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('BT66')
print 'BT66',count1

count1 = 0
for elmt in hitlist_match:
        name = elmt[1]
        if((name is not None) and (elmt[0][:8] == '00:06:66')):
                if((name == 'Magnetic Speaker') and (elmt[0] not in hitmatch)):
                        count1 += 1
                        hitmatch[elmt[0]] = 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('Magnetic Speaker')
print 'Magnetic Speaker',count1

count1 = 0
for elmt in hitlist_match:
	name = elmt[1]
	if(elmt[0][:8] == '00:06:66'):
		if((name is None) and (name != 'None') and (name != '') and (elmt[0] not in hitmatch)):
			count1 += 1
			hitmatch[elmt[0]] = 1
		#count2 += 1
if(count1 > 0):
        bar_vals.append(count1)
        bar_keys.append('None')
print 'No Name',count1

hitcheck = {}
for elmt in hitlist_match:
	if(elmt[0] not in hitcheck):
		total_count += 1
		hitcheck[elmt[0]] = 1

max_val = 0
max_idx = 0
bar_vals2 = []
bar_keys2 = []

for idx in range(0,len(bar_keys)):
	if (bar_keys[idx] == 'Default'):
		bar_keys2.append('Default \nName')
		#Add 4 for new PB skimmers and 1 for Hillcrest skimmer, subtract 11 for skimmers 
		bar_vals2.append((bar_vals[idx] + 1 + 4) - 15) 

for idx in range(0,len(bar_keys)):
	if (bar_keys[idx] == 'None'):
		bar_keys2.append('No \n Name')
		#Add 1 for 3011 Bell Rd, 2 for 7620 Mcclintock Dr, 2 for Anapolis, subtract 5 for skimmers
		bar_vals2.append((bar_vals[idx] + 3) - 3) 

for idx in range(0,len(bar_keys)):
	if (bar_keys[idx] == '"Police*"'):
		bar_keys2.append('Police*')
		#Subtract 2 for skimmers
		bar_vals2.append(bar_vals[idx] - 2) 


for idx in range(0,len(bar_keys)):
	if (bar_keys[idx] == '"11*"'):
		bar_keys2.append('11*')
		#Subtract 2 for skimmers
		bar_vals2.append(bar_vals[idx]-2) 


for idx in range(0,len(bar_keys)):
	if (bar_keys[idx] == '"AP00*"'):
		bar_keys2.append('AP00*')
		bar_vals2.append(bar_vals[idx]) 

for idx in range(0,len(bar_keys)):
	if (bar_keys[idx] == '"GENX*"'):
		bar_keys2.append('GENX*')
		bar_vals2.append(bar_vals[idx]) 

for idx in range(0,len(bar_keys)):
	if (bar_keys[idx] == '"SP100*"'):
		bar_keys2.append('SP100*')
		bar_vals2.append(bar_vals[idx]) 
'''
for i in range(0,len(bar_vals)):
	maxval = bar_vals[i]
	max_idx = i
	for j in range(i+1,len(bar_vals)):
		if bar_vals[j] > maxval:
			maxval = bar_vals[j]
			max_idx = j 
	temp = bar_vals[max_idx]
	temp1 = bar_keys[max_idx]
	bar_vals[max_idx] = bar_vals[i]
	bar_keys[max_idx] = bar_keys[i]
	bar_vals[i] = temp
	bar_keys[i] = temp1
'''

#ax.scatter(default_list_x,default_list_y,color = 'blue',marker='+')
print bar_vals2
bar_vals3 = [15,3,2,2,0,0,0]
print 'Total',total_count
fig,ax = plt.subplots(figsize=(7,2.5))
x_vals = np.arange(len(bar_keys2) + 2)
p1 = ax.bar([0.6,2.6,4.6,6,8,9.4,10.8],bar_vals3,align='center',width = 0.8,edgecolor='none',color='r')
p2 = ax.bar([0.6,2.6,4.6,6,8,9.4,10.8],bar_vals2,bottom = bar_vals3,align='center',width = 0.8,edgecolor='none',color='#3093DB')
ax.legend((p1[0],p2[0]),('Skimmer','Other RN or HC'),loc='upper right',frameon=False)
#ax.arrow((0-0.4),(bar_vals2[0]+1), (0+0.8),0,label = 'Default',head_width=1, head_length=0.2,fc='k', ec='k')
#ax.arrow((0+0.4),(bar_vals2[0]+1), (0-0.8),0,label = 'Default',head_width=1, head_length=0.2,fc='k', ec='k')

#ax.arrow((2-0.4),(bar_vals2[0]+1), (2+0.8),0,label = 'Default',head_width=1, head_length=0.2,fc='k', ec='k')
#ax.arrow((4+0.4),(bar_vals2[0]+1), (-2-0.8),0,label = 'Default',head_width=1, head_length=0.2,fc='k', ec='k')

#ax.arrow((6-0.4),(bar_vals2[0]+1), (2+0.8),0,label = 'Default',head_width=1, head_length=0.2,fc='k', ec='k')
#ax.arrow((8+0.4),(bar_vals2[0]+1), (-2-0.8),0,label = 'Default',head_width=1, head_length=0.2,fc='k', ec='k')
#ax.arrow((0+0.4),(bar_vals2[0]+1), (0-0.8),0)
#ax.text((0-0.6),17,'Default')
#ax.text((2+0.3),17,'Unknown')
#ax.text((6+0.4),17, 'Products')
#ax.set_xlabel('Device Name',fontsize = 20)
ax.set_ylabel('# of devices',fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=13,pad = 10)
ax.set_ylim(0,20)
ax.set_xlim(0,11.4)
ax.set_xticks([0.6,2.6,4.6,6,8,9.4,10.8])
ax.set_yticks([0,3,6,9,12,15,18,21])
ax.set_xticklabels(bar_keys2,fontsize = 11)
ticklabels = ax.get_xticklabels()
ticklabels[0].set_fontstyle("italic")
ticklabels[1].set_fontstyle("italic")
trans = ax.get_xaxis_transform()
ax.annotate('Unknown',xy=((4.6+6)/2,-.2),xycoords=trans,ha='center',va='top',fontsize=15)
ax.plot([(4.6-.4),(6+0.4)],[-.17,-.17], color="k", transform=trans, clip_on=False)
#ax.legend(loc='right')
ax.annotate('Known product',xy=(9.4,-.2),xycoords=trans,ha='center',va='top',fontsize=15)
ax.plot([(8-.4),(10.8+0.4)],[-.17,-.17], color="k", transform=trans, clip_on=False)
fig.savefig('bar_plot_name_cluster.pdf',bbox_inches ='tight')		
#print count1
