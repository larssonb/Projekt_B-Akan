# -*- coding: utf-8 -*-
"""Define IO-pins, PWM channels and PWM to RPM for each motor."""


from __future__ import annotations


class MotorConfig(object):
    """Motor config with IO-pins, PWM-channel and PWM to RPM transfer function.

    IO-pin A and B is used to control motor direction.
        A=0, B=0 motor is breaking to ground.
        A=1, B=0 motor is operating forward with speed set by PWM signal
        A=0, B=1 motor is operating backward with speed set by PWM signal
        A=1, B=1 motor is breaking to VCC

    Attributes:
        A: IO-pin A used together with IO-pin B for motor direction
        B: IO-pin B used together with IO-pin A for motor direction
        PWM: PWM-channel to control speed
        RPM2PWM: Lookup table for RPM to PWM convertions
    """

    def __init__(self,
                 label: str,
                 A: int,
                 B: int,
                 PWM: float,
                 RPM2PWM: list[tuple[int, float]]
                 ) -> None:
        """Init MotorConfig class."""
        self.label = label
        self.A = A
        self.B = B
        self.PWM = PWM
        self.RPM2PWM = RPM2PWM


_RPM2PWM = [(0, 0.0),
            (540, 0.3),
            (880, 0.4),
            (1290, 0.5),
            (1660, 0.6),
            (2240, 1.0)]

LEFT = MotorConfig('Left', 23, 24, 13, _RPM2PWM)
RIGHT = MotorConfig('Right', 27, 22, 12, _RPM2PWM)
TOP = MotorConfig('Top', 26, 16, 15, _RPM2PWM)
BOTTOM = MotorConfig('Bottom', 6, 5, 14, _RPM2PWM)

BAKAN = [LEFT, RIGHT, TOP, BOTTOM]
