import os
import numpy as np
import xarray as xr
from tqdm.contrib.concurrent import thread_map

year = ['1950'] 

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

month = [str(i).zfill(2) for i in range(1,13)]

timeout = [
    '00000',
    '21600',
    '43200',
    '64800',
]

timein = [
    0,
    6,
    12,
    18
]

DATA_PATH = '/glade/derecho/scratch/glydia/inputdata/nudging/'

def split_files(cyr,cmonth,cday):
    # Set input data file paths
    ufile = os.path.join(DATA_PATH,'ERA5regrid',f'e5.oper.an.pl.128_131_u.regrid.{cyr}{cmonth}day{int(cday)}.nc')
    vfile = os.path.join(DATA_PATH,'ERA5regrid',f'e5.oper.an.pl.128_132_v.regrid.{cyr}{cmonth}day{int(cday)}.nc')
    tfile = os.path.join(DATA_PATH,'ERA5regrid',f'e5.oper.an.pl.128_130_t.regrid.{cyr}{cmonth}day{int(cday)}.nc')
    qfile = os.path.join(DATA_PATH,'ERA5regrid',f'e5.oper.an.pl.128_133_q.regrid.{cyr}{cmonth}day{int(cday)}.nc')

    # Check to make sure input files exist
    if not os.path.isfile(ufile):
        print(ufile, 'does not exist')
        return False
    
    if not os.path.isfile(vfile):
        print(vfile, 'does not exist')
        return False
    
    if not os.path.isfile(tfile):
        print(tfile, 'does not exist')
        return False
    
    if not os.path.isfile(qfile):
        print(qfile, 'does not exist')
        return False
    
    # Open datasets
    du = xr.open_dataset(ufile).load()
    dv = xr.open_dataset(vfile).load()
    dt = xr.open_dataset(tfile).load()
    dq = xr.open_dataset(qfile).load()

    # Rename attributes
    du['U'].attrs['long_name'] = 'Zonal wind'
    dv['V'].attrs['long_name'] = 'Meridional wind'

    # Merge datasets
    ds = xr.merge([du,dv,dt,dq])
    ds = ds.rename({'level':'lev'})
    ds['PS'] = xr.zeros_like(ds['U'][dict(lev=0)])
    ds['PS'].attrs['long_name'] = 'Surface pressure'
    ds['PS'].attrs['units'] = 'Pa'
    ds['PS'].attrs['short_name'] = 'ps'
    ds.compute()

    # Loop through all four times
    for i in range(0,4):
        ctime = timeout[i]
        itime = timein[i]
        index = dict(time=itime)

        # Set outfile path
        outfile = f'ERA5.6hour.32level.uvtq.{cyr}-{cmonth}-{cday}-{ctime}.nc'
        outpath = os.path.join(DATA_PATH,'ERA5_CESM2',outfile)

        try:
            # Check if exists
            if os.path.isfile(outpath):
                print(outfile,' already exists')
                continue

            print(f'Spliting: {cyr}-{cmonth}-{cday}')

            dstime = ds[index]
            dstime.compute()

            dstime.to_netcdf(outpath)
            dstime.close()

        except Exception as e:
            print(e)
            print(f'File split failed for {ctime}, {cday}, {cmonth}, {cyr}')
            continue

    ds.close()



def main():
   for cyr in year:
        for cmonth in month:
            for cday in day:
                try:
                    split_files(cyr,cmonth,cday)
                except Exception as e:
                    print(e)
                    print(f'Split failed for {cday} {cmonth} {cyr}')




if __name__ == '__main__':
   main()