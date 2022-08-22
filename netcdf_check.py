import netCDF4 as nc
fn = '/home/francis/Documents/Data/OIH_Output/network_after_gen_hrus/temps.nc'
ds = nc.Dataset(fn)
print(ds)