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
			'offset': 0,
			'length': 0,
			'single-bit': False,
			'bit': 0,
		}
	]
"""
		
class CANDataHandler():
	"""
	CAN Data Handler Class

	This class is responsible for parsing CAN frames based on predefined bit-field 
	descriptor objects. It converts a list of sensor values to a CAN frame, and vice
	versa.
	"""
	
	#CAN Handler to be used by this class
	can_handler = None
	
	#rtr list, used to prevent multiple send
	req_list = []
	
	recv_buffer_frame = []
	recv_buffer_id = []
	
	def __init__(self, dev):
		"""
		Instantiate the SocketCAN listener device
		"""
		self.can_handler = SocketCANHandler(dev)
	
	#TODO more detail in comment
	def request_data(self, can_id):
		"""
		Send a remote transmit request, if one has already been sent
		no request is sent...
		"""
		req_list.append(can_id)
		self.can_handler.send_rtr(can_id)
	
	def recv_data_frame(self, can_id, frame_descr):
		"""
		Parse a CAN data frame.
		A frame descriptor object is passed in in the following format:
			[{
				'name': 'Field Name 1',
				'offset': 0,
				'length': 0,
				'single-bit': False,
				'bit': 0,
			},
			...
			]
		The object above is a list of dictionaries. The returned data will
		consist of a list of dicts with 'name' and 'value' fields. 
		[{'name': 'Field Name 1', 'value': 1000}]
		"""
		#rtr_exist = self.req_list.count(can_id) != 0
		rtr_exist = True
		frm_recvd = self.recv_buffer_id.count(can_id) != 0
		if rtr_exist and frm_recvd:
			#remove the request from the list
			#self.req_list.remove(can_id)
			
			index = self.recv_buffer_id.index(can_id)
			packet = self.recv_buffer_frame[index]
			
			#clean items
			self.recv_buffer_id.pop(index)
			self.recv_buffer_frame.pop(index)
			
			recv_data = []
			for slot in frame_descr:
				field_value = 0;
				for i in range(0, slot['length']):
					data_index = slot['offset'] + i
					shift = slot['length'] - 1 - i;
					field_value += packet['data'][data_index] << (8*shift)
				recv_data.append({'id': slot['id'], 'name': slot['name'], 'value': field_value})
			return recv_data
		else:
			print('ERROR: RTR not sent, or frame not received!')
	
	def recv_frame(self):
		#this func should receive all available can frames in os buffer
		packet = self.can_handler.recv_frame()
		if packet is not None:
			self.recv_buffer_id.append(packet['id'])
			self.recv_buffer_frame.append(packet)
			return True
		return False
	
	def frame_available(self, can_id):
		return self.recv_buffer_id.count(can_id) != 0
		
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
