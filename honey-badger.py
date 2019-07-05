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
import os
import clr
import json
import argparse
import string


def main(badger_file, editable, install):
    # temporary create the helloworld dll adding the honey-badger.json to it
    with open(badger_file, 'r') as bf:
        badger_config = json.load(bf)

    badger_dir = os.path.abspath(os.path.dirname(badger_file))
    build_dir = os.path.join(badger_dir, '_build')
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    with open(os.path.join(os.path.dirname(__file__), 'template.pyt'), 'r') as template:
        s = string.Template(template.read())
    with open(os.path.join(build_dir, '__honey_badger_main__.py'), 'w') as hb_main:
        hb_main.write(s.substitute(badger_config=badger_config))

    clr.CompileModules(os.path.join(build_dir, '{}.ghpy'.format(badger_config['name'])),
                       os.path.join(build_dir, '__honey_badger_main__.py'),
                       *[os.path.join(badger_dir, f) for f in badger_config['include-files']])
    print('done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="honey-badger - make for .ghpy")
    parser.add_argument('-e', '--editable', action="store_true", default=False)
    parser.add_argument('-i', '--install', action="store_true", default=False)
    parser.add_argument('file', action="store")
    args = parser.parse_args(sys.argv[1:])
    main(badger_file=args.file, editable=args.editable, install=args.install)
