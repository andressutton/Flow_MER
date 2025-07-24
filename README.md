# Flow_MER
This is a collection of notebooks and scripts for processing and analysing remotely sensed surface water extent/inundation data.

## DEA notebooks
These are Jupyter notebooks that run in Digital Earth Australia's (DEA) **[Sandbox Environment](https://app.sandbox.dea.ga.gov.au/)**. Examples in this folder
use Sentinel-2 data to obtain images of water extent and annual inundation dynamic metrics: longest inundation period duration and date of start (in number 
of days since start of the water year)


## Local notebooks
These are Jupyter notebooks that can be un locally, in Github Codespaces (requirements.txt file in this repository has the environment requirements to run 
the notebooks), Google Colab, etc. Examples in this folder use DEA's Landsat data to obtain images of seasonal maximum water extent and inundation dynamic 
metrics (longest inundation period duration -in number of days- and date of start -in number of days since start of the water year-).


## Local scripts
These are Python scripts for processing inundation maps (i.e., raster images with pixel values 1=water, 0=dry). Examples in this folder include code to
extract and plot time series water extent (%) for sites of interest; process single date inundation maps into annual maximum extent or annual inundation dynamic
metrics (longest inundation period duration -in number of days- and date of start -in number of days since start of the water year-) and extract these data for
areas of interest.
