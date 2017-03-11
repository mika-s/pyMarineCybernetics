# -*- coding: utf-8 -*-
"""Functions related to transformation of angles."""

from math import fabs, pi
import numpy as np
from pymarcyb.util.math import remainder as r


def transform_to_pipi(input_angle):
    """Transforms an angle to the interval -pi -> pi radians.

    Args:
        input_angle (float)     -- the input angle in radians

    Returns:
        output_angle (float)    -- the output angle in radians
        revolutions (int)       -- number of revolutions
    """

    revolutions = int((input_angle + np.sign(input_angle)*pi) / (2*pi))

    p1 = r.truncated_remainder(input_angle + np.sign(input_angle) * pi, 2*pi)
    p2 = (np.sign(np.sign(input_angle)
          + 2 * (np.sign(fabs((r.truncated_remainder(input_angle + pi, 2*pi))
                              / (2*pi))) - 1))) * pi

    output_angle = p1 - p2

    return output_angle, revolutions
