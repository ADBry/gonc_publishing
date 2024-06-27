import arcpy
from pathlib import Path
arcpy.env.overwriteOutput = True

root_folder = Path(r"C:\Users\ext-adbryson\Documents\ArcGIS\Projects\Annotation")

cache_out = root_folder / "Outputs" / "Tile Caches"
package_out = root_folder / "Outputs" / "Tile Packages"

cache_name = cache_out / "Scripted Cache"
cache_name.mkdir(parents=True, exist_ok=True)

package_name = package_out / "Scripted Package"
package_name.mkdir(parents=True, exist_ok=True)

# project_file = Path(r"C:\Users\ext-adbryson\Documents\ArcGIS\Projects\Annotation\Scaled Background Tiles.aprx")
# project_file = Path(r"C:\Users\ext-adbryson\Documents\ArcGIS\Projects\Annotation\testing\streamlined AOI 5-22.aprx")

project_root = root_folder / "APRX Files"
project_file = project_root / "Cook" / "Alpha Tiles.aprx"

main_proj = arcpy.mp.ArcGISProject(project_file.as_posix())
map_to_cache = main_proj.listMaps("*Tile Maker Map*")[0]

# lyr_for_AOI = map_to_cache.listLayers("*State Line*")[0]
lyr_for_AOI = map_to_cache.listLayers("*County Boundary*")[0]

extent_for_AOI = arcpy.Describe(lyr_for_AOI).extent
coordinates = [[extent_for_AOI.XMin, extent_for_AOI.YMin], [extent_for_AOI.XMax, extent_for_AOI.YMin],
               [extent_for_AOI.XMax, extent_for_AOI.YMax], [extent_for_AOI.XMin, extent_for_AOI.YMax]]

nc_pcs = arcpy.SpatialReference(2264)

feature_class = arcpy.CreateFeatureclass_management(
    "in_memory", "tempfc", "POINT", spatial_reference=nc_pcs)[0]

with arcpy.da.InsertCursor(feature_class, ["SHAPE@XY"]) as cursor:
    for (x,y) in coordinates:
        cursor.insertRow([(x,y)])

feature_set = arcpy.FeatureSet()
feature_set.load(feature_class)

arcpy.ManageTileCache_management(
    cache_name.as_posix(),
    "RECREATE_ALL_TILES",
    "AOI 528",
    in_datasource=map_to_cache,
    tiling_scheme="ARCGISONLINE_SCHEME",
    scales="1155581.108577;577790.554289;288895.277144;144447.638572;72223.819286,36111.909643",
    # area_of_interest=lyr_for_AOI,
    area_of_interest=feature_set,
    min_cached_scale=1155581.108577,
    max_cached_scale=36111.909643)


arcpy.management.ExportTileCache(
    (cache_name / "AOI 528" / map_to_cache.name).as_posix(),
    package_name.as_posix(),
    "ScaleAOI528",
    export_cache_type="TILE_PACKAGE_TPKX",
    storage_format_type="COMPACT_V2",
    # scales="1155581.108577;577790.554289;288895.277144;144447.638572;72223.819286,36111.909643")
    scales="1155581.108577;577790.554289;288895.277144;144447.638572;72223.819286,36111.909643",
    area_of_interest=lyr_for_AOI)

# arcpy.ManageTileCache_management(
#     cache_name.as_posix(),
#     "RECREATE_ALL_TILES",
#     "Scale Background AOI2",
#     in_datasource=map_to_cache,
#     tiling_scheme="ARCGISONLINE_SCHEME",
#     scales="1155581.108577;577790.554289;288895.277144;144447.638572;72223.819286,36111.909643",
#     area_of_interest=lyr_for_AOI,
#     # area_of_interest=feature_set,
#     min_cached_scale=1155581.108577,
#     max_cached_scale=36111.909643)
#
# arcpy.ManageTileCache_management(
#     cache_name.as_posix(),
#     "RECREATE_ALL_TILES",
#     "Scale Background no AOI",
#     in_datasource=map_to_cache,
#     tiling_scheme="ARCGISONLINE_SCHEME",
#     scales="1155581.108577;577790.554289;288895.277144;144447.638572;72223.819286,36111.909643",
#     min_cached_scale=1155581.108577,
#     max_cached_scale=36111.909643)

# arcpy.management.ExportTileCache(
#     (cache_name / "Scale Background no AOI" / map_to_cache.name).as_posix(),
#     package_name.as_posix(),
#     "ScalenoAOITest2",
#     export_cache_type="TILE_PACKAGE_TPKX",
#     storage_format_type="COMPACT_V2",
#     # scales="1155581.108577;577790.554289;288895.277144;144447.638572;72223.819286,36111.909643")
#     scales="1155581.108577;577790.554289;288895.277144;144447.638572;72223.819286,36111.909643",
#     area_of_interest=lyr_for_AOI)
#
# arcpy.management.ExportTileCache(
#     (cache_name / "Scale Background no AOI" / map_to_cache.name).as_posix(),
#     package_name.as_posix(),
#     "ScalenoAOITest3",
#     export_cache_type="TILE_PACKAGE_TPKX",
#     storage_format_type="COMPACT_V2",
#     scales="1155581.108577;577790.554289;288895.277144;144447.638572;72223.819286,36111.909643")