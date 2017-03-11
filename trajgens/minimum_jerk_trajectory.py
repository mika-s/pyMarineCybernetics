# -*- coding: utf-8 -*-
"""Minimum jerk trajectory generator."""


def mjtg(current, setpoint, frequency, move_time):
    """Minumum jerk trajectory generator.
    http://www.shadmehrlab.org/book/minimum_jerk/minimumjerk.htm

    Args:
        current (float)     -- the current value
        setpoint (float)    -- the wanted value
        frequency (float)   -- the frequency of the system
        move_time (float)   -- how much time to use to get from
                               current to setpoint

    Returns:
        trajectory (list of floats)             -- a trajectory from current
                                                   to setpoint

        trajectory_derivative (list of floats)  -- the trajectory of the
                                                   derivative
    """

    trajectory = []
    trajectory_derivative = []
    timefreq = int(move_time * frequency)

    for time in range(1, timefreq):
        trajectory.append(
            current + (setpoint - current) *
            (10.0 * (time/timefreq)**3
             - 15.0 * (time/timefreq)**4
             + 6.0 * (time/timefreq)**5))

        trajectory_derivative.append(
            frequency * (setpoint - current) *
            (30.0 * (time)**2.0 * (1.0/timefreq)**3
             - 60.0 * (time)**3.0 * (1.0/timefreq)**4
             + 30.0 * (time)**4.0 * (1.0/timefreq)**5))

    return trajectory, trajectory_derivative
