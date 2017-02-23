#include "adc.h"

#include <avr/io.h>

#include <stdint.h>

void analogSetup(uint8_t mode, uint8_t scale) {
	//switch(mode) {
	//	//AREF SETUP
	//	case ADC_AREF:
	//		ADCSRA = (scale << ADPS0);
	//		ADCSRB = (1 << AREFEN);
	//		ADCSRA = (1 << ADEN);
	//		break;
	//	//AVCC
	//	case ADC_AVCC:
			// AREF = AVcc
			ADMUX = (1<<REFS0);
			// ADC Enable and prescaler of 128
			// 16000000/128 = 125000
			ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
	//		break;
	//}
}

uint16_t adcRead(uint8_t pin) {
	//Clear Lower 5 bits (MUX[4:0])
	ADMUX &= ~(0x1F << MUX0);
	ADMUX |= (pin << MUX0);
	
	//Start conversion
	ADCSRA |= (1 << ADSC);
	//Wait for complete conversion
	while(ADCSRA & (1<<ADSC));
	return ADC;
}

void enableDAC(void) {
	DACON = (1 << DAOE) | (1 << DAEN);
}

void disableDAC(void) {
	DACON = 0;
}

void dacWrite(uint16_t level) {
	DACH = (level >> 8);
	DACL = level;
}


