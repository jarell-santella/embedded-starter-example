#ifndef SIGNAL_HANDLER_H
#define SIGNAL_HANDLER_H

#include <signal.h>

extern volatile sig_atomic_t keep_running;

void handle_sigint(int sig);

void setup_signal_handling();

#endif
