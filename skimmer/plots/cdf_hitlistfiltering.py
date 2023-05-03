#!/usr/bin/python3
import os
import psycopg2
import sys
import re
from os import path
import reverse_geocoder as rg
import pickle
import numpy as np
import matplotlib.pyplot as plt
from lib.generate_metrics import *
#from ast import literal_eval
import json

hitlist_filter = {}
hitlist_filter['CA'] = []
hitlist_filter['AZ'] = []
hitlist_filter['MD'] = []
hitlist_filter['IL'] = []
hitlist_filter['NV'] = []
hitlist_filter['NC'] = []
'''
uncat_maryland = []
cat_arizona = []
uncat_arizona = []
cat_illinois = []
uncat_illinois = []
'''
con = None
cnt = 0
con = psycopg2.connect("dbname='skimmer' user='server'")
cur = con.cursor()

cur.execute("select distinct(loc) from fuelsta")
rows = cur.fetchall()
cur.execute("select count(distinct(mac)) from enqresp where loc is not null;")
rows = cur.fetchall()
print("Stage 0")
print(rows[0][0])
# Get all classic bt devices
cur.execute("create table bluetana_filter1 as (select distinct on (mac) mac,loc,devname,devmajor,devminor from enqresp where devtype = 1 and loc is not null)")
cur.execute("select count(*) from bluetana_filter1;")
rows = cur.fetchall()
print("Stage 1")
print(rows[0][0])
# Get points near stations
cur.execute("create table bluetana_filter1_0 as (select distinct on (a.mac) a.mac,a.loc,a.devmajor,a.devminor,a.devname,b.loc as fuelsta_loc from bluetana_filter1 a left join fuelsta b on a.loc <@> b.loc < 0.038::double precision)") 
# Get unique number of MACs
cur.execute("select count(distinct(mac)) from bluetana_filter1_0 where fuelsta_loc is not null")
rows = cur.fetchall()
print("Stage 2")
print(rows[0][0])
# Get uncatagorized devices
cur.execute("create table bluetana_filter1_1 as (select mac,loc,devname,fuelsta_loc from bluetana_filter1_0 where devmajor = 31 and devminor = 0 and fuelsta_loc is not null)")
# Get count of uncatagorized devices
cur.execute("select count(distinct(mac)) from bluetana_filter1_1")
rows = cur.fetchall()
print("Stage 3")
print(rows[0][0])
# Filter by the hitlist
print("Stage 4")
cur.execute("create table bluetana_filter2 as (select a.mac, a.devname, a.loc, a.fuelsta_loc, b.mac as hitlist_mac from bluetana_filter1_1 a left join (select distinct(trunc(mac)) mac from btskim_reduced) b on trunc(a.mac) = trunc(b.mac) where a.fuelsta_loc is not null)")
cur.execute("select count(*) from bluetana_filter2 where hitlist_mac is not null")
rows = cur.fetchall()
print(rows[0][0])
# Cluster names
print("Stage 5")
manager = Data_Manager()
print(manager.get_me_some_good_name_clusters_uh_huh_thats_what_im_talking_about(cur, "select * from bluetana_filter2 where hitlist_mac is not null"))
#print output
'''
cur.execute("select mac,devname,loc,fuelsta_loc,hitlist_mac from bluetana_filter2 where hitlist_mac is not null")
output = cur.fetchall()
'''
cur.execute("drop table bluetana_filter1")
cur.execute("drop table bluetana_filter1_0")
cur.execute("drop table bluetana_filter1_1")
cur.execute("drop table bluetana_filter2")

'''
for row in output:
	r = eval(row[3])
	l = (r[1],r[0])
	statesearch = rg.search(l)
	#print statesearch[0]['admin1']
	if (statesearch[0]['admin1'] == 'California'):
		hitlist_filter['CA'].append(row)               
	if (statesearch[0]['admin1'] == 'North Carolina'):
		hitlist_filter['NC'].append(row)        
	if (statesearch[0]['admin1'] == 'Nevada'):
		hitlist_filter['NV'].append(row)
	if (statesearch[0]['admin1'] == 'Arizona'):
		hitlist_filter['AZ'].append(row)  
	if (statesearch[0]['admin1'] == 'Illinois'):
		hitlist_filter['IL'].append(row)  
	if (statesearch[0]['admin1'] == 'Maryland'):
		hitlist_filter['MD'].append(row)	

with open('hitlist_filtered.json','wb') as file:
	file.write(json.dumps(hitlist_filter))
'''

cur.close()
con.close()
'''

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

fig,ax = plt.subplots(figsize=(12,6))
counts,bin_edges = np.histogram (categorized,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Categorized')

#fig,ax = plt.subplots(figsize=(12,6))
counts,bin_edges = np.histogram (no_skimmer,bins=bin_vals,normed=True)
cdf = np.cumsum(counts)
ax.plot (bin_edges[1:],cdf/cdf[-1],linewidth = 2.0,label = 'Uncategorized')
'''
