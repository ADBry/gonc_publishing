import arcpy
from pathlib import Path
from .pro_utils import MapLUT

class ProProject(arcpy.mp.ArcGISProject):

    def __init__(self, aprx_path):
        super().__init__(aprx_path)

        self.maps = False

    def setup_maps(self, ):
        self.maps = MapLUT(self)
        success = True
        return success