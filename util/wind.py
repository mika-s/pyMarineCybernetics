# -*- coding: utf-8 -*-
"""Functions related to wind."""

from enumerations import CoefficientType, DirectionType, DOF
from math import fabs, pi, radians, degrees
import numpy as np
import matplotlib.pyplot as plt
from sys import exit


def wind_forces_and_moment(wind_speed, wind_direction, frontal_area, lateral_area,
                           Loa, s_L, coeffs = CoefficientType.blendermann, vessel_type = None,
                           wind_dir_type = DirectionType.going_to, temperature = 20.0,
                           vessel_heading = 0.0, vessel_speed_surge = 0.0, vessel_speed_sway = 0.0):
    """Returns the wind force (surge and sway) and moment (yaw) acting
    on the vessel.

    Args:
        wind_speed (float)                  -- wind speed in m/s
        wind_direction (float)              -- wind direction in radians
        frontal_area (float)                -- frontal area of the vessel in m^2
        lateral_area (float)                -- lateral area of the vessel in m^2
        Loa (float)                         -- length over all in m
        s_L (float)                         -- centroid of the wind area in the lateral
                                               direction, ahead of Lpp/2, in m
        coeffs (CoefficientType)            -- how to determine the wind coefficients
        vessel_type (string)                -- vessel type to use with Blendermann
        wind_dir_type (DirectionType)       -- whether the wind is going to or coming from
        temperature (float)                 -- temperature in degrees C
        vessel_heading (float)              -- vessel heading in radians
        vessel_speed_surge (float)          -- vessel speed in surge in m/s
        vessel_speed_sway (float)           -- vessel speed in sway in m/s

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

    if wind_dir_type is DirectionType.going_to:
        # The wind is going to the angle of attack
        angle_of_attack = -np.arctan2(relative_velocity_sway, relative_velocity_surge)
    else:
        # The wind is coming from the angle of attack
        angle_of_attack = -np.arctan2(relative_velocity_sway, relative_velocity_surge) - pi

    # Calculate coefficients depending on coefficient calculation method
    if coeffs is CoefficientType.blendermann:
        if vessel_type == None:
            print("Vessel type can not be None.\n")
            C_X, C_Y, C_N = 0, 0, 0
        else:
            C_X, C_Y, C_N = blendermann(vessel_type, frontal_area, lateral_area, \
                Loa, s_L, angle_of_attack)

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
        temperature (float)     -- the air temperature in C degrees

    Returns:
        rho_w (float)           -- the density of air in kg/m^3

    """

    rho_w = 3.318 * 10**-12 * temperature**5 + 1.172 * 10**-10 * temperature**4 \
          - 6.845 * 10**-8  * temperature**3 + 1.744 * 10**-5  * temperature**2 \
          - 4.728 * 10**-3  * temperature    + 1.292

    return rho_w


def blendermann(vessel_type, frontal_area, lateral_area, Loa, s_L, angle_of_attack):
    """Returns the wind coefficients in surge, sway and yaw, calculated
    using Blendermann's method.

    Args:
        vessel_type (string)        -- vessel type to use with Blendermann
        frontal_area (float)        -- frontal area of the vessel in m^2
        lateral_area (float)        -- lateral area of the vessel in m^2
        Loa (float)                 -- length over all in m
        s_L (float)                 -- centroid of the wind area in the lateral
                                       direction, ahead of Lpp/2, in m
        angle_of_attack (float)     -- wind angle of attack relative to the bow

    Returns:
        C_X (float)                 -- wind coefficient in surge
        C_Y (float)                 -- wind coefficient in sway
        C_N (float)                 -- wind coefficient in yaw
    """

    #        Type                           CDt     CDl(0)  CDl(pi) delta   kappa
    coefficient_table = \
        [['Car carrier',                    0.95,   0.55,   0.60,   0.80,   1.2], \
        ['Cargo vessel, loaded',            0.85,   0.65,   0.55,   0.40,   1.7], \
        ['Cargo vessel, container on deck', 0.85,   0.55,   0.50,   0.40,   1.4], \
        ['Container ship, loaded',          0.90,   0.55,   0.55,   0.40,   1,4], \
        ['Destroyer',                       0.85,   0.60,   0.65,   0.65,   1.1], \
        ['Diving support vessel',           0.90,   0.60,   0.80,   0.55,   1.7], \
        ['Drilling vessel',                 1.00,   0.85,   0.92,   0.10,   1.7], \
        ['Ferry',                           0.90,   0.45,   0.50,   0.80,   1.1], \
        ['Fishing vessel',                  0.95,   0.70,   0.70,   0.40,   1.1], \
        ['Liquefied natural gas tanker',    0.70,   0.60,   0.65,   0.50,   1.1], \
        ['Offshore supply vessel',          0.90,   0.55,   0.80,   0.55,   1.2], \
        ['Passenger liner',                 0.90,   0.40,   0.40,   0.80,   1.2], \
        ['Research vessel',                 0.85,   0.55,   0.65,   0.60,   1.4], \
        ['Speed boat',                      0.90,   0.55,   0.60,   0.60,   1.1], \
        ['Tanker, loaded',                  0.70,   0.90,   0.55,   0.40,   3.1], \
        ['Tanker, in ballast',              0.70,   0.75,   0.55,   0.40,   2.2], \
        ['Tender',                          0.85,   0.55,   0.55,   0.65,   1.1]]

    for row in coefficient_table:
        if row[0] == vessel_type:
            CDt, CDl_0, CDl_pi, delta, kappa = row[1], row[2], row[3], row[4], row[5]
            break;

    # Check if heads or tails wind.
    if fabs(angle_of_attack) <= pi / 2:
        CDl = CDl_0 * (frontal_area / lateral_area)
    else:
        CDl = CDl_pi * (frontal_area / lateral_area)

    denominator = 1 - 0.5 * delta * (1 - CDl / CDt) * np.sin(2 * angle_of_attack)**2

    C_X = -CDl * (lateral_area / frontal_area) * np.cos(angle_of_attack) / denominator
    C_Y = CDt * np.sin(angle_of_attack) / denominator
    C_K = kappa * C_Y   # Not used for anything. From Fossen [2011].
    C_N = (s_L / Loa - 0.18 * (angle_of_attack - pi/2)) * C_Y

    return C_X, C_Y, C_N


def plot_wind_forces(wind_speed, vessel_heading, frontal_area, lateral_area, Loa,
                     s_L, coeffs, vessel_type, wind_dir_type = DirectionType.going_to,
                     plot_surge = True, plot_sway = True, plot_yaw = True, subplots = False):
    """Plot the wind forces between 0 and 360 degrees.

    Args:
        wind_speed (float)              -- wind speed in m/s
        vessel_heading (float)          -- vessel heading in radians
        frontal_area (float)            -- frontal area of the vessel in m^2
        lateral_area (float)            -- lateral area of the vessel in m^2
        Loa (float)                     -- length over all in m
        s_L (float)                     -- centroid of the wind area in the lateral
                                           direction, ahead of Lpp/2, in m
        coeffs (CoefficientType)        -- how to calculate the wind coefficients
        vessel_type (string)            -- vessel type to use with Blendermann
        wind_dir_type (DirectionType)   -- whether the wind is going to or coming from
        plot_surge (bool)               -- plot surge forces
        plot_sway (bool)                -- plot sway forces
        plot_yaw (bool)                 -- plot yaw moment
        subplots (bool)                 -- plot subplots if True, everything together if False

    Returns:
        N/A
    """

    start = 0.0
    stop = 360.0
    step = 0.1

    wind_fmom = wind_forces_and_moment(wind_speed, 0.0, frontal_area, lateral_area,
        Loa, s_L, vessel_type = vessel_type, wind_dir_type = wind_dir_type,
        vessel_heading = vessel_heading)

    for wind_direction in np.arange(radians(start + step), radians(stop), radians(step)):
        temp = wind_forces_and_moment(wind_speed, wind_direction, frontal_area, lateral_area,
            Loa, s_L, vessel_type = vessel_type, wind_dir_type = wind_dir_type,
            vessel_heading = vessel_heading)
        wind_fmom = np.hstack((wind_fmom, temp))

    if subplots == True and plot_surge == True:
        plt.subplot(int(plot_surge + plot_sway + plot_yaw), 1, int(plot_surge))
        plt.title("Wind force in surge")

    if plot_surge == True:
        plt.xlim(start, stop)
        plt.plot(np.arange(start, stop, step), wind_fmom[DOF.surge].T, 'b', label = "Surge")
        plt.legend()

    if subplots == True and plot_sway == True:
        plt.subplot(int(plot_surge + plot_sway + plot_yaw), 1, int(plot_surge + plot_sway))
        plt.title("Wind force in sway")

    if plot_sway == True:
        plt.xlim(start, stop)
        plt.plot(np.arange(start, stop, step), wind_fmom[DOF.sway].T, 'r', label = "Sway")
        plt.legend()

    if subplots == True and plot_yaw == True:
        plt.subplot(int(plot_surge + plot_sway + plot_yaw), 1, int(plot_surge + plot_sway + plot_yaw))
        plt.title("Wind moment in yaw")

    if plot_yaw == True:
        plt.xlim(start, stop)
        plt.plot(np.arange(start, stop, step), wind_fmom[DOF.yaw].T, 'k', label = "Yaw")
        plt.legend()

    if subplots == False:
        plt.title("Wind forces and moment")

    plt.show()


def plot_blendermann(frontal_area, lateral_area, Loa, s_L, vessel_type,
                     plot_surge = True, plot_sway = True, plot_yaw = True, subplots = False):
    """Plot the wind coefficients calculated by Blendermann's formulas.

    Args:
        frontal_area (float)    -- frontal area of the vessel in m^2
        lateral_area (float)    -- lateral area of the vessel in m^2
        Loa (float)             -- length over all in m
        s_L (float)             -- centroid of the wind area in the lateral
                                   direction, ahead of Lpp/2, in m
        vessel_type (string)    -- vessel type to use with Blendermann
        plot_surge (bool)       -- plot C_X
        plot_sway (bool)        -- plot C_Y
        plot_yaw (bool)         -- plot C_N
        subplots (bool)         -- plot subplots if True, everything together if False

    Returns:
        N/A
    """

    start = 0.0
    stop = 180.0
    step = 0.1

    C_Xs, C_Ys, C_Ns = [], [], []
    for angle in np.arange(radians(start), radians(stop), radians(step)):
        C_X, C_Y, C_N = blendermann(vessel_type, frontal_area, lateral_area, Loa, s_L, angle)
        C_Xs.append(C_X)
        C_Ys.append(C_Y)
        C_Ns.append(C_N)


    if subplots == True and plot_surge == True:
        plt.subplot(int(plot_surge + plot_sway + plot_yaw), 1, int(plot_surge))
        plt.title("Blendermann coefficient in surge")

    if plot_surge == True:
        plt.plot(np.arange(start, stop, step), C_Xs, 'b', label = "C_X")
        plt.legend()

    if subplots == True and plot_sway == True:
        plt.subplot(int(plot_surge + plot_sway + plot_yaw), 1, int(plot_surge + plot_sway))
        plt.title("Blendermann coefficient in sway")

    if plot_sway == True:
        plt.plot(np.arange(start, stop, step), C_Ys, 'r', label = "C_Y")
        plt.legend()

    if subplots == True and plot_yaw == True:
        plt.subplot(int(plot_surge + plot_sway + plot_yaw), 1, int(plot_surge + plot_sway + plot_yaw))
        plt.title("Blendermann coefficient in yaw")

    if plot_yaw == True:
        plt.plot(np.arange(start, stop, step), C_Ns, 'k', label = "C_N")
        plt.legend()

    if subplots == False:
        plt.title("Blendermann wind coefficients")

    plt.show()


def main():
    """The main function. Used to test the other functions."""

    if False:
        plot_wind_forces(wind_speed     = 10.0,
                         vessel_heading = radians(0.0),
                         frontal_area   = 530.0,
                         lateral_area   = 1500.0,
                         Loa            = 107.5,
                         s_L            = 11.5,
                         coeffs         = CoefficientType.blendermann,
                         vessel_type    = "Offshore supply vessel",
                         wind_dir_type  = DirectionType.coming_from,
                         plot_surge     = True,
                         plot_sway      = True,
                         plot_yaw       = False,
                         subplots       = False)

    if True:
        plot_blendermann(frontal_area   = 530.0,
                         lateral_area   = 1500.0,
                         Loa            = 107.5,
                         s_L            = 11.5,
                         vessel_type    = "Offshore supply vessel",
                         plot_surge     = True,
                         plot_sway      = True,
                         plot_yaw       = False,
                         subplots       = False)


if __name__ == "__main__":
    main()
