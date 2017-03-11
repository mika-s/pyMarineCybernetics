# -*- coding: utf-8 -*-
"""Unit tests for the thruster functions."""

import unittest
from pymarcyb.util.thrusters import power_to_force as p2f
from pymarcyb.util.enumerations import ThrusterType


class TestThrusterMethods(unittest.TestCase):
    """Unit test class for the thruster methods."""

    def setUp(self):
        """Setting up for the test."""

        self.max_force_tunnel_imca, self.min_force_tunnel_imca = \
            p2f.imca_p2f(ThrusterType.tunnel, 880.0, 880.0)

        self.max_force_azimuth_imca, self.min_force_azimuth_imca = \
            p2f.imca_p2f(ThrusterType.azimuth, 2200.0, 2200.0)

        self.max_force_propeller_imca, self.min_force_propeller_imca = \
            p2f.imca_p2f(ThrusterType.propeller, 5000.0, 5000.0)

    def test_tunnel_thruster_pos_imca(self):
        """Unit test for imca_p2f(...), for a tunnel thruster.
        Checking positive force.
        """

        self.assertAlmostEqual(self.max_force_tunnel_imca, 129.46, 2)

    def test_tunnel_thruster_neg_imca(self):
        """Unit test for imca_p2f(...), for a tunnel thruster.
        Checking negative force.
        """

        self.assertAlmostEqual(self.min_force_tunnel_imca, -129.46, 2)

    def test_azimuth_thruster_pos_imca(self):
        """Unit test for imca_p2f(...), for an azimuth thruster.
        Checking positive force.
        """

        self.assertAlmostEqual(self.max_force_azimuth_imca, 382.50, 2)

    def test_azimuth_thruster_neg_imca(self):
        """Unit test for imca_p2f(...), for an azimuth thruster.
        Checking negative force.
        """

        self.assertAlmostEqual(self.min_force_azimuth_imca, -235.39, 2)

    def test_prop_thruster_pos_imca(self):
        """Unit test for imca_p2f(...), for a main propeller.
        Checking positive force.
        """

        self.assertAlmostEqual(self.max_force_propeller_imca, 869.32, 2)

    def test_prop_thruster_neg_imca(self):
        """Unit test for imca_p2f(...), for a main propeller.
        Checking negative force.
        """

        self.assertAlmostEqual(self.min_force_propeller_imca, -608.52, 2)

if __name__ == '__main__':
    unittest.main()
