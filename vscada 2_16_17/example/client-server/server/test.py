import sqlite3

conn = sqlite3.connect('sensors.db')
db = conn.cursor()
for row in db.execute("SELECT * FROM sensor_data"):
	print(row)
