# LFEV 2015 CAN Communications Microprocessor #
This software is written for a CAN 2.0 communications board. The is a microcontroller was designed to interface all low level analog and digital sensors present on the 2015 LFEV with the main Data Acquisition Computer (SCADA). The software is capable of handling both reading and writing data.  

## Target Device ##
This software is written for the **Atmel ATMEGA 16M1 Automotive AVR**  
  
This device was selected for its price, software availability, documentation and onboard CAN bus support.

### Features ###

* Atmel® AVR® 8-bit microcontroller
* Up to 1 MIPS throughput per MHz
* 16KBytes flash of in-system programmable program memory
* 512B of in-system programmable EEPROM
* 1KBytes internal SRAM
* On-chip debug interface (debugWIRE)
* CAN 2.0A/B with six message objects - ISO 16845 certified
* Variable PWM duty cycle and frequency
* Synchronous update of all PWM registers
* Peripheral features
* One 8-bit general purpose timer/counter
* One 16-bit general purpose timer/counter
* One master/slave SPI serial interface
* 10-bit ADC
	* 11 single ended channels
	* Three differential ADC channel pairs (5×, 10×, 20×, 40×)
* 10-bit DAC for variable voltage reference (comparators, ADC)
* Programmable watchdog timer with separate on-chip oscillator
* On-chip temperature sensor

### Operating Specifications ###
- Operating voltage: 2.7V - 5.5V
- Extended operating temperature:
- -40°C to +85°C
- Core speed grade:
- 0 - 8MHz @ 2.7 - 4.5V
- 0 - 16MHz @ 4.5 - 5.5V

### Toolchain Information ###
**Compiler:** GCC-4.9.2 (AVR)  
**C Library:** AVR LibC  
**Downloader:** AVRDude 5.11.1  
**Programmer:** USBtinyISP  

### Toolchain Manuals ###
[GCC User Manual](https://gcc.gnu.org/onlinedocs/gcc-4.9.2/gcc/)  
[AVR LibC User Manual](http://www.nongnu.org/avr-libc/user-manual/index.html)  
[AVRDude User Manual](http://www.nongnu.org/avrdude/user-manual/avrdude.html)  
[USBtinyISP Information](https://learn.adafruit.com/usbtinyisp)  
[ATMega16M1 User Manual](http://www.atmel.com/images/doc8209.pdf)
  
### Compiler Information ###
Here is output information from the C compiler used to write all code. A standard GCC compiler with AVR target has been used. This compiler was built from source, however the latest version of this prebuilt toolchain of can be extracted from the Arduino IDE for Mac/Window/Linux. [Download](http://arduino.cc/en/Main/Software)

To build a GCC AVR cross compiler, insturctions can be found at: [Tutorial](http://www.nongnu.org/avr-libc/user-manual/install_tools.html)

**Compiler Details**
```
user@scada:~/$ avr-gcc -v

Using built-in specs.
COLLECT_GCC=avr-gcc
COLLECT_LTO_WRAPPER=/usr/local/bin/../libexec/gcc/avr/4.9.2/lto-wrapper
Target: avr
Configured with: ../gcc-4.9.2/configure --prefix=/home/scada/avr-gcc/ --target=avr --enable-languages=c,c++ --disable-nls --disable-libssp --with-dwarf2
Thread model: single
gcc version 4.9.2 (GCC)

```

## Building The Software ##

**To compile only:**  
```
make build
```

**To compile and program:**  
```
make
```

## Programming The Microcontroller##
```
make program
```

## Configuring the Onboard Crystal Oscillator##
```
make fuse
```
