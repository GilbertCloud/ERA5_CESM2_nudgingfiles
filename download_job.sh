#!/bin/bash -l
#PBS -N era5_download
#PBS -A UCUB0137
#PBS -q casper
#PBS -l walltime=06:00:00
#PBS -l select=1:ncpus=8:mpiprocs=1
#PBS -M glydia@ucar.edu

module load conda
conda activate cenv

python /glade/derecho/scratch/glydia/inputdata/nudging/ERA5original/download_realtime.py
