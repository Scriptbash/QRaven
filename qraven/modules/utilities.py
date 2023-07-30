import os
import glob
import pandas as pd
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

try:
    import xarray
except ImportError:
    from sys import path
    script_dir = Path(__file__).parent.parent
    module_path = os.path.join(script_dir, 'ext_data/modules/xarray-2023.7.0-py3-none-any')
    path.append(module_path)
    import xarray
    print('xarray loaded locally.')


def merge_netcdf(file_path, filename):
    print('Merging files...')
    ds = xarray.merge([xarray.open_dataset(f) for f in glob.glob(file_path + '/*' + filename+'.nc')], compat='override')
    ds.to_netcdf(file_path + '/' + filename + '_merged.nc')
    print('Files merged.')


def check_missing_dates(ncfile):
    ds = xarray.open_dataset(ncfile)
    time_data = ds['time'].values
    start_year = int(pd.Timestamp(time_data.min()).strftime('%Y'))
    end_year = int(pd.Timestamp(time_data.max()).strftime('%Y'))
    datetime_list = [datetime.utcfromtimestamp(ts.astype('O') / 1e9) for ts in time_data]

    start_date = datetime(start_year, 1, 1, 12, 0)
    end_date = datetime(end_year, 12, 31, 12, 0)

    all_dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    missing_dates = [date for date in all_dates if date not in datetime_list]
    return missing_dates


def fill_missing_dates(ncfile, missing_dates):
    ds = xarray.open_dataset(ncfile)
    if missing_dates:
        # Create an empty DataArray with NaN values for the missing dates
        missing_data = xarray.full_like(ds.isel(time=0), fill_value=float('nan'))
        # Update the time coordinate with the missing dates
        missing_data['time'] = missing_dates
        # Concatenate the missing data with the ds along the 'time' dimension
        updated_data = xarray.concat([ds, missing_data], dim='time')
        updated_data.to_netcdf(ncfile)
        print("Missing dates were filled with NaN values and saved to '" + ncfile)
    else:
        print("No missing dates found.")
