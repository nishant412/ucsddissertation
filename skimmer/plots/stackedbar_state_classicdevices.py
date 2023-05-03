import numpy as np
import matplotlib.pyplot as plt
import json


cat_file = open('categorized_filtered.json','rb').read()
cat_data = json.loads(cat_file)
uncat_file = open('uncategorized_filtered.json','rb').read()
uncat_data = json.loads(uncat_file)
ble_file = open('ble_filtered.json','rb').read()
ble_data = json.loads(ble_file)

bar_dict = {}
bar_dict[0] = []
bar_dict[1] = []
bar_dict[2] = []
#bar_dict[3] = []
#bar_dict[4] = []
bar_percent_dict = {}
bar_percent_dict[0] = []
bar_percent_dict[1] = []
bar_percent_dict[2] = []
#bar_percent_dict[3] = []

'''
bar_dict['IL'] = []
bar_dict['NV'] = []
bar_dict['NC'] = []
'''
count1 = 0
count2 = 0
count3 = 0

for key in uncat_data:
	for i in range(0,len(uncat_data[key])):
		count1 += uncat_data[key][i] + cat_data[key][i]
		count2 += ble_data[key][i]
		#count3 
		'''
		if (uncat_data[key][i] == 0):
			count1 += 1 
		elif (uncat_data[key][i] >= 1 and uncat_data[key][i] < 3):
			count2 += 1
		else:
			count3 += 1
		'''
	count3 = count2 + count1
	if(key != 'NV'):
		bar_dict[0].append(count1)
		bar_percent_dict[0].append(float(count1)/count3*100)
		bar_dict[1].append(count2)
		bar_percent_dict[1].append(float(count2)/count3*100)
		#bar_dict[2].append(count3)
		#bar_percent_dict[2].append(float(count3)/len(uncat_data[key]))
		bar_dict[2].append(key)
		bar_percent_dict[2].append(key)
		#bar_dict[4].append(len(uncat_data[key]))
	count1 = 0
	count2 = 0
	count3 = 0



N = len(bar_dict[2])
ind = np.arange(N)
width = 0.35

fig1,ax1 = plt.subplots()
p1 = ax1.bar(ind,bar_dict[1],width,color = 'c')
p2 = ax1.bar(ind,bar_dict[0],width,bottom = bar_dict[1], color = 'g')
#p3 = ax1.bar(ind,bar_dict[2],width,bottom = [sum(x) for x in zip(bar_dict[0], bar_dict[1])],color = 'r')
ax1.set_xticks(ind)
ax1.set_xticklabels(bar_dict[2])
ax1.set_xlabel('State')
ax1.set_ylabel('Number of gas stations')
ax1.legend((p1[0],p2[0]),('BLE','classic'))
fig1.savefig('stackedbar_state_classicdevices_abc.pdf',bbox_inches='tight')

fig2,ax2 = plt.subplots()
p1 = ax2.bar(ind,bar_percent_dict[1],width,color = 'c')
p2 = ax2.bar(ind,bar_percent_dict[0],width,bottom = bar_percent_dict[1], color = 'g')
#p3 = ax2.bar(ind,bar_percent_dict[2],width,bottom = [sum(x) for x in zip(bar_percent_dict[0], bar_percent_dict[1])],color = 'r')
ax2.set_xticks(ind)
ax2.set_xticklabels(bar_percent_dict[2])
ax2.set_xlabel('State')
ax2.set_yticks([0,20,40,60,80,100,120])
ax2.set_ylabel('Percentage of devices')
ax2.legend((p1[0],p2[0]),('BLE','Classic'))
fig2.savefig('stackedbar_state_classicdevices_percent_abc.pdf',bbox_inches='tight')

			

