"""
Compile parameters to a ".gha" assembly. Currently, this only supports the parameter-type "ValueList". This
will produce subclasses of "GH_ValueList" with a pre-compiled list of values.

Why? Because GhPython only works for subclasses of "DotNetCompiledComponent" - So we're using Reflection.Emit to
create a dll (a .gha _is_ a dll, just renamed...) with the types we want.
"""
print("before imports")
import os
import csv
import json
import clr
print("between imports")

clr.AddReference("IronPython")
clr.AddReference("System")
clr.AddReference("System.Reflection")


hbrt_path = os.path.join(os.path.dirname(os.path.normpath(os.path.abspath(__file__))), "honey-badger-runtime", "bin",
                         "honey-badger-runtime.dll")
clr.AddReferenceToFileAndPath(hbrt_path)
clr.AddReferenceToFileAndPath(r"C:\Program Files\Rhino 6\Plug-ins\Grasshopper\Grasshopper.dll")
clr.AddReferenceToFileAndPath(r"C:\Program Files\Rhino 6\System\RhinoCommon.dll")

from System import Array, Type, AppDomain
from System.Reflection import (AssemblyName, TypeAttributes, MethodInfo, MethodAttributes, CallingConventions,
                               PropertyAttributes)
from System.Reflection.Emit import AssemblyBuilderAccess, OpCode, OpCodes
from Grasshopper.Kernel import GH_AssemblyInfo

from HoneyBadgerRuntime import HoneyBadgerValueList, HoneyBadgerRuntimeInfo
print("after imports")


def compile_parameters(badger_config, badger_dir, dll_path):
    """Compile ValueList parameters and save them to a .gha assembly."""
    # https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.assemblybuilder?view=netframework-4.8
    parameters = badger_config["parameters"]
    base_constructor = clr.GetClrType(HoneyBadgerValueList).GetConstructor(Array[Type]([str, str, str, str, str, str]))

    dll_folder = os.path.dirname(dll_path)
    dll_name = os.path.splitext(os.path.basename(dll_path))[0]
    assembly_name = AssemblyName(dll_name)
    assembly_builder = AppDomain.CurrentDomain.DefineDynamicAssembly(assembly_name, AssemblyBuilderAccess.RunAndSave, dll_folder)
    module_builder = assembly_builder.DefineDynamicModule(assembly_name.Name, assembly_name.Name + ".gha")
    for parameter in parameters:
        assert parameter["parameter-type"] == "ValueList", "honey-badger can only produce ValueList parameters"
        keys, values = read_values(badger_dir, parameter["csv"])
        type_builder = module_builder.DefineType(parameter["class-name"],
                                                 TypeAttributes.Public,
                                                 HoneyBadgerValueList)
        constructor_builder = type_builder.DefineConstructor(MethodAttributes.Public, CallingConventions.Standard,
                                                             Type.EmptyTypes)
        il_generator = constructor_builder.GetILGenerator()
        il_generator.Emit(OpCodes.Ldarg_0)  # load "this" onto stack
        il_generator.Emit(OpCodes.Ldstr, parameter["name"])  # load constructor args (name)
        il_generator.Emit(OpCodes.Ldstr, parameter["abbreviation"])  # load constructor args (nickname)
        il_generator.Emit(OpCodes.Ldstr, parameter["description"])  # load constructor args (description)
        il_generator.Emit(OpCodes.Ldstr, parameter["category"])  # load constructor args (category)
        il_generator.Emit(OpCodes.Ldstr, parameter["subcategory"])  # load constructor args (subCategory)
        il_generator.Emit(OpCodes.Ldstr, parameter["id"])  # load constructor args (guid)
        il_generator.Emit(OpCodes.Call, base_constructor)  # call constructor, consumes args and "this"
        il_generator.Emit(OpCodes.Ret)  # return from constructor

        override_load_value_list(type_builder, keys=keys, values=values)

        type_builder.CreateType()

    # add a GH_AssemblyInfo to the assembly...
    create_gh_assembly_info(badger_config, module_builder)

    assembly_builder.Save(assembly_name.Name + ".gha")


def override_load_value_list(type_builder, keys, values):
    """Override HoneyBadgerValueList.LoadValues to load the keys and corresponding values"""
    add_list_item = clr.GetClrType(HoneyBadgerValueList).GetMethod("AddListItem", Array[Type]([str, str]))
    method_attributes = (MethodAttributes.Public | MethodAttributes.Virtual)
    method_builder = type_builder.DefineMethod("LoadValueList", method_attributes, CallingConventions.Standard,
                                               None, None)
    il_generator = method_builder.GetILGenerator()
    for key, value in zip(keys, values):
        il_generator.Emit(OpCodes.Ldarg_0)  # this
        il_generator.Emit(OpCodes.Ldstr, str(key))
        il_generator.Emit(OpCodes.Ldstr, json.dumps(value))
        il_generator.Emit.Overloads[OpCode, MethodInfo](OpCodes.Call, add_list_item)

    il_generator.Emit(OpCodes.Ret)


def create_gh_assembly_info(badger_config, module_builder):
    """Create a GH_AssemblyInfo subclass for the assembly, as it seems we need to directly subclass it."""
    type_builder = module_builder.DefineType(badger_config["name"] + "AssemblyInfo", TypeAttributes.Public,
                                             GH_AssemblyInfo)

    # create an empty constructor
    constructor_builder = type_builder.DefineConstructor(MethodAttributes.Public, CallingConventions.Standard,
                                                         Type.EmptyTypes)
    il_generator = constructor_builder.GetILGenerator()
    il_generator.Emit(OpCodes.Ret)

    # create the properties
    create_string_property("Name", badger_config["name"] + "Parameters", type_builder)
    create_string_property("Version", badger_config["version"], type_builder)
    create_string_property("Description", badger_config["description"], type_builder)

    # create the Version property
    type_builder.CreateType()


def create_string_property(name, value, type_builder):
    """Override a (string) property getter"""
    property_builder = type_builder.DefineProperty(name, PropertyAttributes.HasDefault, str, None)
    getter_attributes = (MethodAttributes.Public | MethodAttributes.SpecialName | MethodAttributes.HideBySig
                         | MethodAttributes.Virtual)
    getter = type_builder.DefineMethod("get_{name}".format(name=name), getter_attributes, str, None)
    il_generator = getter.GetILGenerator()
    il_generator.Emit(OpCodes.Ldstr, value)
    il_generator.Emit(OpCodes.Ret)  # return from constructor
    property_builder.SetGetMethod(getter)


def read_values(badger_dir, csv_file):
    """Import the value_producer module relative to badger_dir and return the results of running the main() function."""
    with open(os.path.join(badger_dir, "planets.csv")) as planets:
        reader = csv.DictReader(planets)
        keys = []
        values = []
        for row in reader:
            keys.append(row[reader.fieldnames[0]])
            values.append(floatify(row))
        return keys, values


def floatify(dict):
    """convert as many values to float as possible"""
    for key in dict.keys():
        try:
           dict[key] = float(dict[key])
        except ValueError:
            pass
    return dict
