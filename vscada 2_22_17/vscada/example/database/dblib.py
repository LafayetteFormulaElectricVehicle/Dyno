import sqlite3
import csv
import os

'''
need to do something about the path
'''
directory = os.path.dirname(os.path.abspath(__file__))
Database = os.path.join(directory, 'Test.db')

# fucntion for getting calibration info
def getSampleRateTable():
	return readDatabase(columns='sample_rate,id_can,id_sensor', tables='sensor_table')

# fucntion for getting calibration info
def getFullSensorTable():
	return readDatabase(columns='*', tables='sensor_table')

# function call that can read some columns from one or more tables
def readDatabase(tables, columns, **kargs):


	db = sqlite3.connect(Database)

	cursor = db.cursor()

	'''
	TO DO: parse kargs
	'''
	try:
		tuples = cursor.execute("select %s from %s" % (columns, tables))
	except sqlite3.Error:
		'''

		'''
		raise

	result = []

	result.append(tuple([i[0] for i in cursor.description]))

	for e in tuples:
		result.append(e);

	db.close()

	return result
