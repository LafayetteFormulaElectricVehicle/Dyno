import logging

logger = logging.getLogger('VSCADA.'+__name__)

my_server = None

def setup(server):
	my_server = server

def action(sensor_id, action_name, sensor_name, param1, param2, param3):
	name_to_func[action_name](sensor_id, sensor_name, param1, param2, param3)

def default(sensor_id, sensor_name, param1, param2, param3):
	pass

def warn_msg(sensor_id, sensor_name, param1, param2, param3):

	sql_level_dict = {
	1:logger.debug,
	2:logger.info,
	3:logger.error,
	4:logger.critical
	}

	sql_level_dict[param1]('%d %s has triggered an error' % (int(sensor_id), str(sensor_name)))

def set_sensor(sensor_id, sensor_name, param1, param2, param3):
	my_server.insert_can_request_main(param1, param2, urgent = True)

name_to_func = {
	'default':default,
	'warn_msg':warn_msg,
	'set_sensor':set_sensor
}