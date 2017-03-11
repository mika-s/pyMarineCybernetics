# -*- coding: utf-8 -*-
"""Functions for testing the trajectory generators."""

from pymarcyb.trajgens import minimum_jerk_trajectory as traj
import matplotlib.pyplot as plt


def minimum_jerk_trajectory_testing():
    """Make a minimum jerk trajectory and plot it."""

    average_velocity = 1.0    # deg / sec
    current = 15.0
    setpoint = 27.0
    frequency = 100.0
    time = (setpoint - current) / average_velocity

    trajectory, trajectory_derivative = \
        traj.mjtg(current, setpoint, frequency, time)

    xaxis = list(range(1, int(time * frequency)))

    for i in range(0, len(xaxis)):
        xaxis[i] = xaxis[i] / frequency

    print("Average velocity: {0}\nMax velocity: {1:.2f}"
          .format(average_velocity, max(trajectory_derivative)))

    plt.figure(1)

    plt.subplot(211)
    plt.title("Minimum jerk trajectory")
    plt.plot(xaxis, trajectory)
    plt.legend(["Position"], loc=2)
    plt.ylabel("Angle [deg]")

    plt.subplot(212)
    plt.plot(xaxis, trajectory_derivative, 'r')
    plt.xlabel("Time [s]")
    plt.ylabel("Angular velocity [deg/s]")
    plt.legend(["Velocity"], loc=2)

    plt.show()


def main():
    """For testing all the trajectory generators."""

    minimum_jerk_trajectory_testing()


if __name__ == "__main__":
    main()
