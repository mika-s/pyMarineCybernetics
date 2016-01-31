# -*- coding: utf-8 -*-
"""Functions related to reference frame transformation."""

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
