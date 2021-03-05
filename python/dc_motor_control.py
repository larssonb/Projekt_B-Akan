#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np
from itertools import chain

try:
    from board import SCL, SDA
    import busio
    import RPi.GPIO as GPIO
    from adafruit_pca9685 import PCA9685
    test_environment = False
except (ImportError, RuntimeError):
    test_environment = True

if test_environment:
    pass
else:
    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)
    # Create a simple PCA9685 class instance.
    pca = PCA9685(i2c_bus)
    # Set the PWM frequency to 60hz.
    pca.frequency = 60

    GPIO.setmode(GPIO.BCM)  # choose BCM pin numbering

    # LEFT MOTOR
    GPIO.setup(23, GPIO.OUT)  # set GPIO23 as an output
    GPIO.setup(24, GPIO.OUT)  # set GPIO24 as an output

    # RIGHT MOTOR
    GPIO.setup(17, GPIO.OUT)  # set GPIO17 as an output
    GPIO.setup(27, GPIO.OUT)  # set GPIO27 as an output

Motor_pins = {'LEFT': (24, 23, 12),
              'RIGHT': (17, 27, 13),
              'TOP': (5, 6, 14),
              'BOTTOM': (16, 26, 15)}


class MotorController(object):
    """docstring for MotorController."""

    def __init__(self, location):
        # Setup output pins and initialize
        self.pin_A, self.pin_B, self.PWM_channel = Motor_pins[location]
        self.speed = 0
        GPIO.output(self.pin_B, 0)
        GPIO.output(self.pin_A, 1)
        self.set_speed(self.speed)

    def _set_direction_forward(self):
        print('Switching forward')
        GPIO.output(self.pin_B, 0)
        GPIO.output(self.pin_A, 1)

    def _set_direction_backward(self):
        print('Switching backward')
        GPIO.output(self.pin_A, 0)
        GPIO.output(self.pin_B, 1)

    def set_speed(self, speed):

        if speed == self.speed:
            return
        # Ramp step size
        step_size = 0x0800
        # Sleep time - UPDATE LATER
        timer = 0.1

        int_speed = int(speed*0xFFFF)
        old_speed = int(self.speed*0xFFFF)

        if np.sign(int_speed)*np.sign(old_speed) < 0:
            ramp_speeds = chain(
                    range(old_speed, 0,
                          np.sign(int_speed-old_speed)*step_size),
                    range(0, int_speed,
                          np.sign(int_speed-old_speed)*step_size),
                    [int_speed])
        else:
            ramp_speeds = chain(
                    range(old_speed, int_speed,
                          np.sign(int_speed-old_speed)*step_size),
                    [int_speed])

        for ramp_speed in ramp_speeds:
            pca.channels[self.PWM_channel].duty_cycle = abs(ramp_speed)

            print(abs(ramp_speed), ' ', abs(ramp_speed)/0xFFFF)
            if ramp_speed == 0:
                if np.sign(int_speed)*np.sign(old_speed) <= 0:
                    if int_speed >= 0:
                        self._set_direction_forward()
                    elif int_speed < 0:
                        self._set_direction_backward()
            time.sleep(timer)
        self.speed = speed


MC_L = MotorController('LEFT')
MC_R = MotorController('RIGHT')

MC_L.set_speed(0.0)
MC_R.set_speed(0.0)
