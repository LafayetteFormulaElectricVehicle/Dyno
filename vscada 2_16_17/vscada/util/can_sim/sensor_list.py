import math
import time

ANALOG = 0
DIGITAL = 1

SP_BIN = 2
SP_I2C = 3

INPUT = 0
OUTPUT = 1

SLOTA = 0
SLOTB = 1
SLOTC = 2
SLOTD = 3
SLOTE = 4

RPM = 0
TORQUE = 1
VOLTAGE = 2
CURRENT = 3
SWITCH = 4
RELAY = 5
MANUAL = 6
AUTO = 7

#//can_board0 - 0x20
sensor00 = {'name': 'Sensor 00', 'mode': SP_BIN,  'direction': INPUT,  'addr': 0x20, 'slot': 0, 'value': 0, 'size':1}
sensor01 = {'name': 'Sensor 01', 'mode': SP_BIN,  'direction': INPUT,  'addr': 0x20, 'slot': 1, 'value': 0, 'size':1}
sensor02 = {'name': 'Sensor 02', 'mode': SP_BIN,  'direction': INPUT,  'addr': 0x20, 'slot': 2, 'value': 0, 'size':1}
sensor03 = {'name': 'Sensor 03', 'mode': SP_BIN,  'direction': OUTPUT, 'addr': 0x20, 'slot': 3, 'value': 0, 'size':1}
sensor04 = {'name': 'Sensor 04', 'mode': SP_BIN,  'direction': OUTPUT, 'addr': 0x20, 'slot': 4, 'value': 0, 'size':1}
sensor05 = {'name': 'Sensor 05', 'mode': SP_BIN,  'direction': OUTPUT, 'addr': 0x20, 'slot': 5, 'value': 0, 'size':1}
sensor06 = {'name': 'Sensor 06', 'mode': ANALOG,  'direction': INPUT,  'addr': 0x20, 'slot': SLOTC, 'value': 0, 'size':1}
sensor07 = {'name': 'Sensor 07', 'mode': ANALOG,  'direction': INPUT,  'addr': 0x20, 'slot': SLOTD, 'value': 0, 'size':1}
sensor08 = {'name': 'Sensor 08', 'mode': ANALOG,  'direction': OUTPUT, 'addr': 0x20, 'slot': SLOTE, 'value': 0, 'size':1}

#//can_board0 - 0x21
sensor09 = {'name': 'Sensor 09', 'mode': SP_BIN,  'direction': OUTPUT, 'addr': 0x21, 'slot': 0, 'value': 0, 'size':1}
sensor10 = {'name': 'Sensor 10', 'mode': SP_BIN,  'direction': OUTPUT, 'addr': 0x21, 'slot': 1, 'value': 0, 'size':1}
sensor11 = {'name': 'Sensor 11', 'mode': SP_BIN,  'direction': OUTPUT, 'addr': 0x21, 'slot': 2, 'value': 0, 'size':1}
sensor12 = {'name': 'Sensor 12', 'mode': SP_BIN,  'direction': INPUT,  'addr': 0x21, 'slot': 3, 'value': 0, 'size':1}
sensor13 = {'name': 'Sensor 13', 'mode': SP_BIN,  'direction': INPUT,  'addr': 0x21, 'slot': 4, 'value': 0, 'size':1}
sensor14 = {'name': 'Sensor 14', 'mode': SP_BIN,  'direction': INPUT,  'addr': 0x21, 'slot': 5, 'value': 0, 'size':1}
sensor15 = {'name': 'Sensor 15', 'mode': ANALOG,  'direction': OUTPUT, 'addr': 0x21, 'slot': SLOTC, 'value': 0, 'size':1}
sensor16 = {'name': 'Sensor 16', 'mode': ANALOG,  'direction': OUTPUT, 'addr': 0x21, 'slot': SLOTD, 'value': 0, 'size':1}
sensor17 = {'name': 'Sensor 17', 'mode': ANALOG,  'direction': OUTPUT, 'addr': 0x21, 'slot': SLOTE, 'value': 0, 'size':1}

#//can_board1 - 0x30
sensor18 = {'name': 'Sensor 18', 'mode': ANALOG,  'direction': INPUT,  'addr': 0x30, 'slot': SLOTA, 'value': 0, 'size':1}
sensor19 = {'name': 'Sensor 19', 'mode': ANALOG,  'direction': OUTPUT, 'addr': 0x30, 'slot': SLOTB, 'value': 0, 'size':1}
sensor20 = {'name': 'Sensor 20', 'mode': DIGITAL, 'direction': OUTPUT, 'addr': 0x30, 'slot': SLOTC, 'value': 0, 'size':1}
sensor21 = {'name': 'Sensor 21', 'mode': DIGITAL, 'direction': INPUT,  'addr': 0x30, 'slot': SLOTD, 'value': 0, 'size':1}
sensor22 = {'name': 'Sensor 22', 'mode': ANALOG,  'direction': OUTPUT, 'addr': 0x30, 'slot': SLOTE, 'value': 0, 'size':1}

#//can_board1 - 0x31
sensor23 = {'name': 'Sensor 23', 'mode': SP_I2C, 'direction': OUTPUT,  'addr': 0x31, 'slot': 0, 'value': 0, 'size':1}

#//motor controller - 0x61
sensor24 = {'name': 'tachometer', 'mode': ANALOG, 'direction': OUTPUT,  'addr': 0x61, 'slot': 0, 'value': 0, 'size':2, 'type': RPM}
sensor25 = {'name': 'torque', 'mode': ANALOG, 'direction': OUTPUT,  'addr': 0x61, 'slot': 2, 'value': 0, 'size':2, 'type': TORQUE}

#//GLV main - 0x99
sensor26 = {'name': 'voltage1', 'mode': ANALOG, 'direction': OUTPUT,  'addr': 0x99, 'slot': 0, 'value': 0, 'size':1, 'type': VOLTAGE}
sensor27 = {'name': 'voltage2', 'mode': ANALOG, 'direction': OUTPUT,  'addr': 0x99, 'slot': 1, 'value': 0, 'size':1, 'type': VOLTAGE}
sensor28 = {'name': 'current1', 'mode': ANALOG, 'direction': OUTPUT,  'addr': 0x99, 'slot': 2, 'value': 0, 'size':1, 'type': CURRENT}
sensor29 = {'name': 'current2', 'mode': ANALOG, 'direction': OUTPUT,  'addr': 0x99, 'slot': 3, 'value': 0, 'size':1, 'type': CURRENT}
sensor30 = {'name': 'input', 'mode': DIGITAL, 'direction': INPUT,  'addr': 0x99, 'slot': 4, 'value': 0, 'size':1, 'type': AUTO}
sensor31 = {'name': 'relay', 'mode': DIGITAL, 'direction': INPUT,  'addr': 0x99, 'slot': 5, 'value': 0, 'size':1, 'type': RELAY}

#//Safety loop -0x01
sensor32 = {'name': 'safety', 'mode': DIGITAL, 'direction': INPUT,  'addr': 0x01, 'slot': 0, 'value': 1, 'size':1, 'type': SWITCH}

#//test board -0x100
sensor33 = {'name': 'knot', 'mode': DIGITAL, 'direction': OUTPUT,  'addr': 0x100, 'slot': 0, 'value': 0, 'size':1, 'type': MANUAL}


can_board0 = [
	{
		'addr': 0x020, 
		'sensor_list': [
			sensor00,
			sensor01,
			sensor02,
			sensor03,
			sensor04,
			sensor05,
			sensor06,
			sensor07,
			sensor08
		]
	},
	{
		'addr': 0x021, 
		'sensor_list': [
			sensor09,
			sensor10,
			sensor11,
			sensor12,
			sensor13,
			sensor14,
			sensor15,
			sensor16,
			sensor17
		]
	},
]

can_board1 = [
	{
		'addr': 0x030, 
		'sensor_list': [
			sensor18,
			sensor19,
			sensor20,
			sensor21,
			sensor22
		]
	},
	{
		'addr': 0x031, 
		'sensor_list': [
			sensor23
		]
	},
]

motor = {
	'addr': 0x061,
	'sensor_list': [
		sensor24,
		sensor25
	],
	'power': True
}

glv = {
	'addr': 0x099,
	'sensor_list': [
		sensor26,
		sensor27,
		sensor28,
		sensor29,
		sensor30,
		sensor31
	],
	'power': True
}

safety = {
	'addr': 0x001,
	'sensor_list': [
		sensor32
	],
	'power': True
}

test = {
	'addr': 0x100,
	'sensor_list': [
		sensor33
	],
	'power': True
}

device_list = [
	motor,
	glv,
	safety,
	test
]

def sine_sim(param):
	t = time.time()
	return int(10*(math.sin(t) + param))

def square_sim(param):
	t = int(time.time()) % 10
	if t + param > 5:
		return 1
	else:
		return 0

def linear_sim(param):
	return param + int(time.time()) % 10

def constant_sim(param):
	return param

type_to_func_dict = {
	
	RPM: sine_sim,
	TORQUE: square_sim,
	VOLTAGE: linear_sim,
	CURRENT: constant_sim,
	# RELAY: relay_sim,
	# SWITCH: switch_sim

}