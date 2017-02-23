"""
A simulation of all of the can id's you can expect to see on the
CAN communication line

This script will be extended to eventually collect all of the CAN
bus activity and save the data in whatever database is nessesary
or implement functions to take in the data 
Created by: Sam Cesario
"""
#imports
import CANlib
import binascii

dataGen = CANlib.DataFields
motorIds, jgbIds, packmanIds  = dataGen.getCanIds()
while True:
	listener = CANlib.bsr()
	can_id, data = listener.listenToCANframe()
	#MOTOR
	if can_id in motorIds:
		print("MOTOR can_id:",can_id)
	#JGB's
	if can_id in jgbIds:
		sensorId = [b'\x01',b'\x02',b'\x03',b'\x04']
		sensorData = [b'\x10',b'\x55',b'\x45',b'\x47']
		timeS = 1
		#listener.sendMessage(listener.buildJGBFrame(333,header,measH, measL))
		dataGen.simData(listener,sensorId,timeS,sensorData)
		#listener.printJGBMsg(can_id,header,measH,measL)

	#PACKMAN
	if can_id in packmanIds:
		print("PACKMAN can_id:",can_id," Data:",data)