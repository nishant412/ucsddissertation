import os
import psycopg2
import sys
import re
from os import path
import reverse_geocoder as rg
import numpy as np
import matplotlib.pyplot as plt
#from ast import literal_eval
import json

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
ble = {}
ble['CA'] = []
ble['AZ'] = []
ble['MD'] = []
ble['IL'] = []
ble['NV'] = []
ble['NC'] = []
hitlist_by_man = {}
'''
uncat_maryland = []
cat_arizona = []
uncat_arizona = []
cat_illinois = []
uncat_illinois = []
'''
con = None
cnt = 0
con = psycopg2.connect("dbname='skimmer' user='nibhaska'")
cur = con.cursor()

cur.execute("select distinct(loc) from fuelsta")
rows = cur.fetchall()

cur.execute("create table cod_cdf_table as (select distinct on (mac) mac,loc,devmajor,devminor,devtype from enqresp where loc is not null)")
for row in rows:
	cur.execute("select count(distinct(mac)) from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision and devtype = 1 and (devmajor = 31 and devminor = 0)")
#cur.execute("select count(distinct(mac)) from enqresp where loc <@> '(-117.0638248,32.5941849)'::point < 0.038::double precision and devtype = 1 and not(devmajor = 31 and devminor = 0)")
	count1 = cur.fetchall()
#categorized.append(count[0][0])
	#print count[0][0]
	cur.execute("select count(distinct(mac)) from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision and devtype = 1 and not(devmajor = 31 and devminor = 0)")
	count2 = cur.fetchall()
	
	cur.execute("select count(distinct(mac)) from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision and devtype != 1")
	count3 = cur.fetchall()
	
	if (not(count1[0][0] == 0 and count2[0][0] == 0 and count3[0][0] ==0)):
		r = eval(row[0])
		l = (r[1],r[0])
		statesearch = rg.search(l)
		print statesearch[0]['admin1'] 
		print count1[0][0]
		if (statesearch[0]['admin1'] == 'California'):
			uncategorized['CA'].append(count1[0][0])
			categorized['CA'].append(count2[0][0])
			ble['CA'].append(count3[0][0])
        	if (statesearch[0]['admin1'] == 'North Carolina'):
                	uncategorized['NC'].append(count1[0][0])
			categorized['NC'].append(count2[0][0])
			ble['NC'].append(count3[0][0])
        	if (statesearch[0]['admin1'] == 'Nevada'):
			uncategorized['NV'].append(count1[0][0])
                	categorized['NV'].append(count2[0][0])
			ble['NV'].append(count3[0][0])
        	if (statesearch[0]['admin1'] == 'Arizona'):
                	uncategorized['AZ'].append(count1[0][0])
			categorized['AZ'].append(count2[0][0])
			ble['AZ'].append(count3[0][0])
        	if (statesearch[0]['admin1'] == 'Maryland'):
                	uncategorized['MD'].append(count1[0][0])
			categorized['MD'].append(count2[0][0])
			ble['MD'].append(count3[0][0])
        	if (statesearch[0]['admin1'] == 'Illinois'):
                	uncategorized['IL'].append(count1[0][0])	
			categorized['IL'].append(count2[0][0])
			ble['IL'].append(count3[0][0])
        
	#cur.execute("select count(distinct(mac)) from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision and not(devmajor = 31 and devminor = 0)")
        #count = cur.fetchall()
		print l
	cur.execute("select distinct(mac) from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision and devtype = 1 and (devmajor = 31 and devminor = 0)")
	hitmatches = cur.fetchall()
	for row in hitmatches:
		
	cnt += 1
	print cnt
	
cur.execute("drop table cod_cdf_table")
#print categorized
with open('categorized_filtered.json','wb') as file:
	file.write(json.dumps(categorized))

with open('uncategorized_filtered.json','wb') as file:
	file.write(json.dumps(uncategorized))
with open('ble_filtered.json','wb') as file:
	file.write(json.dumps(ble))
#num_bins = 10
'''
fig,ax = plt.subplots(figsize=(12,6))
counts,bin_edges = np.histogram (categorized,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Categorized')

#fig,ax = plt.subplots(figsize=(12,6))
counts,bin_edges = np.histogram (no_skimmer,bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Uncategorized')
'''
