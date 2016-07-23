# -*- coding: utf-8 -*-
"""Functions for testing wind spectrum functions."""

from pymarcyb.util.wind import wind_plot as wp
import numpy as np


def main():
    """The main function. Used to test the other functions."""

    #wp.plot_davenport(U_10=10.0)
    #wp.plot_harris(U_10=10.0)
    wp.plot_ochi_shin(U_10=10.0)
    #wp.plot_npd(U_10=10.0)
    #wp.plot_api(U_10=10.0)


if __name__ == "__main__":
    main()
