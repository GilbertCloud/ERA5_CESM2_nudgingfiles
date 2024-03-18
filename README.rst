########
ERA5_CESM2_nudgingfiles
########
Code to process ERA5 data (U,V,T,Q) for use in nudging CESM2. 

Based on code written and process developed by Zac Espinosa (zespinosa97@gmail.com).

==========
Workflow for processing data
==========
#. Download hourly ERA5 data into scratch
   ::

      qsub download_job.sh

#. Regrid horizontially (0.9°x0.9°) and vertically (32 levels)
   ::

      qsub regridoriginal_job.sh

#. Split single files with 24 hours of data into 4 6-hourly file\
   ::

      module load matlab; matlab
      run scratch.io

#. Sanity check all CESM2 files
   ::

      python3 sanity_check_files.py

Notes:
***********
* 1 file containing 1 day's worth of data for 1 variable is 1.8 GB
* 1 year's worth of data for all four variables (U,V,T,Q) is 2.6 TB
* Recommended that only process 1 year of data at a time
