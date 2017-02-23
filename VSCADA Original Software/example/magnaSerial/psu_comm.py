#!/bin/env/python3

"""This Python Class Handles Communication with the Power Supply Control"""

from scpi import scpi_device
import serial
import re


class magnascpi():
	def __init__(self):
		self.ser = serial.Serial()
		self.configSerial()

	def configSerial(self):
		self.ser.baudrate = 19200
		self.ser.port = "/dev/pts/ttyS0"
		self.ser.bytesize = serial.EIGHTBITS
		self.ser.parity = serial.PARITY_NONE
		self.ser.timeout = 0
		self.ser.open()


	def serialWrite(self,data):
		return self.ser.write(data.encode())


	def serialClose(self):
		print("Closing")
		self.ser.close()

	def serialRead(self):
		print("Data:",self.ser.read(1))

	# Control the state of the Magna Power Controller

	#MEAS:VOLT?
	#Read the Voltage, Current and Power Supply
	def get_volt(self):
			cmd = "MEAS:VOLT?"
			regex = '''MEAS:VOLT(\d{0,2}\.\d{0,2})'''####################
			resp = _send_cmd(self, cmd, regex)
			#return resp[0]
			print("Sent get_voltage \n")

	#Current 
	# MEAS:CURR?
	def get_curr(self):
		cmd = "MEAS:CURR?"
		regex = '''MEAS:CURR(\d{0,2}\.\d{0,2})'''########################
		resp = _send_cmd(self, cmd, regex)
		#return resp[0]

	def get_state(self):
		cmd = 'OUTP?'
		regex = '''OUTP?='''
		resp = _send_cmd(self, cmd, regex)
		#return resp[0]
		print("The Power Supply is (1=ON, 0=OFF)???")



	
	#Voltage
	# VOLT 200
	def set_voltage(self,setTo):
			cmd = "VOLT " + str(setTo)
			regex = '''VOLT'''#########################
			resp = _send_cmd(self,cmd, regex)
			print("Voltage set to:", setTo,"\n")
			#return resp[0]

	#Set the Current 
	def set_current(self,setTo):####################################
			cmd = "CURR " + str(setTo)
			regex = '''CURR'''
			resp = _send_cmd(self, cmd, regex)
			print("Current set to:", setTo,"\n")
			#return resp[0]

	def set_state(self,OnoOff):
		if OnoOff == "On":
			cmd = "OUTP:START"
			regex = "OUTP:START"
			resp = _send_cmd(self,cmd, regex)
			print("Turned On")

		elif OnoOff ==  "Off":
			cmd = "OUTP:STOP"
			regex = "OUTP:STOP"
			resp = _send_cmd(self,cmd, regex)
			print("Turned Off")


def _send_cmd(self, cmd, regex):
	try:
		#resp = dev.send_message(cmd)
		resp = serialComm.serialWrite(cmd)
		m = re.findall(regex, resp)
		if m:
			return m
	except:
		print('ERR: Message "' + cmd + '" not recognized!')
	return None


if __name__ == "__main__":
	print("Hello")
	serialComm = magnascpi()
	serialComm.set_voltage(555)
	serialComm.set_current(432)
	serialComm.set_state("On")
	serialComm.set_state("Off")
	serialComm.get_volt()
	serialComm.get_curr()
	serialComm.get_state()


	#print("Data Written:",serialComm.serialWrite('hello Test'))
	


	#serialComm.serialClose()
