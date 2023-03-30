/*
 * CFile1.c
 *
 * Created: 2023-03-29 오전 11:09:53
 *  Author: dlxogus
 */ 
#include <avr/io.h>
#include "ADC.h"

unsigned short ReadADC1(void)  //조도 PC3
{
	ADMUX = 0x43; // ADC3을 사용할 것이다.
	ADCSRA |= (1 << ADSC); // 변환시작
	while (ADCSRA & (1 << ADSC));
	return ADC;
}

/*  ADC channel 2값을 읽어서 리턴하는 함수 */
unsigned short ReadADC2(void) //토양 PC4
{
	ADMUX = 0x44; // ADC4를 사용할 것이다.
	ADCSRA |= (1 << ADSC); // 변환시작
	while (ADCSRA & (1 << ADSC));
	return ADC;
}