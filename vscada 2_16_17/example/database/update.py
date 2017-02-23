import sqlite3
import csv

Database = 'Test.db'

db = sqlite3.connect(Database);

cursor = db.cursor()

with open('sensorList.csv', 'r') as ifile:
	reader = csv.reader(ifile)
	headers = next(reader)

	
	for row in reader:
		id_main = int(row[0])
		name = row[1]
		id_CAN = int(row[2])
		id_sensor = int(row[3])
		Type = row[4]
		sample_rate = int(row[5])
		overwrite_peroid = int(row[6])
		units = row[7]
		factor = int(row[8])
		offset = int(row[9])
		RRD_db = row[10]
		# (%i,%s,%i,%i,%s,%i,%i,%s,%i,%i,%s)
		cursor.execute('insert into sensor_table values(?,?,?,?,?,?,?,?,?,?,?)' , (id_main, name, id_CAN, id_sensor, Type, sample_rate,overwrite_peroid,units,factor, offset,RRD_db))

db.commit()

cursor.close()