import json
import matplotlib.pyplot as plt
import numpy as np

cat_file = open('categorized_nishant.json','rb').read()
cat_data = json.loads(cat_file)
uncat_file = open('uncategorized_nishant.json', 'rb').read()
uncat_data = json.loads(uncat_file)
ble_file = open('ble_nishant.json','rb').read()
ble_data = json.loads(ble_file)

total_bluetooth = {}

total_bluetooth['CA'] = []
#total_bluetooth['AZ'] = []
#total_bluetooth['MD'] = []
#total_bluetooth['IL'] = []
#total_bluetooth['NV'] = []
#total_bluetooth['NC'] = []

#for key in uncat_data:
for i in range(0,len(uncat_data['CA'])):
	total_bluetooth['CA'].append(uncat_data['CA'][i] + cat_data['CA'][i])

print total_bluetooth['CA']
print ble_data['CA']
bin_vals = [0,1,2,3,4,5,6,7,8,9,10]

fig,ax = plt.subplots(figsize=(24,12))
counts,bin_edges = np.histogram (total_bluetooth['CA'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'total classic Bluetooth')

counts,bin_edges = np.histogram (uncat_data['CA'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Uncategorized Bluetooth')

'''
counts,bin_edges = np.histogram (total_bluetooth['NV'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Nevada')

counts,bin_edges = np.histogram (total_bluetooth['AZ'],bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Arizona')
'''
ax.set_xlabel('Total number of Bluetooth devices seen at a gas station',fontsize = 25)
ax.set_ylabel('CDF',fontsize=25)
plt.tick_params(axis='both', which='major', labelsize=25,pad = 10)
ax.set_ylim(0,1.1)
ax.set_xticks(bin_vals)
ax.legend(loc='right')
fig.savefig('cdf_tota_nishant.pdf',bbox_inches ='tight')
