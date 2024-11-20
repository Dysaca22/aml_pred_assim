import unittest
from datetime import datetime
import numpy as np

from aml_pred_assim.core import (
    get_climate_data_from_api,
    get_climate_data_from_file,
    get_predecessors
)


class TestClimateData(unittest.TestCase):
    def setUp(self):
        self.variables = ['temperature', 'humidity']
        self.datetime_obj = datetime(2024, 10, 10, 6)
        self.pressure_levels = ['1000', '850']
        self.api_key = 'test_key'
        self.file_path = 'test_data.nc'


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