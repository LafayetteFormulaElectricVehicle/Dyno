#ifndef LIN_UART_H 
#define LIN_UART_H

#define F_CPU 16000000
#define BAUD 115200

#define RX_BUFFER_SIZE 128

//Circular serial buffer
struct ringBuffer {
	uint8_t buffer[RX_BUFFER_SIZE];
	uint8_t head;
	uint8_t tail;
};


void uart_init(void);
void uart_tx(uint8_t);
uint8_t uart_rx(void);
#endif /*LIN_UART_H*/
