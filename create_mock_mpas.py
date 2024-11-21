from netCDF4 import Dataset
import numpy as np

def create_mock_mpas_file(file_path: str):
    with Dataset(file_path, 'w', format='NETCDF4') as ds:
        # Define dimensions
        nCells = ds.createDimension('nCells', 10)
        nLevels = ds.createDimension('nLevels', 5)

        # Define variables
        lat = ds.createVariable('latCell', np.float32, ('nCells',))
        lon = ds.createVariable('lonCell', np.float32, ('nCells',))
        temp = ds.createVariable('temperature', np.float32, ('nCells', 'nLevels'))

        # Populate variables with mock data
        lat[:] = np.linspace(-90, 90, 10)
        lon[:] = np.linspace(-180, 180, 10)
        temp[:, :] = np.random.rand(10, 5)

# Create the mock file
create_mock_mpas_file('test_mpas.nc')
