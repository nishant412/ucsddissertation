import json
import psycopg2
import csv

con = None

con = psycopg2.connect("dbname='skimmer' user='nibhaska'")
cur = con.cursor()

cur.execute("create table scatter_1 as (select * from enqresp where devtype = 1 and devmajor = 31 and devminor = 0)")
cur.execute("create table scatter_2 as (select t.* from (select mac,max(rssi) as max_rssi from scatter_1 group by mac) as m inner join scatter_1 as t on t.mac = m.mac and t.rssi = m.max_rssi)")
cur.execute("create table scatter_3 as (select a.mac,a.loc,a.devname,a.rssi,a.geo_accuracy,b.loc as fuelsta_loc from scatter_2 a left join fuelsta b on a.loc <@> b.loc <= 0.095::double precision)")
cur.execute("create table scatter_4 as (select * from scatter_3 where (trunc(mac) = '00:06:66:00:00:00' or trunc(mac) = '20:13:04:00:00:00' or trunc(mac) = '20:17:11:00:00:00' or trunc(mac) = '20:18:01:00:00:00' or trunc(mac) = '20:18:08:00:00:00') and fuelsta_loc is not null)")
cur.execute("create table scatter_5 as (select *,(loc <@> fuelsta_loc) as loc_diff from scatter_4)")
cur.execute("select t.* from (select mac,min(loc_diff) as min_diff from scatter_5 group by mac) as m inner join scatter_5 as t on t.mac = m.mac and t.loc_diff = m.min_diff order by t.mac asc")
#cur.execute("select * from scatter_5")
rows = cur.fetchall()

with open ('scatter_rssi_loc_data.csv',mode='wb') as scatter_file:
	scatter_writer = csv.writer(scatter_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
	for row in rows:
		scatter_writer.writerow(row)

cur.execute("drop table scatter_1")
cur.execute("drop table scatter_2")
cur.execute("drop table scatter_3")
cur.execute("drop table scatter_4")
cur.execute("drop table scatter_5")

cur.close()
con.close()

