/*
 * CFile1.c
 *
 * Created: 2023-03-29 오전 11:14:54
 *  Author: dlxogus
 */ 
#define F_CPU 16000000UL 
#include <avr/io.h>
#include <stdio.h>
#include <util/delay.h>
#include "Sensor.h"
#include "../buzzer/buzzer.h"
#include "../uart/uart.h"
#include "../ADC/ADC.h"

void Sensor_init()
{
	DDRD |= (1 << RELAY4_PIN); //1채널 릴레이 모듈 핀을 출력으로 설정
	
	// 수위센서 핀을 풀업 모드로 설정
	DDRC &= ~(1 << SENSOR1_PIN);
	
	// 내부 풀업 저항 사용
	PORTC |= (1 << SENSOR1_PIN);
	
	// 불꽃 감지 센서 모듈 핀을 입력으로 설정
	PORTC |= (1 << SENSOR2_PIN);
}

void Fire()
{
	if (PINC & (1 << SENSOR2_PIN))
	{
		
		sprintf( p, "fire : 0 \n" ); //불꽃 미감지
		Puts0( p );
		// 불꽃이 감지되지 않았다면 부저 끄기
		PORTD &= ~(1 << BUZZER_PIN);
		DDRD &= ~(1 << BUZZER_PIN);
		_delay_ms(1000);
		
		
	}
	else
	{
		sprintf( p, "fire : 1 \n" );  //불꽃감지!
		Puts0( p );
		// 부저 핀을 출력으로 설정
		init_pwm();
		
		for(int r=1;r<=5;r++)
		{
			// 불꽃이 감지되었다면 피에조 부저 울리기
			play_tone(500, 10000);
		}
		
	}
}

void water()
{
	//수위센서 관련
	if (PINC & (1 << SENSOR1_PIN))  // 수위센서 핀이 LOW인 경우
	{
		sprintf( p, "water : 0 \n" ); //물이 부족합니다.
		Puts0( p );
		_delay_ms( 500 );
		PORTD |= (1 << RELAY4_PIN);
		
	}
	
	else
	{
		sprintf( p, "water : 1 \n" );
		Puts0( p );
		_delay_ms( 500 );
		
		if(ReadADC2()<440 )//수중펌프 동작관련
		{
			PORTD &= ~(1 << RELAY4_PIN);
			_delay_ms( 10000 );
			PORTD |= (1 << RELAY4_PIN);
			
		}
		
		else
		{
			PORTD |= (1 << RELAY4_PIN);
		}
	}
}