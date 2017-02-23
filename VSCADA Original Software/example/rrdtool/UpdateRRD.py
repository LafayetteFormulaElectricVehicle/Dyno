import sys
import time 
import random
import rrdtool 

total_input_traffic = 0;
total_output_traffic = 0;
step = 300 

while 1:
	updated_speed = random.randrange(1,100)
	updated_temperature  = random.randrange(1,100)
	updated_battery =  random.randrange(1,100)
	ret = rrdtool.update('sample.rrd', 'N:'+ str(updated_speed) + ':' + str(updated_temperature) + ':'+ str(updated_battery))

	if ret:
		print rrdtool.error()
		time.sleep(5)
