"""
The data is from here: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

This file is the "producer" for the ValueList - it's read at honey-badger compile-time, so it's results need to
be static.
"""
from __future__ import print_function
import csv
import os


def floatify(dict):
    """convert as many values to float"""
    for key in dict.keys():
        try:
           dict[key] = float(dict[key])
        except ValueError:
            pass
    return dict


def show_planet(planet):
    return planet


def main():
    with open(os.path.join(os.path.dirname(__file__), "planets.csv")) as planets:
        reader = csv.DictReader(planets)
        for planet in reader:
            yield planet[reader.fieldnames[0]], floatify(planet)


if __name__ == "__main__":
    # test to make sure the data fits
    import pprint
    pprint.pprint(list(main()))