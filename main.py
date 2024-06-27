import arcpy
import logging
from pathlib import Path
from time import strftime

logfile = r'Logs\TileTilter.log'
logging.basicConfig(filename = logfile, level = logging.INFO, format = "%(asctime)s - %(levelname)s:%(message)s", datefmt = "%Y-%m-%d %H:%M:%S")

def logMessage(message):
    print(message + ": " + strftime("%Y-%m-%d %H:%M:%S"))
    logging.info(message)
    return

arcpy.env.overwriteOutput = True

anno_layers = {"4x": ["NonNBISPipes_4xMap",
                      "Structures_4xMap",
                      "Transportation_4xMap",
                      "Boundary_4xMap",
                      "Cultural_4xMap",
                      "Hydro_4xMap"],
               "8x": ["NonNBISPipes_8xInsetMap",
                      "Structures_8xInsetMap",
                      "Transportation_8xInsetMap",
                      "Boundary_8xInsetMap",
                      "Cultural_8xInsetMap",
                      "Hydro_8xInsetMap"]}

toplevel = Path(r"S:\Mapping\MapProd\Data\CountyMapProjects")

output_gdb = {"4x": toplevel / "WebPublishing" / "WGS84_Anno.gdb",
              "8x": toplevel / "WebPublishing" / "Anno_8x.gdb"}

output_pcs = arcpy.SpatialReference(3857)
nc_pcs = arcpy.SpatialReference(2264)

db_dict = {}
logMessage("Reading GDBs...")
for i in range(1, 15):
    istr = "{:02}".format(i)
    div_gdb = toplevel / f"Division{istr}" / f"Division{istr}.gdb"
    db_dict[istr] = div_gdb

gdb_out = output_gdb["4x"]
lyr_list = anno_layers["4x"]

logMessage("Compacting output gdb...")

arcpy.Compact_management(gdb_out.as_posix())

for div_key in db_dict.keys():
    logMessage(f"\n\nProcessing Division {div_key}...")
    feature_set = gdb_out / f"Annotation_div{div_key}"

    if arcpy.Exists(feature_set.as_posix()):
        logMessage("Deleting existing annotation dataset...")
        arcpy.Delete_management(feature_set.as_posix(),
                                data_type="FeatureDataset")

    logMessage("Creating container dataset for annotation...")

    arcpy.management.CreateFeatureDataset(gdb_out.as_posix(),
                                          f"Annotation_div{div_key}",
                                          output_pcs)

    for lyr in lyr_list:
        logMessage(f"\nNow processing layer:\n{lyr}")
        div_gdb = db_dict[div_key]
        anno_old = div_gdb / "Annotation" / lyr
        anno_new = feature_set / f"{lyr}{div_key}"
        anno_result = arcpy.Project_management(in_dataset=anno_old.as_posix(),
                                               out_dataset=anno_new.as_posix(),
                                               out_coor_system=output_pcs,
                                               transform_method="WGS_1984_(ITRF00)_To_NAD_1983",
                                               in_coor_system=nc_pcs)

        # Fixing issues with reprojected "horizontal" annotation
        select_where = "{0} = 0".format(arcpy.AddFieldDelimiters(anno_new.as_posix(), "Angle"))
        anno_sel = arcpy.management.SelectLayerByAttribute(anno_new.as_posix(), "NEW_SELECTION", select_where, None)
        logMessage("Tilting tiles...")
        arcpy.management.CalculateField(anno_sel, "Angle", "0", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
        arcpy.SelectLayerByAttribute_management(anno_sel, "CLEAR_SELECTION")

