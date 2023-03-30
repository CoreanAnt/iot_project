#include <avr/io.h>
#include "uart.h"


void Init_UART0(void)
{
	//	UCSR0B는 Tx, Rx를 설정한다. Tx(08), Rx(10)으로 설정
	UCSR0B = 0x18;		//	Tx와 Rx를 설정한다. 송/수신 가능하도록 설정
	UCSR0C = 0x06;		//	8bit data, no parity(0), 1 stop bit(0) 설정
	
	//	바운드 레이트 설정. 9600baud rate로 설정. 115200baud rate는 8로 설정
	UBRR0H = 0;
	UBRR0L = 103;
}

void USART_Init(void)
{
	UCSR0A=0x00; // clear
	UCSR0B=(1<<RXEN0) | (1<<TXEN0); // Rx, Tx Enable
	UCSR0C=(0<<UCSZ02) | (1<<UCSZ01) | (1<<UCSZ00); // Tx data len : 8-bit
	
	UBRR0H=0;
	UBRR0L=103; // baudrate 9600bps
}

unsigned char USART_Receive(void)
{
	while(!(UCSR0A & (1<<RXC0))); // Wait for data to be received
	return UDR0; // Get and return received data form buffer
}

void USART_Transmit(unsigned char data)
{
	while(!(UCSR0A & (1<<UDRE0))); // Wait for empty transmit buffer
	UDR0=data; // Put data into buffer, sends the  data
}

void strTransmit(char *str) {
	while (*str) {
		USART_Transmit(*str);
		str++;
	}
	USART_Transmit(10); // 개행문자
}



void UART_INIT(void) {
	UCSR0A |= _BV(U2X0);

	UBRR0H = 0x00;
	UBRR0L = 207;

	UCSR0C |= 0x06;
	
	UCSR0B |= _BV(RXEN0);
	UCSR0B |= _BV(TXEN0);
}

unsigned char UART_receive(void)
{
	while( !(UCSR0A & (1<<RXC0)) );
	return UDR0;
}

void UART_transmit(unsigned char data)
{
	while( !(UCSR0A & (1<<UDRE0)) );
	UDR0 = data;
}

void UART_printString(char *str)
{
	for(int i = 0; str[i]; i++)
	UART_transmit(str[i]);
}

void UART_print8bitNumber(uint8_t no)
{
	char numString[4] = "0";
	int i, index = 0;
	
	if(no > 0){
		for(i = 0; no != 0 ; i++)
		{
			numString[i] = no % 10 + '0';
			no = no / 10;
		}
		numString[i] = '\0';
		index = i - 1;
	}
	
	for(i = index; i >= 0; i--)
	UART_transmit(numString[i]);
}

void UART_print16bitNumber(uint16_t no)
{
	char numString[6] = "0";
	int i, index = 0;
	
	if(no > 0){
		for(i = 0; no != 0 ; i++)
		{
			numString[i] = no % 10 + '0';
			no = no / 10;
		}
		numString[i] = '\0';
		index = i - 1;
	}
	
	for(i = index; i >= 0; i--)
	UART_transmit(numString[i]);
}

void UART_print32bitNumber(uint32_t no)
{
	char numString[11] = "0";
	int i, index = 0;
	
	if(no > 0){
		for(i = 0; no != 0 ; i++)
		{
			numString[i] = no % 10 + '0';
			no = no / 10;
		}
		numString[i] = '\0';
		index = i - 1;
	}
	
	for(i = index; i >= 0; i--)
	UART_transmit(numString[i]);
}

void PutChar0(char c)
{
	//   5번째 비트가 켜져있지 않으면 while문이 무한 반복하는데
	//   5번째 비트가 켜지는 순간에 while 루프를 빠져나와서 데이터를 전송하는 원리
	
	//   데이터가 들어오지 않았다면 while문 반복
	while ( !( UCSR0A & 0x20 ) );   //   5번째 bit를 사용
	
	//   데이터를 전송
	UDR0 = c;
}

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