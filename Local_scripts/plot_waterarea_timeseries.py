#!/usr/bin/env python
"""
Create time series figures of water extent using the CSVs created with extract_water_area.py

"""
import os
import sys
import glob
import datetime
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

params = {'text.usetex': False, 'mathtext.fontset': 'stixsans',
          'xtick.direction': 'out', 'ytick.direction': 'out',
          'font.sans-serif': "Arial"}
plt.rcParams.update(params)


# Get matching csv files for sites
waterCSVdir = r"C:\Users\z5368575\OneDrive - UNSW\General - Flow MER2.0 LB and MM\Lower Balonne Selected Area\Waterbirds\water_extent_surveysites\2024-2025" #folder with CSVs
waterCSVs = glob.glob(os.path.join(waterCSVdir, "rookery_waterarea*.csv")) #file name that identifies the list of CSVs with data to plot
wetlandAreas = [os.path.basename(x).replace(".csv", "").replace("rookery_waterarea", "rookery") for x in waterCSVs]


# Iterate over wetland areas
nameList = []
areaList = []
climateList = []
fireSeasonList = []
pvSeasonList = []
npvSeasonList = []
for i, wetlandArea in enumerate(wetlandAreas):
    
    nameList.append(wetlandAreas)
    
    # Read in water area data
    # Columns are ID, Date, Water_area_percent, Pixel_count
    waterData = np.genfromtxt(waterCSVs[i], names=True, delimiter=',')
    waterDates = np.array([datetime.date(year=int(str(x)[0:4]),
                                        month=int(str(x)[4:6]), day=int(str(x)[6:8]))
                                        for x in waterData["Date"]])
    
        
    # Create figure of water extent time series
    fig = plt.figure(i)
    fig.set_size_inches((8, 2))
    area = " ".join(wetlandArea.split('_')[0:-1])
    if area == 'NAR':
        area = 'Narran Waterbird Survey'
    areaList.append(area)
    climate = wetlandArea.split('_')[-1]
    climateList.append(climate)
    fig.text(0.07, 0.9, "rookery_%s"%(climate),fontsize=14)
    ax1 = plt.axes([0.07, 0.15, 0.78, 0.6])
    ax1.set_xlim((datetime.date(2024, month=7, day=1),
                  datetime.date(2025, month=2, day=28)))

    # Line graph of wet area
    ax1.set_ylabel('Water extent (%)')  
    ax1.plot(waterDates, waterData["Water_area_percent"], color='blue',linewidth=1, alpha=0.5)
    if np.max(waterData["Water_area_percent"]) < 100.0:
        ax1.set_ylim((0.0, 100.0))
    ax1.axvline(x=datetime.date(2024, month=8, day=15), ymin=0, ymax=100, color='black',linewidth=1, alpha=0.5, label = 'S1')
    ax1.axvline(x=datetime.date(2024, month=10, day=30), ymin=0, ymax=100, color='black',linewidth=1, alpha=0.5, label = 'S2')
    ax1.axvline(x=datetime.date(2024, month=12, day=13), ymin=0, ymax=100, color='black',linewidth=1, alpha=0.5, label = 'S3')
    ax1.axvline(x=datetime.date(2025, month=2, day=20), ymin=0, ymax=100, color='black',linewidth=1, alpha=0.5, label = 'S4')
    plt.text(datetime.date(2024, month=8, day=12),101,'S1')
    plt.text(datetime.date(2024, month=10, day=27),101,'S2')
    plt.text(datetime.date(2024, month=12, day=10),101,'S3')
    plt.text(datetime.date(2025, month=2, day=17),101,'S4')
    
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
   
    # Put legend at the top
    axLeg = plt.axes([0, 0.85, 1, 0.15], frameon=False)
    axLeg.set_xlim((0, 100))
    axLeg.set_ylim((0, 2))
    axLeg.set_xticks([])
    axLeg.set_yticks([])
    
    
    outDir = r"C:\Users\z5368575\OneDrive - UNSW\General - Flow MER2.0 LB and MM\Lower Balonne Selected Area\Waterbirds\water_extent_surveysites\2024-2025" #output folder path
    plt.savefig(os.path.join(outDir, r'%s.png'%wetlandArea), dpi=300)
    plt.close(fig)
    
