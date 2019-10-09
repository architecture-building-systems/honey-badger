
import json
import GhPython
import System
import hblib
import Grasshopper

BADGER_CONFIG = json.loads('''{
    "description": "an example on how to import a c# dll and use its functions", 
    "name": "usecsharpdll", 
    "id": "e2ae062a-b547-40ac-8b1a-9447f8d866b2", 
    "components": [
        {
            "subcategory": "Hello World Sub-Category", 
            "inputs": [
                {
                    "description": "x1", 
                    "nick-name": "x1", 
                    "default": null, 
                    "name": "x1", 
                    "type": "float"
                }, 
                {
                    "description": "x2", 
                    "nick-name": "x2", 
                    "default": null, 
                    "name": "x2", 
                    "type": "float"
                }
            ], 
            "description": "import and use dll", 
            "outputs": [
                {
                    "nick-name": "dist2pt", 
                    "type": "float", 
                    "name": "dist2pt", 
                    "description": "dist2pt"
                }
            ], 
            "name": "UseCSharpdll", 
            "id": "d2fd6e31-1482-4db1-b002-1c7acf291979", 
            "main-module": "usecsharpdll", 
            "category": "Hello World Category", 
            "class-name": "UseCSharpdll", 
            "abbreviation": "csharp"
        }
    ], 
    "version": "0.1", 
    "author": "christophwaibel", 
    "include-files": [
        "usecsharpdll.py"
    ]
}''')

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

