#!/usr/bin/env python
"""

This extracts annual inundation metrics (i.e., number of days and julian date of 
start of the longest inundated period) data for sites of interest (e.g., vegetation 
survey points, waterbird survey polygons)

"""


import os
import sys
import glob
import numpy as np
from osgeo import gdal, ogr
from rios import applier
from rios import rat
from scipy import ndimage
from datetime import datetime

"""
Extracts the mean and standard deviation of annual inundation metrics for each 
polygon in the input shapefile. The shapefile needs to have an attribute called 
"Id" which has a unique integer for each site. It should also be in the same 
coordinate reference system as the image data, which is EPSG:3577, or in ArcGIS 
this is defined as GDA_1994_Australia_Albers.
"""


def getPixels(info, inputs, outputs, otherargs):
    """
    Gets metrics from the pixels within a certain site or sites 
    """
    sites = inputs.sites[0]
    for idvalue in np.unique(sites[sites != 0]):
        singlesite = (sites == idvalue)
        im = inputs.im
        nodataPixels = (im[0] == 'nan')
        duration = im[0][singlesite]
        start = im[1][singlesite]
        nodata = nodataPixels[singlesite]
        duration = duration[nodata == 0]
        start = start[nodata == 0]
        with open(otherargs.csvfile, 'a') as f:
            line = '%i,%s'%(idvalue, otherargs.date)
            if duration.size > 0:
                line = '%s,%i'%(line, duration.size)
                line = '%s,%.2f'%(line, np.mean(duration))
                line = '%s,%.2f\n'%(line, np.mean(start))
            else:
                line = '%s,999'%line
                line = '%s,999,999'%line
                line = '%s,999,999\n'%line
            f.write(line)


def extract_pixels(polyfile, imagefile, csvfile):
    """
    This sets up RIOS to extract pixel statistics for the points.
    """
    # Extract the pixels
    infiles = applier.FilenameAssociations()
    outfiles = applier.FilenameAssociations()
    otherargs = applier.OtherInputs()
    controls = applier.ApplierControls()
    controls.setBurnAttribute("Site_Code")
    controls.setAlltouched(True)
    controls.setVectorDatatype(np.int_)
    controls.setReferenceImage(imagefile)
    controls.setFootprintType(applier.BOUNDS_FROM_REFERENCE)
    controls.setWindowXsize(512)
    controls.setWindowYsize(512)
    infiles.sites = polyfile
    infiles.im = imagefile
    otherargs.csvfile = csvfile
    otherargs.date = os.path.basename(imagefile).split('_')[4][0:4]
    applier.apply(getPixels, infiles, outfiles,
                  otherArgs=otherargs, controls=controls)


# Get imageList
imageDir = r'C:\Users\z5368575\OneDrive - UNSW\General - Flow MER2.0 LB and MM\Lower Balonne Selected Area\River Connectivity and Hydrology\GIS\annual water metrics\Sentinel-2\DEA' #path to 
imageList = glob.glob(os.path.join(imageDir, "*.tif"))

# Write the csvfile header
csvfile = r'vegsite_inundation_extracts.csv' #output csv
with open(csvfile, 'w') as f:
    f.write('Id,date,pixels,'+
            'duration,start\n')

# Iterate over images and get pixel values
polyFile = (r"C:\Users\z5368575\OneDrive - UNSW\Documents\Projects\MER_flow\Lower_Balone\GIS\Narran_survey_points_proj.shp") #path shapefile with sites to extract annual water metric data
for imagefile in imageList:
    extract_pixels(polyFile, imagefile, csvfile)