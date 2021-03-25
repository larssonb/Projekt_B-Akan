#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import config
import numpy as np
from time import sleep
import threading
import logging
from math import copysign

try:
    from board import SCL, SDA
    import busio
    import RPi.GPIO as GPIO
    from adafruit_pca9685 import PCA9685
    TEST_ENV = False
except (ImportError, RuntimeError):
    from test_env import GPIO, busio, SCL, SDA, PCA9685
    TEST_ENV = True

RPM_STEP = 50
STEP_TIME = 0.1


class BAkan(object):
    """docstring for BAkan."""

    def __init__(self,
                 position: tuple(float, float) = (-7.0, 0)):
        """Init BAkan class."""
        GPIO.setmode(GPIO.BCM)

        i2c_bus = busio.I2C(SCL, SDA)
        # Create a simple PCA9685 class instance.
        pca = PCA9685(i2c_bus)
        # Set the PWM frequency in hz.
        pca.frequency = 1526

        self.motors = {}

        for mc in config.BAKAN:
            self.motors[mc.label.lower()] = DCMotor(mc.label, mc.A, mc.B,
                                                    mc.PWM, mc.RPM2PWM, pca)

    def set_all_RPM(self, RPM):
        for label in self.motors:
            self.set_RPM(label, RPM)
            
    def set_RPM(self, label: str, RPM: int) -> None:
        label = label.lower()
        if label in [engine.label.lower() for engine in config.BAKAN]:
            self.motors[label].set_target_RPM(RPM)
        else:
            logging.warning(f'DCEngine \'{label}\' does not exist.')

    def set_speed_all(self, speed):
        for label in self.motors:
            self.set_speed(label, speed)

    def set_speed(self, label: str, speed: float):
        label = label.lower()
        if label in [engine.label.lower() for engine in config.BAKAN]:
            d = 0.15
            RPM = speed * 60 / (d * np.pi)
            self.set_RPM(label, RPM)
        else:
            logging.warning(f'DCEngine \'{label}\' does not exist.')


class DCMotor(object):
    """docstring for DCMotor."""

    def __init__(self,
                 label: str,
                 A: int,
                 B: int,
                 PWM: int,
                 RPM2PWM: list[tuple[int, float]],
                 pca: PCA9685,
                 ) -> None:
        """Init DCMotor class."""
        self.label = label

        # Setup pin A
        GPIO.setup(A, GPIO.OUT)
        self._pin_A = A
        GPIO.output(self._pin_A, 0)

        # Setup pin B
        GPIO.setup(B, GPIO.OUT)
        self._pin_B = B
        GPIO.output(self._pin_B, 0)

        # Setup PWM channel
        self._PWM = pca.channels[PWM]

        # Setup RPM to PWM lookup table
        self._RPM2PWM_lookup = RPM2PWM

        self._current_RPM = 0
        self._target_RPM = 0

        # Setup a thread lock
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def _RPM2PWM(self) -> float:
        xp, fp = zip(*self._RPM2PWM_lookup)
        return np.interp(self._current_RPM, xp, fp)

    def set_target_RPM(self, RPM: int) -> None:
        """Set motor target RPM."""
        if RPM != self._target_RPM:
            self._target_RPM = RPM
            logging.info(f'{self.label} motor - '
                         f'New target speed {self._target_RPM} RPM')
            t = threading.Thread(target=self._update_RPM)
            t.start()

    def _set_RPM(self) -> None:
        self._PWM.duty_cycle = int(self._RPM2PWM()*0xFFFF)

    def _update_RPM(self):
        logging.debug(f'{self.label} motor - Waiting for lock')
        self._lock.acquire()
        logging.debug(f'{self.label} motor - Acquired lock')
        if self._target_RPM == self._current_RPM:
            self._lock.release()
            logging.debug(f'{self.label} motor - Released lock')
            return
        while (self._target_RPM != self._current_RPM
               and not self._stop_event.is_set()):
            logging.debug(f'{self.label} motor - {self._current_RPM} RPM -> '
                          f'{self._target_RPM} RPM')

            if self._current_RPM == 0 and self._target_RPM != 0:
                if self._target_RPM > 0:
                    # Set pin A =1, B = 0
                    GPIO.output(self._pin_A, 1)
                    logging.debug(f'{self.label} motor - A = 1')
                if self._target_RPM < 0:
                    # Set pin A = 0, B = 1
                    GPIO.output(self._pin_B, 1)
                    logging.debug(f'{self.label} motor - B = 1')

            if abs(self._current_RPM) <= RPM_STEP and self._current_RPM != 0:
                # Set pin A, B = 0
                if (self._current_RPM > 0
                        and self._target_RPM < self._current_RPM):
                    # Set pin A =1, B = 0
                    GPIO.output(self._pin_A, 0)
                    logging.debug(f'{self.label} motor - A = 0')
                    self._current_RPM = 0
                elif (self._current_RPM < 0
                        and self._target_RPM > self._current_RPM):
                    # Set pin A = 0, B = 1
                    GPIO.output(self._pin_B, 0)
                    logging.debug(f'{self.label} motor - B = 0')
                    self._current_RPM = 0
            
            if abs(self._target_RPM - self._current_RPM) <= RPM_STEP:
                self._current_RPM = self._target_RPM
            else:
                self._current_RPM += copysign(
                        RPM_STEP, self._target_RPM - self._current_RPM)
            self._set_RPM()
            sleep(STEP_TIME)
            if (not self._stop_event.is_set()
                    and self._target_RPM == self._current_RPM):
                logging.info(f'{self.label} motor @ '
                             f'{self._current_RPM} RPM')

        if self._current_RPM == 0:
            logging.info(f'{self.label} motor - Stopped')

        self._stop_event.clear()
        self._lock.release()
        logging.debug(f'{self.label} motor - Released lock')

    def stop(self) -> None:
        """Stop motor."""
        if self._target_RPM != 0 and self._current_RPM != 0:
            logging.info(f'{self.label} motor - Stopping')
            logging.debug(f'{self.label} motor - Sending stop event')
            self._stop_event.set()
            self._target_RPM = 0
            t = threading.Thread(target=self._update_RPM)
            t.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    bakan = BAkan()
    bakan.set_speed_all(10)
#     bakan.set_all(1500)
#     bakan.set_RPM('top', 0)
#     bakan.set_RPM('bottom', 2000)
