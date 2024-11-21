import unittest
from datetime import datetime
import numpy as np
import os

from aml_pred_assim.core import (
    get_climate_data_from_api,
    get_climate_data_from_file,
    get_mpas_data,
    get_predecessors
)


class TestClimateData(unittest.TestCase):
    def setUp(self):
        self.variables = ['temperature', 'humidity']
        self.datetime_obj = datetime(2024, 10, 10, 6)
        self.pressure_levels = ['1000', '850']
        self.api_key = 'test_key'
        self.file_path = 'test_data.nc'
        self.mesh_url = "https://www2.mmm.ucar.edu/projects/mpas/atmosphere_meshes/x1.40962.tar.gz"
        self.target_lat = np.linspace(-90, 90, 180)  # Example latitude grid
        self.target_lon = np.linspace(-180, 180, 360)  # Example longitude grid

    def test_get_climate_data_from_api_invalid_inputs(self):
        with self.assertRaises(ValueError):
            get_climate_data_from_api([], self.datetime_obj, self.pressure_levels, self.api_key)
        
        with self.assertRaises(TypeError):
            get_climate_data_from_api(self.variables, "2023-01-01", self.pressure_levels, self.api_key)
        
        with self.assertRaises(ValueError):
            get_climate_data_from_api(self.variables, self.datetime_obj, [], self.api_key)
        
        with self.assertRaises(ValueError):
            get_climate_data_from_api(self.variables, self.datetime_obj, self.pressure_levels, "")

    def test_get_climate_data_from_file_invalid_inputs(self):
        with self.assertRaises(ValueError):
            get_climate_data_from_file([], self.file_path)
        
        with self.assertRaises(ValueError):
            get_climate_data_from_file(self.variables, "")
        
        with self.assertRaises(FileNotFoundError):
            get_climate_data_from_file(self.variables, "nonexistent_file.nc")

    def test_get_mpas_data_invalid_inputs(self):
        with self.assertRaises(ValueError):
            get_mpas_data([], self.mesh_url, self.target_lat, self.target_lon)
        
        with self.assertRaises(ValueError):
            get_mpas_data(self.variables, "", self.target_lat, self.target_lon)
        
        with self.assertRaises(ValueError):
            get_mpas_data(self.variables, self.mesh_url, None, self.target_lon)
        
        with self.assertRaises(ValueError):
            get_mpas_data(self.variables, self.mesh_url, self.target_lat, "invalid_grid")

    def test_get_mpas_data_valid_inputs(self):
        # Assuming a mock mesh or local test data to avoid downloading
        mock_file_path = "test_mpas.nc"  # Use a real file path in practice
        try:
            result = get_mpas_data(self.variables, self.mesh_url, self.target_lat, self.target_lon, mock_file_path)
            self.assertIsInstance(result, np.ndarray)
            self.assertEqual(len(result.shape), 4)  # Expected shape: (variable, layer, lat, lon)
        except FileNotFoundError:
            self.skipTest("Mock file for MPAS data does not exist. Test skipped.")

    def test_get_mpas_data_download(self):
        try:
            result = get_mpas_data(self.variables, self.mesh_url, self.target_lat, self.target_lon)
            self.assertIsInstance(result, np.ndarray)
            self.assertEqual(len(result.shape), 4)
        except Exception as e:
            self.fail(f"get_mpas_data raised an exception: {e}")

    def test_get_mpas_data_valid_inputs(self):
        # Ensure the mock file exists before running the test
        mock_file_path = "test_mpas.nc"
        if not os.path.exists(mock_file_path):
            self.skipTest("Mock file for MPAS data does not exist. Test skipped.")

        try:
            result = get_mpas_data(self.variables, self.mesh_url, self.target_lat, self.target_lon, mock_file_path)
            self.assertIsInstance(result, np.ndarray)
            self.assertEqual(len(result.shape), 4)  # Expected shape: (variable, layer, lat, lon)
        except Exception as e:
            self.fail(f"get_mpas_data raised an exception: {e}")

class TestPredecessors(unittest.TestCase):
    def setUp(self):
        self.matrix = np.zeros((2, 2, 4, 4))  # 2 layers, 2 variables, 4x4 grid
        self.matrix[0, 0, 1, 1] = 1.0
        self.point = (0, 0, 1, 1)
        self.radius = 1
        self.edge_point = (0, 0, 0, 0)

    def test_get_predecessors_invalid_inputs(self):
        with self.assertRaises(TypeError):
            get_predecessors([[]], self.point, self.radius)
        
        with self.assertRaises(ValueError):
            get_predecessors(np.zeros((2, 2)), self.point, self.radius)
        
        with self.assertRaises(ValueError):
            get_predecessors(self.matrix, (0, 0, 0), self.radius)
        
        with self.assertRaises(ValueError):
            get_predecessors(self.matrix, self.point, -1)
        
        with self.assertRaises(TypeError):
            get_predecessors(self.matrix, self.point, self.radius, x_bound="invalid")

    def test_get_predecessors_valid_inputs(self):
        result = get_predecessors(self.matrix, self.point, self.radius)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result.shape), 1)

    def test_get_predecessors_boundary_conditions(self):
        result_edge = get_predecessors(self.matrix, self.edge_point, self.radius)
        self.assertIsInstance(result_edge, np.ndarray)

    def test_get_predecessors_different_boundaries(self):
        result_no_bounds = get_predecessors(self.matrix, self.point, self.radius, x_bound=False, y_bound=False)
        self.assertIsInstance(result_no_bounds, np.ndarray)


if __name__ == '__main__':
    unittest.main()