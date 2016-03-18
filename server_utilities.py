"""Helper functions for server.py"""


def get_distance_per_hour(distance, duration_in_minutes):
    """Calculates pace (distance over time) per hour, rounded to two decimals

    distance: a float
    duration: a float
    returns: distance over duration, multiplied by 60


        >>> get_distance_per_hour(1.2, 10)
        '7.20'
    """
    result = (distance/duration_in_minutes) * 60
    return "{0:.2f}".format(result)


# def get_lat_long(string_location):
#     """Returns array of lat, longitude for a given location"""

#     return geocoder.google(string_location)
