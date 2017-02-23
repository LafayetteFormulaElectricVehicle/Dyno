#!/bin/env/python3

import re
import daqflex
import datetime

#INPUT
#CH0 - Tach
#CH1 - Strain guage
#
#OUTPUT
#D/A OUT 1 - Power (throttle)
#D/A OUT 0 - Solenoid
class HuffBox():
	dev = None
	
	def __init__(self):
		self.dev = DataDevice()
		
	def set_throttle(self, value):
		if value > 4095:
			value = 4095
		elif value < 0:
			value = 0
		self.dev.analog_out.set_value(1, value)
		
	def set_load_valve(self, value):
		if value > 4095:
			value = 4095
		elif value < 0:
			value = 0
		self.dev.analog_out.set_value(0, value)
		
		
	def get_strain_guage(self):
		return self.dev.analog_in.get_value(1)
		
	def get_tachometer(self):
		return self.dev.analog_in.get_value(0)
		

def _send_cmd(dev, cmd, regex):
	try:
		resp = dev.send_message(cmd)
		m = re.findall(regex, resp)
		if m:
			return m
	except:
		print('ERR: Message "' + cmd + '" not recognized!')
	return None

class _DeviceCmd():
	dev = None
	
	def __init__(self, _dev):
		self.dev = _dev
	#?DEV:FWV
	#	DEV:FWV=02.04
	def get_firmware_version(self):
		cmd = '?DEV:FWV'
		regex = '''DEV:FWV=([-+]?[0-9]*\.?[0-9]+)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return float(*resp)
		
	#?DEV:MFGCAL
	#	DEV:MFGCAL=2014-11-15 15:59:21
	def get_cal_date(self):
		cmd = '?DEV:MFGCAL'
		regex = '''DEV:MFGCAL=(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)'''
		resp = _send_cmd(self.dev, cmd, regex)
		year = int(resp[0][0])
		month = int(resp[0][1])
		day =  int(resp[0][2])
		hour = int(resp[0][3])
		minute = int(resp[0][4])
		second = int(resp[0][5])
		date = datetime.datetime(year, month, day, hour, minute, second)
		return date
		
	#?DEV:MFGSER
	#	DEV:MFGSER=019E0F78
	def get_serial(self): 
		cmd = '?DEV:MFGSER'
		regex = '''DEV:MFGSER=([0-9A-E]+)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return resp[0]
		
class _AnalogInCmd:
	dev = None
	def __init__(self, _dev):
		self.dev = _dev
		
	#?AI
	#	AI=4
	def get_channel_count(self):
		cmd = '?AI'
		regex= '''AI=(\d+)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return int(resp[0])
		
	#?AI:CHMODE
	#   AI:CHMODE=DIFF
	def get_channel_mode(self):
		cmd = '?AI:CHMODE'
		regex = '''AI:CHMODE=(SE|DIFF)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return resp[0]

	#?AI{*}:OFFSET
	#	AI{0}:OFFSET=2.094889
	def get_offset(self, chan):
		cmd = '?AI{' + str(chan) + '}:OFFSET'
		regex = '''AI{\d+}:OFFSET=([-+]?[0-9]*\.?[0-9]+)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return float(resp[0])
		
	#?AI{*}:RANGE
	#	AI{0}:RANGE=BIP10V
	def get_range(self, chan):
		cmd = '?AI{' + str(chan) + '}:OFFSET'
		regex = '''AI{\d+}:OFFSET=([-+]?[0-9]*\.?[0-9]+)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return resp[0]
		
	#?AI{*}:SLOPE
	#	AI{0}:SLOPE=9.998740e-1
	def get_slope(self, chan):
		cmd = '?AI{' + str(chan) + '}:SLOPE'
		#TODO TEST regex...
		regex = '''AI{\d+}:SLOPE=([-+]?[0-9]*\.?[0-9]+e?[-+?][0-9])'''
		resp = _send_cmd(self.dev, cmd, regex)
		return float(resp[0])
		
		
	#?AI{*}:VALUE
	#	AI{0}:VALUE=2047.837093
	def get_value(self, chan):
		cmd = '?AI{' + str(chan) + '}:VALUE'
		regex = '''AI{\d+}:VALUE=([-+]?[0-9]*\.?[0-9]+)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return int(resp[0])

	#AI:CHMODE=*
	#	AI:CHMODE
	def set_channelMode(self, mode):
		cmd = 'AI:CHMODE=' + mode
		regex = '''AI:CHMODE'''
		resp = _send_cmd(self.dev, cmd, regex)
		return resp != None
		
class _AnalogOutCmd:
	dev = None
	def __init__(self, _dev):
		self.dev = _dev
	#?AO
	#	AO=2
	def getChannelCount(self):
		cmd ='?AO'
		regex = '''AO=(\d+)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return int(resp[0])
	
	#?AO{*}:RANGE
	#	AO{0}:RANGE=UNI4.096V
	def get_range(self, chan):
		cmd = '?AO{' + str(chan) + '}:RANGE'
		regex = '''AO{\d+}:RANGE=(.*?)'''
		resp = _send_cmd(self.dev, cmd, regex)
		return resp != None
	
	#TODO CHECK
	#AO{*]:VALUE=*
	#	AO{0}:VALUE
	def set_value(self, chan, value):
		cmd = 'AO{' + str(chan) + '}:VALUE=' + str(value)
		regex = '''AO{\d+}:VALUE'''
		resp = _send_cmd(self.dev, cmd, regex)
		return resp != None

class DataDevice:
	dev = None
	
	device = None
	analog_in = None
	analog_out = None
	
	def __init__(self):
		self.dev = daqflex.USB_7204();
		
		self.device = _DeviceCmd(self.dev)
		self.analog_in = _AnalogInCmd(self.dev)
		self.analog_out = _AnalogOutCmd(self.dev)

if __name__ == "__main__":
	#device
	dev = DataAcquisitionDevice()
	print(dev.device.get_firmware_version())
	print(dev.device.get_cal_date())
	print(dev.device.get_serial())
	
	#analog in
	print(dev.analog_in.get_channel_count())
	print(dev.analog_in.get_channel_mode())
	print(dev.analog_in.get_offset(0))
	print(dev.analog_in.get_range(1))
	print(dev.analog_in.get_slope(0))
	print(dev.analog_in.get_value(1))
	print(dev.analog_in.set_channelMode('DIFF'))
	
	#analog out
	print(dev.analog_out.getChannelCount())
	print(dev.analog_out.get_range(0))
	print(dev.analog_out.set_value(0, 1000))

