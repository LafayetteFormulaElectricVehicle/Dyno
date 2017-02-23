#!/usr/bin/python
import rrdtool 


data_sources=[  'DS:speed:GAUGE:5:0:100',
                'DS:temperature:GAUGE:5:0:100',
                'DS:chargelevel:GAUGE:5:0:100' ]

ret = rrdtool.create(	"sample.rrd", 
						"--step", "1800",
						"--start", '0',
						data_sources,
						'RRA:AVERAGE:0.5:1:24',
						'RRA:AVERAGE:0.5:6:10'
)

if ret:
	print rrdtool.error()


