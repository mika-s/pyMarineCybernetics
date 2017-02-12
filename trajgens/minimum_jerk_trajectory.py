# -*- coding: utf-8 -*-
"""Minimum jerk trajectory generator."""

import matplotlib.pyplot as plt
import numpy as np


def mjtg(current, setpoint, frequency, time):
    """Minumum jerk trajectory generator.
    http://www.shadmehrlab.org/book/minimum_jerk/minimumjerk.htm

    Args:
        current (float)     -- the current value
        setpoint (float)    -- the wanted value
        frequency (float)   -- the frequency of the system
        time (float)        -- how much time to use to get from
                               current to setpoint

    Returns:
        trajectory (list of floats)  -- a trajectory from current
                                        to setpoint
    """
    
    trajectory = []
    tf = int(time * frequency)
    
    for t in range(1, tf):
        trajectory.append(current + (setpoint - current) * \
            (10.0 * (t/tf)**3 - 15.0 * (t/tf)**4 + 6.0 * (t/tf)**5))

    return trajectory
