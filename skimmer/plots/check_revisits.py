import pickle
import psycopg2
import csv
hitlist_match = []
with open('hitlist_matchlist','rb') as f:
        hitlist_match = pickle.load(f)
rssi_dict = {}
con = None

con = psycopg2.connect("dbname='skimmer' user='nibhaska'")
cur = con.cursor()

for idx in hitlist_match:
	if idx[0] not in rssi_dict:
		cur.execute("select t,loc,rssi from near_gasstation where mac = '"+idx[0]+"'::macaddr and fuelsta_loc is not null")
		records = cur.fetchall()
		maxrssi = records[0][2]
		maxloc = records[0][1]
		for jdx in range(0,len(records)):
			if records[jdx][2] > maxrssi :
				maxrssi = records[jdx][2]
				maxloc = records[jdx][1]
		rssi_dict[idx[0]] = (maxrssi,maxloc)
		print idx[0],maxrssi,maxloc

print 'Number of records: ',len(rssi_dict)
cur.close()
con.close()
with open('max_rssi_location.csv','wb') as rssi_file:
	rssi_writer = csv.writer(rssi_file,delimiter=',')
	for idx in rssi_dict:
		newrow = []
		loc = eval(rssi_dict[idx][1])
		newrow.append(idx)
		newrow.append(loc[1])
		newrow.append(loc[0])
		newrow.append(rssi_dict[idx][0]) 
		rssi_writer.writerow(newrow)


	
#for idx in rssi_dict:
	#print idx,rssi_dict[idx][0],rssi_dict[idx][1]	
