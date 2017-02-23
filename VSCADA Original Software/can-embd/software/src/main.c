//Clock Frequency
//#define F_CPU 16.00E6
#define F_CPU 16.00E6

//AVR-LIBC Headers 
#include <avr/cpufunc.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include <avr/sleep.h>

#include <util/delay.h>

#include "canlib/can_lib.h"
#include "adc.h"
#include "timer.h"

#define CAN_BUFFER_SIZE 8

#define CAN_ID 0x080

uint8_t response_data[CAN_BUFFER_SIZE];

void setup(void) {
	//Initialize ADC at AVCC level, 125kHz
	analogSetup(ADC_AVCC, ADC_SCALE_128);
	enableDAC();

	timer0_init(TIM_SCALE_1);
	timer0_pwm_init(PWM_OCxA, PWM_NRM, WGM_MODE_3);

	DDRD |= (1 << PD3);
	OCR0A = 0;
	
	can_init(0);
}

int main(void) {
	//Setup Comment
	setup();
	
	//Enable global interrupts
	sei();
	uint8_t tx_buffer[CAN_BUFFER_SIZE];
	st_cmd_t tx_msg;
	
	uint8_t rx_buffer[CAN_BUFFER_SIZE];
	st_cmd_t rx_msg;

	// Simulate collecting local sensor data: put test bytes in response buffer
	tx_buffer[0] = 0x00;
	tx_buffer[1] = 0x11;
	tx_buffer[2] = 0x22;
	tx_buffer[3] = 0x33;
	tx_buffer[4] = 0x44;
	tx_buffer[5] = 0x55;
	tx_buffer[6] = 0x66;
	tx_buffer[7] = 0x77;
	
	for(int i=0;i<256;i++) {
		tx_buffer[0] = i;
		tx_buffer[1] = (adcRead(ADC7) >> 2);
		tx_buffer[2] = (adcRead(ADC7) >> 2);
		//point message object to first element of data buffer
		tx_msg.pt_data = &tx_buffer[0];
		//standard CAN frame type (2.0A)
		tx_msg.ctrl.ide = 0;
		//Number of bytes being sent (8 max)
		tx_msg.dlc = CAN_BUFFER_SIZE;
		//populate ID field with ID Tag
		tx_msg.id.std = CAN_ID;
		//assign this as a "Standard (2.0A) Reply" message object
		tx_msg.cmd = CMD_TX_DATA; 
		
		//FIXME: Strange bug, call Atmel?
		//Does not work... should be able to work around
		//with CMD_RX_REMOTE_MASKED & CMD_TX_DATA
		//reply_message.cmd = CMD_REPLY_MASKED;
		
		rx_msg.pt_data = &rx_buffer[0];
		rx_msg.ctrl.ide = 0;
		rx_msg.dlc = CAN_BUFFER_SIZE;
		rx_msg.id.std = CAN_ID;
		rx_msg.cmd = CMD_RX_MASKED; 
		
		
		//wait for MOb to configure
		while(can_cmd(&rx_msg) != CAN_CMD_ACCEPTED); 
		
		//wait for a transmit request to come in
		while(can_get_status(&rx_msg) == CAN_STATUS_NOT_COMPLETED); 

		if(rx_msg.ctrl.rtr == 1) {	
			//wait for MOb to configure
			while(can_cmd(&tx_msg) != CAN_CMD_ACCEPTED); 
			
			// send a response
			while(can_get_status(&tx_msg) == CAN_STATUS_NOT_COMPLETED); 
		}
		else {
			OCR0A =rx_msg.pt_data[0];
			//_delay_ms(5000);
		}
	}

	for(;;) {
		for(int i=0;i<256;i++) {
			//OCR0A = i;
			timer0_pwm_write(PWM_OCxA, i);
			_delay_ms(10);
		}
		for(int i=255;i>=0;i--) {
			//OCR0A = i;
			timer0_pwm_write(PWM_OCxA, i);
			_delay_ms(10);
		}
	}
	
	return 0;
}
