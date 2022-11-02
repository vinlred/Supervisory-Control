#include <stdio.h>
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/timer.h"
#include "fsmmotor.h"

#define GPIO_INPUT_PB 5
#define GPIO_INPUT_PIN_SEL (1ULL<<GPIO_INPUT_PB)
#define TIMER_DIVIDER 16
#define DEBOUNCE 50

#define kp  0.8
#define ki  0.3
#define kd  0.0

double current_time_sec = 0;
double last_time_sec = 0;

float accel = 0;
float position1 = 0;
float outpid = 0;
float target1 = 0;
int button = 0;
int serial_valid = 0;
int state1 = 0;

float error = 0; 
float ierror = 0;
float derror = 0;
float preverror = 0;

void debounce_button(void *pvParam)
{
	while(1)
	{
		timer_get_counter_time_sec(0, 0, &current_time_sec);
    		if (gpio_get_level(GPIO_INPUT_PB) == 0 && (current_time_sec - last_time_sec > DEBOUNCE)) 
			{
        		button = 1;
			    timer_get_counter_time_sec(0, 0, &last_time_sec);
    		}
		vTaskDelay(100/portTICK_PERIOD_MS);
	}
}

void door_control(void *pvParam){
	while(1){
		TickType_t xLastWakeTime1 = xTaskGetTickCount();

        if(scanf("%f;%f", &accel, &position1) == 2){
            serial_valid = 1;
        }

        if(serial_valid == 1 ){
			fsm(&button, &state1, &target1, &position1);
			
			error = target1 - accel;
			ierror = ierror + (error * 0.01);
			derror = (preverror - error)/0.01;
			preverror = error;
			outpid = kp * error + ki * ierror + kd * derror;
			
			printf("%.8f\r\n",outpid);
			serial_valid = 0;
        }
        vTaskDelayUntil(&xLastWakeTime1, 30/portTICK_PERIOD_MS);
	}
}

void app_main()
{
	gpio_config_t io_conf;
	io_conf.pin_bit_mask = GPIO_INPUT_PIN_SEL;
	io_conf.mode = GPIO_MODE_INPUT; // mode input
	io_conf.intr_type = 1;
	io_conf.pull_up_en = 1; // menggunakan pull up
	gpio_config(&io_conf);
	
    timer_config_t config = {
        .divider = TIMER_DIVIDER,
        .counter_dir = TIMER_COUNT_UP, 
        .counter_en = TIMER_START, 
        .alarm_en = TIMER_ALARM_EN, 
        .auto_reload = TIMER_AUTORELOAD_DIS,
    }; 

    timer_init(0, 0, &config);
    timer_set_counter_value(0, 0, 0x00000000ULL);
    timer_start(0, 0);
	
		xTaskCreatePinnedToCore(debounce_button, "Button Activation", 2048, NULL, 1, NULL, 0);
		xTaskCreatePinnedToCore(door_control, "Door Activated", 2048, NULL, 1, NULL, 1);
}
