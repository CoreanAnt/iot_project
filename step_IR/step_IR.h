#ifndef STEP_IR_H_
#define STEP_IR_H_

#define IR_IN_PIN PC2
#define STEP_1_PIN PD4
#define STEP_2_PIN PD5
#define STEP_3_PIN PD6
#define STEP_4_PIN PD7



void Step_init();
void step_forward();
void step_backward();
uint8_t read_ir();
void Pulse();



#endif /* STEP_H_ */