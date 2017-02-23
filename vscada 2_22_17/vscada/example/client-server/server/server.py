import socketserver
import struct
import sqlite3
import sys
import threading
import json
import csv
from pprint import pprint

HOST, PORT = ('127.0.0.1', 2015)

conn = sqlite3.connect('sensors.db')
db = conn.cursor()

db.execute('CREATE TABLE IF NOT EXISTS sensor_table (' + 
		   'id INTEGER PRIMARY KEY, ' + 
		   'name TEXT UNIQUE, ' + 
		   'id_can INTEGER, ' +
		   'id_sensor INTEGER, ' +
		   'type INTEGER, ' +
		   'sample_rate INTEGER, ' +
		   'overwrite_period INTEGER, ' +
		   'units INTEGER, ' +
		   'factor REAL, ' +
		   'offset REAL, ' +
		   'rrd_db TEXT)')

db.execute('CREATE TABLE IF NOT EXISTS sensor_types (' + 
		   'id INTEGER, ' + 
		   'description TEXT UNIQUE, ' + 
		   'type INTEGER, ' +
		   'direction INTEGER)')

db.execute('CREATE TABLE IF NOT EXISTS sensor_levels (' + 
		   'id INTEGER, ' + 
		   'warning_low REAL, ' + 
		   'warning_high REAL, ' +
		   'error_low REAL, ' +
		   'error_high REAL, ' +
		   'fail_low REAL, ' +
		   'fail_high REAL)')

db.execute('CREATE TABLE IF NOT EXISTS sensor_actions (' + 
		   'id INTEGER, ' + 
		   'action_name TEXT, ' + 
		   'priority_level INTEGER, ' +
		   'effector_name INTEGER, ' +
		   'effector_value INTEGER)')

db.execute('CREATE TABLE IF NOT EXISTS sensor_units (' + 
		   'id INTEGER, ' + 
		   'unit_description TEXT, ' + 
		   'unit_abbr TEXT)')
conn.commit()
conn.close()

class MyTCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		recv = self.request.recv(4096).strip().decode('utf8')
		addr = self.client_address[0]
		cmd  = recv.split(' ')
		print(addr)
		print(cmd)
		class_type     = cmd[0]
		action_type    = cmd[1]
		request_params = json.loads(cmd[2])
		handler = None
		if class_type == 'SQL':
			handler = SQLRequestHandler(action_type, request_params)
			self.request.sendall(bytes(handler.execute(), 'utf8'))
		elif class_type == 'RRD':
			handler = RRDRequestHandler(action_type, request_params)
			self.request.sendall(bytes(handler.execute(), 'utf8'))
		elif class_type == 'MSG':
			handler = MSGRequestHandler(action_type, request_params)
			self.request.sendall(bytes(handler.execute(), 'utf8'))
		else:
			self.request.sendall('ERROR')

class RequestHandler():
	def __init__(self, action_type, args):
		self.action_type = action_type
		self.args = args

	def execute():
		pass

class SQLRequestHandler(RequestHandler):
	def execute():
		conn = sqlite3.connect('sensors.db')
		db = conn.cursor()
		query = ''
		if(action_type == 'GET'):
			query = query + 'SELECT ' + request_params['name'] + ' FROM '
			query = query + request_params['type'] + ' WHERE '
			query = query + request_params['data'] + '=?'
			db.execute(query, request_params['value'])
			response = db.fetchone()[0]
			return response
		elif(action_type == 'SET'):
			query = query + 'INSERT INTO '
			
		elif(action_type == 'CREATE'):
			query = query + 'CREATE TABLE IF NOT EXISTS '
			pass

class RRDRequestHandler(RequestHandler):
	def execute():
		if(action_type == 'GET'):
			pass
		elif(action_type == 'SET'):
			pass
		elif(action_type == 'CREATE'):
			pass

class MSGRequestHandler(RequestHandler):
	def execute():
		if(action_type == 'GET'):
			pass
		elif(action_type == 'SET'):
			pass
		elif(action_type == 'CREATE'):
			pass

if __name__ == "__main__":
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()
