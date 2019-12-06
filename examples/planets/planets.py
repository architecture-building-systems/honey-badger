"""
The data is from here: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

Pretty print the output of PlanetValueList
"""
from __future__ import print_function


def show_planet(planet):
    return "\n".join("{key}: {value}".format(key=key, value=value)
                     for key, value in planet.items())
