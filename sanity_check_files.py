import os
import pickle
import numpy as np
import xarray as xr
from tqdm.contrib.concurrent import thread_map

#years = list(np.arange(1950, 1980))
years = [str(i) for i in range(1954,1961)]

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

hoursec = 3600


month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
daysinmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#month = ['10', '11', '12']

DATA_VARS = set(['V', 'T', 'U', 'PS', 'Q'])
SAVE_PATH = '/glade/campaign/univ/ucub0137/ERA5_CESM2_nudging'

nlat = 192
nlon =288
nlev = 32

def _sanity_check(arg):
    """ Return True if bad file and False otherwise """
    ctime, cday, cmonth, cyr = arg

    outFile = f"ERA5.6hour.32level.uvtq.{cyr}-{cmonth}-{cday}-{ctime}.nc"
    outDir = f"{cyr}{cmonth}/"
    fullPath = os.path.join(SAVE_PATH, outDir, outFile)

    if os.path.isfile(fullPath):
        try:
            ds = xr.open_dataset(fullPath)

            dtime = ds.time

            # Checks for all possible problems will file and saves all problems
            # If encounters at least one error, sets file as bad (return True)
            file_probs = []
            prob_encountered = False

            # Check has all variables
            if not DATA_VARS.issubset(set(ds.data_vars.keys())):
                file_probs.append('not all variables')
                prob_encountered = True
            # Check number of levels
            if ds.sizes['lev'] != nlev:
                file_probs.append('number of levels wrong')
                prob_encountered = True
            # Check number of lats
            if ds.sizes['lat'] != nlat:
                file_probs.append('number of lats wrong')
                prob_encountered = True
            # Check number of lons
            if ds.sizes['lon'] != nlon:
                file_probs.append('number of lons wrong')
                prob_encountered = True
            # Check that file name date matches internal year
            if dtime.dt.year.values != int(cyr):
                file_probs.append('internal year wrong')
                prob_encountered = True
            # Check that file name date matches internal month
            if dtime.dt.month.values != int(cmonth):
                file_probs.append('internal month wrong')
                prob_encountered = True
            # Check that file name date matches internal day
            if dtime.dt.day.values != int(cday):
                file_probs.append('internal day wrong')
                prob_encountered = True
            # Check that file name date matches internal hour
            if dtime.dt.hour.values*hoursec != int(ctime):
                file_probs.append('internal hour wrong')
                prob_encountered = True

            # If no problems encountered, returns prob_encountered=False & empty list of file problems
            return prob_encountered, outFile, file_probs

        except:
            return True, outFile, 'error'

    return True, outFile,'missing file'



def main():
    # # Load pickle file with bad files
    #with open('bad_files.pkl', 'rb') as f:
    #    s = pickle.load(f)
    #    print(s)

    #return
    bad_files = []
    for cyr in years:
        # Check if leap year
        leap = (int(cyr) % 4) == 0

        for cmonth in month:
            print("Checking: ", cyr, cmonth)

            # Set max day in month
            if cmonth == '02' and leap:
                maxdayinmonth = 29
            else:
                maxdayinmonth = daysinmonth[int(cmonth)-1]

            for cday in day:

                # If day is less than or equal to max day in month, proceed with sanity check
                if int(cday) <= maxdayinmonth:
                    for ctime in time:

                        #for bad_file in s:
                        # bad, fn = _sanity_check((ctime, cday, cmonth, cyr))
                        #cyr, cmonth, cday, ctime = bad_file.split(".")[-2].split("-")
                        bad, fn, why = _sanity_check((ctime, cday, cmonth, cyr))
                        #print(bad, fn)

                        if bad:
                            bad_files.append((fn,why))
                        #return


    print("Bad files: ", bad_files)
    # Save bad files
    with open('bad_files.pkl', 'wb') as f:
        pickle.dump(bad_files, f)


if __name__ == '__main__':
   main()
