# Setting up CAN protocol #

##Library Requirements##
1. can-utils
2. python3

*NOTE: Python3 is required for CAN support, Python2 will not work.*

##Python 3 Installation##

1. Download and install Python 3.4.2 (Must be at Least Python 3 for CAN support)

2. Get and extract .tgz (https://www.python.org/downloads/release/python-342/)

**In a terminal window run:**
	```
		./configure
		make
		make test
		sudo make install
	```
	

##Setting Up Virtual CAN##

1. Install can-utils (http://elinux.org/Can-utils) (need libtool)

**In a terminal window run:**
	```
		apt-get install can-utils
	```

For more information read the [SocketCAN Wikipedia Page](http://en.wikipedia.org/wiki/SocketCAN).

2. Virtual CAN Link Setup (vcan)

Setting up the Can link, run the following commands as the root user:
	```
	$ modprobe can
	$ modprobe vcan
	$ ip link add dev vcan0 type vcan
	$ ip link set up vcan0
	$ ip link show vcan0
	```
	
*Note: A script 'vcan-setup.sh', will run these commands for you using sudo.*
	```
		$ sh vcan-setup.sh
	```

##Running the Test Environment##
To run the test environment, execute the python script 'can-sim.py'.

	```
		$ python3 can-sim.py
	``` 
*Note: This script can also be executed via command line with './can-sim.py'.


