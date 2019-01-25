"""Draws a graphic symbol parallel to world XYZ showing orientations.
            Inputs:
                P: The point where the symbol should be drawn
            Output:
                X: The symbol, drawn as three lines"""

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
from Rhino.Geometry import Point3d as p3
import rhinoscriptsyntax as rs

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Friday", "FR", """Celebrate Friday like a boss!""", "Hive", "6. honey-badger")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("e291edaf-aeb6-4f44-9bbc-dfdd3936d48f")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Point()
        self.SetUpParam(p, "P", "P", "The point where the symbol should be drawn")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "X", "X", "The symbol, drawn as three lines")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARRSURBVEhLnZYLTJNXFMdLCy2gYFvcXBoyAeeQIQ9BioIw5mMggkb2ABoEkYdxGOemMNxM0AiZ02UQxQJ7mE0WZ9iWRWY23TLtULYQiATCXBjbgGERkPJR2vKonf9957ZguwXCuMk/Pb3fPed37jn3ewhmG1KpNMlrmZyTyWSYS7SG1trc5j/kvGPV1XJ0Trah1fQTbhmv4ZrhC3yl/xifcmdQoyvDu4NFyPoyiUFsbvMflN11Qz02nQvBqjRvPK8Ox/7+HTjQv5OJ7ALtduzp2sx2YnOb/yCnutFqBKQ9Cf8Ub6xW+eLQQCoKB9OZyH598CXkdW5dOECtO47E6kgEqVZgR00M3hzOxFFdNhPZxfczkN+xbeGA0vsFKB7KYAFLdLk4zu3FCW4fE9k0t7c9eW6Ae4QgaZFSyLmFCmAvj+VuDv+n9c7YQaaT+ldRNlqA/NvJWOzjCtcggYPcwgWcOEyQxAOcuJqGcvRO/o47E7fRPP4jGkzf8Cfmc9QbL6DOWI1aYznOm05CbSpBhamY6T1jEU4bXkNeUxLbwbdTl1A1fgyF+lS8OBwC/ysuBBkRUFYtppvY1ROD3L4t7GRQ86i+VALKkgJR0MqJo6iaPMZENs3lNFp7EDXqiXUjixE57I6IIVeE/iFmO2GAG2P1yOqJQ/7deHb86IRQE6nOVArKlgK+P3UC5x+8zUQ2ze3WJDBArF6O9ZwHInU2wG+SR4D60QvY3WsF0BmnY1ikVeFQF69OFQp/zcQbHdkobs/BkbYcHG7JREHjy8jVbEdixTo85uNlTjAsnwEoh9wRfMduB7XDZxwAB3peQMpHcQ8V3gozZTeXHvddao697Pdw85jCEdBuBzg7WOJQopyOeCgUCvPp6yVotmigsVzGFUstLlkq8aGlDBV/F6HUko8icyryJjYi2bQS0folDiUKanV5BCjt3+/Q5F0tz7Hsrpo/Q7RhCWJMUsSOy/HshBfipqwim+boGq35d5MDm+0Ah/vSkdETjT1/bcI+bSJSG2MYoG5SjSi9JzYYpDYI30w+qFUyNkfXaI19edYO8oCf7QDZ3Ruh6o6a6cNOTSQDfDBehvWjHiwAZbnB6CiWOQXn19hnHz7gioBbzlYA3WjKT7yx5cYqxP8QiK3fB2PbdyEMcMp4kDlSdlQCBhrjaz3Cl2PAA0rtIqztdkdYlxtCf3FFcJsEq1vELHu/i0J2N7NHhbtS8J9HBQHeGstiWdHWp0GU1Xw086iYbRDgFS6RbZnqOg1K5lbiiCEDF8fPov1BE2jQWpvb/Ac5pQ9HsHpS0wg0DVtRI8FSlQh+1WJ23hcMSLjnizX9YoTdkzARjOSVLoI8RcR+A26KFg5Q9nkg9K4L0xqtmMFIPmpnyNOc4HPOGU997bRAwDJP7uk6vgS9QgT/KUJQpzMCO4R4plWIgCZejUL4NzjBr1IC2RPS///Sp08RcqTs5hS/ZvbPFoHgH+aYkAe+xCUYAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, P):
        __author__ = "piac"
        
        X = None
        
        if P:
            X = "hello, amr!"
        
        # return outputs if you have them; here I try it for you:
        return X


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Friday"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("f961ed6a-6c29-426b-8126-0d0e40bf4f66")