# -*- coding: utf-8 -*-
"""Functions related to wind spectras."""

from math import log, sqrt
import numpy as np


def davenport(U_10, kappa=0.0025, L=1200, step_size=0.001):
    """Returns a list representing the entire Davenport wind gust spectrum,
    for a given kappa (surface drag coefficient), L (scale length) and U_10.

    From Davenport (1961).

    Args:
        U_10 (float)                 -- mean wind speed at 10 m altitude [m/s]
        kappa (float)                -- surface drag coefficient [-]
        L (float)                    -- scale length [m]
        step_size (float)            -- determines the resolution of the spectrum

    Returns:
        frequencies (list of floats) -- the frequencies [Hz]
        spectrum (list of floats)    -- the entire Davenport wind spectrum
    """

    spectrum = []
    frequencies = np.arange(0.0, 1.0, step_size)

    for frequency in frequencies:
        chi = frequency * L / U_10
        spectrum.append((4 * kappa * L * U_10 * chi) / (1 + chi**2)**(4.0/3.0))

    return frequencies, spectrum


def harris(U_10, kappa=0.0025, L=1800, step_size=0.001):
    """Returns a list representing the entire Harris wind gust spectrum,
    for a given kappa (surface drag coefficient), L (scale length) and U_10.

    Should not be used for frequencies below 10^-2.
    "DNV" spectrum.

    From Harris (1983).

    Args:
        U_10 (float)                 -- mean wind speed at 10 m altitude [m/s]
        kappa (float)                -- surface drag coefficient [-]
        L (float)                    -- scale length [m]
        step_size (float)            -- determines the resolution of the spectrum

    Returns:
        frequencies (list of floats) -- the frequencies [Hz]
        spectrum (list of floats)    -- the entire Harris wind spectrum
    """

    spectrum = []
    frequencies = np.arange(0.0, 1.0, step_size)

    for frequency in frequencies:
        chi = frequency * L / U_10
        spectrum.append((4 * kappa * L * U_10) / (2 + chi**2)**(5.0/6.0))

    return frequencies, spectrum


def ochi_shin(U_10, C_10=0.025, step_size=0.001):
    """Returns a list representing the entire Ochi-Shin wind gust spectrum,
    for a given C_10 (surface drag coefficient) and U_10.

    From Ochi-Shin (1988).

    Args:
        C_10 (float)                 -- surface drag coefficient at altitude 10 m [-]


    Returns:
        frequencies (list of floats) -- the frequencies
        spectrum (list of floats)    -- the entire Ochi-Shin wind spectrum
    """

    spectrum_dimensional = []
    spectrum_nondimensional = []
    frequencies = []                            # dimensional frequencies at altitude 10 m
    f_stars = np.arange(0.001, 1, step_size)    # non-dimensional frequencies


    for f_star in f_stars:
        if f_star <= 0.003:
            nondimensional = 583 * f_star
        elif f_star > 0.003 and f_star <= 0.1:
            nondimensional = (420 * f_star**0.70) / (1 + f_star**0.35)**11.5
        else:
            nondimensional = (838 * f_star) / (1 + f_star**0.35)**11.5

        spectrum_nondimensional.append(nondimensional)
        frequency = U_10 * f_star
        frequencies.append(frequency)
        u_star = sqrt(C_10) * U_10
        spectrum_dimensional.append(nondimensional * u_star**2 / frequency)

    #return f_stars, spectrum_nondimensional
    return frequencies, spectrum_dimensional


def npd(U_10, step_size=0.001):
    """Returns a list representing the entire NPD wind gust spectrum,
    for a given U_10.

    NPD = Norwegian Petroleum Directorate

    Args:
        U_10 (float)                 -- mean wind speed at 10 m altitude [m/s]
        step_size (float)            -- determines the resolution of the spectrum

    Returns:
        frequencies (list of floats) -- the frequencies [Hz]
        spectrum (list of floats)    -- the entire NPD wind spectrum
    """

    n = 0.468

    spectrum = []
    frequencies = np.arange(0.0, 1.0, step_size)

    for frequency in frequencies:
        f_bar = 172.0 * frequency * (U_10/10.0)**-0.75
        spectrum.append((320.0 * (U_10/10.0)**2) / (1 + f_bar**n)**(5/(3*n)))

    return frequencies, spectrum


def api(U_10, C=0.025, step_size=0.001):
    """Returns a list representing the entire API wind gust spectrum,
    for a given C (surface drag coefficient) and U_10.


    API = American Petroleum Institute

    Args:
        U_10 (float)                 -- mean wind speed at 10 m altitude [m/s]
        C                            -- spectrum parameter, between 0.01 and 0.1 [-]
        step_size (float)            -- determines the resolution of the spectrum

    Returns:
        frequencies (list of floats) -- the frequencies [Hz]
        spectrum (list of floats)    -- the entire API wind spectrum
    """

    omega = 0.15 * U_10 * 0.5**-0.125
    f_p = C * 0.1 * U_10

    spectrum = []
    frequencies = np.arange(0.0, 1.0, step_size)

    for frequency in frequencies:
        spectrum.append((omega**2 / f_p) / (1 + 1.5 * (frequency/f_p)**(5.0/3.0)))

    return frequencies, spectrum


def U10_to_Uz(U_10, C_10, z):
    """Returns the mean wind speed at height z given the mean wind speed
    at 10 m (U_10).

    Args:
        U_10 (float)                 -- mean wind speed at 10 m altitude [m/s]
        C_10 (float)                 -- surface drag coefficient at altitude 10 m [-]
        z (float)                    -- the altitude to calculate mean wind speed for

    Returns:
        U_z (float)                  -- mean wind speed at altitude z (m)
    """

    u_star = sqrt(C_10 * U_10)
    U_z = U_10 + 2.5 * u_star * log(z/10.0)
    return U_z
