import sqlite3
import csv

DATABASE = "Test.db"
FILE = "sensorList.csv"



db = sqlite3.connect(DATABASE)

cursor = db.cursor()

cursor.execute('SELECT * FROM sensorList')

with open(FILE, 'r') as ifile:
	reader = csv.reader(ifile)
	headers = next(reader)

	for row in range(4):
		cursor.execute("""insert into sensorList values('a','b','c','d','e','f','g','h','i','j','k') """)

for row in cursor:
	print (row)
db.commit()

cursor.close()

	# table_name = FILE.replace('.csv', '')
	
	# table_headers = headers[0]
	# for i in range(1, len(headers)):
	# 	table_headers = ',' + table_headers;

	# c.execute('CREATE TABLE table_name(%s )' %table_headers)

	# for row in reader:
	# 	print(row)
		# cursor.execute('''INSERT INTO sensorList(id, name, id_CAN, id_Sensor, Type, Sample_rate, Overwrite_peroid, Units, Factor, Offset, RRD_DB) VALUES('A','B','C','D','E','F','G','H','I','J','K');''')



# # add table in database in csv file
# # def addTable(file, database)
# db = sqlite3.connect(DATABASE);

# cursor = db.cursor()

# cursor.execute(''' '''')



# # cursor.execute('''
# #     CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT,
# #                        phone TEXT, email TEXT unique, password TEXT)
# # ''')

# cursor.execute()
# db.commit()

# # c = conn.cursor()		

# # c.execute('create table test(name, address, college, phone)')

# # c.execute('insert into test(bikrm, fisher, lafayette, %s)'%str(123456789))

# # c.execute('select * from test')

# # conn.commit()

# # c.close()










