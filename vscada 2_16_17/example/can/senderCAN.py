import CANlib
import socket
import sys


#CANlib.sendMessage(CANlib.buildMessage(0x123,b'\x11\x22\x33\x44\x55\x66\x77\x88'))
#CANlib.listenToCANframe()

#Send out a Message to all Sensors to See if they are alive

#import the CAN id's
#Ordering: Motor, GLVPD, PACKMAN
#Send To MOTOR
def sendToMotor(can_id,data):
	CANlib.sendMessage(CANlib.buildMessage(can_id,b'\x52'))

#Send To JGB 
def sendToJGB(can_id,data):
	sender = CANlib.bsr()
	msg = sender.buildMessage(can_id,data)
	sender.sendMessage(msg)

#Send To PACKMAN
def sendToPACKMAN(can_id,data):
	CANlib.sendMessage(CANlib.buildMessage(can_id,b'\x52'))


counter = 0 
while counter !=5:
	sendToJGB(200+counter,b'\x52')
	counter = counter + 1

