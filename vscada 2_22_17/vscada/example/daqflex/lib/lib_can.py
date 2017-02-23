import socket
import struct
import sys
import time
import select

"""
	Frame Description Object:
	[
		{
			'name': 'Field Name 1',
			'bit-offset': 0
			'bit-length': 0
			'single-bit': False
		}
	]
"""
		
class CANDataHandler():
	can_handler = None
	def __init__(self):
		self.can_handler = SocketCANHandler('vcan0')
		
	def recv_data_frame(self, can_id, frame_descr):
		self.can_handler.send_rtr(can_id)
		
		#TODO Block until response received
		#FIXME bit vs byte offset in frame descr object
		packet = self.can_handler.recv_frame_blk()
		while packet['id'] != can_id:
			packet = self.can_handler.recv_frame_blk()
		
		recv_data = []
		#try:
		for slot in frame_descr:
			field_value = 0;
			for i in range(0, slot['bit-length']):
				data_index = slot['bit-offset'] + i
				shift = slot['bit-length'] - 1 - i;
				field_value += packet['data'][data_index] << (8*shift)
			recv_data.append({'name': slot['name'], 'value': field_value})
		#except:
		#print('ERROR: CAN format descriptor wrong!')
		return recv_data
		
	#TODO implement me!
	def send_data_frame(self, can_id, frame_descr):
		print('send_data_frame() Not yet implemented...')
		

class SocketCANHandler():
	"""SocketCAN Listener Class
	
	Opens a SocketCAN port for read/write.
	"""
	#CAN frame format descriptor by byte
	can_fmt = ''
	
	#linux socketCAN device
	can_dev = None
	
	def __init__(self, can_device):
		"""Open a bi-directional SocketCAN device
		
		Opens a SocketCAN port for read/write.
		
		Args:
			can_device (str): Linux SocketCAN Device Ex. 'vcan0'
		"""
		self.can_fmt = '=HHB3x8B'
		#Create a Raw Socket
		self.can_dev = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
		self.can_dev.setblocking(0)
		#bind the socket to the CAN interface
		self.can_dev.bind((can_device,))
		
	def build_frame(self, can_id, can_rtr, can_data=()):
		"""Build a CAN frame dict
		Create a CAN frame dictionary object. This creates a dictionary of the
		following format for use with send_frame(), recv_frame(), and other
		similar methodcan_dev.
		
		{"id", 0-2047, "rtr": True/False, "data": [0, 1 ...]}
		
		Args
			can_id (int): CAN device identifier field
			can_rtr (int): CAN remote transmit field
				can_rtr is True, otherwise this field is ignored.
			can_data (tuple, optinal): CAN message payload 0-8 Bytecan_dev.
			
		Returns:
			A dictionary object used to describe a CAN frame.
		"""
		return {"id": can_id, "rtr": can_rtr, "data": can_data}
	
	def send_frame(self, frame):
		"""Send a CAN frame
		Send a SocketCAN frame. The following dictionary format is used to
		describe a frame. 
		
		{"id", 0-2047, "rtr": True/False, "data": [0, 1 ...]}
		Args:
			frame (dict): A dict describing the received CAN frame to be sent.
		"""
		RTR_FLAG = 0x4000
		#raw can frame binary string
		#  (int)[id] 
		fmt = 'B'*len(frame['data'])
		rtr = RTR_FLAG if frame['rtr'] else 0
		data = struct.pack(fmt, *frame['data'])
		data = data.ljust(8, b'\x00')
		
		raw_frame = struct.pack(self.can_fmt, frame['id'], rtr, len(data), *data)
		# print(raw_frame)
		self.can_dev.send(raw_frame)
	
	def send_rtr(self, can_id):
		"""Sends a SocketCAN remote transmit request (RTR)
		
		Sends an RTR frame to a remote CAN node, requesting data.
		
		Args:
			can_id (int): Device CAN ID
		"""

		frame = self.build_frame(can_id, True)
		self.send_frame(frame)
	
	def send_payload(self, can_id, payload):
		"""Sends a SocketCAN data frame
		
		Sends an data payload frame to a remote CAN node.
		
		Args:
			can_id (int): Deice CAN ID
			payload (tuple): Data payload, 0-8 Bytes
		"""
		frame = self.build_frame(can_id, False, payload)
		self.send_frame(frame)

	def recv_frame(self):
		"""Receive a socketCAN frame
		
		This is a non-blocking method to return a 'frame' dictionary. If a frame is
		available, it will return a dict of format {"id", "rtr", "data"}. If no
		frame is available, it will return 'None'.
		
		Returns:
			A dict describing the received CAN frame. The following format is used:
			{"id", 0-2047, "rtr": True/False, "data": [0, 1 ...]}
		"""
	
		try:
			cf, addr = self.can_dev.recvfrom(16)
		except:
			return None
		can_resp = struct.unpack(self.can_fmt, cf)
		can_id = can_resp[0]
		can_rtr = can_resp[1] != 0
		can_dlc = can_resp[2]
		can_data = can_resp[3:]
		frame = {'id': can_id, 'rtr': can_rtr, 'data': can_data[:can_dlc]} 
		return frame
	
	def recv_frame_blk(self):
		"""Receive a socketCAN frame (blocking)
		
		This is a blocking version of the recv_frame() method, which blocks in the
		event that no CAN frame is currently available.
		
		Returns:
			A dict describing the received CAN frame. The following format is used:
			{"id", 0-2047, "rtr": True/False, "dlc": 0-8, "data": [0, 1 ...]}
		"""
		self.can_dev.setblocking(1)
		frame = self.recv_frame()
		self.can_dev.setblocking(0)
		return frame;

if __name__=='__main__':
	frame_descr_1 = [
		{
			'name': 'Motor RPM', 
			'bit-offset': 0,
			'bit-length': 2, 
			'single-bit': False
		}, 
		{
			'name': 'Motor Temp', 
			'bit-offset': 2,
			'bit-length': 1, 
			'single-bit': False
		},
		{
			'name': 'Controller Temp',
			'bit-offset': 3,
			'bit-length': 1,
			'single-bit': False
		},
		{
			'name': 'RMS Current',
			'bit-offset': 4,
			'bit-length': 2,
			'single-bit': False
		},
		{
			'name': 'Capacitor Voltage',
			'bit-offset': 6,
			'bit-length': 2,
			'single-bit': False
		}
	]
	frame_descr_2 = [
		{
			'name': 'Stator Frequency', 
			'bit-offset': 0,
			'bit-length': 2, 
			'single-bit': False
		}, 
		{
			'name': 'Controller Fault Primary', 
			'bit-offset': 2,
			'bit-length': 1, 
			'single-bit': False
		},
		{
			'name': 'Controller Fault Secondary', 
			'bit-offset': 3,
			'bit-length': 1,
			'single-bit': False
		},
		{
			'name': 'Throttle Input',
			'bit-offset': 4,
			'bit-length': 1,
			'single-bit': False
		},
		{
			'name': 'Brake Input',
			'bit-offset': 5,
			'bit-length': 1,
			'single-bit': False
		}
	]
	can = CANDataHandler()
	recv = can.recv_data_frame(10, frame_descr_1)
	print(recv)
	for slot in recv:
		print(slot['name'], '\n\t', slot['value'])
	
	recv = can.recv_data_frame(10, frame_descr_2)
	for slot in recv:
			print(slot['name'], '\n\t', slot['value'])
