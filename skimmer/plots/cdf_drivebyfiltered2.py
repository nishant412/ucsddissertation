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
cur.execute("create table cod_cdf_table as (select t,mac,loc,devmajor,devminor,devtype from near_gasstation where fuelsta_loc is not null)")
for row in rows:
	cur.execute("select * from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision order by t asc")
	records = cur.fetchall()
	
	flag = 0
	flag2 = 0
	i = 0
	gs_count = 0
	more_than_30 = 0
	drivebycheck = {}
	while i < len(records) :
		if(flag == 0):
			cur_time = records[i][0]
			if (records[i][5] == 1 and records[i][3] == 31 and records[i][4] == 0 and (records[i][1] not in drivebycheck_uc)):
				drivebycheck[records[i][1]] = 1
				gs_count += 1
				count1 += 1
			else:
				gs_count += 1
			flag = 1
			i += 1
		else:
			new_time = records[i][0]
			difftime = new_time-cur_time
			if(flag2 == 1):
				if (difftime.seconds <= 300):
					if (records[i][5] == 1 and records[i][3] == 31 and records[i][4] == 0 and (records[i][1] not in drivebycheck_uc)):
						drivebycheck[records[i][1]] = 1
						gs_count += 1
						count1 += 1
					else:
						gs_count += 1
					i += 1
				elif (difftime.seconds > 300 and difftime.seconds <= 900):
					i += 1
				else:
					flag = 0
					flag2 = 0
					i += 1
			else:
				#if (difftime.seconds <= 30):
				new_time = records[i][0]
				difftime = new_time-cur_time
				if (records[i][5] == 1 and records[i][3] == 31 and records[i][4] == 0 and (records[i][1] not in drivebycheck_uc)):
					drivebycheck[records[i][1]] = 1
					gs_count += 1
					count1 += 1
				else:
					gs_count += 1
				i += 1
				if(difftime.seconds > 30)
					flag2 = 1
					more_than_30 = 1
				
	if (more_than_30 == 1):
		r = eval(row[0])
		l = (r[1],r[0])
		statesearch = rg.search(l)
		print statesearch[0]['admin1'] 
		print count1
		if (statesearch[0]['admin1'] == 'California'):
			uncategorized['CA'].append(count1)
			categorized['CA'].append(count2)
			ble['CA'].append(count3)
        	if (statesearch[0]['admin1'] == 'North Carolina'):
                	uncategorized['NC'].append(count1)
			categorized['NC'].append(count2)
			ble['NC'].append(count3)
        	if (statesearch[0]['admin1'] == 'Nevada'):
			uncategorized['NV'].append(count1)
                	categorized['NV'].append(count2)
			ble['NV'].append(count3)
        	if (statesearch[0]['admin1'] == 'Arizona'):
                	uncategorized['AZ'].append(count1)
			categorized['AZ'].append(count2)
			ble['AZ'].append(count3)
        	if (statesearch[0]['admin1'] == 'Maryland'):
                	uncategorized['MD'].append(count1)
			categorized['MD'].append(count2)
			ble['MD'].append(count3)
        	if (statesearch[0]['admin1'] == 'Illinois'):
                	uncategorized['IL'].append(count1)	
			categorized['IL'].append(count2)
			ble['IL'].append(count3)
	
	count1 = 0
	count2 = 0
	count3 = 0
	more_than_30 = 0
	cnt +=1
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
