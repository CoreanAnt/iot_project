#ifndef DHT11_H_
#define DHT11_H_

#define DHT11_ERROR 255

#define DHT11_DDR DDRC
#define DHT11_PORT PORTC
#define DHT11_PIN PINC
#define DHT11_INPUTPIN PC5

void dht11_getdata(uint8_t num, uint8_t *data);
uint8_t getdata(uint8_t select);


#endif /* DHT11_H_ */