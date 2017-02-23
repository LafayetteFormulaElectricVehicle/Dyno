#!/usr/bin/env python3
#Add main direcotry to search path
import sys
sys.path.append('../..')

import sys
import threading
import time
import os

#from lib.can import CANlib
from lib.sql_handler import sql_handler
from lib.can import lib_can

#sensor configuration file 
from sensor_list import *

SENSOR_UPDATE_FREQ = 1

class DataGenerator(threading.Thread): 
	device_list = []
	
	def setup(self, device_list):
		self.device_list = device_list
		
	def run(self):
		while True:
			time.sleep(SENSOR_UPDATE_FREQ / 1000)

			if not sensor32['value']:
				print('safety loop has been pulled')
				os._exit(0)

			for device in self.device_list:

				if not device['power']:
					continue

				input_sensor = [x for x in device['sensor_list'] if x['type'] == AUTO]
				if input_sensor:
					input_param = input_sensor[0]['value']
				else:
					input_param = 0

				for sensor in device['sensor_list']:
					if sensor['direction'] == OUTPUT:
						if sensor['type'] in type_to_func_dict:
							sensor['value'] = type_to_func_dict[sensor['type']](input_param)
					elif sensor['type'] == RELAY:
						if not sensor['value']:
							device['power'] = False
							print(device['addr'], 'is shut off')

						# print('update sensor', sensor['name'], 'to', sensor['value'])
	
class ManualSwitch(threading.Thread): 
	device_list = []
	
	def setup(self, device_list):
		self.device_list = device_list
		
	def run(self):
		while True:

			value = int(input('\ntype in the value you desired\n'))

			try:
				sensor33['value'] = value

			except Exception:
				pass

def formatCanFromDevice(device, canListener):
	# data = [0 for i in range(8)]
	data = []
	for sensor in device['sensor_list']:
		raw_value = sensor['value']
		raw_slot = sensor['slot']
		size = sensor['size']
		try:
			value = raw_value.to_bytes(size, byteorder = 'big', signed = True)
		except Exception as e:
			print(e)
			value = [0]
		slot = raw_slot
		for byte in value:
			data.append(byte)
			slot += 1
		# print('id', device['addr'], 'data:', data, 'raw_value:', raw_value)
	canListener.send_payload(device['addr'], data)

def setDeviceFromCan(can_device, can_data):

	for sensor in can_device['sensor_list']:
		if sensor['direction'] == OUTPUT:
			continue
		sensor['value'] = int.from_bytes(
			can_data[sensor['slot']:sensor['slot']+sensor['size']],
			byteorder = 'big', signed = True)
	
def simulate():
	fake_data = DataGenerator()
	fake_data.setup(device_list)
	fake_data.setDaemon(True)
	fake_data.start()

	knot = ManualSwitch()
	knot.setDaemon(True)
	knot.start()

	canListener = lib_can.SocketCanHandler('vcan0')

	while True:
		can_recv = canListener.recv_frame_blk()
		can_id = can_recv['id']
		can_rtr = can_recv['rtr']
		can_data = can_recv['data']

		
		try:
			can_device, = [device for device in device_list if device['addr'] == can_id]
		except Exception:
			print('can id', can_id, 'is either missing or non-unique')
			continue

		if can_rtr:
			formatCanFromDevice(can_device, canListener)
		else:
			setDeviceFromCan(can_device, can_data)
		
if __name__ == '__main__':
	#can_sim = CANSimulation(device_list)
	#can_sim.simulate()
	simulate()

