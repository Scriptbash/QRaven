import os
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sys

try:
    import xarray
except ImportError:
    script_dir = Path(__file__).parent.parent
    # List of module names and their corresponding .whl file paths
    modules_to_import = [
        ('fsspec', 'fsspec-2023.6.0-py3-none-any.whl'),
        ('cloudpickle', 'cloudpickle-2.2.1-py3-none-any.whl'),
        ('toolz', 'toolz-0.12.0-py3-none-any.whl'),
        ('dask', 'dask-2022.11.0-py3-none-any'),
        ('xarray', 'xarray-2022.11.0-py3-none-any.whl'),
    ]

    # Add the plugin directory to the Python path
    sys.path.insert(0, str(script_dir))

    # Loop through the module paths and import the modules
    for module_name, module_whl in modules_to_import:
        module_path = os.path.join(script_dir, 'ext_data/modules', module_whl)
        sys.path.append(module_path)
        import_statement = f'import {module_name}'
        exec(import_statement)
        print(f'{module_name} loaded locally.')


def merge_netcdf(file_path, filename):
    print('Merging files...')
    ds = xarray.open_mfdataset(file_path + '/*' + filename+'.nc', chunks='auto')
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
