#read in packages
import arcpy
from arcpy.sa import *

#read in dem Huntsville file
dem = arcpy.Raster('C:/Users/mpullman/Desktop/n34_w087_1arc_v2_utm.tif')
                   
#gather info on file
desc = arcpy.Describe(dem)

print 'raster file name: ' + desc.basename
print 'raster data type: ' + desc.dataType
print 'raster file extension: ' + desc.extension

#gathering spatial information
xSize = desc.meanCellWidth
ySize = desc.meanCellHeight
mapUnits = desc.spatialReference.linearUnitName
print 'the raster resolution is {0} by {1} {2}.'.format(xSize,ySize,mapUnits)

#calculate raster extent
pt1 = arcpy.Point(546378, 3816214)
pt2 = arcpy.Point(485366, 3803126)
print dem.extent.contains(pt1) #data point falls within raster extent (true)
print dem.extent.contains(pt2) #data point falls outside raster extent (false)

#check out spatial extension for raster operation b/c we are in IDLE (must turn on ArcGIS extensions)
arcpy.CheckOutExtension('Spatial')

dem_ft = dem*3.281 #convert meters to feet, automatically returns raster obj b/c raster multiplication
high_elev = dem_ft > 600

#saving raster objects as data b/c data is currently saved in arcpy temporary memory
high_elev.save('C:/Users/mpullman/Desktop/high_elev_raster5.tif')

#delete temporary raster variable and data on hard disk
del high_elev

#pass DEM raster obj into ArcGIS tool to get results
slope = arcpy.sa.Slope(dem, "DEGREE")
slope.save('C:/Users/mpullman/Desktop/slope_out2.tif')

#reclassifying rasters
myremap = RemapRange([[0,5,1], [5,10,2],[10,30,3],[30,90,4]]) #remap range - what ranges of input values should be used to reclassify to in an output raster
outreclass = arcpy.sa.Reclassify(slope, "VALUE", myremap, "NODATA")
outreclass.save('C:/Users/mpullman/Desktop/slope_reclass1.tif')

#can speed up processing by using raster datasets as Numpyarrays
#convert raster objects to numpy arrays
#create spatial extent data
lowerLeft = arcpy.Point(dem.extent.XMin, dem.extent.YMin)
cellSize = dem.meanCellWidth

#loading spatial extent data into an array and save out the data
dem_arr = arcpy.RasterToNumPyArray(dem, nodata_to_value=0)
out_dem = dem_arr**2
out_ras = arcpy.NumPyArrayToRaster(out_dem, lowerLeft, cellSize, cellSize, value_to_nodata=0) #requires the spatial information to be input
out_ras.save('C:/Users/mpullman/Desktop/dem_arr.tif')
