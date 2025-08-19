# Flow_MER
This is a collection of notebooks and scripts for processing and analysing remotely sensed surface water extent/inundation data.

## DEA notebooks
These are Jupyter notebooks that run in Digital Earth Australia's (DEA) **[Sandbox Environment](https://app.sandbox.dea.ga.gov.au/)**. 

-[LS_annualmax_waterextent.ipynb](https://github.com/andressutton/Flow_MER/blob/main/DEA_notebooks/LS_annualmax_waterextent.ipynb) Create annual maximum water 
extent maps for from Landsat surface reflectance using a Water Index.

-[S2_annual_metrics.ipynb](https://github.com/andressutton/Flow_MER/blob/main/DEA_notebooks/S2_annual_metrics.ipynb): Creates a raster of annual inundation dynamic 
metrics (longest inundation period duration -in number of days- and date of start -in number of days since start of the water year-) from Sentinel-2 surface 
reflectance data using a Water Index. 

-[S2_water_extent.ipynb](https://github.com/andressutton/Flow_MER/blob/main/DEA_notebooks/S2_water_extent.ipynb): Create water extent maps for a series of dates 
from Sentinel-2 surface reflectance using a Water Index.

## Local notebooks
These are Jupyter notebooks that can be run locally, in Github Codespaces (requirements.txt file in this repository has the environment requirements to run 
the notebooks), Google Colab, etc. 

-[LS_annual_metrics.ipynb](https://github.com/andressutton/Flow_MER/blob/main/Local_notebooks/LS_annual_metrics.ipynb): Creates a raster of annual inundation dynamic 
metrics (longest inundation period duration -in number of days- and date of start -in number of days since start of the water year-) from Landsat isurface reflectance 
data using a Water Index.

-[LS_seasonalmax_waterextemt.ipynb](https://github.com/andressutton/Flow_MER/blob/main/Local_notebooks/LS_seasonalmax_waterextemt.ipynb): Create seasonal maximum water 
extent maps for from Landsat surface reflectance using a Water Index.

## Local scripts
These are Python scripts for processing inundation maps (i.e., raster images with pixel values 1=water, 0=dry). 

-[Site_annualwatermetric_extract.py](https://github.com/andressutton/Flow_MER/blob/main/Local_scripts/Site_annualwatermetric_extract.py): extracts time series of annual inundation dynamic metrics into CSV files for sites of interest.

-[annual_max_water_extent.py](https://github.com/andressutton/Flow_MER/blob/main/Local_scripts/annual_max_water_extent.py): Create annual maximum water extent maps for
a series of inundation/water extent maps.

-[annual_metrics_water_extent.py](https://github.com/andressutton/Flow_MER/blob/main/Local_scripts/annual_metrics_water_extent.py): Creates a raster of annual inundation 
dynamic metrics (longest inundation period duration -in number of days- and date of start -in number of days since start of the water year-) from a series of inundation/
water extent maps.

-[extract_water_area.py](https://github.com/andressutton/Flow_MER/blob/main/Local_scripts/extract_water_area.py): Extracts time series of water extent (%) into CSV files
for sites of interest.

-[plot_waterarea_timeseries.py](https://github.com/andressutton/Flow_MER/blob/main/Local_scripts/plot_waterarea_timeseries.py): Creates graphs of water extent (%) time
series from CSV files.
