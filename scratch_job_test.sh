#!/bin/bash -l
#PBS -N era5_split_6hour
#PBS -A UCUB0137
#PBS -q casper
#PBS -l walltime=24:00:00
#PBS -l select=1:ncpus=8:mpiprocs=1
#PBS -M glydia@ucar.edu

module load conda
conda activate cenv

python3 /glade/derecho/scratch/glydia/inputdata/nudging/scratch_io_test.py