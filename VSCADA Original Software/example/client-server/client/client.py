import socket
import struct
import sys
import time

#PyQt4 Bindings
from PyQt4 import QtCore, QtGui
from ui_client import *

HOST, PORT = ('127.0.0.1', 2015)

def send(msg):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	s.sendall(bytes(msg, 'utf8'))

	recv = s.recv(4096)

	s.close()

	return recv

def recv():
	sensorList = send('sensor list').decode('utf8').split(',')
	rValue = []
	for sensor in sensorList:
		cmd = 'sensor value ' + sensor
		val = struct.unpack('f', send(cmd))[0]
		rValue.append(val)
	return rValue

class Window(QtGui.QMainWindow, Ui_ClientDemo):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setupUi(self)

def update():
	sensorList = recv()

	window.lcd1.display(sensorList[0])
	window.lcd2.display(sensorList[1])
	window.lcd3.display(sensorList[2])
	window.lcd4.display(sensorList[3])

window = ''
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = Window()
	timer = QtCore.QTimer()
	timer.timeout.connect(update)
	timer.start(250)
	
	window.show()
	sys.exit(app.exec_())
