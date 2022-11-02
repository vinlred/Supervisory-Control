#ifndef FSMMOTOR_H
#define FSMMOTOR_H

#define STATE_CLOSE 0
#define STATE_OPEN  1
#define ACCEL_UP    2
#define ACCEL_DOWN  3
#define OPENING     4
#define CLOSING     5

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fsm(int *input,int *state, float *target,float *position){
	switch(*state)
	{
		case STATE_CLOSE:
		{
			if(*input == 1){
				*state = ACCEL_UP;
				*target = 1;
			}
			break;
		}
		case ACCEL_UP:
		{
			if(*position >= 1){
				*state = OPENING;
				*target = 0;
			}
			else if(*position <= 0){
				*state = STATE_CLOSE;
				*target = 0;
			}
			break;
		}
		case OPENING:
		{
			if(*position >= 2){
				*state = ACCEL_DOWN;
				*target = -1;
			}
			break;
		}
		case CLOSING:
		{
			if(*position <= 1){
				*state = ACCEL_UP;
				*target = 1;
			}
			break;
		}
		case ACCEL_DOWN:
		{
			if(*position >= 3){
				*state = STATE_OPEN;
				*target = 0;
			}
			else if(*position <= 2){
				*state = CLOSING;
				*target = 0;
			}
			break;
		}
		case STATE_OPEN:
		{
			if (*input == 1){
				*state = ACCEL_DOWN;
				*target = -1;
			}
			break;
		}
		default:
		{
			break;
		}
	}
}

#endif // FSMMOTOR_H