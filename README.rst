########
ERA5_CESM2_nudgingfiles
########
Code to process ERA5 data (U,V,T,Q) for use in nudging CESM2. 

Based on code written and process developed by Zac Espinosa (zespinosa97@gmail.com).

Modified and developed for processing large amounts of ERA5 data by Ash Gilbert (ash.gilbert@colorado.edu).

==========
Workflow for processing data
==========
#. Regrid ERA5 data from GLADE storage horizontially (0.9°x0.9°) and vertically (32 levels)
   ::

      qsub regridoriginal_job.sh

   * Script runs regrid_ERA5original_32.py

#. Split single files with 24 hours of data into 4 6-hourly file
   ::

      qsub scratch_job.sh

   * Script runs scratch_io.py

#. Sanity check all CESM2 files
   ::

      python3 sanity_check_files.py

Notes:
***********
* 1 file containing 1 day's worth of data for 1 variable is 163 MB (After regridding in step 1)
* 1 year's worth of data for all four variables (U,V,T,Q) is 0.26 TB
* Recommended that only process 10 years of data at a time
* DO NOT run more than one regridoriginal_job at a time because it uses a temp variable
