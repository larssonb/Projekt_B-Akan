# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# This simple test outputs a 10% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.
#from board import SCL, SDA
#import busio
#import RPi.GPIO as GPIO  # import RPi.GPIO module
from enum import Enum
import time

# # Import the PCA9685 module.
# from adafruit_pca9685 import PCA9685
# # Create the I2C bus interface.
# i2c_bus = busio.I2C(SCL, SDA)
# # Create a simple PCA9685 class instance.
# pca = PCA9685(i2c_bus)
# # Set the PWM frequency to 60hz.
# pca.frequency = 60


class Motor(Enum):
    LEFT_A = 24
    LEFT_B = 23
    RIGHT_A = 17
    RIGHT_B = 27
    TOP_A = 5
    TOP_B = 6
    BOTTOM_A = 16
    BOTTOM_B = 26


class MotorController(object):
    """docstring for MotorController."""

    def __init__(self):#, location):
        # Setup output pins and initialize
        self.pin_A = 0
        self.pin_B = 0
        self.PWM_channel = 0
        self.speed = 0
        #GPIO.output(self.pin_B, 0)
        #GPIO.output(self.pin_A, 1)
        #self.set_speed(self.speed)

    def _set_direction_forward(self):
        print('Switching forward')
        #GPIO.output(self.pin_B, 0)
        #GPIO.output(self.pin_A, 1)

    def _set_direction_backward(self):
        print('Switching backward')
        #GPIO.output(self.pin_A, 0)
        #GPIO.output(self.pin_B, 1)

    def set_speed(self, speed):

        if speed == self.speed:
            return

        # Sleep time - UPDATE LATER
        timer = 0.1

        if speed >= 0 and self.speed < 0:
            # Code for changing direction from backward to forward
            steps_A = round(abs(0 - self.speed) / 0.05)
            steps_B = round(abs(speed) / 0.05)

            speed_step_A = (0 - self.speed) / steps_A
            ramp_speed = self.speed
            for step in range(steps_A):
                ramp_speed += speed_step_A
                print(ramp_speed)
                #pca.channels[self.PWM_channel].duty_cycle = hex(int(ramp_speed * 0xFFFF))
                time.sleep(timer)

            self._set_direction_forward()

            speed_step_B = abs(speed) / steps_B
            for step in range(steps_B):
                ramp_speed += speed_step_B
                print(ramp_speed)
                #pca.channels[self.PWM_channel].duty_cycle = hex(int(ramp_speed * 0xFFFF))
                time.sleep(timer)

        elif speed < 0 and self.speed >= 0:
            # Code for changing direction from forward to backward
            steps_A = round(abs(0 - self.speed) / 0.05)
            steps_B = round(abs(speed) / 0.05)

            speed_step_A = (0 - self.speed) / steps_A
            ramp_speed = self.speed
            for step in range(steps_A):
                ramp_speed += speed_step_A
                print(ramp_speed)
                #pca.channels[self.PWM_channel].duty_cycle = hex(int(ramp_speed * 0xFFFF))
                time.sleep(timer)

            self._set_direction_backward()

            speed_step_B = abs(speed) / steps_B
            for step in range(steps_B):
                ramp_speed += speed_step_B
                print(ramp_speed)
                #pca.channels[self.PWM_channel].duty_cycle = hex(int(ramp_speed * 0xFFFF))
                time.sleep(timer)

        else:
            steps = round(abs(speed - self.speed) / 0.05)
            speed_step = (speed - self.speed) / steps
            ramp_speed = self.speed
            for step in range(steps):
                ramp_speed += speed_step
                print(ramp_speed)
                #pca.channels[self.PWM_channel].duty_cycle = hex(int(ramp_speed * 0xFFFF))
                time.sleep(timer)

        self.speed = speed

        # Set the PWM duty cycle for channel zero to 10%. duty_cycle is 16 bits to match other PWM objects
        # but the PCA9685 will only actually give 12 bits of resolution.
        # pca.channels[self.PWM_channel].duty_cycle = hex(int(speed * 0xFFFF))


MC = MotorController()

MC.set_speed(0.9)




# Set IN_A and IN_B for the DC motor driver.

# GPIO.setmode(GPIO.BCM) # choose BCM pin numbering
#
# GPIO.setup(23, GPIO.OUT) # set GPIO23 as an output
# GPIO.setup(24, GPIO.OUT) # set GPIO24 as an output
#
# GPIO.output(24, 1) # set GPIO24 to 1/GPIO.HIGH/True
# GPIO.output(23, 0) # set GPIO23 to 0/GPIO.LOW/False
