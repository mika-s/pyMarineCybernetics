# -*- coding: utf-8 -*-
"""Functions related to power to force conversion."""

from pyMarineCybernetics.util.thrusters import power_to_force as p2f
from pyMarineCybernetics.util.enumerations import ThrusterType


def main():
    """The main function. Used to test the other functions."""

    # IMCA
    print("IMCA power-to-force:\n")

    max_force, min_force = p2f.imca_p2f(ThrusterType.tunnel, 880.0, 880.0)
    print("Max force: {0:.2f} kN\t Min force: {1:.2f} kN".format(max_force, min_force))

    max_force, min_force = p2f.imca_p2f(ThrusterType.azimuth, 2200.0, 2200.0)
    print("Max force: {0:.2f} kN\t Min force: {1:.2f} kN".format(max_force, min_force))

    max_force, min_force = p2f.imca_p2f(ThrusterType.propeller, 5000.0, 5000.0)
    print("Max force: {0:.2f} kN\t Min force: {1:.2f} kN".format(max_force, min_force))

    print("\n")

    # ABS
    print("ABS power-to-force:\n")

    max_force, min_force = p2f.abs_p2f(880.0, 880.0, 2.0)
    print("Max force: {0:.2f} kN\t Min force: {1:.2f} kN".format(max_force, min_force))

    max_force, min_force = p2f.abs_p2f(2200.0, 2200.0, 3.2)
    print("Max force: {0:.2f} kN\t Min force: {1:.2f} kN".format(max_force, min_force))

    max_force, min_force = p2f.abs_p2f(5000.0, 5000.0, 4.2)
    print("Max force: {0:.2f} kN\t Min force: {1:.2f} kN".format(max_force, min_force))

    print("\n")


if __name__ == "__main__":
    main()
