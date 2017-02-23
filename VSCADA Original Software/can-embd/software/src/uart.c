#include "lin_uart.h"

#include <stdbool.h>

volatile struct ringBuffer serialBuffer = {{0}, 0, 0};

//NOTE:
//Useful Code Reference http://www.avrfreaks.net/forum/usart-interrupt-atmega32m1

//Receive interrupt routine
ISR(LIN_TC_vect) {
	if(true) {
		//FIXME check for RX_OK int
		//Increment head pointer
		serialBuffer.head = (serialBuffer.head + 1) % RX_BUFFER_SIZE;
		
		//Increment tail pointer if necessary
		if(serialBuffer.head == serialBuffer.tail) {
			//Increment tail and prevent overload of buffer
			serialBuffer.tail = (serialBuffer.tail + 1) % RX_BUFFER_SIZE;
		}

		//Update buffer with latest bite
		serialBuffer.buffer[serialBuffer.head] = LINDAT;
	}
}

void uart_init(void){
	//Reset LIN/UART hardware
	LINCR = (1 << LSWRES);
	
	//Calculate, and set UART baud rate
	LINBRRH = (((F_CPU / BAUD) / 16) - 1) >> 8;
	LINBRRL = (((F_CPU / BAUD) / 16) - 1);
	
	//Bit sampling rate/resync
	LINBTR = (1 << LDISR) | (16 << LBT0);

	//RX interrupt
	LINENIR = (1 << LENRXOK);

	//Enable UART RX & TX
	LINCR = (1 << LENA) | (1 << LCMD2) | (1 << LCMD1) | (1 << LCMD0);

	sei();
}
			
void uart_tx(uint8_t dataByte) {
	//Wait until UART is ready
	while (LINSIR & (1 << LBUSY));

	LINDAT = dataByte;
}

uint8_t uart_rx(void) {
	//Read circular buffer
	uint8_t size;

	//I don't want to type this...
	uint8_t* head = &(serialBuffer.head);
	uint8_t* tail = &(serialBuffer.tail);
	
	//Calculate buffer size
	size = (*head > *tail) ?
			*head - *tail : *tail - *head;
	for(int i=0;i<size;i++) {
		int index = (*head + i) % RX_BUFFER_SIZE;
		serialBuffer[index]
	}

}
