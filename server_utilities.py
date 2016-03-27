"""Helper functions for server.py"""

from geocoder import google
from polyline.codec import PolylineCodec


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


def get_lat_long(string_location):
    """Returns array of lat, longitude for a given location"""

    result = google(string_location).latlng
    return result


def decode_polyline(polyline):
    """Returns an array of tuples, corresponding to lat long points on a path

    polyline: encoded polyline string, representing a given set of coordinates

        >>> decode_polyline('u{~vFvyys@fS]')
        [(40.63179, -8.65708), (40.62855, -8.65693)]
    """
    return PolylineCodec().decode(polyline)
