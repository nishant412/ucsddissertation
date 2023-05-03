import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
categorized = {}
categorized['CA'] = []
categorized['AZ'] = []
categorized['MD'] = []
categorized['IL'] = []
categorized['NV'] = []
categorized['NC'] = []
uncategorized = {}
uncategorized['CA'] = []
uncategorized['AZ'] = []
uncategorized['MD'] = []
uncategorized['IL'] = []
uncategorized['NV'] = []
uncategorized['NC'] = []

uncat_file = open('uncategorized_filtered.json','rb').read()
uncat_data = json.loads(uncat_file)
#cat_nishant_file = open('uncategorized_nishant.json','rb').read()
#cat_nishant_data = json.loads(cat_nishant_file)
#uncat_file = open('categorized.json', 'rb').read()
#uncat_data = json.loads(uncat_file)
#print cat_data
print 'California'
print len(uncat_data['CA'])
print 'Maryland'
print len(uncat_data['MD'])
print 'Arizona'
print len(uncat_data['AZ'])
print 'Illinois'
print len(uncat_data['IL'])
print 'Nevada'
print len(uncat_data['NV'])
print 'North Carolina'
print len(uncat_data['NC'])
bin_vals = [-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
fig,ax = plt.subplots(figsize=(4,3.5))

for key in uncat_data:
	uncat_data[key].sort()
	x = []
	y = []
	x.append(uncat_data[key][0])
	y.append(0.0)
	for idx in range(0,len(uncat_data[key])):
		if (idx == (len(uncat_data[key]) - 1)):
			x.append(uncat_data[key][idx])
			y.append((idx+1)/float(len(uncat_data[key])))
		else:
			if(uncat_data[key][idx] != uncat_data[key][idx+1]):
				x.append(uncat_data[key][idx])
				x.append(uncat_data[key][idx+1])
				y.append((idx)/float(len(uncat_data[key])))
				y.append((idx+1)/float(len(uncat_data[key])))
	labval = ''
	if (key == 'CA'):
		labval = 'California'
	if (key == 'MD'):
		labval = 'Maryland'
	if (key == 'NC'):
		labval = 'North Carolina'
	if (key == 'AZ'):
		labval = 'Arizona'
	if (key == 'IL'):
		labval = 'Illinois'
	if (key != 'NV'):
		ax.plot(x,y,label = key)
		#counts,bin_edges = np.histogram (uncat_data[key],bins=bin_vals,normed=True)
		#cdf = np.cumsum(counts)
		#ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = labval)

#ax.xaxis.set_major_locator(MultipleLocator(1.))
#ax.xaxis.set_major_locator(FormatStrFormatter('%d'))
#ax.xaxis.set_minor_locator(MultipleLocator(5.))
ax.set_xlabel('Number of uncategorized classic Bluetooth devices seen at a gas station',fontsize = 25)
ax.set_ylabel('CDF',fontsize=25)
ax.tick_params(axis='both', which='major', labelsize=25,pad = 10)
ax.set_ylim(0,1.1)
ax.set_xlim(0,8)
ax.legend(loc='right')
fig.savefig('cdf_uncategorized_filtered_nodriveby.pdf',bbox_inches ='tight')

fig1,ax1 = plt.subplots(figsize=(4,3.5))

array0 = []
count0 = 0
array1 = []
count1 = 0
array2 = []
count2 = 0
key_list = []
for key in uncat_data:
	for i in range(0,len(uncat_data[key])):
		if (uncat_data[key][i] == 0):
			count0 += 1
		elif (uncat_data[key][i] == 1):
			count1 += 1
		else:
			count2 += 1
	if(key != 'NV'):
		array0.append(count0/float(count0+count1+count2))
		array1.append(count1/float(count0+count1+count2))
		array2.append(count2/float(count0+count1+count2))
		key_list.append(key)

N = len(key_list)
ind = np.arange(N)
width = 0.2

rects1 = ax1.bar(ind,array0,width = 0.2,color = 'y',label = '0')
rects2 = ax1.bar(ind+width,array1,width = 0.2, color = 'g',label = '1')
rects3 = ax1.bar(ind+width+width,array2,width = 0.2, color = 'b',label = '2+')
ax1.legend((rects1[0],rects2[0],rects3[0]),('0','1','2+'))	
ax1.set_xlabel('State',fontsize = 25)
ax1.set_ylabel('Percentage of uncategorized \ndevices seen at gas stations',fontsize=25)
ax1.set_xticks(ind + width + width/ 2)
ax1.set_xticklabels(key_list)
ax1.tick_params(axis='both', which='major', labelsize=20,pad = 10)
ax1.set_ylim(0,1.1)
ax1.legend(loc='right')
fig1.savefig('barplot_uncategorized_filtered_nodriveby.pdf',bbox_inches ='tight')

fig3,ax3 = plt.subplots(figsize=(6,4))
	
for key in uncat_data:
	uncat_data[key].sort()
	x = []
	y = []
	x.append(uncat_data[key][0])
	y.append(1.0)
	for idx in range(0,len(uncat_data[key])):
		if (idx == (len(uncat_data[key]) - 1)):
			x.append(uncat_data[key][idx])
			y.append(1-((idx+1)/float(len(uncat_data[key]))))
		else:
			if(uncat_data[key][idx] != uncat_data[key][idx+1]):
				x.append(uncat_data[key][idx])
				x.append(uncat_data[key][idx+1])
				y.append(1-((idx)/float(len(uncat_data[key]))))
				y.append(1-((idx+1)/float(len(uncat_data[key]))))
	labval = ''
	if (key == 'CA'):
		labval = 'California'
	if (key == 'MD'):
		labval = 'Maryland'
	if (key == 'NC'):
		labval = 'North Carolina'
	if (key == 'AZ'):
		labval = 'Arizona'
	if (key == 'IL'):
		labval = 'Illinois'
	if (key != 'NV'):
		ax3.step(x,y,label = labval,linewidth = 2.5,clip_on=False)
		#counts,bin_edges = np.histogram (uncat_data[key],bins=bin_vals,normed=True)
		#cdf = np.cumsum(counts)
		#ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = labval)
	print labval
	print x
	print y
#ax.xaxis.set_major_locator(MultipleLocator(1.))
#ax.xaxis.set_major_locator(FormatStrFormatter('%d'))
#ax.xaxis.set_minor_locator(MultipleLocator(5.))
#ax3.set_axisbelow(True)
ax3.spines['left'].zorder = 0.5
ax3.spines['bottom'].zorder = 0.5
ax3.set_xlabel('# of uncategorized devices \nseen at a gas station',fontsize = 20)
ax3.set_ylabel('Complementary CDF',fontsize=20)
ax3.tick_params(axis='both', which='major', labelsize=15,pad = 10)
ax3.set_ylim(0,1.1)
ax3.set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
ax3.set_xlim(0,6)
ax3.legend(loc='upper right',frameon=False)
fig3.savefig('cdf_uncategorized_filtered_nodriveby2.pdf',bbox_inches ='tight')

table_dict = {}
table_dict[10] = []
table_dict[11] = []
table_dict[0] = []
cnt0 = 0
table_dict[1] = []
cnt1 = 0
table_dict[2] = []
cnt2 = 0
table_dict[3] = []
cnt3 = 0
table_dict[4] = []
cnt4 = 0
table_dict[5] = []
cnt5 = 0
table_dict[6] = []
cnt6 = 0
for key in uncat_data:
	table_dict[11].append(len(uncat_data[key]))
	for i in range(0,len(uncat_data[key])):
		test = uncat_data[key][i]
		if (test == 0):
			cnt0 += 1
		if(test == 1):
			cnt1 += 1
		if(test == 2):
			cnt2 += 1
		if(test == 3):
			cnt3 += 1
		if(test == 4):
			cnt4 += 1
		if(test == 5):
			cnt5 += 1
		if(test == 6):
			cnt6 += 1
	if(key != 'NV'):
		table_dict[0].append(cnt0)
		table_dict[1].append(cnt1)
		table_dict[2].append(cnt2)
		table_dict[3].append(cnt3)
		table_dict[4].append(cnt4)
		table_dict[5].append(cnt5)
		table_dict[6].append(cnt6)
		if (key == 'CA'):
        		table_dict[10].append('California')
        	if (key == 'MD'):
        		table_dict[10].append('Maryland')
        	if (key == 'NC'):
        		table_dict[10].append('North Carolina')
        	if (key == 'AZ'):
               		table_dict[10].append('Arizona')
        	if (key == 'IL'):
                	table_dict[10].append('Illinois')
	cnt0=0
	cnt1=0
	cnt2=0
	cnt3=0
	cnt4=0
	cnt5=0
	cnt6=0
print 'State',
for i in range(0,len(table_dict[10])):
	print ' & ',table_dict[10][i],
print ' \\\\'

print '0',
for i in range(0,len(table_dict[0])):
	print ' & ',table_dict[0][i],
print ' \\\\'

print '1',
for i in range(0,len(table_dict[1])):
	print ' & ',table_dict[1][i],
print ' \\\\'

print '2',
for i in range(0,len(table_dict[2])):
	print ' & ',table_dict[2][i],
print ' \\\\'

print '3',
for i in range(0,len(table_dict[3])):
	print ' & ',table_dict[3][i],
print ' \\\\'

print '4',
for i in range(0,len(table_dict[4])):
	print ' & ',table_dict[4][i],
print ' \\\\'

print '5',
for i in range(0,len(table_dict[5])):
	print ' & ',table_dict[5][i],
print ' \\\\'

print '6',
for i in range(0,len(table_dict[6])):
	print ' & ',table_dict[6][i],
print ' \\\\'

print 'Total # of gas stations',
for i in range(0,len(table_dict[11])):
	print ' & ',table_dict[11][i],
print ' \\\\'
