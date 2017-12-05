# header information
#
#
#

# import modules
import arcpy

# define variables
yr = 2006

overlay = 'Census' # or 'County'

northArrow = 'place holder'

ndvi_name = 'CONUS NDVI YYYY'

extent = None #[-130,30,-120,40]

# define map document
mxd = arcpy.mapping.MapDocument(r'C:\Users\mpullman\Desktop\ESS508\mapping_assignment\map_template\map_template\ess408_map_template2.mxd')

# define data frame
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

lyrs = arcpy.mapping.ListLayers(df)

for i in range(len(lyrs)):
    if 'ndvi' in lyrs[i].name:
        lyr_yr = lyrs[i].name[-12:-8]
        lyrs[i].name = ndvi_name.replace('YYYY',str(lyr_yr))

if yr == 2006:
    lyrs[3].visible = False
    lyrs[2].visible = True
else:
    lyrs[2].visible = False
    lyrs[3].visible = True

if overlay == 'State':
    lyrs[1].visible = True
    lyrs[0].visible = False
else:
    lyrs[0].visible = True
    lyrs[1].visible = False

if extent != None:
    ext = arcpy.Extent(extent[0],extent[1],extent[2],extent[3])
    df.extent = ext
else:
    pass

arcpy.mapping.ExportToPDF(mxd, r'C:\Users\markert\Desktop\markert_ess408\week12\example_outmap2.pdf')

    


