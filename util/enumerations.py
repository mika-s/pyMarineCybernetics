# -*- coding: utf-8 -*-
"""Various enumerations."""

from enum import Enum, IntEnum


class CoefficientType(Enum):
    """Calculation type of wind and current coefficients."""

    blendermann = 1
    hughes = 2


class DirectionType(Enum):
    """The direction of the current, wind, etc. can either
    be going to or coming from.

    """

    going_to = 1
    coming_from = 2


class DOF(IntEnum):
    """Degrees of freedom."""

    surge = 0
    sway = 1
    yaw = 2
