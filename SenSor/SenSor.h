/*
 * IncFile1.h
 *
 * Created: 2023-03-29 오전 11:14:59
 *  Author: dlxogus
 */ 


#ifndef SenSor_H_
#define SenSor_H_

// 불꽃 감지 센서 모듈 핀 설정
#define SENSOR1_PIN PC0

// 피에조 부저 핀 설정
#define BUZZER_PIN PD3

// 수위센서 핀 설정
#define SENSOR2_PIN PC1

//1채널 릴레이 관련 (환기팬)
#define RELAY4_PIN PD2 // 릴레이 모듈 제어 핀


void Sensor_init();
void Fire();
void water();



#endif /* INCFILE1_H_ */