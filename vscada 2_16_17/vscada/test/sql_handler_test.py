import sys
sys.path.append('../')

from lib.sql_handler import sql_handler

testee = sql_handler.SQLDatabaseHandler('.././data/sql/sensor.db')

def test1():
	result = testee.select('table')

def test2():
	result = testee.select('can')

def test3():
	result = testee.select(['sensor', 'can'], "sensor_id","address_offset","byte_size", system_id=1,type_id=0)

tests = [test1, test2, test3]

if __name__ == "__main__":
	
	for test in tests:
		test()