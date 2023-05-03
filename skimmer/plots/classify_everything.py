import psycopg2

con = None
cnt = 0
con = psycopg2.connect("dbname='skimmer' user='nibhaska'")
cur = con.cursor()

class_dict = {}
class_dict[0] = ['Miscellaneous',0]
class_dict[1] = ['Computer',0]
class_dict[2] = ['Phone',0]
class_dict[3] = ['Network Access Point',0]
class_dict[4] = ['A/V',0]
class_dict[5] = ['Peripheral',0]
class_dict[6] = ['Imaging',0]
class_dict[7] = ['Wearable',0]
class_dict[8] = ['Toy',0]
class_dict[9] = ['Health',0]
class_dict[31] = ['Uncategorized',0]
mac_dict = {}
ble_mac_dict = {}
cur.execute("select mac,devname,devmajor,devminor from missing_1 where devtype = 1 and fuelsta2_loc is not null and t <= '2018-11-01 07:00:00'")
rows = cur.fetchall()

uncategorized_names = []
for row in rows :
	if row[0] not in mac_dict:
		if row[2] in class_dict:
			class_dict[row[2]][1] += 1
			mac_dict[row[0]] = 1
			if (row[2] == 31 or row[2] == 0) :
				uncategorized_names.append(row)	
		else:
			print row[0],row[1],row[2],row[3]

#print class_dict

ble_count = 0
cur.execute("select mac,devname,devmajor,devminor from missing_1 where devtype != 1 and fuelsta2_loc is not null")
rows = cur.fetchall()
for row in rows:
	if row[0] not in ble_mac_dict:
		ble_count += 1
		ble_mac_dict[row[0]] = 1

print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
print 'BLE Devices:', ble_count	
print 'Classic Devices:', len(mac_dict)
print '================================'
for key in class_dict:
	print class_dict[key][0],':',class_dict[key][1]
print '================================'

no_name_count = 0
#lmu_count = 0
#kt_count = 0
#ap_count = 0
tracker_count = 0
obd_count = 0
default_count = 0
sleep_count = 0
audio_count = 0
for row in uncategorized_names:
	if ((row[1] == '') or (row[1]== None) or (row[1] == 'None')):
		no_name_count += 1
	elif ((row[1][:3] == 'LMU') or (row[1][:4] == 'HDLM') or (row[1][:5] == 'fleet')):
		tracker_count += 1
	elif ((row[1][:2] == 'KT') or (row[1][:4] == 'AP00') or (row[1][:3] == 'OBD') or (row[1][:4] == 'Dash') or (row[1][:7] == 'IMClean')):
		obd_count += 1
	elif ((row[1][:4] == 'RNBT') or (row[1][:5] == 'HC-05')):
		default_count += 1
	elif ((row[1][:5] == 'PR BT')):
		sleep_count += 1
	elif ((row[1][:4] == 'FH-X') or (row[1][:3] == 'DEH') or (row[1][:4] == 'GENX') or (row[1][:5] == 'SP100') or (row[1][:5] =='AVH-P') or (row[1][:8] == 'Magnetic') or (row[1][:3] == 'AVH')):
		audio_count += 1
	else:
		print row[1]
print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
print 'No Names: ', no_name_count
print 'Vehicle Tracker:',tracker_count
print 'OBD Reader:',obd_count
print 'Sleep Monitoring:',sleep_count
print 'Car stereo/speaker:',audio_count
print 'Default module name:',default_count

cur.close()
con.close()
