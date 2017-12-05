#********************************************************
# FILE: homework4.py
# AUTHOR: Melinda Pullman 
# EMAIL: mkp0015@uah.edu
# MODIFIED BY: n/a
# ORGANIZATION: UAH/ATS Dept.
# CREATION DATE: 04/20/2017
# LAST MOD DATE: n/a
# PURPOSE: This script downloads a storm events CSV file from
#          the storm events database FTP site, extracts the CSV
#          file from the zipped file, then makes an XY event layer
#          from the csv file data.
# DEPENDENCIES: os, ftplib, gzip, arcpy
#********************************************************

#import dependencies 
import os, ftplib
import gzip
import arcpy

#declare variables
destdir = r'C:\Users\mpullman\Desktop\ESS508\homework4'
filename = 'StormEvents_locations-ftp_v1.0_d2016_c20170419.csv.gz'

#login to FTP
ftp = ftplib.FTP('ftp.ncdc.noaa.gov', 'anonymous')

#change directory in FTP
ftp.cwd('pub/data/swdi/stormevents/csvfiles/')

#save file to local directory
local_file = os.path.join(destdir, filename)
ftp.retrbinary('RETR %s' % filename, open(local_file, 'wb').write)

#close connection to FTP
ftp.quit()

#extract csv from zipped file
infile = gzip.open(local_file, 'rb')
outfile = open('storm_events_2012.csv', 'wb')
outfile.write(infile.read())
infile.close()
outfile.close()

#output csv file name for arcpy input
csvfile = r'C:\Users\mpullman\Desktop\ESS508\homework4\storm_events_2012.csv'

#set arcpy environmental settings
arcpy.env.overwriteOutput = True

#create file geodatabase to store xy event layer
out_gdb = 'storm_events_manual.gdb'
arcpy.CreateFileGDB_management(destdir, out_gdb)

#make xy event layer for csv file
longitude = 'LONGITUDE'
latitude = 'LATITUDE'
sr = arcpy.SpatialReference('NAD 1983')
out_xy = csvfile + '_layer'
saved_xy_layer = csvfile + '.lyr'
saved_xy_shp = csvfile + '.shp'

arcpy.MakeXYEventLayer_management(csvfile, longitude, latitude, out_xy, sr)

#create output layer file
arcpy.SaveToLayerFile_management(out_xy, saved_xy_layer)

#copy layer file to shapefile
arcpy.CopyFeatures_management(saved_xy_layer, saved_xy_shp)

#move shapefile to file geodatabase
arcpy.FeatureClassToGeodatabase_conversion(saved_xy_shp, out_gdb)



