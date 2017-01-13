#import modules
import numpy as np
from astropy  import units as u

#Body class definition
class Body:
    """
    Description of class
    """
    #define constructor, arguments mass, radius, temp, age
    def __init__(self, mass, radius, temp, age):
        """
        Description of constructor
        """
        #store the mass, radius, temp, age
        self.m = mass
        self.r = radius
        self.T = temp
        self.age = age

    #define method to work out density
    def calculate_density(self):
        """
        Description of method
        """
        #calcaulte volume = (4/3)*pi*r^3
        self.volume = (4.0/3.0)*np.pi*self.r**3
        #calculate density = mass/volume
        self.density = self.m/self.volume
        #return the density
        return self.density

    #define method to work out spectral radiance and lambda_max
    #argument is frequency
    def spec_radiance(self, nu):
        """
        Description of method
        """
        #define planck's constant h = 6.62606957e-34 m^2 kg s^-1
        h = 6.62606957e-34
        #define speed of light c = 299792458 m s^-1
        c = 299792458
        #define boltzmanns constant k = 1.3806488e-23 m^2 kg s^-2 K^-1
        k = 1.3806488e-23
        #work out spectral radiance
        part1 = (2*h*nu**3)/c**2
        part2 = np.exp((h*nu)/(k*self.T))
        self.I = part1*(1.0/part2)
        #work out lambda_max 2.898e-3/T m
        self.lammax = (2.898e-3)/self.T
        #return spectral radiance and temp
        return self.I, self.lammax

    #define method to set the name of the body
    def set_name(self, name):
        """
        Description of method
        """
        #store name
        self.name = name


#Planet class definition
class Planet(Body):
    """
    Description of class
    """
    #define constructor, arguments mass, radius, temp, age
    def __init__(self, mass, radius, temp, age):
        """
        Description of constructor
        """
        #store the mass, radius, temp, age
        self.m = mass
        self.r = radius
        self.T = temp
        self.age = age
        #add attribute to store whether Planet has satellite (boolean)
        self.has_satellite = False
        #set number of satellites to zero
        self.num_satellites = 0
        #call the convert mass method
        self.convert_mass()

    #define method to add satellite, arguments = another body and orbital radius
    def add_satellite(self, satellite, orbital_radius):
        """
        Description of method
        """
        #
        #store the new body
        self.satellite = satellite
        #store the orbital radius
        self.satellite_radius = orbital_radius
        #call the orbital period method
        self.orbital_period(self)
        #change the has_satellite from False to True
        self.has_satellite = True
        #add one to the number of satellites
        self.num_satellites += 1

    #define method to work out orbital period if we have a satellite
    def orbital_period(self):
        """
        Description of method
        """
        #check if we have satellite using hasattr(self, 'satellite')
        if hasattr(self, 'satellite'):
            #define gravitational constant = 6.67384e-11 m^3 kg^-1 s^-2
            G = 6.67384e-11
            #work out constant of proportionality k = 4*pi^2/GM
            k = (4.0*np.pi**2)/(G*self.M)
            #work out period T^2 = k*r^3
            self.satellite_period = np.sqrt(k*self.satellite_radius**3)

    #define method to convert the planets mass into earth masses and jupiter masses
    def convert_mass(self):
        """
        Description of method
        """
        #define 1 earth mass = 5.97219e24 kg
        one_earth_mass = 5.97219e24
        #define 1 jupiter mass = 1.89813e27 kg
        one_jupiter_mass = 1.89813e27
        #work out the mass in earth masses and store
        self.mass_Me = self.m/one_earth_mass
        #work out the mass in jupiter masses and store
        self.mass_Mj = self.m/one_jupiter_mass


#Star class definition
class Star(Planet):
    """
    Description of class
    """
    #define constructor, arguments mass, radius, temp, age, spt [opitional]
    def __init__(self, mass, radius, temp, age, spt=None):
        """
        Description of constructor
        """
        #store the mass, radius, temp, age
        self.m = mass
        self.r = radius
        self.T = temp
        self.age = age
        #add attribute to store whether Planet has satellite (boolean)
        self.has_satellite = False
        #set number of satellites to zero
        self.num_satellites = 0
        #calculate mass in solar masses
        self.mass_Msun = self.m/one_solar_mass
        #set spectral type if spt is not None
        if spt is not None:
            self.spt = spt


    #define method to work out main sequence lifetime of star
    def calculate_lifetime(self):
        """
        Description of method
        """
        #define 1 solar mass = 1.9891e30 kg
        one_solar_mass = 1.9891e30
        #define the suns lifetime = 10e10 years
        lifetime_sun = 10e10

        #calculate store and return lifetime of the star
        self.lifetime = lifetime_sun*(self.mass_Msun**(-2.5))
        return self.lifetime
