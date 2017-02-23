# Setting up CAN protocol #

1.__Installing Python3__

 Download and install Python 3.4.2 (Must be at Least Python 3 for CAN support)

Get and extract .tgz (https://www.python.org/downloads/release/python-342/)

	**Run:**   
	```
		./configure
		make
		make test
		sudo make install
	```

2.__Steps to get CAN working with python:__

	Install can-utils (http://elinux.org/Can-utils) (need libtool)

	For more information read: [SocketCAN Wikipedia](http://en.wikipedia.org/wiki/SocketCAN)

3.__CAN Link Setup__

	Setting up the Can link: (Script Located in vcanSetup.sh, need sudo)
		```
		$ modprobe can
		$ modprobe vcan
		$ sudo ip link add dev vcan0 type vcan
		$ sudo ip link set up vcan0
		$ ip link show vcan0
		```

4.__Testing Environment as of April 1__

	Run (in two seperate terminals):

	```python3 showMsg.py ``` 
	```python3 mainCAN.py ``` 


