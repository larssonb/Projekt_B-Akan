# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# This simple test outputs a 10% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.
from board import SCL, SDA
import busio
import RPi.GPIO as GPIO  # import RPi.GPIO module
from enum import Enum
import time
import numpy as np
from itertools import chain

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685
# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)
# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)
# Set the PWM frequency in hz.
pca.frequency = 1526


# class Motor(Enum):
#     LEFT_A = 24
#     LEFT_B = 23
#     RIGHT_A = 17
#     RIGHT_B = 27
#     TOP_A = 5
#     TOP_B = 6
#     BOTTOM_A = 16
#     BOTTOM_B = 26
#     
# class PWM(Enum):
#     LEFT = 12
#     RIGHT = 13

Motor_pins = {'LEFT': (23, 24, 13),
              'RIGHT': (27, 22, 12),
              'TOP': (26, 16, 15),
              'BOTTOM': (6, 5, 14)}

# Set IN_A and IN_B for the DC motor driver.

GPIO.setmode(GPIO.BCM) # choose BCM pin numbering

# LEFT MOTOR
GPIO.setup(23, GPIO.OUT) # set GPIO22 as an output
GPIO.setup(24, GPIO.OUT) # set GPIO27 as an output

# RIGHT MOTOR

GPIO.setup(22, GPIO.OUT) # set GPIO23 as an output
GPIO.setup(27, GPIO.OUT) # set GPIO24 as an output

# TOP MOTOR

GPIO.setup(26, GPIO.OUT) # set GPIO23 as an output
GPIO.setup(16, GPIO.OUT) # set GPIO24 as an output

# BOTTOM MOTOR

GPIO.setup(5, GPIO.OUT) # set GPIO23 as an output
GPIO.setup(6, GPIO.OUT) # set GPIO24 as an output


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
        step_size = 2048 # 0x0800
        # Sleep time - UPDATE LATER
        timer = 0.02 

        int_speed = int(speed*0xFFFF)
        old_speed = int(self.speed*0xFFFF)

        if np.sign(int_speed)*np.sign(old_speed) < 0:
            
            ramp_speeds_A = range(old_speed, 0, np.sign(int_speed-old_speed)*step_size)
            ramp_speeds_B = range(0, int_speed, np.sign(int_speed-old_speed)*step_size)
            
            ramp_speeds   = chain(ramp_speeds_A, ramp_speeds_B, [int_speed])
            
        
        else:
            ramp_speeds = chain(range(old_speed, int_speed, np.sign(int_speed-old_speed)*step_size), [int_speed])
        

        for ramp_speed in ramp_speeds:
            
            pca.channels[self.PWM_channel].duty_cycle = abs(ramp_speed)
            
            print(abs(ramp_speed),' ',round(100*abs(ramp_speed)/0xFFFF), ' %')
            if ramp_speed == 0:
                             
                if np.sign(int_speed)*np.sign(old_speed) <= 0:
                    if int_speed >= 0:
                        self._set_direction_forward()
                        
                    elif int_speed < 0:
                        self._set_direction_backward()                
                
            time.sleep(timer)
            
        self.speed = speed
        
def set_all(speed):
    t = 0.5
    MC_L.set_speed(speed)
    time.sleep(t)
    MC_R.set_speed(speed)
    time.sleep(t)
    MC_T.set_speed(speed)
    time.sleep(t)
    MC_B.set_speed(speed)
    
            
MC_L = MotorController('LEFT')
MC_R = MotorController('RIGHT')
MC_T = MotorController('TOP')
MC_B = MotorController('BOTTOM')

MC_L.set_speed(0.0)
MC_R.set_speed(0.0)
MC_T.set_speed(0.0)
MC_B.set_speed(0.0)


# def set_speeds(s_left, s_right = s_left):
#     MC_L.set_speed(s_left)
#     MC_R.set_speed(s_right)


