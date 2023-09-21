import os
import pandas as pd
from zipfile import ZipFile, BadZipfile
import tarfile
import shutil
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
import sys
from PyQt5.QtWidgets import QApplication

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


def merge_netcdf(file_path, variable):
    print('Merging files...')
    try:
        ds = xarray.open_mfdataset(file_path + '/*' + variable + '.nc', parallel=True)
        # Remove the time dimension from the lat and lon variables
        lat_without_time = ds['lat'].isel(time=0)
        lon_without_time = ds['lon'].isel(time=0)
        ds_modified = xarray.Dataset({
            'lat': lat_without_time,
            'lon': lon_without_time,
            variable: ds[variable]
        })
        ds_modified.to_netcdf(file_path + '/' + variable + '_merged.nc')
        ds.close()
        ds_modified.close()
    except:
        print('The merging attempt failed. Manual processing will be required.')
        return
    # try:
    #     print('ValueError: Coordinate variable time is neither monotonically '
    #           'increasing nor monotonically decreasing on all datasets')
    #     print('Attempting a nested merge, time dimension will be concatenated.')
    #     ds = xarray.open_mfdataset(file_path + '/*' + filename+'.nc',
    #                                chunks='auto', combine="nested", concat_dim='time')
    #     ds.to_netcdf(file_path + '/' + filename + '_merged.nc')
    # except:
    #     print('All attempts to merge the netCDF files failed. Manual processing will be required.')
    #     return



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
    ds.close()
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
    ds.close()


def set_fill_values(ncfile, variable):
    ds = xarray.open_dataset(ncfile)
    new_variable_name = variable + '_new'  # Create a new variable with the desired _FillValue
    ds[new_variable_name] = ds[variable].where(ds[variable] != -9999.0, -1.2345)
    ds = ds.drop_vars(variable)  # Remove the original variable
    ds = ds.rename({new_variable_name: variable})  # Rename the new variable to the original variable name
    ds.to_netcdf(ncfile + '_tmp')
    os.remove(ncfile)
    os.rename(ncfile + '_tmp', ncfile)


# Creates a new folder if it does not exist
def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Extracts an archive
def extract_archive(file):
    folder = os.path.dirname(file)
    filename, extension = os.path.splitext(file)

    if extension == '.zip':
        with ZipFile(file, 'r') as zip_ref:
            for elem in zip_ref.namelist():
                filename = os.path.basename(elem)
                # skip directories
                if not filename:
                    continue
                source = zip_ref.open(elem)
                target = open(os.path.join(folder, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
                #QApplication.processEvents()
    elif extension == '.tgz' or extension == '.tar':
        tar = tarfile.open(file)
        for member in tar.getmembers():
            if member.isreg():  # skip if the TarInfo is not files
                if 'nariv' in member.name:
                    member.name = os.path.basename(member.name)
                    tar.extract(member,folder) # extract
                    #QApplication.processEvents()
    os.remove(file)


def download_request(dlg, url, output):
    timeout = dlg.spin_connection_timeout.value()
    req = urllib.request.Request(
                                url,
                                data=None,
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                }
                                )
    response = urllib.request.urlopen(req, timeout=timeout)

    totalsize = response.info()['Content-Length']
    currentsize = 0
    chunk = 4096
    with open(output,'wb') as file:
        while 1:
            data = response.read(chunk)
            if not data:
                #print ("Download complete.")
                break
            file.write(data)
            currentsize += chunk
            try:    #Try required for the soil dbf file... maybe file size too small
                handle_progress(dlg, currentsize, int(totalsize))
            except:
                dlg.progress_gisdownload.setValue(100)


def handle_progress(dlg, blocksize, totalsize):
    if totalsize > 0:
        download_percentage = (blocksize / totalsize) * 100
        dlg.progress_gisdownload.setValue(download_percentage)
    QApplication.processEvents()