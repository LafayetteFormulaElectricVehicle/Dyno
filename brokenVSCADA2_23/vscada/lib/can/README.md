#Python SocketCAN Abstraction Library#

##Overview##

This library is responsible for managing linux SocketCAN connections, and 
wrapping them to human-reabalbe python methods. This library contains the 
methods necessary to form, send and receive CAN frames.

##Requirements##

This library requires Python3 to run. SocketCAN is not supported by Python2,
so this library is not backwards compatible. This library requires no
additional library support to operate, however 'can-utils' package is
recomended for debugging purposes.

##Usage##
All commands given below are run in a python3 interpreter shell.

**Initialize:**
```
	python3 > import can_lib 
	python3 > can_handler = can_lib.CANHandler('vcan0')
```
**Send a Frame:**
```
	python3 > frame = {
		"id": 0,
		"rtr": False,
		"data": (0, 1, 2, 3, 4, 5, 6, 7)
	}
	python3 > can_handler.send_frame(frame)
```
**Receive a Frame:**
```
	python3 > can_handler.recv_frame()
	{"id": 0, "rtr": False, "dlc": 0, data": (0, 1, 2, 3, 4, 5, 6, 7)}
```
