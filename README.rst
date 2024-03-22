########
ERA5_CESM2_nudgingfiles
########
Code to process ERA5 data (U,V,T,Q) for use in nudging CESM2. 

Based on code written and process developed by Zac Espinosa (zespinosa97@gmail.com).

Modified and developed for processing large amounts of ERA5 data by Ash Gilbert (ash.gilbert@colorado.edu).

==========
Workflow for processing data
==========
#. Create a folder "nudging" in your scratch directory (or wherever you want to do the processing, but the storage required is usually large enough you want to use scratch space)
   * Create subfolders in "nudging" called "ERA5regrid", "ERA5_CESM2", and "tempFiles"
   * Load all necessary files from this repository into "nudging"

#. Modify filepath variables in all files to your filepaths and change project account information

#. Regrid ERA5 data from GLADE storage horizontially (0.9°x0.9°) and vertically (32 levels)
   ::

      qsub regridoriginal_job.sh

   * Script runs ``regrid_ERA5original_32.py``
   * Regridding 1 year of data takes between 10-12 hours on Casper, so usually process 1 year per script
   * It is possible to regrid more than one year at once, just change the year in the python script and resubmit the shell script

#. Split single files with 24 hours of data into 4 6-hourly file
   ::

      qsub scratch_job.sh

   * Script runs ``scratch_io.py``

#. Sanity check all CESM2 files
   ::

      python3 sanity_check_files.py

Notes:
***********
* 1 file containing 1 day's worth of data for 1 variable is 163 MB (after regridding in step 1)
* 1 year's worth of data for all four variables (U,V,T,Q) is 0.26 TB
* 1 file containing all four variables at a single timepoint is 28 MB (after splitting in step 2 - each day produces four of these)
* 1 year's worth of data for all four variables after step 2 is 41 GB

==========
Individual file descriptions
==========
Regridding files:
*************
* ``cdo_grid.txt``: text file that describes 0.9°x0.9° grid for the regridding process
* ``regrid_ERA5original_32.py``: Python script that does the horizontal regridding using ``cdo_grid.txt`` and the vertical pressure level interpolation (37 to 32 levels for CESM2)
* ``regridoriginal_job.sh``: shell script to submit ``regrid_ERA5original_32.py`` to Casper

Splitting files:
*************
* ``scratch_io.py``: Python script that combines all four variables (U,V,T,Q) into a single file and splits the file (containing 24 hours of data) into four files at 00 UTC, 06 UTC, 12 UTC, and 18 UTC
* ``scratch_job.sh``: shell script to submit ``scratch_io.py`` to Casper

Sanity checking file:
*************
* ``sanity_check_files.py``: Python script that checks whether all files have all four variables, 32 levels, regridded lat/lon dimensions, and that the file date and date save in the file match. The script will output a list of bad files and their respective problems.
