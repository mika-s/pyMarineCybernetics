# -*- coding: utf-8 -*-
"""Functions for testing the trajectory generators."""

from pymarcyb.trajgens import minimum_jerk_trajectory as traj
import numpy as np
import matplotlib.pyplot as plt


def minimum_jerk_trajectory_testing():
    """Make a minimum jerk trajectory and plot it."""

    velocity = 1    # deg / sec
    current = 15.0
    setpoint = 27.0
    frequency = 100.0
    time = (setpoint - current) / velocity

    trajectory = traj.mjtg(current, setpoint, frequency, time)

    xaxis = list(range(1, int(time * frequency)))
    
    for i, x in enumerate(xaxis):
        xaxis[i] = xaxis[i] / frequency

    plt.plot(xaxis, trajectory)
    plt.title("Minimum jerk trajectory")
    plt.xlabel("Time [s]")
    plt.ylabel("Angle [deg]")
    plt.show()


def main():
    """For testing all the trajectory generators."""

    minimum_jerk_trajectory_testing()


if __name__ == "__main__":
	main()