#ifndef UART_H_
#define UART_H_

void USART_Init(void);
unsigned char USART_Receive(void);
void USART_Transmit(unsigned char data);
void strTransmit(char *str);
void Init_UART0(void);
void UART_INIT(void);
unsigned char UART_receive(void);
void UART_transmit(unsigned char data);
void UART_printString(char *str);
void UART_print8bitNumber(uint8_t no);
void UART_print16bitNumber(uint16_t no);
void UART_print32bitNumber(uint32_t no);

#endif /* UART_H_ */