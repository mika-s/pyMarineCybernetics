# -*- coding: utf-8 -*-
"""Functions related to waves."""

from math import exp, pi
import numpy as np


def pierson_moskowitz(U_10, calc_alpha = False, alpha = 0.0081, H_s = 0.0, T_0 = 0.0,
                      calc_beta = False, beta = 0.74, step_size = 0.01):
    """Returns a list representing the entire Pierson-Moskowitz wave spectrum,
    for a given alpha, beta and U_10.

    alpha and beta can be calculated from H_s and T_0. Experience values can also
    be used.

    Assumes a fully developed sea, i.e. fetch length and duration are infinite.

    Args:
        U_10 (float)                -- wind velocity at 10 m above sea level
        calc_alpha (bool)           -- whether to calculate alpha or not
        alpha (float)               -- wave spectrum parameter
        H_s (float)                 -- signficant wave height (for calculating
                                       alpha)
        T_0 (float)                 -- zero-cross wave period (for calculating
                                       alpha and beta)
        calc_beta (bool)            -- whether to calculate beta or not
        beta (float)                -- wave spectrum parameter
        step_size (float)           -- determines the resolution of the spectrum

    Returns:
        omegas (list of floats)     -- the circular frequencies
        spectrum (list of floats)   -- the entire PM wave spectrum
    """

    grav = 9.81
    U_195 = 1.026 * U_10     # Assumes a drag coefficient of 1.3 * 10^(-3).
    omega_0 = grav / U_195

    if calc_alpha == True:
        alpha = 4 * pi**3 * (H_s / (grav * T_0**2))**2

    if calc_beta == True:
        beta = 16 * pi**3 * (U_195 / (grav * T_0))**4

    spectrum = []
    omegas = np.arange(0.01, 2.0, step_size)

    for omega in omegas:
        spectrum.append(((alpha * grav**2) / omega**5)
            * exp(-beta * (omega_0 / omega)**4))

    return omegas, spectrum


def jonswap(U_10, fetch_dependent = False, fetch = None, alpha = 0.0081,
            beta = 1.25, gamma = 3.3, omega_p = 0.5, step_size = 0.01):
    """Returns a list representing the entire JONSWAP wave spectrum,
    for a given alpha, beta, gamma, omega_p, fetch length and U_10.

    omega_p and alpha can be calculated from the fetch length. Experience
    values can also be used.

    Args:
        U_10 (float)                -- wind velocity at 10 m above sea level
        fetch_dependent (bool)      -- determines if alpha and omega_p should
                                       be calculated from fetch length
        fetch (float)               -- wave spectrum parameter
        alpha (float)               -- wave spectrum parameter
        beta (float)                -- wave spectrum parameter
        gamma (float)               -- wave spectrum parameter
        omega_p (float)             -- wave spectrum parameter
        step_size (float)           -- determines the resolution of the spectrum

    Returns:
        omegas (list of floats)     -- the circular frequencies
        spectrum (list of floats)   -- the entire JONSWAP wave spectrum
    """

    grav = 9.81

    if (fetch_dependent == True):
        omega_p = (2 * pi * 16.04) / (fetch * U_10)**0.38
        alpha = 0.076 * ((fetch * grav) / U_10**2)**-0.22

    spectrum = []
    omegas = np.arange(0.01, 2.0, step_size)

    for omega in omegas:
        if omega <= omega_p:
            sigma = 0.07
        else:
            sigma = 0.09

        r = exp(-((omega - omega_p)**2) / (2 * sigma**2 * omega_p**2))

        spectrum.append(((alpha * grav**2) / omega**5)
            * exp(-beta * (omega_p / omega)**4)
            * gamma**r)

    return omegas, spectrum
