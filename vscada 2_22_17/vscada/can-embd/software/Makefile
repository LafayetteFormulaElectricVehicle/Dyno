AVR=atmega16m1
CC=avr-gcc
CFLAGS=-Os -g -Wall -std=c99 -mmcu=$(AVR)

AVRDUDE=avrdude
AVR_AVRD=m16

ELF=bin/blink.elf
HEX=bin/blink.hex


all: program

build:
	$(CC) $(CFLAGS) -c src/main.c -o obj/main.o
	$(CC) $(CFLAGS) -c src/adc.c -o obj/adc.o
	$(CC) $(CFLAGS) -c src/timer.c -o obj/timer.o
	$(CC) $(CFLAGS) -c src/canlib/can_lib.c -o obj/can_lib.o
	$(CC) $(CFLAGS) -c src/canlib/can_drv.c -o obj/can_drv.o
	$(CC) $(CFLAGS) obj/main.o obj/adc.o obj/timer.o obj/can_lib.o obj/can_drv.o -o $(ELF)
	
hex: build
	avr-objcopy -j .text -j .data -O ihex $(ELF) $(HEX)
	
program: hex
	$(AVRDUDE) -F -V -c usbtiny -p $(AVR_AVRD) -U flash:w:$(HEX)


#PHONY
fuse:
	$(AVRDUDE) -c usbtiny -p $(AVR_AVRD) -F -U lfuse:w:0xef:m

clean:
	rm -rf bin/*.hex bin/*.elf obj/*.o

.PHONY: fuse clean
