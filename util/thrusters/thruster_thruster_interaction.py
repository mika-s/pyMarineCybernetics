# -*- coding: utf-8 -*-
"""Functions related to thruster-thruster interaction."""


def abs_inline_tandem_condition(x, diameter):
    """Return thrust reduction ratio, t, due to in line tandem condition,
    as defined by ABS.

    Args:
        x (float)           -- distance between the thrusters, in m
        diameter (float)    -- diameter of the thruster in question, in m

    Returns:
        t (float)           -- thrust reduction ratio, unitless

    """

    t = 1 - 0.75**((x/diameter)**(2.0/3.0))

    return t
