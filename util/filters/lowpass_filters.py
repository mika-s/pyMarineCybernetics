# -*- coding: utf-8 -*-
"""Functions related to lowpass filtering."""


def lowpass_filter(input_series, time_constant):
    """Lowpass filter a time series. First order.

    Args:
        input_series (list of floats)   -- time series to filter
        time_constant (float)           -- time constant for the filter

    Returns:
        output_series (list of floats)  -- filtered time series
    """

    output_series = []
    output_series.append(input_series[0])

    for current_unfiltered_value in input_series:
        previous_filtered_value = output_series[-1]

        B = 1.0 / time_constant
        A = 1.0 - B

        new_filtered_value = (A * previous_filtered_value
            + B * current_unfiltered_value)

        output_series.append(new_filtered_value)

    return output_series
