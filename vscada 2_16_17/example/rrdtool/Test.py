
import sys
import rrdtool , tempfile

print("rrd tool is sucessfully imported")

#ys.path.append('/path/to/rrdtool/li#b/python2.6/site-packages/')


data_sources=[  'DS:speed:GAUGE:5:0:100',
                'DS:temperature:GAUGE:5:0:100',
                'DS:chargelevel:GAUGE:5:0:100' ]


rrdtool.create(	'Test.rrd',
				'--start',
				'920804400',
				data_sources,
				'RRA:AVERAGE:0.5:1:24',
				'RRA:AVERAGE:0.5:6:10'
			)



fd, path = tempfile.mkstemp('.png');

rrdtool.graph(path,
              '--imgformat', 'PNG',
              '--width', '540',
              '--height', '100',
              '--start', "-%i" % YEAR,
              '--end', "-1",
              '--vertical-label', 'Downloads/Day',
              '--title', 'Annual downloads',
              '--lower-limit', '0',
              'DEF:downloads=Test.rrd:downloads:AVERAGE',
              'AREA:downloads#990033:Downloads')

info = rrdtool.info('Test.rrd')
print info['last_update']
print info['ds[Test].minimal_heartbeat']