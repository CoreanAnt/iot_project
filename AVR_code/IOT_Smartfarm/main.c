#define F_CPU 16000000UL   //   16MHz
#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "dht11/dht11.h"
#include "uart/uart.h"
#include "step_IR/step_IR.h"
#include "buzzer/buzzer.h"
#include "ADC/ADC.h"
#include "SenSor/SenSor.h"

bool forward = true;

int main(void)
{
   int temperature;
   int humidity;
   /*
   ADMUX |= 0x40;                  //   AVCC를 기준전압으로 설정
   ADCSRA |= 0x07;                  //   분주비를 128로 설정
   ADCSRA |= ( 1 << ADEN );         //   ADC 활성화
   ADCSRA |= ( 1 << ADATE );         //   자동 트리거 모드
   ADMUX |= ( ( ADMUX & 0xE0 ) | 0 );   //   채널 선택
   ADCSRA |= ( 1 << ADSC );         //   변환시작
   */
   
   //   위의 설정을 한 번에 처리한 문장이 아래의 두 문장
   
   ADCSRA = 0x87;   //   0x87 = 0b1000 0111
   
   uint8_t data = 0;
   char buf[40] = {0,};
   USART_Init();
   Init_UART0();
   Sensor_init();
   Step_init();

   while (1)
   {
      
	  
		dht11_getdata(0, &data);
		temperature=data;
		sprintf(buf, "temperature:%d", temperature); //temperature:
		strTransmit(buf);
		memset(buf, 0x00, 40);
		_delay_ms(1000);
     
		dht11_getdata(1, &data);
		humidity=data;
		sprintf(buf, "humidity: %d", humidity); ////humidity:
		strTransmit(buf);
		memset(buf, 0x00, 40);
		_delay_ms( 1000 );
	 
	 
		sprintf( p, "soil : %d \n", ReadADC2() ); // ADC2의 값을 문자열로 변경. 채널4  //soil :
		Puts0( p );
		_delay_ms( 1000 );
     
		sprintf( p, "light : %d \n", ReadADC1() ); // ADC1의 값을 문자열로 변경. 채널1   //light :
		Puts0( p );
		_delay_ms( 1000 );
		
		
		Fire();
	 
     
		water();
	
	
	    uint8_t pulse_width = read_ir();   //IR센서및 스텝모터 관련
		Pulse();
		if (pulse_width > 0 && forward == true)
		{
			step_forward();
			forward = false;
		}
		else if(pulse_width > 0 && forward == false)
		{
			step_backward();
			forward = true;
		}
	}
   return 0;
}