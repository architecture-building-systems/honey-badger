# honey-badger

honey-badger is a build system for Python based Rhino/Grasshopper plugins

## Why bother?

For the [HIVE](https://github.com/architecture-building-systems/hive) project, we intend to build a bunch of GrassHopper components.

The current workflow uses the GhPython component and manually pasting the code into the editor exported by that component. This is
cumbersome and could result in errors due to the manual steps in the process. In order to keep the code in a review-able state,
it is kept in separate Python files in GitHub - this gives the advantages of pull requests and diffs of the code.

An ideal solution would be to edit the code in a nice IDE like PyCharm or VSCode and have a build tool (honey-badger!) build and deploy the
GH components automatically - no manual copying of Python source code.

Another project, the [City Energy Analyst](https://github.com/architecture-building-systems/CityEnergyAnalyst), has a GrassHopper
plugin that allows the CEA scripts to be run from in GrassHopper. But this component is pretty simple in that it has a fixed interface
and uses a `script-name` input parameter to decide which CEA script to run. Since the CEA has meta-data about all the scripts' 
parameters, a GH component for each script in the CEA family could be created. honey-badger could be a part of such a sollution. 

## How To Use

- open command shell (windows-key + R, then enter ``cmd``)
- navigate to your IronPython installation folder, for me it's C:\Program Files\IronPython 2.7 (although Rhino ships with IronPython, you need a **standalone version installed**)
- enter: ``ipy.exe honey-badger_path\honey-badger.py -i grasshopper-project_path\component.json``
  - NOTE: You should have the exact same version of IronPython installed as Grasshopper uses. At the time of writing this is [2.7.8](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8) for Rhino 6, [2.7.9](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.9) for RHino 7.
  - use `-v [6 or 7]` to specify Rhino version to use for SDK. Default is 6.
  - use `-s` to skip a compability check between rhino version and IronPython version used. Default False (as in, checks compatibility by default).
  - You can always check the IronPython version used in Rhino by navigating to `C:\Program Files\Rhino 7\Plug-ins\IronPython\IronPython.dll`, rightclick Properties > Details Tab > File Version Property.
- your new python component should now be loaded when opening grasshopper

## A collection of links and facts I've found while researching possible solutions

- https://discourse.mcneel.com/t/tutorial-creating-a-grasshopper-component-with-the-python-ghpy-compiler/38552
  - it seems there is already some support in Rhino/Grasshopper for what we want to do
  - this mentions the `clr.CompileModules` function which seems to do the heavy lifting
  - https://blogs.msdn.microsoft.com/srivatsn/2008/08/06/static-compilation-of-ironpython-scripts/
  - it looks like it should be possible to compile these (and name then `.ghpy` instead of `.dll`) from source
  - also, it looks like GrassHopper will automatically re-load the assemblies when they're updated!
- The folder `%programfiles%\Rhino 6\Plug-ins\Grasshopper\Components\` contains the GhPython `.gha` file...
  - ghpythonlib `%appdata%\McNeel\Rhinoceros\6.0\Plug-ins\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\settings\lib\`

## FAQ

- You can use .Net libraries with the clr libray. This is a simple example [usecsharpdll](/examples/usecsharpdll/usecsharpdll.py) 
  - Your Python IDE won't recognize that library, meaning it will tell you that no module named `yourlibrary` is found. But you can still use it.
  - Installing stubs (if any exist for your library) will solve this problem. See next point
- You can use typehints of .Net libraries by importing stubs: https://stevebaer.wordpress.com/2019/02/25/autocomplete-and-type-hints-with-python-scripts-for-rhino-grasshopper/
  - Make sure you set your Python interpreter to Python 2.7, otherwise with IronPython it won't let you install the stub files. In PyCharm: File->Settings->Projet:Honey-Badger->Project Interpreter.
  - Don't forget to install clr package to your Python 2.7 environment
- You can package .csv databases into your component, with Daren's awesome [planets-example](/examples/planets/). But make sure it follows the same structure as his .csv example file, i.e. 1 header, comma separated, utf-8 encoding
  - Make sure you have `from __future__ import print_function` in your `.py` file, otherwise you'll get an error in Grasshopper: `The supplied data could not be converted: Parameter type: GH_Number. Supplied type: String`
- Here is the results of checking compabitility of IronPython and Rhino. Best option is to use IronPython 2.6.8 with Rhino 6 SDK, as it will work for both RHino 6 and 7 no problemos. Rhino SDKs are forward but not backward compatible.

|IronPython version | Rhino SDK version | Worked in Rhino 6 | Worked in Rhino 7|
|-|-|-|-|
|2.7.8| 6| yes| yes|
|2.7.8| 7| warning about SDK but seemed to work| yes|
|2.7.9| 6| no| yes|
|2.7.9| 7| no| yes|
|2.7.11| 6| no| no|
|2.7.11| 7| no| no|