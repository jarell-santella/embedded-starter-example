# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
import sys
import time
import spidev
import logging
import numpy as np
import gpiod
from threading import Thread, Event

class PWM:
    def __init__(self, line, frequency=1000, duty_cycle=0):
        self.line = line
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.running = False
        self.thread = None
        self.stop_event = Event()

    def start(self):
        if not self.running:
            self.running = True
            self.stop_event.clear()
            self.thread = Thread(target=self._run)
            self.thread.start()

    def _run(self):
        period = 1.0 / self.frequency
        high_time = period * (self.duty_cycle / 100.0)
        low_time = period - high_time
        while not self.stop_event.is_set():
            if high_time > 0:
                self.line.set_value(1)
                if self.stop_event.wait(high_time):
                    break
            if low_time > 0:
                self.line.set_value(0)
                if self.stop_event.wait(low_time):
                    break

    def change_frequency(self, frequency):
        self.frequency = frequency
        if self.running:
            self.stop()
            self.start()

    def change_duty_cycle(self, duty_cycle):
        self.duty_cycle = duty_cycle

    def stop(self):
        if self.running:
            self.running = False
            self.stop_event.set()
            self.thread.join()

    def close(self):
        self.stop()
        self.line.set_value(0)

class RaspberryPi:
    # Mapping GPIO numbers to (gpiochip, line)
    GPIO_PINS = {
        18: ('gpiochip2', 14),
        25: ('gpiochip1', 42),
        27: ('gpiochip1', 33),
    }

    def __init__(self, spi_bus=0, spi_device=0, spi_freq=40000000, rst=27, dc=25, bl=18, bl_freq=1000, i2c=None, i2c_freq=100000):
        self.np = np
        self.INPUT = False
        self.OUTPUT = True

        self.SPEED = spi_freq
        self.BL_freq = bl_freq

        logging.debug("Initializing GPIO chips")
        
        # Open the necessary gpiochips based on GPIO_PINS
        self.chips = {}
        for gpio in [rst, dc, bl]:
            chip_name, line = self.GPIO_PINS[gpio]
            if chip_name not in self.chips:
                try:
                    # Use absolute path
                    chip_path = f'/dev/{chip_name}'
                    self.chips[chip_name] = gpiod.Chip(chip_path)
                    logging.debug(f"Opened {chip_path}")
                except OSError as e:
                    logging.error(f"Failed to open {chip_path}: {e}")
                    sys.exit(1)

        logging.debug("GPIO chips opened successfully")

        # Initialize GPIO lines
        self.RST_LINE = self.gpio_mode(rst, self.OUTPUT)
        self.DC_LINE = self.gpio_mode(dc, self.OUTPUT)
        self.BL_LINE = self.gpio_mode(bl, self.OUTPUT)

        # Initialize PWM for backlight
        self.BL_PWM = PWM(self.BL_LINE, frequency=self.BL_freq, duty_cycle=0)
        self.BL_PWM.start()
        logging.debug("Backlight PWM started")

        # Initialize SPI
        self.SPI = spidev.SpiDev()
        if self.SPI is not None:
            try:
                self.SPI.open(spi_bus, spi_device)
                self.SPI.max_speed_hz = spi_freq
                self.SPI.mode = 0b00
                logging.debug(f"Opened SPI bus {spi_bus}, device {spi_device} at {spi_freq} Hz")
            except Exception as e:
                logging.error(f"Failed to open SPI bus {spi_bus}, device {spi_device}: {e}")
                sys.exit(1)

    def gpio_mode(self, pin, mode, pull_up=None, active_state=True):
        chip_name, line_num = self.GPIO_PINS[pin]
        chip = self.chips[chip_name]
        line = chip.get_line(line_num)
        try:
            if mode == self.OUTPUT:
                line.request(consumer="lcdconfig", type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
                logging.debug(f"Set GPIO{pin} as OUTPUT on {chip_name} line {line_num}")
            else:
                req = gpiod.LineRequest()
                req.consumer = "lcdconfig"
                req.request_type = gpiod.LINE_REQ_DIR_IN
                if pull_up is not None:
                    req.flags = gpiod.LINE_REQ_FLAG_BIAS_PULL_UP if pull_up else gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN
                line.request(req)
                logging.debug(f"Set GPIO{pin} as INPUT on {chip_name} line {line_num}")
            return line
        except Exception as e:
            logging.error(f"Failed to set GPIO mode for pin {pin} on {chip_name} line {line_num}: {e}")
            sys.exit(1)

    def digital_write(self, line, value):
        try:
            line.set_value(1 if value else 0)
            logging.debug(f"Wrote {'HIGH' if value else 'LOW'} to GPIO line")
        except Exception as e:
            logging.error(f"Failed to write to GPIO line: {e}")

    def digital_read(self, line):
        try:
            value = line.get_value()
            logging.debug(f"Read value {value} from GPIO line")
            return value
        except Exception as e:
            logging.error(f"Failed to read GPIO line: {e}")
            return 0

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        if self.SPI is not None:
            try:
                self.SPI.writebytes(data)
                logging.debug(f"Wrote bytes to SPI: {data}")
            except Exception as e:
                logging.error(f"Failed to write bytes to SPI: {e}")

    def bl_DutyCycle(self, duty):
        self.BL_PWM.change_duty_cycle(duty)
        logging.debug(f"Changed backlight duty cycle to {duty}%")

    def bl_Frequency(self, freq):  # Hz
        self.BL_PWM.change_frequency(freq)
        logging.debug(f"Changed backlight frequency to {freq} Hz")

    def module_init(self):
        if self.SPI is not None:
            self.SPI.max_speed_hz = self.SPEED
            self.SPI.mode = 0b00
            logging.debug("SPI module initialized")
        return 0

    def module_exit(self):
        logging.debug("Shutting down SPI")
        if self.SPI is not None:
            self.SPI.close()

        logging.debug("Cleaning up GPIO")
        try:
            self.digital_write(self.RST_LINE, 1)
            self.digital_write(self.DC_LINE, 0)
            self.BL_PWM.close()
            logging.debug("GPIO cleaned up successfully")
        except Exception as e:
            logging.error(f"Error during GPIO cleanup: {e}")
        
        # Close all gpiochips
        for chip_name, chip in self.chips.items():
            try:
                chip.close()
                logging.debug(f"Closed {chip_name}")
            except Exception as e:
                logging.error(f"Failed to close {chip_name}: {e}")
        
        time.sleep(0.001)

'''
if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    implementation = RaspberryPi()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))
'''

### END OF FILE ###
