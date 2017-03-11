# -*- coding: utf-8 -*-
"""Functions related to transformation of angles."""

from pymarcyb.util.kinematics import angle_transformation as at


def main():
    """The main function. Used to test the other functions."""

    input_angle = -4.0

    output_angle, revolutions = at.transform_to_pipi(input_angle)

    print("Output angle: {0:.2f}, revolutions: {1}"
          .format(output_angle, revolutions))


if __name__ == "__main__":
    main()
