"""Helper functions for server.py"""

import geocoder


def get_distance_per_hour(distance, duration_in_minutes):
    """Calculates distance per hour, rounded to two decimals"""

    return ((distance/duration_in_minutes) * 60)


def get_lat_long(string_location):
    """Returns array of lat, longitude for a given location"""

    return geocoder.google(string_location)
