import json
import matplotlib.pyplot as plt
import numpy as np

cat_file = open('categorized_filtered.json','rb').read()
cat_data = json.loads(cat_file)
uncat_file = open('uncategorized_filtered.json', 'rb').read()
uncat_data = json.loads(uncat_file)

total_bluetooth = {}

total_bluetooth['CA'] = []
total_bluetooth['AZ'] = []
total_bluetooth['MD'] = []
total_bluetooth['IL'] = []
total_bluetooth['NV'] = []
total_bluetooth['NC'] = []

for key in uncat_data:
	for i in range(0,len(uncat_data[key])):
		sum = uncat_data[key][i] + cat_data[key][i]
		if (sum < 50) :
			total_bluetooth[key].append(sum)
		else:
			total_bluetooth[key].append(sum)

print total_bluetooth

bin_vals = [0,10,20,30,40,50,60,70,80,90,100,120]

fig,ax = plt.subplots(figsize=(24,12))
counts,bin_edges = np.histogram (total_bluetooth['CA'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'California')

counts,bin_edges = np.histogram (total_bluetooth['NC'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'North Carolina')

counts,bin_edges = np.histogram (total_bluetooth['MD'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Maryland')

counts,bin_edges = np.histogram (total_bluetooth['IL'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Illinois')


counts,bin_edges = np.histogram (total_bluetooth['AZ'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Arizona')

ax.set_xlabel('Total number of Bluetooth devices seen at a gas station',fontsize = 25)
ax.set_ylabel('CDF',fontsize=25)
plt.tick_params(axis='both', which='major', labelsize=25,pad = 10)
ax.set_ylim(0,1.1)
ax.set_xticks(bin_vals)
ax.legend(loc='right')
fig.savefig('cdf_total_classic.png',bbox_inches ='tight')
