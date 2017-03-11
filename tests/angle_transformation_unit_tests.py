# -*- coding: utf-8 -*-
"""Unit tests for the thruster functions."""

import unittest
from pymarcyb.util.kinematics import angle_transformation as at


class TestAngleTransformationMethods(unittest.TestCase):
    """Unit test class for the angle transformation methods."""

    def test_transform_to_pipi_positive(self):
        """Unit test for transform_to_pipi() with positive angle."""

        input_angle = 4.0
        output_angle, revolutions = at.transform_to_pipi(input_angle)

        self.assertAlmostEqual(output_angle, -2.28, 2)
        self.assertEqual(revolutions, 1)

    def test_transform_to_pipi_negative(self):
        """Unit test for transform_to_pipi() with negative angle."""

        input_angle = -4.0
        output_angle, revolutions = at.transform_to_pipi(input_angle)

        self.assertAlmostEqual(output_angle, 2.28, 2)
        self.assertEqual(revolutions, -1)


if __name__ == '__main__':
    unittest.main()
