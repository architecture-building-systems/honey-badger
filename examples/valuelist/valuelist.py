import Grasshopper.Kernel.Special
import System


class HbValueList(Grasshopper.Kernel.Special.GH_ValueList):
    def get_ComponentGuid(self):
        return System.Guid("1b91e1d3-b612-4075-90fe-811bafd96ce4")


def main():
    return None