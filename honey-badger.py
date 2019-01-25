"""
honey-badger - a build system for Rhino/Grasshopper components written in Python.

USAGE:
------

honey-badger build [-f BADGERFILE] [-e] [-i]

    reads in the BADGERFILE (defaults to "honey-badger.json" in the current directory) and
    compiles it into a single *.ghpy file containing the classes necessary.

    The -e switch makes the tool editable - the python files are not included in the *.ghpy file, instead, the
    component will source it on each run from disk (using reload()). Use this only for developer purposes as the
    path to the scripts are hard-coded into the *.ghpy file.

    The -i switch installes the honey-badger kit after building to the user's Grasshopper Library folder.

honey-badger install [-d .]

    installs a (previously built) honey-badger kit to the user's Grasshopper Library folder.
"""

import clr
import argparse


def main():
    print('hello, world')

if __name__ == '__main__':
    main()