"""Helper functions for server.py"""


def get_distance_per_hour(distance, duration_in_minutes):
    """Calculates distance per hour, rounded to two decimals"""

    return ((distance/duration_in_minutes) * 60)
