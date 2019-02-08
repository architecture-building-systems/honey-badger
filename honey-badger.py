from __future__ import print_function

"""
honey-badger - a build system for Rhino/Grasshopper components written in Python.

USAGE:
------

honey-badger build [-e] [-i] [-f BADGERFILE] 

    reads in the BADGERFILE (defaults to "honey-badger.json" in the current directory) and
    compiles it into a single *.ghpy file containing the classes necessary.

    The -e switch makes the tool editable - the python files are not included in the *.ghpy file, instead, the
    component will source it on each run from disk (using reload()). Use this only for developer purposes as the
    path to the scripts are hard-coded into the *.ghpy file.

    The -i switch installes the honey-badger kit after building to the user's Grasshopper Library folder.
"""

import sys
import clr
import argparse


def main(badger_file, editable, install):
    # temporary create the helloworld dll adding the honey-badger.json to it
    clr.CompileModules('helloworld.p2.7.5.0.ghpy', 'helloworld.py')
    print('done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="honey-badger - make for .ghpy")
    parser.add_argument('-e', '--editable', action="store_true", default=False)
    parser.add_argument('-i', '--install', action="store_true", default=False)
    parser.add_argument('file', action="store")
    args = parser.parse_args(sys.argv[1:])
    main(badger_file=args.file, editable=args.editable, install=args.install)