#define F_CPU 16000000UL
#include <stdio.h>
#include <string.h>
#include <avr/io.h>
#include <util/delay.h>
#include "step+IR.h"
#include "../uart/uart.h"


#define IR_IN_PIN PC2
#define STEP_1_PIN PD4
#define STEP_2_PIN PD5
#define STEP_3_PIN PD6
#define STEP_4_PIN PD7

void init() //핀설정
{
	DDRC &= ~(1<<IR_IN_PIN); // Set IR input pin as input
	PORTC |= (1<<IR_IN_PIN); // Enable internal pull-up resistor for IR input pin
	DDRD |= (1<<STEP_1_PIN)|(1<<STEP_2_PIN)|(1<<STEP_3_PIN)|(1<<STEP_4_PIN); // Set step motor pins as output
	Init_UART0();
}

void step_forward()   // 정방향
{
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_2_PIN)| (1 << STEP_3_PIN));   // low
	PORTD |= (1 << STEP_4_PIN);      // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_2_PIN));   // low
	PORTD |= (1 << STEP_3_PIN) | (1 << STEP_4_PIN);      // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_2_PIN)| (1 << STEP_4_PIN));   // low
	PORTD |= (1 << STEP_3_PIN);      // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_4_PIN));   // low
	PORTD |= (1 << STEP_2_PIN) | (1 << STEP_3_PIN);      // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_3_PIN)| (1 << STEP_4_PIN));   // low
	PORTD |= (1 << STEP_2_PIN);      // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_3_PIN) | (1 << STEP_4_PIN));   // low
	PORTD |= (1 << STEP_1_PIN) | (1 << STEP_2_PIN);      // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_2_PIN) | (1 << STEP_3_PIN)| (1 << STEP_4_PIN));   // low
	PORTD |= (1 << STEP_1_PIN);      // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_2_PIN) | (1 << STEP_3_PIN));   // low
	PORTD |= (1 << STEP_4_PIN) | (1 << STEP_1_PIN);      // high
	_delay_us(1000);
}

void step_backward() //역방향
{
	PORTD &= ~((1 << STEP_2_PIN) | (1 << STEP_3_PIN)); // low
	PORTD |= (1 << STEP_4_PIN) | (1 << STEP_1_PIN); // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_2_PIN) | (1 << STEP_3_PIN)| (1 << STEP_4_PIN)); // low
	PORTD |= (1 << STEP_1_PIN); // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_3_PIN) | (1 << STEP_4_PIN)); // low
	PORTD |= (1 << STEP_1_PIN) | (1 << STEP_2_PIN); // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_3_PIN)| (1 << STEP_4_PIN)); // low
	PORTD |= (1 << STEP_2_PIN); // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_4_PIN)); // low
	PORTD |= (1 << STEP_2_PIN) | (1 << STEP_3_PIN); // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_2_PIN)| (1 << STEP_4_PIN)); // low
	PORTD |= (1 << STEP_3_PIN); // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_2_PIN)); // low
	PORTD |= (1 << STEP_3_PIN) | (1 << STEP_4_PIN); // high
	_delay_us(1000);
	PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_2_PIN)| (1 << STEP_3_PIN)); // low
	PORTD |= (1 << STEP_4_PIN); // high
	_delay_us(1000);
}

uint8_t read_ir() //IR신호 수신
{
	uint8_t pulse_width = 0;
	int timeout = 200;
	while(PINC & (1<<IR_IN_PIN) && timeout) // Wait for IR signal to start
	{
		_delay_us(5000);
		timeout--;
	}
	while(!(PINC & (1<<IR_IN_PIN))) // Measure IR signal pulse width
	{
		_delay_us(5000);
		pulse_width++;
	}
	return pulse_width;
}
