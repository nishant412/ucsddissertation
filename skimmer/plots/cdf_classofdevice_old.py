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

cur.execute("create table cod_cdf_table as (select distinct on (mac) mac,loc,devmajor,devminor from enqresp where devtype = 1 and loc is not null)")
for row in rows:
	cur.execute("select count(distinct(mac)) from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision and (devmajor = 31 and devminor = 0)")
#cur.execute("select count(distinct(mac)) from enqresp where loc <@> '(-117.0638248,32.5941849)'::point < 0.038::double precision and devtype = 1 and not(devmajor = 31 and devminor = 0)")
	count = cur.fetchall()
#categorized.append(count[0][0])
	#print count[0][0]
	r = eval(row[0])
	l = (r[1],r[0])
	statesearch = rg.search(l)
	print statesearch[0]['admin1'] 
	print count[0][0]
	if (statesearch[0]['admin1'] == 'California'):
		categorized['CA'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'North Carolina'):
                categorized['NC'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'Nevada'):
                categorized['NV'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'Arizona'):
                categorized['AZ'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'Maryland'):
                categorized['MD'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'Illinois'):
                categorized['IL'].append(count[0][0])	
        
	cur.execute("select count(distinct(mac)) from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision and not(devmajor = 31 and devminor = 0)")
        count = cur.fetchall()
        if (statesearch[0]['admin1'] == 'California'):
                uncategorized['CA'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'North Carolina'):
        	uncategorized['NC'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'Nevada'):
                uncategorized['NV'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'Arizona'):
                uncategorized['AZ'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'Maryland'):
                uncategorized['MD'].append(count[0][0])
        if (statesearch[0]['admin1'] == 'Illinois'):
                uncategorized['IL'].append(count[0][0])
	print l
	cnt += 1
	print cnt
	

#print categorized
with open('categorized.json','wb') as file:
	file.write(json.dumps(categorized))

with open('uncategorized.json','wb') as file:
	file.write(json.dumps(uncategorized))
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
