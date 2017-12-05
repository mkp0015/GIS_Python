#********************************************************
# FILE: python2.3.py
# AUTHOR: Melinda Pullman
# EMAIL: mkp0015@uah.edu
# MODIFIED BY: n/a
# ORGANIZATION: UAH/ATS Dept.
# CREATION DATE: 03/09/2017
# LAST MOD DATE: n/a
# PURPOSE: This script takes an input DEM dataset and creates
#          a Height Above Nearest Drainage (HAND) model that measures
#          elevation relative to the nearest streams (height of elevation
#          above nearest stream channel instead of above mean sea level.
# DEPENDENCIES: arcpy
#********************************************************

#import packages
import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')

#defining main level program
def main():
    """
    FUNCTION: main()
    ARGUMENTS: n/a
    KEYWORDS: n/a
    RETURNS: n/a
    NOTES: main level program for testing
    """

    #pass ArcGIS variable as text
    demfile = arcpy.GetParameterAsText(0)
    str_thresh = arcpy.GetParameterAsText(1)
    outHandfile = arcpy.GetParameterAsText(2)
    
    #read in data for dem
    dem = arcpy.Raster(demfile)
    
    #filling DEM - creates a more continuous flow path for spatial hydrology modeling #will get rid of sinks - missing data / peaks - data that is too high
    #you will always want to fill your DEMs!
    dem_fill = Fill(dem)

    #calculate flow direction - identifies where water will flow cell-to-cell (from high to lower cells)
    flow_dir = FlowDirection(dem_fill, "NORMAL")

    #calculate flow accumulation - identifies how many cells will flow "through" the cell based on upstream flow direction
    flow_accum = FlowAccumulation(flow_dir)

    #extract stream network from flow accumulation raster (more cells flowing through raster == more water / bigger streams)
    #str_thresh = 1000
    streams = SetNull(flow_accum,1,"value<{0}".format(str_thresh))

    #extract elevation at points along stream network - use extract by mask tool
    str_elev = ExtractByMask(dem_fill, streams)

    #derive watershed for each stream point - find area where water flows into each point along stream
    str_watersheds = Watershed(flow_dir, str_elev)

    #subtract stream elevation for each stream point watershed 
    hand = dem_fill - str_watersheds

    #save the HAND model
    outfile = outHandfile
    hand.save(outfile)

    #clean up/delete temporary raster files for the sytem
    del dem, dem_fill, flow_dir, flow_accum, streams, str_elev, str_watersheds, hand

    return

#main level check
if __name__ == "__main__":
    main()
    
