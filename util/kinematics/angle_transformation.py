# -*- coding: utf-8 -*-
"""Functions related to transformation of angles."""

from math import fabs, pi
import numpy as np


def transform_to_pipi(input_angle):
    """Transforms an angle to the interval -pi -> pi radians.

    Args:
        input_angle     -- the input angle in radians

    Returns:
        output_angle    -- the output angle in radians
    """

    output_angle = (input_angle + np.sign(input_angle) * pi) % (2*pi) - \
        (np.sign(np.sign(input_angle) + \
        2 * (np.sign(fabs(((input_angle + pi) % (2*pi))/(2*pi))) - 1))) * pi

    return output_angle
