# -*- coding: utf-8 -*-
"""Unit tests for the hydro functions."""

import unittest
from pyMarineCybernetics.util.hydro import coeffs as c


class TestHydroMethods(unittest.TestCase):
    """Unit test class for the hydro methods."""

    def setUp(self):
        """Seting up for the test."""


    def test_cb_extrapolation_upwards(self):
        """Unit test for block coefficient extrapolation, extrapolating upwards"""

        self.assertAlmostEqual(c.cb_extrapolation(0.75, 7.3, 10.0), 0.775, 3)

    def test_cb_extrapolation_downwards(self):
        """Unit test for block coefficient extrapolation, extrapolating upwards"""

        self.assertAlmostEqual(c.cb_extrapolation(0.80, 10.0, 7.3), 0.778, 3)


if __name__ == '__main__':
    unittest.main()
