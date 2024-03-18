import os
import numpy as np
import xarray as xr
from tqdm.contrib.concurrent import thread_map

CESM1levels = [3.64346569404006,7.59481964632869,14.3566322512925,24.6122200042009,38.2682997733355,54.5954797416925,72.0124505460262,87.8212302923203,103.317126631737,121.547240763903,142.994038760662,168.225079774857,197.908086702228,232.828618958592,273.910816758871,322.241902351379,379.100903868675,445.992574095726,524.687174707651,609.778694808483,691.389430314302,763.404481112957,820.858368650079,859.53476652503,887.020248919725,912.644546944648,936.198398470879,957.485479535535,976.325407391414,992.556095123291]

# CESM2levels = [3.643466,7.59482 ,  14.356632,  24.61222 ,  35.92325 ,  43.19375 , 51.677499,  61.520498,  73.750958,  87.82123 , 103.317127, 121.547241, 142.994039, 168.22508 , 197.908087, 232.828619, 273.910817, 322.241902, 379.100904, 445.992574, 524.687175, 609.778695, 691.38943 , 763.404481, 820.858369, 859.534767, 887.020249, 912.644547, 936.198398, 957.48548 ,976.325407, 992.556095]

CESM2levels = [ 3.64346569404006, 7.59481964632869, 14.3566322512925,
    24.6122200042009, 35.9232500195503, 43.1937500834465, 51.6774989664555,
    61.5204982459545, 73.7509578466415, 87.8212302923203, 103.317126631737,
    121.547240763903, 142.994038760662, 168.225079774857, 197.908086702228,
    232.828618958592, 273.910816758871, 322.241902351379, 379.100903868675,
    445.992574095726, 524.687174707651, 609.778694808483, 691.389430314302,
    763.404481112957, 820.858368650079, 859.53476652503, 887.020248919725,
    912.644546944648, 936.198398470879, 957.485479535535, 976.325407391414,
    992.556095123291
]

#years = list(np.arange(1950, 1979))
years = list(np.arange(1950, 2024))

day = [
    '01', '02', '03',
    '04', '05', '06',
    '07', '08', '09',
    '10', '11', '12',
    '13', '14', '15',
    '16', '17', '18',
    '19', '20', '21',
    '22', '23', '24',
    '25', '26', '27',
    '28', '29', '30',
    '31'
]

time = [
    '00000',
    '21600',
    '43200',
    '64800',
]


month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#month = ['08', '09']
#month = ['10', '11', '12']


SAVE_PATH = '/glade/derecho/scratch/glydia/inputdata/nudging/ERA5_CESM2/'

nlat = 192
nlon =288
nlev = 32

def copy_files(arg):
    ctime, cday, cmonth, cyr = arg

    outFile = f"ERA5.6hour.32level.uvtq.{cyr}-{cmonth}-{cday}-{ctime}.nc"
    fullPath = os.path.join(SAVE_PATH, outFile)

    if os.path.isfile(fullPath):
        print(outFile, " already exists")
        return False

    try:
        #cfile = os.path.join("/glade/scratch/wriggles/code_nudgefiles/ERA5", f'ERA5.6hour.30level.uvtq.{cyr}-{cmonth}-{cday}-{ctime}.nc')
        cfile = os.path.join("/glade/derecho/scratch/glydia/inputdata/nudging/ERA5", f'ERA5.6hour.30level.uvtq.{cyr}-{cmonth}-{cday}-{ctime}.nc')

        if not os.path.isfile(cfile):
            print(cfile, "does not exist")
            return False


        print("Copying: ", cfile)

        # Open and add coordinate labels to vertical levels
        df = xr.open_dataset(cfile).load()
        df['lev'] = CESM1levels

        df['U'].attrs['long_name'] = 'Zonal wind'
        df['U'].attrs['units'] = 'm/s'

        df['V'].attrs['long_name'] = 'Meridional wind'
        df['V'].attrs['units'] = 'm/s'

        df['T'].attrs['long_name'] = 'Temperature'
        df['T'].attrs['units'] = 'K'

        df['Q'].attrs['long_name'] = 'Specific humidity'
        df['Q'].attrs['units'] = 'kg/kg'

        df['lon'].attrs['long_name'] = 'longitude'
        df['lon'].attrs['units'] = 'degrees_east'

        df['lat'].attrs['long_name'] = 'latitude'
        df['lat'].attrs['units'] = 'degrees_north'

        # Set the 'var' variable to float32 type in the encoding dictionary
        encoding = {'U': {'dtype': np.float32}, 'V': {'dtype': np.float32}, 'T': {'dtype': np.float32}, 'Q': {'dtype': np.float32}}

        # Save the dataset to a NetCDF file
        df.to_netcdf(f'tempFiles/temp0-{cyr}-{cmonth}-{cday}-{ctime}.nc', encoding=encoding)
        df.close()
        return True

    except Exception as e:
        print(e)
        print(f'Interpolate failed for {ctime}, {cday}, {cmonth}, {cyr}')
        return False

def interpolate_data(arg):
    try:
        ctime, cday, cmonth, cyr = arg

        outFile = f"ERA5.6hour.32level.uvtq.{cyr}-{cmonth}-{cday}-{ctime}.nc"

        print("Interpolating to: ", outFile)
        fullPath = os.path.join(SAVE_PATH, outFile)

        if os.path.isfile(fullPath):
            print(outFile, " already exists")
            return

        # Regrid x and y
        os.system(f"cdo -L -f nc4 -remapbil,cdo_grid.txt -setgridtype,regular tempFiles/temp0-{cyr}-{cmonth}-{cday}-{ctime}.nc tempFiles/temp1-{cyr}-{cmonth}-{cday}-{ctime}.nc")
        # Interpolate vertical levels
        os.system(f"cdo -L intlevel,3.64346569404006,7.59481964632869,14.3566322512925,24.6122200042009,35.9232500195503,43.1937500834465,51.6774989664555,61.5204982459545,73.7509578466415,87.8212302923203,103.317126631737,121.547240763903,142.994038760662,168.225079774857,197.908086702228,232.828618958592,273.910816758871,322.241902351379,379.100903868675,445.992574095726,524.687174707651,609.778694808483,691.389430314302,763.404481112957,820.858368650079,859.53476652503,887.020248919725,912.644546944648,936.198398470879,957.485479535535,976.325407391414,992.556095123291 tempFiles/temp1-{cyr}-{cmonth}-{cday}-{ctime}.nc tempFiles/temp2-{cyr}-{cmonth}-{cday}-{ctime}.nc")

        # Concatenate variable named pressure to the dataset to be compatible with CESM2.2
        df = xr.open_dataset(f'tempFiles/temp2-{cyr}-{cmonth}-{cday}-{ctime}.nc')
        df['PS'] = (('time', 'lat', 'lon'), np.zeros((1, nlat, nlon), dtype='float32'))

        # Save the dataset
        df.to_netcdf(fullPath, compute=True)
        df.close()

        # Remove temp files
        os.system(f"rm -f tempFiles/temp0-{cyr}-{cmonth}-{cday}-{ctime}.nc")
        os.system(f"rm -f tempFiles/temp1-{cyr}-{cmonth}-{cday}-{ctime}.nc")
        os.system(f"rm -f tempFiles/temp2-{cyr}-{cmonth}-{cday}-{ctime}.nc")

    except Exception as e:
        print(e)
        print(f'Interpolate failed for {ctime}, {cday}, {cmonth}, {cyr}')


def main():
    iterables = []

    for ctime in time:
        for cmonth in month:
            for cday in day:
                for cyr in years:
                    #iterables.append((ctime, cday, cmonth, cyr))
                    # Test
                    interpolate_data((ctime, cday, cmonth, cyr))

    # Break statements for testing
#                    break
#                break
#            break
#        break


    # Try to interpolate all files
    #thread_map(copy_files, iterables, max_workers=8)
    #thread_map(interpolate_data, iterables, max_workers=8)

if __name__ == '__main__':
   main()



