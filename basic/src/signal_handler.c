#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>

#include "signal_handler.h"

volatile sig_atomic_t keep_running = 1;

void handle_sigint(int sig) {
    printf("Received interrupt signal. Attempting to shut down gracefully.\n");
    keep_running = 0;
}

void setup_signal_handling() {
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = handle_sigint;
    sigaction(SIGINT, &sa, NULL);
}
