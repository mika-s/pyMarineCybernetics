# -*- coding: utf-8 -*-
"""Functions related to plotting of wind forces, coefficients and spectras."""

from math import radians
from pymarcyb.util.enumerations import DOF
from pymarcyb.util.wind import wind_forces as wf
from pymarcyb.util.wind import wind_coefficients as wc
from pymarcyb.util.wind import wind_spectrum as ws
import numpy as np
import matplotlib.pyplot as plt


def plot_wind_forces(wind_speed, vessel_heading, frontal_area, lateral_area, Loa,
                     s_L, coeffs, vessel_type=None, superstructure_area=None,
                     breadth=None, S=None, masts=None, plot_surge=True, plot_sway=True,
                     plot_yaw=True, subplots=False):
    """Plot the wind forces between 0 and 180 degrees.

    Args:
        wind_speed (float)              -- wind speed in m/s
        vessel_heading (float)          -- vessel heading in radians
        frontal_area (float)            -- frontal area of the vessel in m^2
        lateral_area (float)            -- lateral area of the vessel in m^2
        Loa (float)                     -- length over all in m
        s_L (float)                     -- centroid of the wind area in the lateral
                                           direction, ahead of Lpp/2, in m
        coeffs (CoefficientType)        -- how to calculate the wind coefficients
        vessel_type (string)            -- vessel type to use with Blendermann (default: None)
        superstructure_area (float)     -- lateral superstructure area in m^2 for use
                                           with Isherwood (default: None)
        breadth (float)                 -- vessel breadth in m (default: None)
        S (float)                       -- length of the lateral projection in m for use
                                           with Isherwood (default: None)
        masts (int)                     -- number of masts or king posts for use with
                                           Isherwood (default: None)
        plot_surge (bool)               -- plot surge forces (default: True)
        plot_sway (bool)                -- plot sway forces (default: True)
        plot_yaw (bool)                 -- plot yaw moment (default: True)
        subplots (bool)                 -- plot subplots if True, everything together if
                                           False (default: False)

    Returns:
        N/A
    """

    # These values in degrees.
    start = 0.0
    stop = 180.0
    step = 0.1

    angles_deg = np.arange(start, stop, step)
    angles_rad = np.arange(radians(start + step), radians(stop), radians(step))

    # Calculate wind forces.

    # First for 0.0 degrees.
    wind_fmom = wf.wind_forces_and_moment(wind_speed, 0.0, frontal_area, lateral_area, Loa, s_L, coeffs=coeffs,
           vessel_type=vessel_type, superstructure_area=superstructure_area, breadth=breadth, S=S, masts=masts,
           vessel_heading=vessel_heading)

    # Then for the remaining angles.
    for wind_direction in angles_rad:
        temp = wf.wind_forces_and_moment(wind_speed, wind_direction, frontal_area, lateral_area, Loa, s_L,
            coeffs=coeffs, vessel_type=vessel_type, superstructure_area=superstructure_area, breadth=breadth, S=S,
            masts=masts, vessel_heading=vessel_heading)
        wind_fmom = np.hstack((wind_fmom, temp))

    # Start plotting.
    number_of_plots = int(plot_surge + plot_sway + plot_yaw)

    if subplots and plot_surge:
        plt.subplot(number_of_plots, 1, int(plot_surge))
        plt.title("Wind force in surge")

    if plot_surge:
        plt.xlim(start, stop)
        plt.plot(angles_deg, wind_fmom[DOF.surge].T, 'b', label="Surge")
        plt.legend()

    if subplots and plot_sway:
        plt.subplot(number_of_plots, 1, int(plot_surge + plot_sway))
        plt.title("Wind force in sway")

    if plot_sway:
        plt.xlim(start, stop)
        plt.plot(angles_deg, wind_fmom[DOF.sway].T, 'r', label="Sway")
        plt.legend()

    if subplots and plot_yaw:
        plt.subplot(number_of_plots, 1, number_of_plots)
        plt.title("Wind moment in yaw")

    if plot_yaw:
        plt.xlim(start, stop)
        plt.plot(angles_deg, wind_fmom[DOF.yaw].T, 'k', label="Yaw")
        plt.legend()

    if subplots:
        plt.title("Wind forces and moment")

    plt.show()


def plot_blendermann(frontal_area, lateral_area, Loa, s_L, vessel_type,
                     plot_surge=True, plot_sway=True, plot_yaw=True,
                     subplots=False):
    """Plot the wind coefficients calculated by Blendermann's formulas.

    Args:
        frontal_area (float)          -- frontal area of the vessel in m^2
        lateral_area (float)          -- lateral area of the vessel in m^2
        Loa (float)                   -- length over all in m
        s_L (float)                   -- centroid of the wind area in the lateral
                                         direction, ahead of Lpp/2, in m
        vessel_type (string)          -- vessel type to use with Blendermann
        plot_surge (bool)             -- plot C_X (default: True)
        plot_sway (bool)              -- plot C_Y (default: True)
        plot_yaw (bool)               -- plot C_N (default: True)
        subplots (bool)               -- plot subplots if True, everything together
                                         if False (default: False)

    Returns:
        N/A
    """

    # These values in degrees.
    start = 0.0
    stop = 180.0
    step = 0.1

    angles_deg = np.arange(start, stop, step)
    angles_rad = np.arange(radians(start), radians(stop), radians(step))

    # Find the coefficients.
    C_Xs, C_Ys, C_Ns = [], [], []
    for angle in angles_rad:
        C_X, C_Y, C_N = wc.blendermann(vessel_type, frontal_area, lateral_area, Loa, s_L, angle)
        C_Xs.append(C_X)
        C_Ys.append(C_Y)
        C_Ns.append(C_N)

    # Start plotting.
    number_of_plots = int(plot_surge + plot_sway + plot_yaw)

    if subplots and plot_surge:
        plt.subplot(number_of_plots, 1, int(plot_surge))
        plt.title("Blendermann coefficient in surge")

    if plot_surge:
        plt.plot(angles_deg, C_Xs, 'b', label="C_X")
        plt.legend()

    if subplots and plot_sway:
        plt.subplot(number_of_plots, 1, int(plot_surge + plot_sway))
        plt.title("Blendermann coefficient in sway")

    if plot_sway:
        plt.plot(angles_deg, C_Ys, 'r', label="C_Y")
        plt.legend()

    if subplots and plot_yaw:
        plt.subplot(number_of_plots, 1, number_of_plots)
        plt.title("Blendermann coefficient in yaw")

    if plot_yaw:
        plt.plot(angles_deg, C_Ns, 'k', label="C_N")
        plt.legend()

    if not subplots:
        plt.title("Blendermann wind coefficients")

    plt.ylim([-1.0, 1.0])
    plt.show()


def plot_isherwood(frontal_area, lateral_area, superstructure_area, Loa,
                   breadth, S, s_L, masts, plot_surge=True,
                   plot_sway=True, plot_yaw=True, subplots=False):
    """Plot the wind coefficients calculated by Isherwood's formulas.

    Args:
        frontal_area (float)          -- frontal area of the vessel in m^2
        lateral_area (float)          -- lateral area of the vessel in m^2
        superstructure_area (float)   -- lateral area of the superstructure in m^2
        Loa (float)                   -- length over all in m
        breadth (float)               -- breadth in m
        S (float)                     -- length of the lateral projection
        s_L (float)                   -- centroid of the wind area in the lateral
                                         direction, ahead of Lpp/2, in m
        masts (int)                   -- number of distinct groups of masts
        plot_surge (bool)             -- plot C_X (default: True)
        plot_sway (bool)              -- plot C_Y (default: True)
        plot_yaw (bool)               -- plot C_N (default: True)
        subplots (bool)               -- plot subplots if True, everything together
                                         if False (default: False)

    Returns:
        N/A
    """

    # These values in degrees.
    start = 0.0
    stop = 180.0
    step = 0.1

    angles_deg = np.arange(start, stop, step)
    angles_rad = np.arange(radians(start), radians(stop), radians(step))

    # Find the coefficients.
    C_Xs, C_Ys, C_Ns = [], [], []
    for angle in angles_rad:
        C_X, C_Y, C_N = wc.isherwood(frontal_area, lateral_area, superstructure_area, Loa, breadth, S, s_L, masts, angle)
        C_Xs.append(C_X)
        C_Ys.append(C_Y)
        C_Ns.append(C_N)

    # Start plotting.
    number_of_plots = int(plot_surge + plot_sway + plot_yaw)

    if subplots and plot_surge:
        plt.subplot(number_of_plots, 1, int(plot_surge))
        plt.title("Isherwood coefficient in surge")

    if plot_surge:
        plt.plot(angles_deg, C_Xs, 'b', label="C_X")
        plt.legend()

    if subplots and plot_sway:
        plt.subplot(number_of_plots, 1, int(plot_surge + plot_sway))
        plt.title("Isherwood coefficient in sway")

    if plot_sway:
        plt.plot(angles_deg, C_Ys, 'r', label="C_Y")
        plt.legend()

    if subplots and plot_yaw:
        plt.subplot(number_of_plots, 1, number_of_plots)
        plt.title("Isherwood coefficient in yaw")

    if plot_yaw:
        plt.plot(angles_deg, C_Ns, 'k', label="C_N")
        plt.legend()

    if not subplots:
        plt.title("Isherwood wind coefficients")

    plt.ylim([-1.0, 1.0])
    plt.show()


def plot_davenport(U_10, kappa=0.0025, L=1200, step_size=0.001):
    """Plot the Davenport wind spectrum.

    Args:
        U_10 (float)        -- mean wind speed at 10 m altitude [m/s]
        step_size (float)   -- determines the resolution of the spectrum

    Returns:
        N/A
    """

    frequencies, spectrum = ws.davenport(U_10, kappa=kappa, L=L, step_size=step_size)
    plt.plot(frequencies, spectrum)
    plt.show()


def plot_harris(U_10, kappa=0.0025, L=1800, step_size=0.001):
    """Plot the Harris wind spectrum.

    Args:
        U_10 (float)        -- mean wind speed at 10 m altitude [m/s]
        kappa (float)       -- surface drag coefficient [-]
        L (float)           -- scale length [m]
        step_size (float)   -- determines the resolution of the spectrum

    Returns:
        N/A
    """

    frequencies, spectrum = ws.harris(U_10, kappa=kappa, L=L, step_size=step_size)
    plt.plot(frequencies, spectrum)
    plt.show()


def plot_ochi_shin(U_10, C_10=0.025, step_size=0.001):
    """Plot the Harris wind spectrum.

    Args:
        U_10 (float)        -- mean wind speed at 10 m altitude [m/s]
        step_size (float)   -- determines the resolution of the spectrum

    Returns:
        N/A
    """

    frequencies, spectrum = ws.ochi_shin(U_10, C_10=C_10, step_size=step_size)
    plt.plot(frequencies, spectrum)
    plt.show()


def plot_npd(U_10, step_size=0.001):
    """Plot the NPD wind spectrum.

    Args:
        U_10 (float)        -- mean wind speed at 10 m altitude [m/s]
        step_size (float)   -- determines the resolution of the spectrum

    Returns:
        N/A
    """

    frequencies, spectrum = ws.npd(U_10, step_size=step_size)
    plt.plot(frequencies, spectrum)
    plt.show()


def plot_api(U_10, C=0.025, step_size=0.001):
    """Plot the API wind spectrum.

    Args:
        U_10 (float)        -- mean wind speed at 10 m altitude [m/s]
        step_size (float)   -- determines the resolution of the spectrum

    Returns:
        N/A
    """

    frequencies, spectrum = ws.api(U_10, C=C, step_size=step_size)
    plt.plot(frequencies, spectrum)
    plt.show()
