import os
import glob
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


def merge_netcf(file_path, filename):
    ds = xarray.merge([xarray.open_dataset(f) for f in glob.glob(file_path +'/*'+filename+'.nc')])
    ds.to_netcdf(file_path+'/'+filename+'_merged.nc')
