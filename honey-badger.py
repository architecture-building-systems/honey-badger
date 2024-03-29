"""
honey-badger - a build system for Rhino/Grasshopper components written in Python.

USAGE:
------

honey-badger [-e] [-i] [-v RHINO_VERSION] [-s] [-f BADGERFILE]

    reads in the BADGERFILE (defaults to "honey-badger.json" in the current directory) and
    compiles it into a single *.ghpy file containing the classes necessary.

    The -e switch makes the tool editable - the python files are not included in the *.ghpy file, instead, the
    component will source it on each run from disk (using reload()). Use this only for developer purposes as the
    path to the scripts are hard-coded into the *.ghpy file.

    The -i switch installs the honey-badger kit after building to the user's Grasshopper Library folder.
    
    The -v parameter defines the Rhino version to find / add RhinoCommon and Grasshopper DLLs from.
    
    The -s switch skips a compatibility check to see that IronPython version matches the Rhino version desired (note: Rhino plugins are, for now, forward but not backward compatible!)
"""

import sys
import os
import platform
import clr
import json
import argparse
import string
import shutil
import traceback

clr.AddReference("System")
clr.AddReference("System.IO")
import System
import System.IO

import parameter_compiler

def main(badger_file, editable, install, rhino_version, skip_compatibility_check):
    
    if not skip_compatibility_check:
        # Asserts rhino version is installed and compatible with IronPython used.
        
        rhino_to_ipy_version = {
            '6': ['2.7.8'],
            '7': ['2.7.8', '2.7.9']
        }
        
        ipy_version_actual = '{}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
        ipy_version_allowed = rhino_to_ipy_version[rhino_version]
        # Checks that IronPython is being used
        assert platform.python_implementation() == 'IronPython', "You need to use IronPython to badger your components. Currently using {}".format(platform.python_implementation())
        assert ipy_version_actual in ipy_version_allowed, \
            "IronPython version does not match for Rhino {rhino_version}. Must be {version_target} but was {version_actual}".format(
                rhino_version=rhino_version,
                version_target=' or '.join(ipy_version_allowed),
                version_actual=ipy_version_actual
                )
        
        assert os.path.exists(
            os.path.join(os.path.expandvars("${PROGRAMFILES}"),
                         "Rhino {v}".format(v=rhino_version),
                         "Plug-ins", "Grasshopper", "Grasshopper.dll")), \
            "Could not find Grasshopper.dll. Is Rhino {v} installed?".format(v=rhino_version)
        
        assert os.path.exists(
            os.path.join(os.path.expandvars("${PROGRAMFILES}"),
                         "Rhino {v}".format(v=rhino_version),
                         "System", "RhinoCommon.dll")), \
            "Could not find RhinoCommon.dll. Is Rhino {v} installed?".format(v=rhino_version)
    
    parameter_compiler.setup(rhino_version)
    
    try:
        # temporary create the helloworld dll adding the honey-badger.json to it
        with open(badger_file, mode='r') as bf:
            badger_file_contents = bf.read()
            badger_config = json.loads(badger_file_contents)

        badger_dir = os.path.abspath(os.path.dirname(badger_file))
        build_dir = os.path.join(badger_dir, '_build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        badger_config = check_badger_config(badger_config, badger_dir)

        template = string.Template(TEMPLATE)
        guid = badger_config["id"].replace('-', '_')
        hb_main_py = 'honey_badger_{guid}.py'.format(guid=guid)
        with open(os.path.join(build_dir, hb_main_py), 'w') as hb_main:
            json_badger_config = json.dumps(badger_config, indent=4)
            assert not "'''" in json_badger_config, "Tripple single quotes not allowed in badger-file!"
            json_badger_config = json_badger_config.replace("\\", "\\\\")  # make sure we escape backslashes
            hb_main.write(template.substitute(badger_config=json_badger_config, guid=guid))

        # copy hblib.py to build dir
        src_hblib_py = os.path.join(os.path.dirname(os.path.normpath(os.path.abspath(__file__))), 'hblib.py')
        dst_hblib_py = os.path.join(build_dir, "hblib_{guid}.py".format(guid=guid))
        # print("Copying hblib.py from {src} to {dst}".format(src=src_hblib_py, dst=dst_hblib_py))
        shutil.copy(src_hblib_py, dst_hblib_py)

        # compile to .ghpy file
        ghpy_path = os.path.join(build_dir, "{}.ghpy".format(badger_config['name']))
        clr.CompileModules(ghpy_path,
                           os.path.join(build_dir, hb_main_py),
                           dst_hblib_py,
                           *[os.path.join(badger_dir, f) for f in badger_config['include-files']])

        gha_path = os.path.join(build_dir, "{}.gha".format(badger_config['name']))
        if "parameters" in badger_config:
            parameter_compiler.compile_parameters(
                badger_config, badger_dir, os.path.join(build_dir, gha_path))

        if install:
            destination = os.path.join(os.path.expandvars("${APPDATA}"), "Grasshopper", "Libraries")
            print('installing {ghpy_name} to {destination}'.format(
                ghpy_name=os.path.basename(ghpy_path), destination=destination))
            shutil.copy(ghpy_path, destination)

            if "parameters" in badger_config:
                print("installing {gha_name} to {destination}".format(
                    gha_name=os.path.basename(gha_path), destination=destination))
                shutil.copy(gha_path, destination)
                hbrt_path = os.path.join(os.path.dirname(os.path.normpath(os.path.abspath(__file__))),
                                         "honey-badger-runtime", "bin", "honey-badger-runtime.dll")
                print("installing {hbrt_name} to {destination}".format(
                    hbrt_name=os.path.basename(hbrt_path), destination=destination))
                shutil.copy(hbrt_path, destination)

            # copy additional files (from "include-install")
            for file_name in badger_config["include-install"]:
                if os.path.isabs(file_name):
                    file_path = file_name
                else:
                    # relative paths are relative to the folder containing the badger-file
                    file_path = os.path.join(badger_dir, file_name)
                assert os.path.exists(file_path), "Could not locate file: {}".format(file_path)
                print("copying {file_path} to {destination}".format(**locals()))
                shutil.copy(file_path, destination)

        print('done.')
    except:
        print traceback.print_exc()


def check_badger_config(badger_config, badger_dir):
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
    if not "include-install" in badger_config:
        badger_config["include-install"] = []
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
            if not "access" in input:
                input["access"] = "item"
            assert input["access"] in {"item", "list", "tree"}, "Input Access needs to be either 'item', 'list' or 'tree'"
        for output in component["outputs"]:
            assert "type" in output, "Input needs a type"
            assert "name" in output, "Input needs a name"
            assert "description" in output, "Input needs a description"
            if not "nick-name" in output:
                output["nick-name"] = output["name"]
        if "icon" in component:
            # convert icon (a path) to a base64 string
            icon_path = os.path.join(badger_dir, component["icon"])
            assert os.path.exists(icon_path), "Could not find icon file: {}".format(icon_path)
            bytes = System.IO.File.ReadAllBytes(icon_path)
            icon_base64 = System.Convert.ToBase64String(bytes)
            component["icon"] = icon_base64
    return badger_config


# This is the code that gets used to create the classes required for GrassHopper Components / Assemblies
TEMPLATE = u"""
import json
import GhPython
import System
import hblib_${guid} as hblib
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
    parser.add_argument('-v', '--rhino-version', choices=['6','7'], default='6', help='Specifies which Rhino SDK version to badger to (only 6 or 7 supported)')
    parser.add_argument('-s', '--skip-compatibility-check', action='store_true', default=False, help='Skips checking IronPython and Rhino compatibility.')
    parser.add_argument('file', action="store")
    args = parser.parse_args(sys.argv[1:])
    main(badger_file=args.file, 
         editable=args.editable, 
         install=args.install, 
         rhino_version=args.rhino_version,
         skip_compatibility_check=args.skip_compatibility_check)
