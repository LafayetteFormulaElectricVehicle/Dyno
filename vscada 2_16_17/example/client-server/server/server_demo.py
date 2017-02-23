import socketserver
import struct
import sqlite3
import sys
import threading
import json
import csv
from pprint import pprint

#PyQt4 Bindings
from PyQt4 import QtCore, QtGui
from ui_server import *

HOST, PORT = ('127.0.0.1', 2015)

try:
	json_data = open('config.json').read()
except IOError:
	print('Config file missing')
	sys.exit(0)
sensorList = json.loads(json_data)
pprint(sensorList)
conn = sqlite3.connect('sensors.db')
db = conn.cursor()
db.execute('CREATE TABLE IF NOT EXISTS sensor_list (id INTEGER PRIMARY KEY, name TEXT UNIQUE)')
db.execute('CREATE TABLE IF NOT EXISTS sensor_data (id INTEGER, value INTEGER)')
for sensor in sensorList['sensorList']:
	db.execute('INSERT OR IGNORE INTO sensor_list (name) VALUES (?)', (sensor['name'],))
conn.commit()
conn.close()

class AsynchrounousTimer(threading.Thread):
	def run(self):
		while True:
			Time.sleep(.5)

class MyTCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		recv = self.request.recv(4096).strip().decode('utf8')
		addr = self.client_address[0]
		cmd = recv.split(' ')
		print(addr)
		print(cmd)
		if cmd[0] == 'sensor':
			if cmd[1] == 'value':
				for sensor in sensorList['sensorList']:
					if sensor['name'] == cmd[2]:
						data = struct.pack('f', sensor['value'])
						self.request.sendall(data)
			elif cmd[1] == 'list':
				response = ''
				for sensor in sensorList['sensorList']:
					if response != '':
						response += (',' + sensor['name'])
					else:
						response += (sensor['name'])
				self.request.sendall(bytes(response, 'utf8'))
		else:
			self.request.sendall('ERROR')

class ServerThread(QtCore.QThread):
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
	
	def run(self):
		self.server.serve_forever()
		
	def quit(self):
		self.server.shutdown()

class Window(QtGui.QMainWindow, Ui_ServerDemo):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setupUi(self)
		self.slider1.valueChanged.connect(self.slider1Changed)
		self.slider2.valueChanged.connect(self.slider2Changed)
		self.slider3.valueChanged.connect(self.slider3Changed)
		self.slider4.valueChanged.connect(self.slider4Changed)
	
	def slider1Changed(self):
		sensorList['sensorList'][0]['value'] = self.slider1.value()
		self.lcd1.display(self.slider1.value())
		conn = sqlite3.connect('sensors.db')
		db = conn.cursor()
		db.execute('SELECT id FROM sensor_list WHERE name="Voltage"')
		sensor_id = db.fetchone()[0]
		db.execute('INSERT INTO sensor_data VALUES (?, ?)', 
				   (sensor_id, self.slider1.value()))
		conn.commit()
		conn.close()
	
	def slider2Changed(self):
		sensorList['sensorList'][1]['value'] = self.slider2.value()
		self.lcd2.display(self.slider2.value())
		
	def slider3Changed(self):
		sensorList['sensorList'][2]['value'] = self.slider3.value()
		self.lcd3.display(self.slider3.value())
		
	def slider4Changed(self):
		sensorList['sensorList'][3]['value'] = self.slider4.value()
		self.lcd4.display(self.slider4.value())

	def closeEvent(self, *args, **kwargs):
		super(QtGui.QMainWindow, self).closeEvent(*args, **kwargs)
		conn = sqlite3.connect('sensors.db')
		db = conn.cursor()
		db.execute('SELECT * FROM sensor_data')
		with open('sensor_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=' ')
			writer.writerows(db)
		conn.commit()
		conn.close()
		
if __name__ == "__main__":
	server = ServerThread()
	server.start()
	app = QtGui.QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec_())
