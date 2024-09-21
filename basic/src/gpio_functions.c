#include <stdio.h>

#include "gpio_functions.h"

int setup_gpio(struct gpiod_chip **chip1, struct gpiod_chip **chip2, struct gpiod_line **button_line, struct gpiod_line **blue_led_line, struct gpiod_line **red_led_line) {
    *chip1 = gpiod_chip_open_by_name("gpiochip1");
    if (!*chip1) {
        fprintf(stderr, "Open gpiochip1 failed.\n");
        return -1;
    }

    *chip2 = gpiod_chip_open_by_name("gpiochip2");
    if (!*chip2) {
        fprintf(stderr, "Open gpiochip2 failed.\n");
        return -1;
    }

    *button_line = gpiod_chip_get_line(*chip2, 8);
    if (!*button_line) {
        fprintf(stderr, "Get gpiochip2 line 8 failed.\n");
        return -1;
    }

    *blue_led_line = gpiod_chip_get_line(*chip1, 33);
    if (!*blue_led_line) {
        fprintf(stderr, "Get gpiochip1 line 33 failed.\n");
        return -1;
    }

    *red_led_line = gpiod_chip_get_line(*chip1, 41);
    if (!*red_led_line) {
        fprintf(stderr, "Get gpiochip1 line 41 failed.\n");
        return -1;
    }

    if (gpiod_line_request_input(*button_line, "basic_example_button") == -1) {
        fprintf(stderr, "Request GPIO17 as input failed.\n");
        return -1;
    }

    if (gpiod_line_request_output(*blue_led_line, "basic_example_blue_led", 0) == -1) {
        fprintf(stderr, "Request GPIO27 as output failed.\n");
        return -1;
    };

    if (gpiod_line_request_output(*red_led_line, "basic_example_red_led", 0) == -1) {
        fprintf(stderr, "Request GPIO22 as output failed.\n");
        return -1;
    }

    return 0;
}

void teardown_gpio(struct gpiod_chip *chip1, struct gpiod_chip *chip2, struct gpiod_line *button_line, struct gpiod_line *blue_led_line, struct gpiod_line *red_led_line) {
    printf("Starting cleanup.\n");

    if (button_line) gpiod_line_release(button_line);
    if (blue_led_line) {
        gpiod_line_set_value(blue_led_line, 0);
        gpiod_line_release(blue_led_line);
    }
    if (red_led_line) {
        gpiod_line_set_value(red_led_line, 0);
        gpiod_line_release(red_led_line);
    }

    if (chip1) gpiod_chip_close(chip1);
    if (chip2) gpiod_chip_close(chip2);

    printf("Finishing cleanup.\n");
}
