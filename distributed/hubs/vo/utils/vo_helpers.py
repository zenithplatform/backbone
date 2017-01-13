from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import funcs

def get_coordinates(right_ascension_value, declination_value):
    c = SkyCoord(right_ascension_value, declination_value, unit=(u.hourangle, u.deg))

    return c

# c.ra.hms = {hms_tuple} hms_tuple(h=5.0, m=55.0, s=10.305300000000273)
    # c.ra.hms[0] = {float64} 5.0
    # c.ra.hms[1] = {float64} 55.0
    # c.ra.hms[2] = {float64} 10.3053
    # c.dec.dms = {dms_tuple} dms_tuple(d=7.0, m=24.0, s=25.430000000002408)
    # c.dec.dms[0] = {float64} 7.0
    # c.dec.dms[1] = {float64} 24.0
    # c.dec.dms[2] = {float64} 25.43

def get_constellation(skycoord_object):
    if skycoord_object:
        return funcs.get_constellation(skycoord_object)

    return 'Unknown'

def get_constellation(right_ascension_value, declination_value):
    skycoord_object = get_coordinates(right_ascension_value, declination_value)

    if skycoord_object:
        return funcs.get_constellation(skycoord_object)

    return 'Unknown'

def get_ra_components(skycoord_object):
    if skycoord_object:
        hms_tuple = skycoord_object.ra.hms
        return hms_tuple

def get_dec_components(skycoord_object):

    if skycoord_object:
        dms_tuple = skycoord_object.dec.dms
        return dms_tuple
