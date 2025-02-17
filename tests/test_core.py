import unittest
from datetime import datetime
import numpy as np

from aml_pred_assim.core import (
    get_climate_data_from_api,
    get_climate_data_from_file,
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


if __name__ == '__main__':
    unittest.main()