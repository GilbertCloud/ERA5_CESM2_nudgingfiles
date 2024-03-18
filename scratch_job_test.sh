#!/bin/bash -l
#PBS -N era5_split_6hour
#PBS -A UCUB0137
#PBS -q casper
#PBS -l walltime=24:00:00
#PBS -l select=1:ncpus=8:mpiprocs=1
#PBS -M glydia@ucar.edu

module load matlab
matlab

run scratch_test.io