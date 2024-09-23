#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include <pthread.h>
#include <time.h>
#include <unistd.h>

#include <gpiod.h>

#include "signal_handler.h"
#include "gpio_functions.h"

typedef struct {
    struct gpiod_line *red_led_line;
    int sleep_length;
} blink_red_led_args_t;

void *blink_red_led(void *args) {
    blink_red_led_args_t *blink_red_led_args = (blink_red_led_args_t *) args;
    struct gpiod_line *red_led_line = blink_red_led_args -> red_led_line;
    int sleep_length = blink_red_led_args -> sleep_length;

    int ret = 0;

    // Blink red LED at a regular interval
    while (keep_running) {
        ret = gpiod_line_set_value(red_led_line, 1);
        if (ret == -1) {
            fprintf(stderr, "Turn on red LED failed.\n");
            keep_running = 0;
        }
        
        if (!keep_running) {
            break;
        }

        sleep(sleep_length);

        ret = gpiod_line_set_value(red_led_line, 0);
        if (ret == -1) {
            fprintf(stderr, "Turn off red LED failed.\n");
            keep_running = 0;
        }

        if (!keep_running) {
            break;
        }

        sleep(sleep_length);
    }

    return (void *) (intptr_t) ret;
}

int main(int argc, char **argv) {
    // Initial set up of GPIO
    struct gpiod_chip *chip1 = NULL, *chip2 = NULL;
    struct gpiod_line *button_line = NULL, *blue_led_line = NULL, *red_led_line = NULL;

    int ret = setup_gpio(&chip1, &chip2, &button_line, &blue_led_line, &red_led_line);
    if (ret == -1) {
        fprintf(stderr, "Set up GPIO failed.\n");
        goto cleanup;
    }

    // Set up of signal handling
    setup_signal_handling();

    // Set up of sleep length from arguments (or default)
    int sleep_length = 1;

    if (argc > 1) {
        sleep_length = atoi(argv[1]);

        if (sleep_length <= 0) {
            sleep_length = 1;
        }
    }

    printf("Using sleep length of %d seconds.\n", sleep_length);

    // Set up of thread to blink red LED
    blink_red_led_args_t *blink_red_led_args = malloc(sizeof(blink_red_led_args_t));
    if (!blink_red_led_args) {
        fprintf(stderr, "Thread argument memory allocation failed.\n");
        ret = -1;
        goto cleanup;
    }

    blink_red_led_args -> red_led_line = red_led_line;
    blink_red_led_args -> sleep_length = sleep_length;

    pthread_t blink_red_led_thread;
    ret = pthread_create(&blink_red_led_thread, NULL, blink_red_led, blink_red_led_args);
    if (ret != 0) {
        fprintf(stderr, "Create thread to blink red LED failed.\n");
        ret = -1;
        free(blink_red_led_args);
        goto cleanup;
    }

    // Listen to button press to turn on blue LED
    while (keep_running) {
        int button_state = gpiod_line_get_value(button_line);
        if (button_state == -1) {
            fprintf(stderr, "Read button state failed.\n");
            ret = -1;
            keep_running = 0;
            break;
        }

        if (button_state == 0) {
            ret = gpiod_line_set_value(blue_led_line, 1);
            if (ret == -1) {
                fprintf(stderr, "Turn on blue LED failed.\n");
                keep_running = 0;
                break;
            }
        } else {
            ret = gpiod_line_set_value(blue_led_line, 0);
            if (ret == -1) {
                fprintf(stderr, "Turn off blue LED failed.\n");
                keep_running = 0;
                break;
            }
        }

        usleep(100000);
    }

    void *thread_ret = NULL;
    ret = pthread_join(blink_red_led_thread, &thread_ret);
    if (ret != 0) {
        fprintf(stderr, "Join thread to blink red LED failed.\n");
        ret = -1;
    } else {
        ret = (int) (intptr_t) thread_ret;

        if (ret == -1) {
            fprintf(stderr, "Thread to blink red LED failed.\n");
        }
    }

    free(blink_red_led_args);

cleanup:
    // Teardown everything gracefully
    teardown_gpio(chip1, chip2, button_line, blue_led_line, red_led_line);

    return ret;
}
