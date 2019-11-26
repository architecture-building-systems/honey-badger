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

import Grasshopper
import Grasshopper.Kernel
import Grasshopper.Kernel.Special

dir(Grasshopper.Kernel.Special)

# emulate "using" from the C# examples
from IronPython.Runtime.Operations import PythonOps
import Grasshopper.Kernel.Special
from System.Reflection import AssemblyName, TypeAttributes
from System.Reflection.Emit import AssemblyBuilderAccess


def get_GH_ValueList():
    """For some reason I can't import this type, but it's possible to find it"""
    return [t for t in clr.GetClrType(Grasshopper.Kernel.Special.GH_ValueListItem).Assembly.GetExportedTypes() if
            str(t) == "Grasshopper.Kernel.Special.GH_ValueList"][0]

def compile(parameters, badger_dir, dll_path):
    # https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.assemblybuilder?view=netframework-4.8
    assembly_name = AssemblyName(os.path.splitext(os.path.basename(dll_path))[0])
    assembly_builder = PythonOps.DefineDynamicAssembly(assembly_name, AssemblyBuilderAccess.RunAndSave)
    module_builder = assembly_builder.DefineDynamicModule(assembly_name.Name, assembly_name.Name + ".gha")
    for parameter in parameters:
        values = read_values(badger_dir, parameter["value-producer"])
        type_builder = module_builder.DefineType(parameter["class-name"],
                                                 TypeAttributes.Public,
                                                 get_GH_ValueList())


def read_values(badger_dir, value_producer):
    """Import the value_producer module relative to badger_dir and return the results of running the main() function."""
    producer = imp.load_source("producer", os.path.join(badger_dir, value_producer))
    return producer.main()