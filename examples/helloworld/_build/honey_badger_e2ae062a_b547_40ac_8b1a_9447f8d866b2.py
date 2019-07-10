
import json
import GhPython
import System
import hblib
import Grasshopper

BADGER_CONFIG = json.loads('''{
    "description": "a simple helloworld example assembly with a single component that says helloworld", 
    "name": "helloworld", 
    "id": "e2ae062a-b547-40ac-8b1a-9447f8d866b2", 
    "components": [
        {
            "subcategory": "Hello World Sub-Category", 
            "inputs": [
                {
                    "description": "a name to say hello world to", 
                    "nick-name": "nickname", 
                    "default": "Randall", 
                    "name": "firstname", 
                    "type": "string"
                }
            ], 
            "description": "say hello, world :)", 
            "outputs": [
                {
                    "nick-name": "o", 
                    "type": "string", 
                    "name": "output", 
                    "description": "output of the script"
                }
            ], 
            "name": "HelloWorldName", 
            "id": "d2fd6e31-1482-4db1-b002-1c7acf291979", 
            "main-module": "helloworld", 
            "category": "Hello World Category", 
            "class-name": "HelloWorldComponent", 
            "abbreviation": "hw"
        }
    ], 
    "version": "0.1", 
    "author": "daren-thomas", 
    "include-files": [
        "helloworld.py"
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

