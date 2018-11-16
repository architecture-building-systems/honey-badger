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

## A collection of links and facts I've found while researching possible solutions

- https://discourse.mcneel.com/t/tutorial-creating-a-grasshopper-component-with-the-python-ghpy-compiler/38552
  - it seems there is already some support in Rhino/Grasshopper for what we want to do
  - this mentions the `clr.CompileModules` function which seems to do the heavy lifting
  - https://blogs.msdn.microsoft.com/srivatsn/2008/08/06/static-compilation-of-ironpython-scripts/
  - it looks like it should be possible to compile these (and name then `.ghpy` instead of `.dll`) from source
  - also, it looks like GrassHopper will automatically re-load the assemblies when they're updated!
- The folder `%programfiles%\Rhino 6\Plug-ins\Grasshopper\Components\` contains the GhPython `.gha` file...
  - ghpythonlib `%appdata%\McNeel\Rhinoceros\6.0\Plug-ins\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\settings\lib\`
