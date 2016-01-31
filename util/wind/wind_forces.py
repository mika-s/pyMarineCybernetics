# -*- coding: utf-8 -*-
"""Functions related to wind forces."""

from pyMarineCybernetics.util.enumerations import CoefficientType
from pyMarineCybernetics.util.wind import wind_coefficients as wc
from math import pi
import numpy as np


def wind_forces_and_moment(wind_speed, wind_direction, frontal_area, lateral_area, Loa, s_L, coeffs=
                           CoefficientType.blendermann, vessel_type=None, superstructure_area=None, breadth=None,
                           S=None, masts=None, temperature=20.0, vessel_heading=0.0, vessel_speed_surge=0.0,
                           vessel_speed_sway=0.0):
    """Return the wind force (surge and sway) and moment (yaw) acting
    on the vessel.

    Args:
        wind_speed (float)                  -- wind speed in m/s
        wind_direction (float)              -- wind direction in radians
        frontal_area (float)                -- frontal area of the vessel in m^2
        lateral_area (float)                -- lateral area of the vessel in m^2
        Loa (float)                         -- vessel length over all in m
        s_L (float)                         -- centroid of the wind area in the lateral direction, ahead of Lpp/2, in m
        coeffs (CoefficientType)            -- how to determine the wind coefficients
        vessel_type (string)                -- vessel type to use with Blendermann (default: None)
        superstructure_area (float)         -- lateral superstructure area in m^2 for use with Isherwood (default: None)
        breadth (float)                     -- vessel breadth in m (default: None)
        S (float)                           -- length of the lateral proj. in m for use with Isherwood (default: None)
        masts (int)                         -- number of masts or king posts for use with Isherwood (default: None)
        temperature (float)                 -- temperature in degrees C (default: 20)
        vessel_heading (float)              -- vessel heading in radians (default: 0.0)
        vessel_speed_surge (float)          -- vessel speed in surge in m/s (default: 0.0)
        vessel_speed_sway (float)           -- vessel speed in sway in m/s (default: 0.0)

    Returns:
        wind_forces_and_moment (np.matrix)  -- the wind forces and moment in kN/kNm
    """

    rho_w = calculate_rho_w(temperature)

    # Relative velocities
    wind_speed_surge = wind_speed * np.cos(wind_direction - vessel_heading)
    wind_speed_sway  = wind_speed * np.sin(wind_direction - vessel_heading)
    relative_velocity_surge = vessel_speed_surge - wind_speed_surge
    relative_velocity_sway  = vessel_speed_sway  - wind_speed_sway
    relative_wind_speed = np.sqrt(relative_velocity_surge**2 + relative_velocity_sway**2)

    # The wind is coming from the angle of attack
    angle_of_attack = np.arctan2(relative_velocity_sway, relative_velocity_surge) + pi

    # Calculate coefficients depending on coefficient calculation method
    if coeffs is CoefficientType.blendermann:
        if vessel_type == None:
            print("Please enter the correct parameters for Blendermann.\n")
            C_X, C_Y, C_N = 0, 0, 0
        else:
            C_X, C_Y, C_N = wc.blendermann(vessel_type, frontal_area, lateral_area, Loa, s_L, angle_of_attack)
    elif coeffs is CoefficientType.isherwood:
        if superstructure_area == None or breadth == None or S == None or masts == None:
            print("Please enter the correct parameters for Isherwood.\n")
            C_X, C_Y, C_N = 0, 0, 0
        else:
            C_X, C_Y, C_N = wc.isherwood(frontal_area, lateral_area, superstructure_area, Loa, breadth, S, s_L, masts,
                angle_of_attack)

    q = 0.5 * rho_w * relative_wind_speed**2
    wind_force_surge = 10**-3 * q * C_X * frontal_area
    wind_force_sway  = 10**-3 * q * C_Y * lateral_area
    wind_moment_yaw  = 10**-3 * q * C_N * lateral_area * Loa

    wind_forces_and_moment = np.matrix([[wind_force_surge],
                                        [wind_force_sway],
                                        [wind_moment_yaw]])

    return wind_forces_and_moment


def calculate_rho_w(temperature):
    """ Calculate the density of air from temperature. Polynomial regression
    done on a table of air density vs. temperature values.

    Args:
        temperature (float)     -- the air temperature in degrees C

    Returns:
        rho_w (float)           -- the density of air in kg/m^3

    """

    rho_w = 3.318 * 10**-12 * temperature**5 + 1.172 * 10**-10 * temperature**4 \
          - 6.845 * 10**-8  * temperature**3 + 1.744 * 10**-5  * temperature**2 \
          - 4.728 * 10**-3  * temperature    + 1.292

    return rho_w
