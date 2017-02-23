import sys
import rrdtool, time
from PIL import Image
import subprocess
 
rrd_db = 'demo.rrd'
start_point = int(time.time()) - 500;
end_point  = int(time.time())

rrdtool.graph( rrd_db,
        '--start' , str(start_point) ,
        '--end' , str(end_point),
        '--vertical-label' , 'Speed m/h' ,
        '--imgformat' , 'PNG' ,
        '--title' , 'Speeds' ,
        '--lower-limit' , '0' 
        'DEF:var1=rrd_db:speed:AVERAGE',
       	'LINE1:var1#00FF00:My Speed'
)


p = subprocess.Popen(["display", gfname])
time.sleep(5)