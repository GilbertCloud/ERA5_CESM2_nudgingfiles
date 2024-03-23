#!/bin/bash -l
#PBS -N era5_sanity_check
#PBS -A UCUB0137
#PBS -q casper
#PBS -l walltime=01:30:00
#PBS -l select=1:ncpus=8:mpiprocs=1
#PBS -M glydia@ucar.edu

module load conda
conda activate cenv

python3 /glade/derecho/scratch/glydia/inputdata/nudging/sanity_check_files.py