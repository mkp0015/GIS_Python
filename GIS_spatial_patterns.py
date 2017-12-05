#********************************************************
# FILE: homework3.py
# AUTHOR: Melinda Pullman 
# EMAIL: mkp0015@uah.edu
# MODIFIED BY: n/a
# ORGANIZATION: UAH/ATS Dept.
# CREATION DATE: 03/23/2017
# LAST MOD DATE: n/a
# PURPOSE: This script takes an input NDVI tif file and an input
#          census shapefile for the United States then derives
#          metrics that compare the census and ndvi data to analyze
#          with spatial pattern tools.
# DEPENDENCIES: arcpy
#********************************************************

#import packages
import arcpy
from arcpy.sa import*

#check out required extensions
arcpy.CheckOutExtension('Spatial')

#declare variables
workspace = r'C:\Users\mpullman\Desktop\ess508'
ndvi = r'C:\Users\mpullman\Desktop\ESS508\homework3\ndvi\modis_conus_ndvi2006_int.tif'
census = r'C:\Users\mpullman\Desktop\ESS508\homework3\CONUS_County_Census\County_2010Census_CONUS.shp'

#out_table = r'C:\Users\mpullman\Desktop\ess508\out_table06.dbf'
#census_joined = r'C:\Users\mpullman\Desktop\ess508\census_joined.shp'

#out_hs_shp = r'C:\Users\mpullman\Desktop\ess508\hotspot.shp'
#out_hs_shp1 = r'C:\Users\mpullman\Desktop\ess508\hotspot1.shp'
#out_hs_shp2 = r'C:\Users\mpullman\Desktop\ess508\hotspot2.shp'

#environmental settings
arcpy.env.overwriteOutput = 'True'
arcpy.env.workspace = workspace

#define rasters from NDVI tif files
ndvi_raster = arcpy.Raster(ndvi)

#zonal statistics as table
out_table = 'out_table06.dbf'
outStats = arcpy.sa.ZonalStatisticsAsTable(census, 'FID', ndvi_raster, out_table, ignore_nodata = 'DATA', statistics_type='ALL')

#join table to shapefile
census_joined = 'census_joined.shp'
joinshp = arcpy.JoinField_management(census, 'FID', outStats, 'OID')
arcpy.CopyFeatures_management(joinshp, census_joined)

#project shapefile into projected coordinate system
census_prj = census_joined[:-4]+'_prj.shp'
arcpy.Project_management(census_joined, census_prj, arcpy.SpatialReference('North America Albers Equal Area Conic'))

#calculate shapefile county area
arcpy.AddField_management(census_prj, field_name='area_true', field_type='FLOAT')
arcpy.CalculateField_management(census_prj, 'area_true', "float(!SHAPE.AREA!) / 1E6", "PYTHON")


#compare total population to mean NDVI normalized by population density
arcpy.AddField_management(census_prj, field_name='ageNDVI', field_type='FLOAT')
arcpy.CalculateField_management(census_prj, 'ageNDVI', '(!MEAN! / !DP0010006!)', "PYTHON")

#compare male population to mean NDVI normalized by total population
arcpy.AddField_management(census_prj, field_name='maleNDVI', field_type='FLOAT')
arcpy.CalculateField_management(census_prj, 'maleNDVI', '(!MEAN! / !DP0030002! )', "PYTHON")

#compare total hispanic ethnicity to mean NDVI normalized by total population
arcpy.AddField_management(census_prj, field_name='his_NDVI', field_type='FLOAT')
arcpy.CalculateField_management(census_prj, 'his_NDVI', '(!MEAN! / !DP0180002!)', "PYTHON")

#hotspot analysis
out_ageNDVI = workspace + 'out_ageNDVI.shp'
out_maleNDVI = workspace + 'out_maleNDVI.shp'
out_hisNDVI = workspace + 'out_hisNDVI.shp'
arcpy.HotSpots_stats(census_prj, 'ageNDVI', out_ageNDVI)
arcpy.HotSpots_stats(census_prj, 'maleNDVI', out_maleNDVI)
arcpy.HotSpots_stats(census_prj, 'his_NDVI', out_hisNDVI)

