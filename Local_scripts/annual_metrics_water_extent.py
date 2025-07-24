import os
import sys
import glob
import joblib
import datetime
import numpy as np
from numba import njit
from osgeo import gdal, ogr, osr
from rios import applier, rat
from rios import cuiprogress
from skimage.measure import block_reduce
from scipy import ndimage
from collections import OrderedDict




def get_inund_metrics(info, inputs, outputs, otherargs):
"""
This function calculates longest inundation period duration and date of start (in number of days since start of the water year) from a stack of inundation images
"""
    
    stack = np.array(inputs.we_list).astype(np.float32)
    wet_stack = stack[:, 0, :, :]
    
       
    wet_nodata = (stack[:, 0, :, :] >= 255)
    wet_stack[wet_stack < 0] = 0
    wet_stack[wet_stack == 3] = 0
    wet_stack = np.ma.masked_where(wet_nodata == 1, wet_stack)
    dateList = []
    
    
      
    diff = np.diff(wet_stack, axis=0)
    
    height, width = wet_stack.shape[1], wet_stack.shape[2]
    starts = np.zeros((height, width), dtype=int)
    ends = np.zeros((height, width), dtype=int)
    

    for imagefile in imageList:
        date = imagefile.replace(r".tif", "").split(r"_")[2]
        dateList.append(date)    
    wet_stack_dates = np.array([datetime.date(year=int(str(x)[0:4]),
                                        month=int(str(x)[4:6]), day=int(str(x)[6:8]))
                                        for x in dateList])
                                        
    time_delta = wet_stack_dates - datetime.date(2022, month = 7, day= 1) #change year according to input data
    
    times = np.array([td.days for td in time_delta])
    
    time_difference_array = np.full((height, width), np.nan, dtype=np.float32)
    start_time_array = np.full((height, width), np.nan, dtype=np.float32)
    
    for y in range(height):
        for x in range(width):
            starts_pixel = np.where(diff[:, y, x] == 1)[0] + 1
            ends_pixel = np.where(diff[:, y, x] == -1)[0] + 1
    
            if wet_stack[0, y, x]:
                starts_pixel = np.insert(starts_pixel, 0, 0)
            if wet_stack[-1, y, x]:
                ends_pixel = np.append(ends_pixel, len(wet_stack))
    
            if len(starts_pixel) == 0 or len(ends_pixel) == 0:
                continue
    
            if len(starts_pixel) != len(ends_pixel):
                min_len = min(len(starts_pixel), len(ends_pixel))
                starts_pixel = starts_pixel[:min_len]
                ends_pixel = ends_pixel[:min_len]
    
            lengths_pixel = ends_pixel - starts_pixel
            if lengths_pixel.size == 0:
                continue
    
            idx_pixel = np.argmax(lengths_pixel)
            start_idx_pixel = starts_pixel[idx_pixel]
            end_idx_pixel = ends_pixel[idx_pixel] - 1
    
            start_time_pixel = times[start_idx_pixel]
            end_time_pixel = times[end_idx_pixel]
    
            if end_time_pixel > start_time_pixel:
                time_difference_pixel = (end_time_pixel + 1) - start_time_pixel
            else:
                time_difference_pixel = 365 - start_time_pixel
    
            time_difference_array[y, x] = time_difference_pixel
            start_time_array[y, x] = start_time_pixel

    combined_array = np.array([time_difference_array, start_time_array]).astype(np.float32)
    outputs.stats = combined_array

dstDir = r'S:\SCI\BEES\All Staff\SPATIAL\Flow_MER\Inundationmaps\NarranLakes' #input folder, where single date inundation maps sit. There should be one directory for each year.
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
controls.setLayerNames(['Duration','Start_date'])
outfiles.stats = r'C:\Users\z5368575\OneDrive - UNSW\General - River flow and connectivity\data\nsw_inundation_maps\annual_water_metrics\NarranLakes_inund_2223.tif' #output folder
controls.setProgress(cuiprogress.CUIProgressBar())
applier.apply(get_inund_metrics, infiles, outfiles, otherArgs=otherargs, controls=controls)

print('Finished')
