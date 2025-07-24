#!/usr/bin/env python
"""
Extracts water surface extent (%) time series for sites of interest
"""
import os, sys, glob
import numpy as np
from osgeo import ogr
from rios import applier


def get_water(info, inputs, outputs, otherargs):
    """
    Counts pixels in polygons.
    """
    water = inputs.water[0]
    poly = inputs.poly[0]
    polysPresent = np.unique(poly[poly != 0])
    if len(polysPresent) > 0:
        for p in polysPresent:
            otherargs.counts[0, p-1] += np.sum((poly == p) & (water == 1))
            otherargs.counts[1, p-1] += np.sum(poly == p)


def extract_waterarea(shapefile):
    """
    Uses RIOS to extract water area for wetland polygons and writes them to a CSV for each site
    """
    outdir = r'C:\Users\z5368575\OneDrive - UNSW\General - River flow and connectivity\data\waterbirds'
    
    # Read in ID values and Names from shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shapefile, 0)
    layer = dataSource.GetLayer()
    ID2Name = {}
    for feature in layer:
        ID = int(feature.GetField("OBJECTID"))
        Name = "NarranLakes_floodplain"
        ID2Name[ID] = Name
    layer.ResetReading()
    n = len(ID2Name)
    
    # Iterate over ID values creating csv files to save results
    for ID in range(1, n+1):
        Name = ID2Name[ID]
        outfile = os.path.join(outdir, 'waterarea_%s.csv'%(Name))
        with open(outfile, 'w') as f:
            f.write('ID,Date,Water_area_percent,Pixel_count\n')
    
    # Iterate over innudation images
    for imagefile in glob.glob(r"C:\Users\z5368575\OneDrive - UNSW\General - River flow and connectivity\data\dea\inundation maps\narran*.tif"):
        date = imagefile.replace(r".tif", "").split(r"_")[1]
        
        print(date)
        
        infiles = applier.FilenameAssociations()
        outfiles = applier.FilenameAssociations()
        otherargs = applier.OtherInputs()
        controls = applier.ApplierControls()
        controls.setBurnAttribute("OBJECTID")
        infiles.water = imagefile
        infiles.poly = shapefile
        otherargs.counts = np.zeros((2, n), dtype=np.uint64)
        applier.apply(get_water, infiles, outfiles, otherArgs=otherargs, controls=controls)
        
        for i, ID in enumerate(range(1, n+1)):
            Name = ID2Name[ID]
            waterpixels = otherargs.counts[0, i]
            totalpixels = otherargs.counts[1, i]
            if totalpixels > 0:
                water_percent = 100 * (waterpixels / totalpixels)
            else:
                water_percent = -999
            outfile = os.path.join(outdir, 'waterarea_%s.csv'%(Name))
            with open(outfile, 'a') as f:
                f.write('%s,%s,%.2f,%i\n'%(ID, date, water_percent, totalpixels))

# Get water area data
shapefile = r"C:\Users\z5368575\OneDrive - UNSW\Documents\Projects\MER_flow\Lower_Balone\GIS\Narran_Lakes_floodplain_v2-2015.shp" #path to shapefile with sites of interest
extract_waterarea(shapefile)