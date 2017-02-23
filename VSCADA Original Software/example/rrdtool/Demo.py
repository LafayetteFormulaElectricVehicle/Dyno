#!/usr/bin/env python
import rrdtool , time , random, math
import subprocess

# RRD database
rrd_db = 'demo.rrd'
step   = 5;
datapoints = 1000;
start_time = int(time.time())
end_time = start_time + (step * datapoints)

data_sources=[  'DS:speed:GAUGE:10:0:100',
                'DS:temperature:GAUGE:10:0:100',
                'DS:chargelevel:GAUGE:5:10:100',
                'RRA:AVERAGE:0.5:2:%s' % str(step*datapoints),
                'RRA:MAX:0.5:2:%s' % str(step*datapoints)]

ret = rrdtool.create(	rrd_db,
						'--step' , str(step),
						'--start', str(start_time),
						data_sources
					)

count =0 
time_stamp = start_time

def xfrange(start, stop, step):
    while start < stop:
        yield start
        start += step



for i in xfrange(0, 1000, 0.523) :

	print(i) 
	updated_speed = 10*math.sin(math.radians(i)) +10

	# updated_speed = random.randrange(0,100)
	updated_temperature  = random.randrange(1,100)
	updated_battery =  random.randrange(1,100)
	time_stamp += 5;
	print(time_stamp, updated_battery, updated_temperature, updated_speed)
	ret1 = rrdtool.update(rrd_db, '%d:%d:%d:%d' % (time_stamp,updated_speed, updated_temperature, updated_battery))
	

	count = count +1
	if ret1:
		print(rrdtool.error())


speed_graph = 'speedgraph.png'
temperature_graph = 'temperature_graph.png'
battery_graph = 'battery_graph.png'

rrdtool.graph( speed_graph,
        '--start' , str(start_time) ,
        '--end' , str(end_time),
        '--vertical-label' , 'Speed m/h' ,
        '--imgformat' , 'PNG' ,
        '--title' , 'Speeds & Temperatures' ,
        '--lower-limit' , '0',
        'DEF:var1=%s:speed:AVERAGE' % rrd_db,
        'DEF:var2=%s:temperature:AVERAGE' % rrd_db,
       	'LINE1:var1#00FF00:My Speeds',
       	'LINE2:var2#0000FF:My Temperatures'
)

p = subprocess.Popen(["display", speed_graph])
# time.sleep(5)


output = rrdtool.fetch(rrd_db, 'AVERAGE'	)

for item in output:
		print(item[1])