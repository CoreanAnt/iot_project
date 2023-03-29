#define F_CPU 16000000UL   //   16MHz
#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "dht11/dht11.h"
#include "uart/uart.h"
#include "step+IR/step+IR.h"
#include "buzzer/buzzer.h"


#define STEP_1_PIN PD4
#define STEP_2_PIN PD5
#define STEP_3_PIN PD6
#define STEP_4_PIN PD7


// 불꽃 감지 센서 모듈 핀 설정
#define SENSOR1_PIN PC0

// 피에조 부저 핀 설정
#define BUZZER_PIN PD3

// 수위센서 핀 설정
#define SENSOR2_PIN PC1   


//1채널 릴레이 관련 (환기팬)
#define RELAY4_PIN PD2 // 릴레이 모듈 제어 핀





bool forward = true;

/*   문자 하나를 전송하는 함수   */
void PutChar0(char c);

/*   문자열을 전송하는 함수   */
void Puts0(char* str);

/*   문자열을 수신하는 함수   */
char Gets0(void);



/*   ADC값을 읽어서 리턴하는 함수   */
unsigned short ReadADC1(void);
unsigned short ReadADC2(void);

int main(void)
{
   char p[12];
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
  
   
   DDRD |= (1 << RELAY4_PIN); //1채널 릴레이 모듈 핀을 출력으로 설정
   
   
   // 불꽃 감지 센서 모듈 핀을 입력으로 설정
   DDRC &= ~(1 << SENSOR1_PIN);
   
   // 내부 풀업 저항 사용
   PORTC |= (1 << SENSOR1_PIN);

   // 수위센서 핀을 풀업 모드로 설정
   PORTC |= (1 << SENSOR2_PIN); 
   
   init();

   int temperature;
   int humidity;
   
   while (1)
   {
      
      
      // 불꽃 감지 센서 모듈에서 신호를 감지했는지 확인
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
       
     
     
     uint8_t pulse_width = read_ir();   //IR센서및 스텝모터 관련
      char buffer[16];
      sprintf(buffer, "Pulse width: %d\r\n", pulse_width);
      for (int i = 0; buffer[i] != 0; i++)
      {
         while (!(UCSR0A & (1 << UDRE0)));
         UDR0 = buffer[i];
      }
      _delay_ms(1000);
         
      if (pulse_width > 0 && forward == true)
      {
         for(int i=0; i < 64; i++)
         {
            for(int j=0; j<8;j++)
            {
               step_forward();
            }
         }
         PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_2_PIN)| (1 << STEP_3_PIN)| (1 << STEP_4_PIN));
         forward = false;
            
      }
      else if(pulse_width > 0 && forward == false)
      {
         for(int i=0; i < 64; i++)
         {
            for(int j=0; j<8;j++)
            {
               step_backward();
            }
         }
         PORTD &= ~((1 << STEP_1_PIN) | (1 << STEP_2_PIN)| (1 << STEP_3_PIN)| (1 << STEP_4_PIN));
         forward = true;
            
      }
      else
      {
     }
   }
   
   return 0;
   
   
}



/*  ADC channel 3값을 읽어서 리턴하는 함수 */
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

/*   문자 하나를 전송하는 함수   */
void PutChar0(char c)
{
   //   5번째 비트가 켜져있지 않으면 while문이 무한 반복하는데
   //   5번째 비트가 켜지는 순간에 while 루프를 빠져나와서 데이터를 전송하는 원리
   
   //   데이터가 들어오지 않았다면 while문 반복
   while ( !( UCSR0A & 0x20 ) );   //   5번째 bit를 사용
   
   //   데이터를 전송
   UDR0 = c;
}

/*   문자열을 전송하는 함수   */
void Puts0(char* str)
{
   while(*str)
   {
      while(!(UCSR0A & (1 << UDRE0)));
      UDR0 = *str++;
   }
}

/*   문자열을 수신하는 함수   */
char Gets0(void)
{
   //   데이터가 들어오지 않았다면 while문 반복
   while ( !( UCSR0A & 0x80 ) );   //   RXC가 Set(8번째 자리)되어 있어야 한다.
   
   //   데이터를 리턴
   return UDR0;
}