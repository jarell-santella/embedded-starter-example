#ifndef GPIO_FUNCTIONS_H
#define GPIO_FUNCTIONS_H

#include <gpiod.h>

int setup_gpio(struct gpiod_chip **chip1, struct gpiod_chip **chip2, struct gpiod_line **button_line, struct gpiod_line **blue_led_line, struct gpiod_line **red_led_line);

void teardown_gpio(struct gpiod_chip *chip1, struct gpiod_chip *chip2, struct gpiod_line *button_line, struct gpiod_line *blue_led_line, struct gpiod_line *red_led_line);

#endif
