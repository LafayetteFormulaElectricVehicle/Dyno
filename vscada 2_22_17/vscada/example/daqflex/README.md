#Dynamometer Control Application#

##Library Requirements##
1. Python3
2. pyusb
3. pydaqflex

*Note: this application should be cross platform, however functionality on Windows or Mac OS has not been tested*

sudo pip3 install pyusb
sudo pip3 install pydaqflex

##Running the User Interface##
./main-dyno.py
or
python3 main-dyno.py

##udev rules##
Create the following udev rule at '/etc/udev/rules.d/50-measurement-computer-daq.rules'
```
SUBSYSTEM=="usb", ATTR{idProduct}=="00f0", ATTRS{idVendor}=="09db", GROUP="plugdev", MODE="0666"
```

To do this, execute the following commands:
1. As root, edit the file /etc/udev/rules.d/50-measurement-computer-daq.rules 
2. Paste the following into 50-measurement-computer-daq.rules:
```
SUBSYSTEM=="usb", ATTR{idProduct}=="00f0", ATTRS{idVendor}=="09db", GROUP="plugdev", MODE="0666"
```

##update user interface##
1. open qt designer
2. save \*.ui file
3. run the following command for each \*.ui file
```
pyuic4 {filename}.ui -o ui_{filename}.py
```
