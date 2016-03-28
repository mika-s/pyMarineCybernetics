# -*- coding: utf-8 -*-
"""Various enumerations."""

from enum import Enum, IntEnum


class CoefficientType(Enum):
    """Calculation type of wind and current coefficients."""

    blendermann = 1
    hughes = 2
    isherwood = 3


class DOF(IntEnum):
    """Degrees of freedom."""

    surge = 0
    sway = 1
    yaw = 2


class ThrusterType(Enum):
    """Type of thruster."""

    tunnel = 1
    azimuth = 2
    propeller = 3
    waterjet = 4
    vsp = 5     # Voith Schneider Propeller
