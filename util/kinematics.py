# -*- coding: utf-8 -*-
"""Functions related to kinematics."""

from math import fabs, pi
import numpy as np


def rotate_NED_to_BODY(coords_NED):
    """Rotate from NED to BODY (surge, sway, yaw).

    Assumes small roll and pitch angle.

    Args:
        coords_NED (np.matrix)	-- the coordinates in NED
                                   phi in radians

    Returns:
        coords_BODY (np.matrix)	-- the coordinates in BODY
    """

    phi = coords_NED[2]
    rotation_matrix = np.matrix([[np.cos(phi), -np.sin(phi), 0],
                                 [np.sin(phi),  np.cos(phi), 0],
                                 [          0,            0, 1]])

    coords_BODY = rotation_matrix * coords_NED

    return coords_BODY


def transform_to_pipi(input_angle):
    """Transforms an angle to the interval -pi -> pi radians.

    Args:
        input_angle     -- the input angle in radians

    Returns:
        output_angle    -- the output angle in radians
    """

    output_angle = (input_angle + np.sign(input_angle) * pi) % (2*pi) - \
        (np.sign(np.sign(input_angle) + \
        2 * (np.sign(fabs(((input_angle + pi) % (2*pi))/(2*pi))) - 1))) * pi;

    return output_angle
