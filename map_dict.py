import arcpy
from pathlib import Path
from pro_utils import MapLUT

# DEFAULT_OUTPUT = Path(r"S:\Mapping\MapProd\WebPublishing")
DEFAULT_OUTPUT = Path(r"C:\Users\ext-adbryson\Documents\ArcGIS\Projects\Annotation\Scripted")

class ProProject(arcpy.mp.ArcGISProject):

    def __init__(self, aprx_path, outpath:Path = DEFAULT_OUTPUT):
        super().__init__(aprx_path)
        self.maps = False
        self.output_folder = outpath / "Output Files" / "Script Test"
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def setup_maps(self):
        self.maps = MapLUT(self)
        success = True
        return success

    def cook_tiles(self, *args):
        print(args)
        m = self.maps
        for i in args:
            m = m[i]
        tilefile = "".join(args)
        m = self.listMaps(m)[0]
        lyr_for_AOI = m.listLayers("*County Boundary*")[0]
        # extent_for_AOI = arcpy.Describe(lyr_for_AOI).extent
        tilename = (self.output_folder / f"{tilefile}.tpkx").as_posix()

        print("Processing tile cache...")
        # logMessage("Processing tile cache...")
        arcpy.management.CreateMapTilePackage(
            in_map=m,
            service_type="ONLINE",
            output_file=tilename,
            format_type="PNG8",
            level_of_detail=16,
            compression_quality=75,
            package_type="tpkx",
            min_level_of_detail=12,
            area_of_interest = lyr_for_AOI
        )

        print("Processing complete!")
