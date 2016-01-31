# -*- coding: utf-8 -*-
"""Functions for testing the other wind related functions."""

from pyMarineCybernetics.util.wind import wind_plot as wp
from pyMarineCybernetics.util.enumerations import CoefficientType
from math import radians
import numpy as np


def main():
    """The main function. Used to test the other functions."""

    if True:
        wp.plot_wind_forces(wind_speed     = 10.0,
                            vessel_heading = radians(0.0),
                            frontal_area   = 530.0,
                            lateral_area   = 1500.0,
                            Loa            = 107.5,
                            s_L            = 11.5,
                            coeffs         = CoefficientType.blendermann,
                            vessel_type    = "Offshore supply vessel",
                            plot_surge     = True,
                            plot_sway      = True,
                            plot_yaw       = False,
                            subplots       = False)

    if True:
        wp.plot_wind_forces(wind_speed          = 10.0,
                            vessel_heading      = radians(0.0),
                            frontal_area        = 530.0,
                            lateral_area        = 1500.0,
                            Loa                 = 107.5,
                            s_L                 = 11.5,
                            coeffs              = CoefficientType.isherwood,
                            superstructure_area = 1500.0/9.0,
                            breadth             = 35.0,
                            S                   = 107.5,
                            masts               = 1,
                            plot_surge          = True,
                            plot_sway           = True,
                            plot_yaw            = False,
                            subplots            = False)

    if True:
        wp.plot_blendermann(frontal_area   = 530.0,
                            lateral_area   = 1500.0,
                            Loa            = 107.5,
                            s_L            = 11.5,
                            vessel_type    = "Offshore supply vessel",
                            plot_surge     = True,
                            plot_sway      = True,
                            plot_yaw       = False,
                            subplots       = False)

    if True:
        wp.plot_isherwood(frontal_area         = 530.0,
                          lateral_area         = 1500.0,
                          superstructure_area  = 1500.0/9.0,
                          Loa                  = 107.5,
                          breadth              = 35.0,
                          S                    = 107.5,
                          s_L                  = 11.5,
                          masts                = 1,
                          plot_surge           = True,
                          plot_sway            = True,
                          plot_yaw             = False,
                          subplots             = False)


if __name__ == "__main__":
    main()
