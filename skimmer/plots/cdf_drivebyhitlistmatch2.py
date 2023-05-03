import pickle
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

uncategorized = {}
uncategorized['California'] = [0,0,0,0]
uncategorized['Arizona'] = [0,0,0,0]
uncategorized['Maryland'] = [0,0,0,0]
uncategorized['Illinois'] = [0,0,0,0]
uncategorized['North Carolina'] = [0,0,0,0]
uncategorized['Nevada'] = [0,0,0,0]
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
hitlist_matchA = ['00:06:66']
hitlist_matchB = ['33:60:80','ab:cd:ef','94:05:6f','20:18:08','20:17:05','1e:03:e0','20:17:09','98:d3:51','33:60:8a','88:18:56','6b:52:7c','8f:44:30','20:16:12','20:17:11','20:16:08','00:3c:7f','00:91:16','20:18:01','aa:bb:cc','8d:04:f8','66:35:56','11:22:33','20:13:04','58:51:00','ad:7a:ba','12:34:56','20:15:03','98:d3:32','09:f0:f0','22:22:83','20:15:04','47:ba:d0','22:22:47','60:30:d4','20:17:03']

drivebyname_uc = []
le_temp = []
uc_temp = []
cc_temp = []
gs_count = 0 
count_mac = []
gas_rows = []
countA = 0
countB = 0
flagA = 0
#cur.execute("create table cod_cdf_table as (select distinct on (mac) mac,loc,devmajor,devminor,devtype from enqresp where loc is not null)")
cur.execute("create table cod_cdf_table as (select t,mac,loc,devmajor,devminor,devtype,devname from near_gasstation where fuelsta_loc is not null)")
flag1 = 0
for row in rows:
	r = eval(row[0])
	l = (r[1],r[0])
	statesearch = rg.search(l)
	key = statesearch[0]['admin1']
	cur.execute("select * from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision order by t asc")
	records = cur.fetchall()
	if(records):
		for idx in records:
			#print idx[1]
			if ((idx[1][:8] in hitlist_matchA) and (idx[3] == 31) and (idx[4] == 0)):
				drivebyname_uc.append((idx[1],idx[6],key))
				if (idx[1] not in drivebycheck_uc):
					countA += 1
					drivebycheck_uc[idx[1]] = 1
				
			if ((idx[1][:8] in hitlist_matchB) and (idx[3] == 31) and (idx[4] == 0)):
				drivebyname_uc.append((idx[1],idx[6],key))
				if (idx[1] not in drivebycheck_uc):
					countB += 1
					drivebycheck_uc[idx[1]] = 1	
	'''
	r = eval(row[0])
	l = (r[1],r[0])
	statesearch = rg.search(l)
	key = statesearch[0]['admin1']	
	'''
	if key in uncategorized :
		if (countA !=0 and countB != 0):
			uncategorized[key][2] += 1
		elif (countA == 0 and countB !=0):
			uncategorized[key][1] += 1
		elif (countA != 0 and countB == 0):
			uncategorized[key][0] += 1
		else:
			flag1 = 1
	countA = 0
	countB = 0
	if (flag1):
		flag = 0
		more_than_30 = 0
		i = 0
		while i < len(records):
			if(flag == 0):
				cur_time = records[i][0]
				flag = 1
				i += 1
			else:
				new_time = records[i][0]
				difftime = new_time - cur_time
				if(difftime.seconds <= 30):
					i += 1
				elif(difftime.seconds > 30 and difftime.seconds < 120):
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
			'''
			r = eval(row[0])
			l = (r[1],r[0])
			statesearch = rg.search(l)
			key = statesearch[0]['admin1']
			'''
			#print count1
			if key in uncategorized :
				uncategorized[key][3] += 1
		more_than_30 = 0
	flag1 = 0
	cnt += 1
	print cnt
'''
drivebycheck_uc = {}
cnt = 0 
print len(gas_rows)

for row in gas_rows:
	cur.execute("select * from cod_cdf_table where loc <@> '" + row[0] +"'::point < 0.038::double precision order by t asc")
	records = cur.fetchall()
	
	flag = 0
	i = 0
	#cur_time = records[0][0]
	while i < len(records):
		if(flag == 0):
			cur_time = records[i][0]
			flag = 1
			i += 1
		else:
			new_time = records[i][0]
			difftime = new_time - cur_time
			if(difftime.seconds <= 30):
				i += 1
			elif(difftime.seconds > 30 and difftime.seconds < 120):
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
		key = statesearch[0]['admin1'] 
		#print count1
		if key in uncategorized :
			uncategorized[key][3] += 1
	more_than_30 = 0
	cnt +=1
	print cnt
'''	
cur.execute("drop table cod_cdf_table")
#print categorized
with open('hitlist_matchlist','wb') as f:
	pickle.dump(drivebyname_uc,f)
with open('uncategorized_hitlist.json','wb') as file:
        file.write(json.dumps(uncategorized))
for key in uncategorized:
	print key,' & ',uncategorized[key][3],' & ',uncategorized[key][0],' & ',uncategorized[key][1],' & ',uncategorized[key][2],' \\\\'
#num_bins = 10
