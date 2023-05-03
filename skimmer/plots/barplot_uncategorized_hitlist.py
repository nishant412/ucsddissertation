import os
import psycopg2
import sys
import re
from os import path
import reverse_geocoder as rg
import numpy as np
import matplotlib.pyplot as plt
import json

hitlist = {}

hitlist['RN-41'] = 0
hitlist['BTM41'] = 0
hitlist['HC-05'] = 0
hitlist['HC-06'] = 0
hitlist['MLT-BT05'] = 0
hitlist['CSRMod'] = 0

con = None
cnt = 0
con = psycopg2.connect("dbname='skimmer' user='nibhaska'")
cur = con.cursor()

cur.execute("create table hitlist_match_1 as (select distinct on (mac) mac,loc from enqresp where devtype = 1 and devmajor = 31 and devminor = 0)")

cur.execute("create table hitlist_match_2 as (select a.mac,b.loc from hitlist_match_1 a left join fuelsta b on a.loc <@> b.loc < 0.038::double precision)")

cur.execute("create table hitlist_match_3 as (select a.mac,b.modname from (select distinct (mac) from hitlist_match_2 where loc is not null) a left join (select * from btskim where mac = '20:16:09:26:63:82' or mac = '34:15:13:e5:ea:98' or mac = '00:06:66:7c:9a:61' or mac = '98:d3:32:70:b3:05' or mac = '00:13:04:00:d9:4e' or mac = '00:02:5B:01:01:01') b on trunc(a.mac) = trunc(b.mac))")

cur.execute("select * from hitlist_match_3 where modname is not null")

rows = cur.fetchall()

for row in rows:
	if(row[1] == 'RN-41'):
		hitlist['RN-41'] += 1
	if(row[1] == 'BTM41'):
		hitlist['BTM41'] += 1
	if(row[1] == 'HC-05'):
		hitlist['HC-05'] += 1
	if(row[1] == 'HC-06'):
		hitlist['HC-06'] += 1
	if(row[1] == 'MLT-BT05'):
		hitlist['MLT-BT05'] += 1
	if(row[1] == 'CSRMod'):
		hitlist['CSRMod'] += 1

'''
cur.execute("create table hitlist_match_3 as (select a.mac,b.name from (select distinct (mac) from hitlist_match_2 where loc is not null) a left join ieeereg2 b on a.mac <@ b.range)")

cur.execute("select * from hitlist_match_3 where name is not null")
rows = cur.fetchall()


for row in rows:
	key = row[1]
	if key not in hitlist:
		hitlist[key] = 1
	else:
		hitlist[key] += 1
'''		

cur.execute("drop table hitlist_match_1")
cur.execute("drop table hitlist_match_2")
cur.execute("drop table hitlist_match_3")
cur.close()
con.close()
with open('barplot_uncategorized_hitlist.json','wb') as file:
        file.write(json.dumps(hitlist))
