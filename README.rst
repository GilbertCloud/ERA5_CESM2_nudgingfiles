########
ERA5_CESM2_nudgingfiles
########
Code to process ERA5 data (U,V,T,Q) for use in nudging CESM2. The test files process 1 year of data.

Based on code written and process developed by Zac Espinosa (zespinosa97@gmail.com).

==========
Workflow for processing data
==========
1) Download hourly ERA5 data into scratch
   ::

      qsub download_job.sh

2) Regrid horizontially (0.9°x0.9°) and vertically (32 levels)
   ::

      qsub regridoriginal_job.sh

3) Split single files with 24 hours of data into 4 6-hourly file\
   ::

      module load matlab; matlab
      run scratch.io

4) Sanity check all CESM2 files
   ::

      python3 sanity_check_files.py

