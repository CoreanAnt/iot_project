#include <avr/io.h>
#include <util/delay.h>


#define PRESCALER 8   // 분주비
#define PWM_FREQ 440  // PWM 주파수 (Hz)

void init_pwm() {
	// PWM 제어 레지스터 설정
	TCCR2A |= (1 << COM2B1) | (1 << WGM21) | (1 << WGM20); // 비반전 모드, 고속 PWM 모드
	TCCR2B |= (1 << CS21); // 분주비 8 설정
	DDRD |= (1 << PD3); // OC2B 핀(PD3) 출력으로 설정
}

void play_tone(int freq, int duration) {
	OCR2B = (F_CPU / (2 * PRESCALER * freq)) - 1;
	for (int i = 0; i < duration; i++) {
		_delay_ms(1);
	}
	OCR2B = 0;
}