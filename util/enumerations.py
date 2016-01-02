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
