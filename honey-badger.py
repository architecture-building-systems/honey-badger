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
import shutil
import traceback


def main(badger_file, editable, install):
    try:
        # temporary create the helloworld dll adding the honey-badger.json to it
        with open(badger_file, mode='r') as bf:
            badger_file_contents = bf.read().decode('utf-8')
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

        ghpy_path = os.path.join(build_dir, '{}.ghpy'.format(badger_config['name']))
        clr.CompileModules(ghpy_path,
                           os.path.join(build_dir, hb_main_py),
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
from ghpythonlib.componentbase import dotnetcompiledcomponent
import Grasshopper, GhPython
import System
import GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import importlib
import json

BADGER_CONFIG = json.loads('''${badger_config}''')

PARAMETER_MAP = {
    'string': Grasshopper.Kernel.Parameters.Param_GenericObject,
    'float': Grasshopper.Kernel.Parameters.Param_Number,
    'number': Grasshopper.Kernel.Parameters.Param_Number,
}


def set_up_param(p, name, nickname, description):
    p.Name = name
    p.NickName = nickname
    p.Description = description
    p.Optional = True


for component in BADGER_CONFIG['components']:
    # dynamically create subclasses of ``component`` for each component in the badger file

    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
                                                           component['name'],
                                                           component['abbreviation'],
                                                           component['description'],
                                                           component['category'],
                                                           component['subcategory'])
        return instance

    def RegisterInputParams(self, pManager):
        for input in component['inputs']:
            p = PARAMETER_MAP[input['type']]()
            set_up_param(p, input['name'], input['nick-name'], input['description'])
            p.Access = Grasshopper.Kernel.GH_ParamAccess.item
            self.Params.Input.Add(p)

    def RegisterOutputParams(self, pManager):
        for output in component['outputs']:
            p = PARAMETER_MAP[output['type']]()
            set_up_param(p, output['name'], output['nick-name'], output['description'])
            # p.Access = Grasshopper.Kernel.GH_ParamAccess.item
            self.Params.Output.Add(p)

    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASDSURBVEhLnZQLUJRVFMcXvmUXRN47I4OQOk5NM2YSBGalmWYDueKEjizrg0DK5GXaSNhUoERINcLwEHeIQClCVEhwyEcSomBMJINoRKiIgMhrP2B3eazgv+/c3YJ1khjOzH/m7P3uOb9zzz17RU8ye5lM7ujkzDs4OGAqOcqcedprDJu+OTrN4ZNV53C9eQTV9UM496sWJ8s1yD0zgNTjPBJy+hCd1g15yCkGMYZN36i6kkoNlvhmwO05BTzlh7H+o068vc8g8v323seanc3sJMaw6RsFqYr78dRiBdwW+WOBuxIBcV0IPNDNRP6mz7rgG9E0c8D+b9V4yf8IFnoosVyhQlBSL4K/6mMif2tiD9ZG3Zw5IPxQL7Yk9LCEoclq7EjlsTPdIPJpbV3U9f8BcF5yc85buCR3YdOErKzmmfz+Rx9kDzLtyhpEeGa/ALiG+ZaWWCwSmcjTQsR7cCK5yIzz4pMzK3Hr3ijq/hzGpWtDKLuqw4kKLY5d0EJVpkVKiRZJxTrEHtchJt+g6Dwt9uRosC6ihp1g9E4BhmrjMHBWgd6jS3AmyAKeYpFaOII7Lv+uw4rQu3gzso1NBl0e9ZdaQFVSIkr66YlhxBWNMJFPa/KwKgboz7eFOnc2elXW6E6zwu1PJOwkDFB6aRAr32uFz652Nn40IXSJ1GdqBVVLCeNLRnHwp4dM5NOa77sVDDBQ6AT+mA36sgRAuhX+ipFOAPJK+/G6EUAzTmO4Ob4Dythb2BzXhG0HGhH8+U1sT2hA6Bf1CIqrxaa91fALq8AyvxTMd3XSa36cBz5PAHxjjZ6MWfjjw0knSP2+zwSwYV8rViqzH7nOddFTdVNpgZtMf/rgwkeaIhcTQEPkJEBsZrdJi3zCb2Cui4u+vDAWY90VGOsswVhHHsbb0jHemoDx29EYa9wBfV0ARqpWQVf2NAYK7ExaVPf+JEBEYqfJJa8KqWXV6VsKoDlpB12JA4bPOmLkZyeMlsuYyKc1+kZ7Hr/k34ItJgCB0W14Nfgu3gi7h7V7OrBcWc0AI42ZQmW20BTZs0RDZY4sKYl8llz4RntYe7KF9mTOQleKJa4qJwFWh7bg5W0t/97DUn/DZAzVJaD/OxsDRKhSW2wP7WmjBJ/W6BvtUedMVP/gkCWubBQbAGbmXrzrC0fx7OpfsGjNRTzvcwHuvucZQHtlNwuk6qgFlGyw0A7qPFt0ZdmgI202WpKs0RwnTE20JeojpajdLmHV57/G0R9NeCGEp8LsP54KAgyeD2JV0dGpv3SJVNV0RMnZU/EkIwB/6i12ZOorAwkTwv/wDDQXt2C4IQ0Pu2pARnuNYdM3CurN9Wb9pEsjEI0fzbgqWArlMg5H3pGgIUoyc8CD1AW4nyhB55dSdH4tZTBS4FIO/h4cAr05XN4gnjmgLd4G7fst0B5vgY4ECYORDivEULxojowAMUpfMZ8ZYI7Mni/cKkHrxxzuxIjRtFuMG2Ec6kI41Cg5VG3kULneHOkrpHAW9hrDpm8ymb2cAqm6qUR7aK8x7DETif4GWQPKTm78ggMAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    def SolveInstance(self, DA):
        main_module = importlib.import_module(component['main-module'])
        if 'main-function' in component:
            main_function = getattr(main_module, component['main-function'])
        else:
            main_function = getattr(main_module, 'main')
        inputs = [self.marshal.GetInput(DA, i) for i in range(len(component['inputs']))]
        # apply default values
        
        results = main_function(*inputs)
        if len(component['outputs']) == 1:
            self.marshal.SetOutput(results, DA, 0, True)
        elif len(component['outputs']) > 1:
            for i, r in enumerate(results):
                self.marshal.SetOutput(r, DA, i, True)

    globals()[component['name']] = type(component['class-name'], (dotnetcompiledcomponent,), {
        '__new__': __new__,
        'get_ComponentGuid': lambda self: System.Guid(component['id']),
        'RegisterInputParams': RegisterInputParams,
        'RegisterOutputParams': RegisterOutputParams,
        'get_Internal_Icon_24x24': get_Internal_Icon_24x24,
        'SolveInstance': SolveInstance,
    })


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
