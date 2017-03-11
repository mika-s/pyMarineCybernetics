# -*- coding: utf-8 -*-
"""Functions related to remainder.

% in Python is floored division remainder, which means -5 % 2 = 1, not -1.
Functions for other types of remainder can be found here.
"""


def truncated_remainder(dividend, divisor):
    """Sign is the same as the dividend.

    Args:
        dividend (float)    -- the dividend
        divisor (float)     -- the divisor

    Returns:
        remainder (float)   -- the truncated remainder of the division

    """

    divided_number = dividend / divisor
    divided_number = \
        -int(-divided_number) if divided_number < 0 else int(divided_number)

    remainder = dividend - divisor * divided_number

    return remainder
