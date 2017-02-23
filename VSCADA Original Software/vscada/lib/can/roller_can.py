from queue import PriorityQueue, Empty as EmptyQueueError, Full as FullQueueError
import threading
import time
import logging

TTL_FOREVER = -1
TTL_ONCE = 1
TTL_MAX = 60
DEFAULT_SAMPLERATE = 5

SQLNAME_SAMPLE_RATE = 'sample_rate'
SQLNAME_CAN_ID = 'can_id'

HEADER = ['priority', 'can_frame', SQLNAME_SAMPLE_RATE, 'TTL']
CAN_FRAME_HEADER = [SQLNAME_CAN_ID, 'rtr', 'data']
CAN_TIMESTEP = .01

class PriorityQueueHandler():
	"""
	This class wraps a python PriorityQueue and acts
	like a timed, rolling buffer for sending CAN frame
	via socketCAN. It is intended to accept inputs from
	multiple sources and deliver output to a single
	destination. In another word, the put method of this
	class is thread-safe but the get method is not, because
	the procedures which the get method operates on the
	first item of the list are not atomic and cannot be
	interupted. A thread-safe method is provided, but
	is not recommended since the intension of this class
	is to serve only one output connection (socketCAN).  
	"""


	def __init__(self, size = -1):
		"""
		create a python PriorityQueue. 
		Args:
			size (int): the size of the queue.
			size <= 0 for infinite size. 
		"""
		self.sensorList = PriorityQueue(size)
		self.nextOne = []
		self.urgent = []
		self.logger = logging.getLogger('VSCADA.server.' + __name__)

	def _get_first_item(self):
		"""
		Get the entry from the queue without raising exceptions
		"""
		try:
			return self.sensorList.get_nowait()
		except EmptyQueueError:
			return []
		except Exception:
			self.logger.error('unknown errror:\n' + e)
			return []

	def enqueue(self, table):
		"""
		Populize the PriorityQueue by a given set of data
		Args:
			table (dict): a dictionary. should have the sam
			format as the result from sql_handler.select()
			throw index error if the arg does not have field
			can_id and sample_rate
		"""

		start_time = time.time()

		i = 1

		for sql_dict in table:

			can_id = sql_dict[SQLNAME_CAN_ID]
			sample_rate = sql_dict[SQLNAME_SAMPLE_RATE]

			self.putCanFrame(can_id, forever = True, sample_rate = sample_rate, delay = i*CAN_TIMESTEP)

			i += 1

		# self.nextOne = self._get_first_item()


	def _getNextSensor(self):
		"""
		get the first item, then process it (change priority,
		add time step, etc.). Put the data back into the queue
		if TTL field is greater than 0
		"""

		curr_time = time.time()
		addback = True

		if not self.nextOne:
		
			self.nextOne = self._get_first_item()
			self.logger.debug('Empty entry detected in the queue and will be dumped')
			return []

		if self.nextOne[0] >= curr_time:
			return []

		# copy of the can_frame
		can_frame = list(self.nextOne[1])
		sample_rate = self.nextOne[2]
		
		if (self.nextOne[-1] is not TTL_FOREVER):
			self.nextOne[-1] -= 1
			if (self.nextOne[-1] == 0):
				# TTL is cleared, drop this entry
				addback = False
		
		if addback:
			self.nextOne[0] = curr_time + sample_rate
			self.sensorList.put(self.nextOne)
		
		self.nextOne = self._get_first_item()

		return can_frame

	def get(self):
		"""
		A get method that gets the next can frame to send.
		Not thread-safe
		"""

		if self.urgent:
			return dict(zip(CAN_FRAME_HEADER, self.urgent.pop()))

		can_frame = self._getNextSensor()
		if not can_frame:
			return {}

		return dict(zip(CAN_FRAME_HEADER, can_frame))

	def get_with_lock(self):
		"""
		A thread safe version of the get method. 
		"""

		try:
			self.get_lock.aquire()
			result =  self.get()
		finally:
			self.get_lock.release()
		return result

	def putNowaitCanFrame(self, can_id, data):
		"""
		insert a command into can sender and will be sent out
		ASAP without waiting in the queue
		"""
		self.putCanFrame(can_id, rtr = False, data = data, delay = -1)

	def putCanFrame(self, can_id, rtr = True, data = (), sample_rate = DEFAULT_SAMPLERATE, forever = False, delay = CAN_TIMESTEP, ttl = TTL_ONCE):
		"""
		insert a command into can sender
		Args:
			can_id (int): CAN device identifier field
			rtr (boolean, optional): CAN remote transmit
			data (tuple, optinal): CAN message payload 0-8 Bytes.
			forever (boolean, optional): if the CAN frame last forever
			delay (float, optional): the delay between the sending of this
			can_frame and the sending of the scheduled next one.
			this value is only an approximation. 
			ttl (int, optional):  the time to live attribute

			By default a remote can_frame will be sent only once ASAP
		"""

		if self.nextOne:
			new_data_prioity = self.nextOne[0] + delay
		else:
			new_data_prioity = time.time() + delay

		if forever:
			new_data_ttl = TTL_FOREVER
		elif ttl > TTL_MAX:
			new_data_ttl = TTL_MAX
		elif ttl < TTL_ONCE:
			new_data_ttl = TTL_ONCE
		else:
			new_data_ttl = ttl

		new_can_frame = [can_id, rtr, data]

		if delay < 0:
			self.urgent.append(new_can_frame)
			return True

		try:
			self.put([new_can_frame, sample_rate], new_data_prioity, new_data_ttl)
			return True
		except FullQueueError:
			return False


	def put(self, data, priority, ttl):

		data.insert(0, priority)
		data.append(ttl)

		# TODO: test for thread safe
		self.sensorList.put(data)