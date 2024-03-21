# Option 1: Download ERA5 data from CDS
# Options 2: Copy from /glade/collections/rda/data/ds633.0/e5.oper.an.pl/
import cdsapi
import os
from tqdm.contrib.concurrent import thread_map


c = cdsapi.Client(timeout=60,quiet=False,debug=True)

variable = [
    'v_component_of_wind',
    'u_component_of_wind',
    'temperature',
    'specific_humidity'
]

year = ['1951'] 

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

SAVE_PATH = '/glade/derecho/scratch/glydia/inputdata/nudging/ERA5original/'

def main():
    args = []
    for cvariable in variable:
        for cyr in year:
            for cday in day:
                for cmonth in month:
                    # Try to do download data, catch error if it fails
                    try:
                        #download((cvariable, cday, cmonth, cyr))
                        args.append((cvariable, cday, cmonth, cyr))
                    except Exception as e:
                        print(e)
                        print(f'Download failed for {cvariable} {cday} {cmonth} {cyr}')
                    # break
                # break
            # break

    thread_map(download, args, max_workers=16)



def download(args):
    try:
        cvariable, cday, cmonth, cyr = args
        if cvariable == 'u_component_of_wind':
            var_alias = '131_u'
            lev = 'll025uv'
        elif cvariable == 'v_component_of_wind':
            var_alias = '132_v'
            lev = 'll025uv'
        elif cvariable == 'temperature':
            var_alias == '130_t'
            lev = 'll025sc'
        elif cvariable == 'specific_humidity':
            var_alias = '133_q'
            lev = 'll025sc'

        fn = f'e5.oper.an.pl.128_{var_alias}.{lev}.{cyr}{cmonth}{cday}00_{cyr}{cmonth}{cday}23.nc'
        fp = os.path.join(SAVE_PATH, f"{cyr}{cmonth}")

        if not os.path.exists(fp):
            os.makedirs(fp)

        # If we already downloaded file, skip
        dir_list = os.listdir(fp)
        if fn in dir_list:
            print(f'Already downloaded {fn}')
            return

        else:
            save_file = os.path.join(fp, fn)

            c.retrieve(
                'reanalysis-era5-pressure-levels',
                {
                    'nocache': '123',
                    'product_type': 'reanalysis',
                    'format': 'netcdf',
                    'pressure_level': [
                        '1', '2', '3',
                        '5', '7', '10',
                        '20', '30', '50',
                        '70', '100', '125',
                        '150', '175', '200',
                        '225', '250', '300',
                        '350', '400', '450',
                        '500', '550', '600',
                        '650', '700', '750',
                        '775', '800', '825',
                        '850', '875', '900',
                        '925', '950', '975',
                        '1000',
                    ],
                    'variable': cvariable,
                    'year': cyr,
                    'month': cmonth,
                    'day': cday,
                    'time': time,
                },
                save_file)
    except Exception as e:
        print(e)
        print(f'Download failed for {cvariable} {cday} {cmonth} {cyr}')

if __name__ == '__main__':
    main()
