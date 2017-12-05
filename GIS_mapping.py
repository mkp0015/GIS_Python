#********************************************************
# FILE: mapping_assignment.py
# AUTHOR: Melinda Pullman
# EMAIL: mkp0015@uah.edu
# MODIFIED BY: n/a
# ORGANIZATION: UAH/ATS Dept.
# CREATION DATE: 03/30/2017
# LAST MOD DATE: n/a
# PURPOSE: This script illustrates how to utilize the Arcpy Mapping
#          module by addding map elements, changing map layers, and
#          editing map elements.
# DEPENDENCIES: arcpy
#********************************************************

#import modules
import arcpy

#pass variables into ArcGIS
yr = arcpy.GetParameterAsText(0)
overlay = arcpy.GetParameterAsText(1)

#define map document
mxd = arcpy.mapping.MapDocument(r'C:\Users\mpullman\Desktop\ESS508\mapping_assignment\map_template\map_template\ess408_map_template2.mxd')

#define Title
mxd.title ='Conus NDVI ' + str(yr)

#define map author name and affiliation
for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    elm.text = elm.text.replace('[YOUR NAME]', 'Melinda Pullman')

for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", 'Author'):
    elm.text = elm.text.replace('[YOUR AFFILIATION]', 'University of Alabama in Huntsville')
    y = elm.elementPositionY  
    elm.elementPositionX = 0.5
    
#define dataframe
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

#obtain layers in map document
lyrs = arcpy.mapping.ListLayers(df)

#replace NDVI YYYY with year of shapefile
ndvi_name = 'CONUS NDVI YYYY'

for i in range(len(lyrs)):
    if 'ndvi' in lyrs[i].name:
        lyr_yr = lyrs[i].name[-12:-8]
        lyrs[i].name = ndvi_name.replace('YYYY', str(lyr_yr))

#adjust visible layers
if yr == 2006:
    lyrs[5].visible = False
    lyrs[4].visible = True
else:
    lyrs[4].visible = False
    lyrs[5].visible = True

if overlay == 'County':
    lyrs[0].visible = True
    lyrs[1].visible = False
else:
    lyrs[1].visible = True
    lyrs[0].visible = False

#adjust legend size and position
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]
legend.elementWidth = 1
legend.elementPositionX = 9.3
legend.elementPositionY = 1

#adjust North arrow for 2006
if yr == 2006:
    arrow = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "North Arrow")[0]
    arrow.elementWidth = 0.5
    arrow.elementPositionX = 0.3
    arrow.elementPositionY = y - 0.8
#else:
    #pass 

#Export Final Map
arcpy.mapping.ExportToPDF(mxd, r'C:\Users\mpullman\Desktop\ESS508\mapping_assignment\map_template\example_outmap2.pdf')

