"""
example on how to load an external c# dll and use its functions.
calculates distance between two 1D points
"""
import Grasshopper
path = Grasshopper.Folders.AppDataFolder
import clr
import os
# need to put that dll into your Grasshopper libraries folder
clr.AddReferenceToFileAndPath(os.path.join(path, "Libraries", "SolarModel.dll"))
import SolarModel
import System

def main(x1, x2):
    x1float = float(x1) # IronPython? wouldn't take it directly from input
    x2float = float(x2)

    dist2pt = SolarModel.Misc.Distance2Pts(System.Array[float]([x1float, 0, 0]), System.Array[float]([x2float, 0, 0])) # .Net stuff like Arrays need to be explicitly declared, otherwise it sees a list
    return dist2pt