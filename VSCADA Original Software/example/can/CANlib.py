"""
This document describes the CAN interface library for the VSCADA team that
will facilitate communication with other subsystems

Created by: Sam Cesario
"""
#imports
import socket
import struct
import sys
import subprocess #For running bash commands
import binascii #For data conversion
import time
import select

#############USING SOCKETS###############

"""This class handles the builing and sending and reading of CAN frames """
class bsr:

	def __init__(self):
		#Package the CAN frame
	#Format: =(native)I(unsigned Int)B(unsinged char)3()x(pad byte)8()s(char[])
	#Our Format:                       can_id             can_dlc    8-byte string
		self.can_frame_fmt = "=IB3x8s"
		#Create a Raw Socket
		self.s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
		#bind the socket to the CAN interface
		#FIXME Parameterize? Input class parameter
		self.s.bind(("vcan0",))
	"""buildMessage(can_id,data) builds a CAN frame with the associated id and data """
	#Build a Message with data and a can_id
	def buildMessage(self,can_id, data):
		#defne the length
		self.can_dlc = len(data)
		#define the data
		data = data.ljust(8, b'\x00')
		return struct.pack(self.can_frame_fmt, can_id, self.can_dlc, data)

	def sendMessage(self,msg):
		self.s.send(msg)
	
	def listenToCANframe(self):
		cf, addr = self.s.recvfrom(16)
		can_id, can_dlc, data = struct.unpack(self.can_frame_fmt, cf)
		#print("ID=%x DLC:=%x  Data=%s" % readCANframe(cf))
		return(can_id, data)

	def listenToCANframeWithTimeout(self, timeout):
		ready = select.select([self.s], [], [], timeout)
		if (ready[0]):
			cf, addr = self.s.recvfrom(16)
			can_id, can_dlc, data = struct.unpack(self.can_frame_fmt, cf)
			return(can_id, data)
		else:
			print('socket time out')
			return ()

	#This method Builds the JGB Frame 
	def buildJGBFrame(self,can_id,header,measHigh,measLow):
		header = header.ljust(2)
		measHigh = measHigh.ljust(2)
		measLow = measLow.ljust(2)
		dataTo = header + measHigh + measLow
		dataTo = dataTo.ljust(8)
		#define the Length
		self.can_dlc = len(dataTo)
		#print(binascii.hexlify(dataTo))
		return struct.pack(self.can_frame_fmt, can_id, self.can_dlc, dataTo)
	#Converts and Decodes Hexidecimal
	def binToHex(self,binData):
		return binascii.hexlify(binData).decode("utf-8")
	def printJGBMsg(self,can_id,header,measH,measL):
		print("JGB", can_id ,", Received Remote Frame")
		print("Replying from Sensor", self.binToHex(header))
		print("Data Sent:",self.binToHex(measH),self.binToHex(measL))
		print("-----------------------\n")
	#temporary
	def decodeJGBFrme(self, message):
		return [message[8], message[10], message[12]]

#This Class handles the simulated Data
#sensor_id = [1,2]
class DataFields:
	def __init__(self):
		listener = bsr()
	def getCanIds():
		motorIds = [61,62]
		jgbIds = [200,201,202,203,204]
		packManIds = [110,120,130,140]
		return(motorIds,jgbIds,packManIds)
	#This Method will eventually allow real data to be simulated
	def simData(listen,sensorId,timeS,sensorData):
		tLH = [b'\x34',b'\x36',b'\x38',b'\x40',b'\x45',b'\x50',b'\x55']
		sd = [0,1,2,3]
		i=0
		for sense in sensorId:
			#for tempData in tLH:
			msg = listen.buildJGBFrame(333,sense,sensorData[i],sensorData[i])
			listen.printJGBMsg(333,sense,sensorData[i],sensorData[i])
			time.sleep(timeS)
			listen.sendMessage(msg)
			print(listen.decodeJGBFrme(msg))
			i = i + 1
