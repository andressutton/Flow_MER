import os
import sys
import glob
import joblib
import numpy as np
from osgeo import gdal, ogr, osr
from rios import applier, rat
from skimage.measure import block_reduce
from scipy import ndimage
from collections import OrderedDict



def get_mac_inund(info, inputs, outputs, otherargs):
    """
    This function is called from RIOS to calculate the the annual maximum extent. 
    """
    stack = np.array(inputs.we_list).astype(np.float32)
    wet_stack = stack[:, 0, :, :]
    
    wet_nodata = (stack[:, 0, :, :] >= 255)
    wet_stack[wet_stack < 0] = 0
    wet_stack[wet_stack == 3] = 0
    wet_stack = np.ma.masked_where(wet_nodata == 1, wet_stack)
    
    maxwater = np.max(wet_stack, axis = 0)
    maxwater_nodata = (maxwater >= 255)
    maxwater = np.ma.masked_where(maxwater_nodata == 1, maxwater)    
       
         
    outputs.stats = np.array([maxwater]).astype(np.float32)

dstDir = r'S:\SCI\BEES\All Staff\SPATIAL\Flow_MER\Inundationmaps\NarranLakes\2324' #input folder, where single date inundation maps sit. There should be one directory for each year.
imageList = glob.glob(os.path.join(dstDir, '*.tif'))
infiles = applier.FilenameAssociations()
infiles.we_list = imageList
outfiles = applier.FilenameAssociations()
otherargs = applier.OtherInputs()
controls = applier.ApplierControls()
controls.setWindowXsize(512)
controls.setWindowYsize(512)
controls.setStatsIgnore(255)
controls.setReferenceImage(infiles.we_list[25]) #Change number accordingly depending on the number of files in your directory, this setting is needed when there are inundation maps with different grids
controls.setCalcStats(True)
controls.setOutputDriverName("GTiff")
controls.setLayerNames(['inundation'])
outfiles.stats = r'C:\Users\z5368575\OneDrive - UNSW\Documents\Projects\MER_flow\Lower_Balone\GIS\max_narran_inund_2324.tif' #output folder
applier.apply(get_mac_inund, infiles, outfiles, otherArgs=otherargs, controls=controls)

print('Finished')