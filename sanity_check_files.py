import os
import pickle
import numpy as np
import xarray as xr
from tqdm.contrib.concurrent import thread_map

#years = list(np.arange(1950, 1980))
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
#month = ['10', '11', '12']

DATA_VARS = set(['V', 'T', 'U', 'PS', 'Q'])
SAVE_PATH = '/glade/derecho/scratch/glydia/inputdata/nudging/ERA5_CESM2/'

nlat = 192
nlon =288
nlev = 32

def _sanity_check(arg):
    """ Return True if bad file and False otherwise """
    ctime, cday, cmonth, cyr = arg

    outFile = f"ERA5.6hour.32level.uvtq.{cyr}-{cmonth}-{cday}-{ctime}.nc"
    fullPath = os.path.join(SAVE_PATH, outFile)

    if os.path.isfile(fullPath):
        try:
            ds = xr.open_dataset(fullPath, decode_cf=False)

            # Check has all variables
            if DATA_VARS != set(ds.data_vars.keys()):
                return True, outFile
            # Check number of levels
            if ds.dims['lev'] != 32:
                return True, outFile

            return False, outFile

        except:
            return True, outFile

    return False, outFile



def main():
    # # Load pickle file with bad files
    #with open('bad_files.pkl', 'rb') as f:
    #    s = pickle.load(f)
    #    print(s)

    #return
    bad_files = []
    for cyr in years:
        for cmonth in month:
            print("Checking: ", cyr, cmonth)
            for cday in day:
                for ctime in time:

                    #for bad_file in s:
                    # bad, fn = _sanity_check((ctime, cday, cmonth, cyr))
                    #cyr, cmonth, cday, ctime = bad_file.split(".")[-2].split("-")
                    bad, fn = _sanity_check((ctime, cday, cmonth, cyr))
                    #print(bad, fn)

                    if bad:
                        bad_files.append(fn)
                    #return


    print("Bad files: ", bad_files)
    # Save bad files
    with open('bad_files.pkl', 'wb') as f:
        pickle.dump(bad_files, f)


if __name__ == '__main__':
   main()