"""
honey-badger - a build system for Rhino/Grasshopper components written in Python.

USAGE:
------

honey-badger [-e] [-i] [-f BADGERFILE]

    reads in the BADGERFILE (defaults to "honey-badger.json" in the current directory) and
    compiles it into a single *.ghpy file containing the classes necessary.

    The -e switch makes the tool editable - the python files are not included in the *.ghpy file, instead, the
    component will source it on each run from disk (using reload()). Use this only for developer purposes as the
    path to the scripts are hard-coded into the *.ghpy file.

    The -i switch installs the honey-badger kit after building to the user's Grasshopper Library folder.
"""

import sys
import os
import clr
import json
import argparse
import string
import shutil
import traceback


def honey_badger_installation_folder():
    """Return the folder where honey-badger is installed / cloned to - we need this to find hblib.py
    The tricky bit is that when compiled to honey-badger.exe, the path to `__file__` is always the current
    directory.
    """
    clr.AddReference("System.Reflection")
    import System.Reflection
    entry_assembly_location = System.Reflection.Assembly.GetEntryAssembly().Location
    if entry_assembly_location.endswith("honey-badger.exe"):
        # compiled version, we're our own entry-assembly
        return os.path.dirname(os.path.normpath(os.path.abspath(entry_assembly_location)))
    else:
        # script version, __file__ actually refers to the proper location
        return os.path.dirname(os.path.normpath(os.path.abspath(__file__)))


def main(badger_file, editable, install):
    try:
        # temporary create the helloworld dll adding the honey-badger.json to it
        with open(badger_file, mode='r') as bf:
            badger_file_contents = bf.read()
            badger_config = json.loads(badger_file_contents)

        badger_config = check_badger_config(badger_config)

        badger_dir = os.path.abspath(os.path.dirname(badger_file))
        build_dir = os.path.join(badger_dir, '_build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        template = string.Template(TEMPLATE)
        hb_main_py = 'honey_badger_{guid}.py'.format(guid=badger_config["id"].replace('-', '_'))
        with open(os.path.join(build_dir, hb_main_py), 'w') as hb_main:
            json_badger_config = json.dumps(badger_config, indent=4)
            assert not "'''" in json_badger_config, "Tripple single quotes not allowed in badger-file!"
            hb_main.write(template.substitute(badger_config=json_badger_config))

        # copy hblib.py to build dir
        src_hblib_py = os.path.join(honey_badger_installation_folder(), 'hblib.py')
        dst_hblib_py = os.path.join(build_dir, 'hblib.py')
        # print("Copying hblib.py from {src} to {dst}".format(src=src_hblib_py, dst=dst_hblib_py))
        shutil.copy(src_hblib_py, dst_hblib_py)

        # compile to .ghpy file
        ghpy_path = os.path.join(build_dir, '{}.ghpy'.format(badger_config['name']))
        clr.CompileModules(ghpy_path,
                           os.path.join(build_dir, hb_main_py),
                           dst_hblib_py,
                           *[os.path.join(badger_dir, f) for f in badger_config['include-files']])

        if install:
            destination = os.path.join(os.path.expandvars("${APPDATA}"), "Grasshopper", "Libraries")
            print('installing {ghpy_name} to {destination}'.format(
                ghpy_name=os.path.basename(ghpy_path), destination=destination))
            shutil.copy(ghpy_path, destination)
        print('done.')
    except:
        print traceback.print_exc()


def check_badger_config(badger_config):
    """
    Make sure the badger file contains all the required info. Fill in default values if they don't exist yet.

    nick-names and defaults for inputs/outputs are added automatically.

    FIXME: this could also be done with some kind of json schema thing. For now, this provides enough info.
    """
    assert "name" in badger_config, "Badger file needs a name"
    assert "description" in badger_config, "Badger file needs a description"
    assert "version" in badger_config, "Badger file needs a version"
    assert "author" in badger_config, "Badger file needs an author"
    assert "id" in badger_config, "Badger file needs an id"
    assert "include-files" in badger_config, "Badger file needs to specify include-files"
    assert "components" in badger_config, "Badger file needs to specify at least one component"
    for component in badger_config["components"]:
        assert "class-name" in component, "Component needs a class name"
        assert "name" in component, "Component needs a name"
        assert "abbreviation" in component, "Component needs an abbreviation"
        assert "description" in component, "Component needs a description"
        assert "category" in component, "Component needs a category"
        assert "subcategory" in component, "Component needs a subcategory"
        assert "id" in component, "Component needs an id"
        assert "main-module" in component, "Component needs a main-module"
        assert "inputs" in component, "Component needs inputs"
        assert "outputs" in component, "Component needs outputs"
        for input in component["inputs"]:
            assert "type" in input, "Input needs a type"
            assert "name" in input, "Input needs a name"
            assert "description" in input, "Input needs a description"
            if not "nick-name" in input:
                input["nick-name"] = input["name"]
            if not "default" in input:
                input["default"] = None
        for output in component["outputs"]:
            assert "type" in output, "Input needs a type"
            assert "name" in output, "Input needs a name"
            assert "description" in output, "Input needs a description"
            if not "nick-name" in output:
                output["nick-name"] = output["name"]
    return badger_config


# This is the code that get's used to create the classes required for GrassHopper Components / Assemblies
TEMPLATE = u"""
import json
import GhPython
import System
import hblib
import Grasshopper

BADGER_CONFIG = json.loads('''${badger_config}''')

for component in BADGER_CONFIG['components']:
    # dynamically create subclasses of ``component`` for each component in the badger file
    globals()[component['class-name']] = type(component['class-name'], (hblib.get_base_class(component),), {})


class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return BADGER_CONFIG['name']

    def get_AssemblyDescription(self):
        return BADGER_CONFIG['description']

    def get_AssemblyVersion(self):
        return BADGER_CONFIG['version']

    def get_AuthorName(self):
        return BADGER_CONFIG['author']

    def get_Id(self):
        return System.Guid(BADGER_CONFIG['id'])

"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="honey-badger - make for .ghpy")
    parser.add_argument('-e', '--editable', action="store_true", default=False)
    parser.add_argument('-i', '--install', action="store_true", default=False)
    parser.add_argument('file', action="store")
    args = parser.parse_args(sys.argv[1:])
    main(badger_file=args.file, editable=args.editable, install=args.install)
