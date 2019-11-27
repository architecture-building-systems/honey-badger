"""
Compile parameters to a ".gha" assembly. Currently, this only supports the parameter-type "ValueList". This
will produce subclasses of "GH_ValueList" with a pre-compiled list of values.

Why? Because GhPython only works for subclasses of "DotNetCompiledComponent" - So we're using Reflection.Emit to
create a dll (a .gha _is_ a dll, just renamed...) with the types we want.
"""
import imp
import os
import clr
clr.AddReference("IronPython")
clr.AddReference("System")
clr.AddReference("System.Reflection")
clr.AddReferenceToFileAndPath(r"C:\Program Files\Rhino 6\Plug-ins\Grasshopper\Grasshopper.dll")
clr.AddReferenceToFileAndPath(r"C:\Program Files\Rhino 6\System\RhinoCommon.dll")

from System import Array, Type
from IronPython.Runtime.Operations import PythonOps
from System.Reflection import AssemblyName, TypeAttributes, MethodAttributes, CallingConventions
from System.Reflection.Emit import AssemblyBuilderAccess
from Grasshopper.Kernel.Special import GH_ValueList


def compile(parameters, badger_dir, dll_path):
    # https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.assemblybuilder?view=netframework-4.8
    assembly_name = AssemblyName(os.path.splitext(os.path.basename(dll_path))[0])
    assembly_builder = PythonOps.DefineDynamicAssembly(assembly_name, AssemblyBuilderAccess.RunAndSave)
    module_builder = assembly_builder.DefineDynamicModule(assembly_name.Name, assembly_name.Name + ".gha")
    for parameter in parameters:
        values = read_values(badger_dir, parameter["value-producer"])
        type_builder = module_builder.DefineType(parameter["class-name"],
                                                 TypeAttributes.Public,
                                                 GH_ValueList)
        constructor_builder = type_builder.DefineConstructor(MethodAttributes.Public, CallingConventions.Standard,
                                                             Type.EmptyTypes)
        t = type_builder.GetType()
        assembly_builder.Save(assembly_name.Name + ".gha")



def read_values(badger_dir, value_producer):
    """Import the value_producer module relative to badger_dir and return the results of running the main() function."""
    producer = imp.load_source("producer", os.path.join(badger_dir, value_producer))
    return producer.main()