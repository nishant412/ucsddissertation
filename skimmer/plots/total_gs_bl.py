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
from datetime import datetime
from datetime import timedelta

count1 = 0
count2 = 0
count3 = 0

categorized = {}
categorized['California'] = []
categorized['Arizona'] = []
categorized['Maryland'] = []
categorized['Illinois'] = []
categorized['Nevada'] = []
categorized['North Carolina'] = []
uncategorized = {}
uncategorized['California'] = []
uncategorized['Arizona'] = []
uncategorized['Maryland'] = []
uncategorized['Illinois'] = []
uncategorized['Nevada'] = []
uncategorized['North Carolina'] = []
ble = {}
ble['CA'] = []
ble['AZ'] = []
ble['MD'] = []
ble['IL'] = []
ble['NV'] = []
ble['NC'] = []
hitlist_by_man = {}
drivebycheck_uc = {}
drivebycheck_cc = {}
drivebycheck_le = {}
con = None
cnt = 0
con = psycopg2.connect("dbname='skimmer' user='nibhaska'")
cur = con.cursor()

cur.execute("select distinct(loc) from fuelsta")
rows = cur.fetchall()

le_temp = []
uc_temp = []
cc_temp = []
gs_count = 0 


#cur.execute("create table cod_cdf_table as (select distinct on (mac) mac,loc,devmajor,devminor,devtype from enqresp where loc is not null)")
cur.execute("create table cod_cdf_table as (select t,mac,loc,devmajor,devminor,devtype from near_gasstation where fuelsta_loc is not null and t <= '2018-11-01 07:00:00')")
for row in rows:
	cur.execute("select * from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision order by t asc")
	records = cur.fetchall()
	
	flag = 0
	flag2 = 0
	i = 0
	gs_count = 0
	more_than_30 = 0
	drivebycheck = {}
	#cur_time = records[0][0]
	while i < len(records):
		if(flag == 0):
			cur_time = records[i][0]
			if (records[i][5] == 1 and (records[i][1] not in drivebycheck_uc)):
				drivebycheck_uc[records[i][1]] = 1
				gs_count += 1
				count1 += 1
			else:
				gs_count += 1
			flag = 1
			i += 1
		else:
			new_time = records[i][0]
			difftime = new_time - cur_time
			if(difftime.seconds <= 30):
				if (records[i][5] == 1 and (records[i][1] not in drivebycheck_uc)):
					drivebycheck_uc[records[i][1]] = 1
					gs_count += 1
					count1 += 1
				else:
					gs_count += 1
				i += 1
			elif(difftime.seconds > 30 and difftime.seconds < 60):
				if (records[i][5] == 1 and (records[i][1] not in drivebycheck_uc)):
					drivebycheck_uc[records[i][1]] = 1
					gs_count += 1
					count1 += 1
				else:
					gs_count +=1
				more_than_30 = 1
				i += 1
			
			else:
				if(more_than_30 == 1):
					break
				else:
					flag = 0
					more_than_30 = 0
					continue

	if (more_than_30 == 1):
		r = eval(row[0])
		l = (r[1],r[0])
		statesearch = rg.search(l)
		print statesearch[0]['admin1'] 
		print count1
		key = statesearch[0]['admin1']
		if key in uncategorized:
			uncategorized[key].append(count1)
		#categorized
	
	count1 = 0
	count2 = 0
	count3 = 0
	more_than_30 = 0
	cnt +=1
	print cnt

for key in uncategorized:
	sum = 0
	for idx in uncategorized[key] :
		sum += idx
	print key,':',sum	
cur.execute("drop table cod_cdf_table")
#print categorized

with open('uncategorized_filtered.json','wb') as file:
	file.write(json.dumps(uncategorized))
#num_bins = 10
