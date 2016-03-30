# -*- coding: utf-8 -*-
"""Functions related to hydrodynamics."""

from pyMarineCybernetics.util.hydro import coeffs as c


def main():
    """The main function. Used to test the other functions."""

    cb_at_10m = c.cb_extrapolation(0.75, 7.3, 10.0)
    print("Estimated block coefficient at 10.0 m: {0:.3f}\n".format(cb_at_10m))

    fr = c.fineness_ratio(160.0, 34000.0)
    print("Fineness ratio for a vessel with lwl = 160.0 m and displacement of 34000 tons: {0:.2f}".
        format(fr))

    fr = c.fineness_ratio(0.97*68.3, 4800.0)
    print("Fineness ratio for a vessel with lwl = 66.2 m and displacement of 4800 tons: {0:.2f}".
        format(fr))


if __name__ == "__main__":
    main()
