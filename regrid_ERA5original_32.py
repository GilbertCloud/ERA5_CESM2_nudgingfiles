import os

CESM1levels = [3.64346569404006,7.59481964632869,14.3566322512925,24.6122200042009,38.2682997733355,54.5954797416925,72.0124505460262,87.8212302923203,103.317126631737,121.547240763903,142.994038760662,168.225079774857,197.908086702228,232.828618958592,273.910816758871,322.241902351379,379.100903868675,445.992574095726,524.687174707651,609.778694808483,691.389430314302,763.404481112957,820.858368650079,859.53476652503,887.020248919725,912.644546944648,936.198398470879,957.485479535535,976.325407391414,992.556095123291]

CESM2levels = [3.643466,7.59482 ,  14.356632,  24.61222 ,  35.92325 ,  43.19375 , 51.677499,  61.520498,  73.750958,  87.82123 , 103.317127, 121.547241, 142.994039, 168.22508 , 197.908087, 232.828619, 273.910817, 322.241902, 379.100904, 445.992574, 524.687175, 609.778695, 691.38943 , 763.404481, 820.858369, 859.534767, 887.020249, 912.644547, 936.198398, 957.48548 ,976.325407, 992.556095]

variable = [
    'v_component_of_wind',
    'u_component_of_wind',
    'temperature',
    'specific_humidity'
]

year = ['2010'] 

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
    '00:00', '01:00', '02:00',
    '03:00', '04:00', '05:00',
    '06:00', '07:00', '08:00',
    '09:00', '10:00', '11:00',
    '12:00', '13:00', '14:00',
    '15:00', '16:00', '17:00',
    '18:00', '19:00', '20:00',
    '21:00', '22:00', '23:00',
]

month = [str(i).zfill(2) for i in range(1,13)]

daysinmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

var_aliases = {
    'u_component_of_wind':'131_u',
    'v_component_of_wind':'132_v',
    'temperature':'130_t',
    'specific_humidity':'133_q'
}

levs = {
    'u_component_of_wind':'ll025uv',
    'v_component_of_wind':'ll025uv',
    'temperature':'ll025sc',
    'specific_humidity':'ll025sc'
}

DATA_PATH = '/glade/campaign/collections/rda/data/ds633.0/e5.oper.an.'
SAVE_PATH = '/glade/derecho/scratch/glydia/inputdata/nudging/ERA5regrid'

def interpolate_data(cvar, cday, cmonth, cyr):
    # Set variables and paths
    var_alias = var_aliases[cvar]
    lev = levs[cvar]

    DATA_PATH_I = DATA_PATH+'pl'

    cfile = os.path.join(DATA_PATH_I, f'{cyr}{cmonth}',f'e5.oper.an.pl.128_{var_alias}.{lev}.{cyr}{cmonth}{cday}00_{cyr}{cmonth}{cday}23.nc')
    ofile = os.path.join(SAVE_PATH,f'e5.oper.an.pl.128_{var_alias}.regrid.{cyr}{cmonth}day{int(cday)}.nc')

    # Exit if file exists
    if os.path.isfile(ofile):
        print(ofile,' already exists')
        return

    # Regrid & interpolate vertically
    os.system(f"cdo -f nc4 -remapbil,cdo_grid.txt -setgridtype,regular {cfile} tempFiles/temp-{var_alias}-{cyr}-{cmonth}-{cday}.nc")
    os.system(f"cdo intlevel,3.64346569404006,7.59481964632869,14.3566322512925,24.6122200042009,35.9232500195503,43.1937500834465,51.6774989664555,61.5204982459545,73.7509578466415,87.8212302923203,103.317126631737,121.547240763903,142.994038760662,168.225079774857,197.908086702228,232.828618958592,273.910816758871,322.241902351379,379.100903868675,445.992574095726,524.687174707651,609.778694808483,691.389430314302,763.404481112957,820.858368650079,859.53476652503,887.020248919725,912.644546944648,936.198398470879,957.485479535535,976.325407391414,992.556095123291 tempFiles/temp-{var_alias}-{cyr}-{cmonth}-{cday}.nc ERA5regrid/e5.oper.an.pl.128_{var_alias}.regrid.{cyr}{cmonth}day{int(cday)}.nc")
    os.system(f"rm -f tempFiles/temp-{var_alias}-{cyr}-{cmonth}-{cday}.nc")

def main():
    for cyr in year:
        # Check if leap year
        leap = (int(cyr) % 4) == 0

        for cmonth in month:

            # Set max day in month
            if cmonth == '02' and leap:
                maxdayinmonth = 29
            else:
                maxdayinmonth = daysinmonth[int(cmonth)-1]

            for cday in day:
                # If day is less than or equal to max day in month, proceed with data download
                if int(cday) <= maxdayinmonth:
                    for cvariable in variable:
                        # Try to do download data, catch error if it fails
                        try:
                            print(f'Trying {cvariable} {cday} {cmonth} {cyr}')
                            interpolate_data(cvariable, cday, cmonth, cyr)
                        except Exception as e:
                            print(e)
                            print(f'Download failed for {cvariable} {cday} {cmonth} {cyr}')

if __name__ == '__main__':
   main()



