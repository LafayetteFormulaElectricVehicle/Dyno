import serial
import re
import time

class PowerSupplyControl():
	#rs-232 serial device
	ser = None
	
	#serial port name
	port = ''
	
	def __init__(self, _port, _baud):
		'''
		'''
		self.ser = serial.Serial('/dev/ttyS0', 19200, timeout=0.5)
	
	def _send_cmd(self, cmd, read=True):
		'''
		Private Method: Send SCPI command
		
		cmd: string containing SCPI command
		
		returns: response message
		'''
		self.ser.flushInput()
		self.ser.flushOutput()
		self.ser.write(cmd.encode('ascii') + b'\r\n')
		time.sleep(.05)
		if(read):
			resp = self.ser.read()
			while self.ser.inWaiting():
				resp+= self.ser.read()
			return resp
		else:
			return None

	def get_voltage(self):
		'''
		Get PSU Voltage
		
		returns: floating point voltage value
		'''
		cmd = "MEAS:VOLT?"
		resp = self._send_cmd(cmd)
		return float(resp)

	def get_current(self):
		'''
		Get PSU Current
		
		returns: floating point current value
		'''
		cmd = "MEAS:CURR?"
		resp = self._send_cmd(cmd)
		return float(resp)

	def get_state(self):
		'''
		'''
		cmd = 'OUTP?'
		resp = self._send_cmd(cmd)
		if resp == '1':
			return True
		elif resp == '0':
			return False
		return None
	
	def set_voltage(self, voltage):
		'''
		Set PSU Voltage
		
		voltage: voltage to be set
		
		returns: SCPI response (float)
		'''
		cmd = "VOLT " + str(voltage)
		resp = self._send_cmd(cmd, read=False)

	def set_current(self, current):
		'''
		Set PSU Voltage
		
		current: current to be set
		
		returns: SCPI response (float)
		'''
		cmd = "CURR " + str(current)
		resp = self._send_cmd(cmd, read=False)
	
	#on -> True; off -> False
	def set_state(self, state):
		'''
		Turn PSU on/off
		
		state: True -> On; False -> Off
		'''
		if state:
			cmd = "OUTP:START"
			resp = self._send_cmd(cmd, read=False)
		else:
			cmd = "OUTP:STOP"
			resp = self._send_cmd(cmd, read=False)
	def turn_on(self):
		self.set_state(True)
		
	def turn_off(self):
		self.set_state(False)
		
