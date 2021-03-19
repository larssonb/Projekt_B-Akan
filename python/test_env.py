# -*- coding: utf-8 -*-

import logging


class GPIO:
    OUT = None
    BCM = None

    @classmethod
    def setmode(cls, mode: any):
        pass

    @classmethod
    def setup(cls, pin: int, io: any):
        pass

    @classmethod
    def output(cls, pin: int, value: int):
        pass


SCL = None
SDA = None


class busio:
    @classmethod
    def I2C(cls, SCL: SCL, SDA: SDA):
        return None


class Channel:
    def __init__(self):
        self.duty_cycle = 0

    @property
    def duty_cycle(self):
        return self.__duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, var):
        self.__duty_cycle = var
        # logging.debug(f'{var}')


class PCA9685:
    def __init__(self, i2c_bus: any) -> None:
        self.frequency = 0
        self.channels = [Channel() for _ in range(16)]
