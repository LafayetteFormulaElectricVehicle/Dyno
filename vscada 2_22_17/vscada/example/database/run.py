import sqlite3
import csv

Database = 'Test.db'

db = sqlite3.connect(Database)

cursor = db.cursor()
search =8
tuple = cursor.execute("select name, Units, rrd_db from sensor_table" )

for e in tuple:
	print (e);