"""
example on how to load an external c# dll and use its functions.
calculates distance between two 1D points
"""
import clr
clr.AddReferenceToFileAndPath(r"C:\Users\chwaibel\Documents\GitHub\honey-badger\examples\usecsharpdll\SolarModel.dll") # path of your dll
import SolarModel # your Python IDE will tell you that this module is missing, even if it isn't. Can be resolved by installing stubs for it, if any exist
import System # also doesn't see it

def main(x1, x2):
    x1float = float(x1) # IronPython? wouldn't take it directly from input
    x2float = float(x2)

    dist2pt = SolarModel.Misc.Distance2Pts(System.Array[float]([x1float, 0, 0]), System.Array[float]([x2float, 0, 0])) # .Net stuff like Arrays need to be explicitly declared, otherwise it sees a list
    return dist2pt