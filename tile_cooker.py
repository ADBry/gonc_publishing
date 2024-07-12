import arcpy
import logging
from pathlib import Path
from time import strftime
from map_dict import ProProject

zoom_levels = {11: 288895.277144,
               12: 144447.638572,
               13: 72223.819286,
               14: 36111.909643,
               15: 18055.954822,
               16: 9027.977411,
               17: 4513.988705,
               18: 2256.994353}

# maps = {}
# "Anno":
#             {"County": "*County Anno*",
#              "Bridge": "*Bridge Anno*",
#              "8x": "*8x*"},
#         {"Basemap":
#          }
#
#         }

arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = "90%"

logfile = r'Logs\WebTiles.log'
logging.basicConfig(filename = logfile, level = logging.INFO, format = "%(asctime)s - %(levelname)s:%(message)s", datefmt = "%Y-%m-%d %H:%M:%S")

def logMessage(message):
    print(message + ": " + strftime("%Y-%m-%d %H:%M:%S"))
    logging.info(message)
    return


# root_folder = Path(r"C:\Users\ext-adbryson\Documents\ArcGIS\Projects\Annotation")
root_folder = Path(r"S:\Mapping\MapProd\WebPublishing")
####
# package_name = root_folder / "Output Files" / "ScriptTest"
# package_name.mkdir(parents=True, exist_ok=True)
####
# project_root = root_folder / "APRX Files"
# project_file = project_root / "Tile Catalog.aprx"

project_file = root_folder / "Tile Catalog.aprx"

my_proj = ProProject(project_file.as_posix())

if my_proj.setup_maps():
    my_proj.cook_tiles("Basemaps", "B")


#
#
# ############################################################
# logMessage("Loading maps...")
# main_proj = arcpy.mp.ArcGISProject(project_file.as_posix())
# #
# map_to_cache = main_proj.listMaps("*new*Tile Maker Map*")[0]
# lyr_for_AOI = map_to_cache.listLayers("*County Boundary*")[0]
# extent_for_AOI = arcpy.Describe(lyr_for_AOI).extent
#
# logMessage("Processing tile cache...")
# arcpy.management.CreateMapTilePackage(
#     in_map=map_to_cache,
#     service_type="ONLINE",
#     output_file=(package_name / "lyrName_12.tpkx").as_posix(),
#     format_type="PNG8",
#     level_of_detail=16,
#     extent=lyr_for_AOI.name,
#     # extent='-9397826.15917723 3992679.08818247 -8395274.29799675 4385890.30626054 PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]',
#     compression_quality=75,
#     package_type="tpkx",
#     min_level_of_detail=12
#     # area_of_interest=lyr_for_AOI
# )
# # logMessage("Processing complete!")
