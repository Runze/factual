"""
Utilities and helpers for the driver
"""

def circle(lat, lon, radius):
    """
    Creates an API-ready circle from the given latitude, longitude,
    and radius parameters
    """
    return {'$circle': {'$center': [lat, lon], '$meters': radius}}

def point(lat, lon):
    """
    Creates an API-ready point from the given latitude and longitue.
    """
    return {'$point': [lat, lon]}

try:
    isinstance('', basestring)
    def is_str(obj):
        return isinstance(obj, basestring)
except NameError:
    def is_str(obj):
        return isinstance(obj, str)
