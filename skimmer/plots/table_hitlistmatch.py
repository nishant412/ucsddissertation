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
hitlist_matchA = ['00:06:66']
hitlist_matchB = ['33:60:80','ab:cd:ef','94:05:6f','20:18:08','20:17:05','1e:03:e0','20:17:09','98:d3:51','33:60:8a','88:18:56','6b:52:7c','8f:44:30','20:16:12','20:17:11','20:16:08','00:3c:7f','00:91:16','20:18:01','aa:bb:cc','8d:04:f8','66:35:56','11:22:33','20:13:04','58:51:00','ad:7a:ba','12:34:56','20:15:03','98:d3:32','09:f0:f0','22:22:83','20:15:04','47:ba:d0','22:22:47','60:30:d4','20:17:03']

gasA = 0
gasB = 0
gasC = 0
gasD = 0
countA = 0
countB = 0

for key in uncat_data:
	dict_element = uncat_data[key]
	for idx in dict_element:
		#ind_array = dict_element[idx]
		if idx:
			for jdx in idx:
				#print jdx[:8]
				if (jdx[:8] in hitlist_matchA):
					countA += 1
				if (jdx[:8] in hitlist_matchB):	
					countB += 1
			if (countA >= 1 and countB == 0):
				#print 'gasA'
				gasA += 1
			elif (countB >= 1 and countA == 0):
				#print 'gasB'
				gasB += 1
			elif (countA >= 1 and countB >= 1):
				#print 'gasD'
				gasD += 1
			else:
				#print 'gasC'
				gasC += 1
			countA = 0
			countB = 0
		else:
			#print 'gasC'
			gasC += 1
	if(key != 'NV'):
		print key,' & ',gasC,' & ',gasA,' & ',gasB,' & ',gasD,' \\\\'
	gasA = 0
	gasB = 0
	gasC = 0
	gasD = 0
	#countA = 0
	#countB = 0
'''
'''
