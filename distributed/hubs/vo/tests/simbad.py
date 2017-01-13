from astroquery.simbad import Simbad
from vo_hub.search_providers.simbad import SimbadSearch

def main():
    query()
    #temp_simbad()

def query():
    ss = SimbadSearch()
    ss.init_configuration()

    ret_val = ss.search_objects("m [1-9]", True)
    #ret_val = ss.search_object('Vega')

    print ret_val

def temp_simbad():
    #Simbad.add_votable_fields("dim_angle")
    Simbad.add_votable_fields("dim_incl")
    #Simbad.add_votable_fields("dim_majaxis")
    #Simbad.add_votable_fields("dim_minaxis")
    #Simbad.add_votable_fields("dim_wavelength")

    result = Simbad.query_object('Vega')
    print result
    #Simbad.add_votable_fields("pos")

    # Simbad.add_votable_fields("sptype")             # Spectral_type     - Spectral type
    # Simbad.add_votable_fields("gen")                # Vmag              - V magnitude
    # Simbad.add_votable_fields("jp11")               # J_1200            - float4 	magnitude at {lambda}eff = 1200 nm 	float 	PHOT.MAG;EM.IR.J
    # Simbad.add_votable_fields("ubv")                # U_B - U-B Color index, B_V - B-V Color index
    # Simbad.add_votable_fields("v*")                 # vartyp - Variable type
    # Simbad.add_votable_fields("orv")               # radvel - Radial velocity
    # #Simbad.add_votable_fields("pm")                 # pmra - Proper motion (RA) (me_pmra -sigma pmra),    pmde - Proper motion (DEC) (me_pmde - sigma pmde)
    #
    # Simbad.add_votable_fields("pmra")
    # Simbad.add_votable_fields("pmdec")
    #
    # Simbad.add_votable_fields("plx")                #plx - Parallax

#def calc_age():
#    one_solar_mass = 1.9891e30
#    m = 0
#    mass_Msun = m/one_solar_mass
#    lifetime_sun = 10e10
#    lifetime = lifetime_sun*(mass_Msun**(-2.5))

if __name__ == "__main__":
    main()