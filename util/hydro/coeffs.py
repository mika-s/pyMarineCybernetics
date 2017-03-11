# -*- coding: utf-8 -*-
"""Functions related to hydrodynamics."""


def cb_extrapolation(cb_des, d_des, d):
    """Return the block coefficient for a arbitrary draught, given the block
    coefficient and draught for the design draught. Riddlesworth's method.

    Args:
        cb_des (float)        -- block coefficient at design draught, unitless
        d_des (float)         -- design draught, in m
        d (float)             -- draught to find the new block coefficient for

    Returns:
        cb (float)            -- block coefficient for the draught d, unitless
    """

    cb = 1 - (1 - cb_des) * (d_des/d)**(1.0/3.0)

    return cb


def fineness_ratio(lwl, displacement):
    """Return the fineness ratio of a vessel, given the length in the waterline
    and the displacement.

    Args:
        lwl (float)           -- length in the waterline, in m
        displacement (float)  -- metric tons displaced by the vessel

    Returns:
        fitness_ratio (float) -- the fitness ratio of the vessel, unitless
    """

    fitness_ratio = lwl / displacement**(1.0/3.0)

    return fitness_ratio
