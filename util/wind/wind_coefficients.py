# -*- coding: utf-8 -*-
"""Functions related to wind coefficients."""

from math import fabs, pi, radians, degrees
import numpy as np


def blendermann(vessel_type, frontal_area, lateral_area, Loa, s_L, angle_of_attack):
    """Return the wind coefficients in surge, sway and yaw, calculated
    using Blendermann's method (from 1994).

    Args:
        vessel_type (string)          -- vessel type to use with Blendermann
        frontal_area (float)          -- frontal area of the vessel in m^2
        lateral_area (float)          -- lateral area of the vessel in m^2
        Loa (float)                   -- length over all in m
        s_L (float)                   -- centroid of the wind area in the lateral direction, ahead of Lpp/2, in m
        angle_of_attack (float)       -- wind angle of attack relative to the bow in radians

    Returns:
        C_X (float)                   -- wind coefficient in surge
        C_Y (float)                   -- wind coefficient in sway
        C_N (float)                   -- wind coefficient in yaw
    """

    # Blendermann coefficients.

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

    # Find the coefficients matching our vessel type.
    for row in coefficient_table:
        if row[0] == vessel_type:
            CDt, CDl_0, CDl_pi, delta, kappa = row[1], row[2], row[3], row[4], row[5]
            break

    # Check if heads or tails wind.
    if fabs(angle_of_attack) <= pi / 2:
        CDl = CDl_0 * (frontal_area / lateral_area)
    else:
        CDl = CDl_pi * (frontal_area / lateral_area)

    denominator = 1 - 0.5 * delta * (1 - CDl / CDt) * np.sin(2 * angle_of_attack)**2

    # Calculate the coefficients.
    C_X = -CDl * (lateral_area / frontal_area) * np.cos(angle_of_attack) / denominator
    C_Y = -CDt * np.sin(angle_of_attack) / denominator
    C_K = kappa * C_Y   # Not used for anything here. From Fossen [2011].
    C_N = (s_L / Loa - 0.18 * (angle_of_attack - pi/2)) * C_Y

    return C_X, C_Y, C_N


def isherwood(frontal_area, lateral_area, superstructure_area, Loa, breadth, S, s_L, masts, angle_of_attack):
    """Return the wind coefficients in surge, sway and yaw, calculated
    using Isherwood's method (from 1972).

    For merchant vessels.

    Args:
        frontal_area (float)        -- frontal area of the vessel in m^2
        lateral_area (float)        -- lateral area of the vessel in m^2
        superstructure_area (float) -- lateral area of the superstructure in m^2
        Loa (float)                 -- length over all in m
        breadth (float)             -- breadth in m
        S (float)                   -- length of the lateral projection
        s_L (float)                 -- centroid of the wind area in the lateral direction, ahead of Lpp/2, in m
        masts (int)                 -- number of distinct groups of masts or king posts
        angle_of_attack (float)     -- wind angle of attack relative to the bow in radians

    Returns:
        C_X (float)                 -- wind coefficient in surge
        C_Y (float)                 -- wind coefficient in sway
        C_N (float)                 -- wind coefficient in yaw
    """

    # Isherwood coefficients.

        # angle    A_0     A_1       A_2      A_3      A_4      A_5     A_6
    surge_coefficients = np.array( \
        [[ 0.0,  2.1520, -5.000,   0.2430, -0.1640,  0.0000,   0.000,  0.000], \
        [ 10.0,  1.7140, -3.330,   0.1450, -0.1210,  0.0000,   0.000,  0.000], \
        [ 20.0,  1.8180, -3.970,   0.2110, -0.1430,  0.0000,   0.000,  0.033], \
        [ 30.0,  1.9650, -4.810,   0.2430, -0.1540,  0.0000,   0.000,  0.041], \
        [ 40.0,  2.3330, -5.990,   0.2470, -0.1900,  0.0000,   0.000,  0.042], \
        [ 50.0,  1.7260, -6.540,   0.1890, -0.1730,  0.3480,   0.000,  0.048], \
        [ 60.0,  0.9130, -4.680,   0.0000, -0.1040,  0.4820,   0.000,  0.052], \
        [ 70.0,  0.4570, -2.880,   0.0000, -0.0680,  0.3460,   0.000,  0.043], \
        [ 80.0,  0.3410, -0.910,   0.0000, -0.0310,  0.0000,   0.000,  0.032], \
        [ 90.0,  0.3550,  0.000,   0.0000,  0.0000, -0.2470,   0.000,  0.018], \
        [100.0,  0.6010,  0.000,   0.0000,  0.0000, -0.3720,   0.000, -0.020], \
        [110.0,  0.6510,  1.290,   0.0000,  0.0000, -0.5820,   0.000, -0.031], \
        [120.0,  0.5640,  2.540,   0.0000,  0.0000, -0.7480,   0.000, -0.024], \
        [130.0, -0.1420,  3.580,   0.0000,  0.0470, -0.7000,   0.000, -0.028], \
        [140.0, -0.6770,  3.640,   0.0000,  0.0690, -0.5290,   0.000, -0.032], \
        [150.0, -0.7230,  3.140,   0.0000,  0.0640, -0.4750,   0.000, -0.032], \
        [160.0, -2.1480,  2.560,   0.0000,  0.0810,  0.0000,   1.270, -0.027], \
        [170.0, -2.7070,  3.970,  -0.1750,  0.1260,  0.0000,   1.810,  0.000], \
        [180.0, -2.5290,  3.760,  -0.1740,  0.1280,  0.0000,   1.550,  0.000]])

        # angle    B_0     B_1       B_2      B_3      B_4      B_5     B_6
    sway_coefficients = np.array( \
        [[ 0.0,  0.0000,  0.000,   0.0000,  0.0000,  0.0000,   0.000,  0.000], \
        [ 10.0,  0.0960,  0.220,   0.0000,  0.0000,  0.0000,   0.000,  0.000], \
        [ 20.0,  0.1760,  0.710,   0.0000,  0.0000,  0.0000,   0.000,  0.000], \
        [ 30.0,  0.2250,  1.380,   0.0000,  0.0230,  0.0000,  -0.290,  0.000], \
        [ 40.0,  0.3290,  1.820,   0.0000,  0.0430,  0.0000,  -0.590,  0.000], \
        [ 50.0,  1.1640,  1.260,   0.1210,  0.0000, -0.2420,  -0.950,  0.000], \
        [ 60.0,  1.1630,  0.960,   0.1010,  0.0000, -0.1770,  -0.880,  0.000], \
        [ 70.0,  0.9160,  0.530,   0.0690,  0.0000,  0.0000,  -0.650,  0.000], \
        [ 80.0,  0.8440,  0.550,   0.0820,  0.0000,  0.0000,  -0.540,  0.000], \
        [ 90.0,  0.8890,  0.000,   0.1380,  0.0000,  0.0000,  -0.660,  0.000], \
        [100.0,  0.7990,  0.000,   0.1550,  0.0000,  0.0000,  -0.550,  0.000], \
        [110.0,  0.7970,  0.000,   0.1510,  0.0000,  0.0000,  -0.550,  0.000], \
        [120.0,  0.9960,  0.000,   0.1840,  0.0000, -0.2120,  -0.660,  0.340], \
        [130.0,  1.0140,  0.000,   0.1910,  0.0000, -0.2800,  -0.690,  0.440], \
        [140.0,  0.7840,  0.000,   0.1660,  0.0000, -0.2090,  -0.530,  0.380], \
        [150.0,  0.5360,  0.000,   0.1760, -0.0290, -0.1630,   0.000,  0.270], \
        [160.0,  0.2510,  0.000,   0.1060, -0.0220,  0.0000,   0.000,  0.000], \
        [170.0,  0.1250,  0.000,   0.0460, -0.0120,  0.0000,   0.000,  0.000], \
        [180.0,  0.0000,  0.000,   0.0000,  0.0000,  0.0000,   0.000,  0.000]])

        # angle    C_0     C_1       C_2      C_3      C_4      C_5
    yaw_coefficients = np.array( \
        [[ 0.0,  0.0000,  0.000,   0.0000,  0.0000,  0.0000,   0.000], \
        [ 10.0,  0.0596,  0.061,   0.0000,  0.0000,  0.0000,  -0.074], \
        [ 20.0,  0.1106,  0.204,   0.0000,  0.0000,  0.0000,  -0.170], \
        [ 30.0,  0.2258,  0.245,   0.0000,  0.0000,  0.0000,  -0.380], \
        [ 40.0,  0.2017,  0.457,   0.0000,  0.0067,  0.0000,  -0.472], \
        [ 50.0,  0.1759,  0.573,   0.0000,  0.0118,  0.0000,  -0.523], \
        [ 60.0,  0.1925,  0.480,   0.0000,  0.0115,  0.0000,  -0.546], \
        [ 70.0,  0.2133,  0.315,   0.0000,  0.0081,  0.0000,  -0.526], \
        [ 80.0,  0.1827,  0.254,   0.0000,  0.0053,  0.0000,  -0.443], \
        [ 90.0,  0.2627,  0.000,   0.0000,  0.0000,  0.0000,  -0.508], \
        [100.0,  0.2102,  0.000,  -0.0195,  0.0000,  0.0335,  -0.492], \
        [110.0,  0.1567,  0.000,  -0.0258,  0.0000,  0.0497,  -0.457], \
        [120.0,  0.0801,  0.000,  -0.0311,  0.0000,  0.0740,  -0.396], \
        [130.0, -0.0189,  0.000,  -0.0488,  0.0101,  0.1128,  -0.420], \
        [140.0,  0.0256,  0.000,  -0.0422,  0.0100,  0.0889,  -0.463], \
        [150.0,  0.0552,  0.000,  -0.0381,  0.0109,  0.0689,  -0.476], \
        [160.0,  0.0881,  0.000,  -0.0306,  0.0091,  0.0366,  -0.415], \
        [170.0,  0.0851,  0.000,  -0.0122,  0.0025,  0.0000,  -0.220], \
        [180.0,  0.0000,  0.000,   0.0000,  0.0000,  0.0000,   0.000]])

    # Isherwood's coefficients are in degrees, so convert the angle of attack.
    angle_of_attack = degrees(angle_of_attack)

    # Interpolate the coefficients to match the correct angle of attack.
    A, B, C = [], [], []
    for i in np.arange(1, 8):
        A.append(np.interp(angle_of_attack, surge_coefficients[:,0], surge_coefficients[:,i]))
        B.append(np.interp(angle_of_attack, sway_coefficients[:,0], sway_coefficients[:,i]))

        # Only 5 coefficients in yaw.
        if i < 7:
            C.append(np.interp(angle_of_attack, yaw_coefficients[:,0], yaw_coefficients[:,i]))

    # Convert from s_L (distance of centroid of lateral area, ahead of Lpp/2) to the distance
    # from bow to the centroid of lateral projection.
    bow_centroid_distance = Loa / 2 - s_L

    # Calculate the wind coefficients .
    C_X = -(A[0] + \
            A[1] * ((2 * lateral_area) / Loa**2) + \
            A[2] * ((2 * frontal_area) / breadth**2) + \
            A[3] * (Loa / breadth) + \
            A[4] * (S / Loa) + \
            A[5] * (bow_centroid_distance / Loa) + \
            A[6] * masts)

    C_Y = -(B[0] + \
            B[1] * ((2 * lateral_area) / Loa**2) + \
            B[2] * ((2 * frontal_area) / breadth**2) + \
            B[3] * (Loa / breadth) + B[4] * (S / Loa) + \
            B[5] * (bow_centroid_distance / Loa) + \
            B[6] * (superstructure_area / lateral_area))

    C_N = C[0] + \
          C[1] * ((2 * lateral_area) / Loa**2) + \
          C[2] * ((2 * frontal_area) / breadth**2) + \
          C[3] * (Loa / breadth) + \
          C[4] * (S / Loa) + \
          C[5] * (bow_centroid_distance / Loa)


    return C_X, C_Y, C_N
