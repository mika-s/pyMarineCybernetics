# -*- coding: utf-8 -*-
"""Functions for testing wind spectrum functions."""

from pymarcyb.util.enumerations import WindSpectrumType
from pymarcyb.util.wind import wind_plot as wp
from pymarcyb.util.wind import wind_spectrum as ws
import matplotlib.pyplot as plt


def main():
    """The main function. Used to test the other functions."""

    #wp.plot_davenport(U_10=10.0)
    #wp.plot_harris(U_10=10.0)
    #wp.plot_ochi_shin(U_10=10.0)
    #wp.plot_npd(U_10=10.0)
    #wp.plot_api(U_10=5.0)

    dp = ws.WindSpectrum(WindSpectrumType.davenport)
    dp.set_U_10(10.0)
    dp.set_kappa()
    #dp.plot_non_dimensional()
    #dp.plot_dimensional()
    #print(dp)

    ha = ws.WindSpectrum(WindSpectrumType.harris)
    ha.set_U_10(10.0)
    ha.set_kappa()
    #ha.plot_non_dimensional()
    #ha.plot_dimensional()

    #npd = ws.WindSpectrum(WindSpectrumType.npd)
    #npd.set_U_10(10.0)
    #npd.set_kappa()
    #npd.plot_non_dimensional()
    #npd.plot_dimensional()

    api = ws.WindSpectrum(WindSpectrumType.api)
    api.set_U_10(5.0)
    api.set_kappa()
    #api.plot_non_dimensional()
    api.plot_dimensional()

    plt.show()


if __name__ == "__main__":
    main()
