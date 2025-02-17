from scipy.sparse import coo_matrix
from netCDF4 import Dataset
import numpy as np
import unittest
import os

from aml_pred_assim.utils import save_matrix_to_netcdf, _save_dense_matrix_to_netcdf, _save_sparse_matrix_to_netcdf

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_dense_matrix = np.array([[1, 2, 3], [4, 5, 6]])
        self.test_sparse_matrix = coo_matrix(([1, 2, 3], ([0, 1, 2], [1, 2, 0])), shape=(3, 3))
        self.test_file_path = "test_matrix.nc"

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_save_dense_matrix(self):
        save_matrix_to_netcdf(self.test_dense_matrix, self.test_file_path)
        
        with Dataset(self.test_file_path, "r") as nc_file:
            self.assertTrue("data" in nc_file.variables)
            saved_matrix = nc_file.variables["data"][:]
            np.testing.assert_array_equal(saved_matrix, self.test_dense_matrix)

    def test_save_sparse_matrix(self):
        save_matrix_to_netcdf(self.test_sparse_matrix, self.test_file_path)
        
        with Dataset(self.test_file_path, "r") as nc_file:
            self.assertTrue("data_row" in nc_file.variables)
            self.assertTrue("data_col" in nc_file.variables)
            self.assertTrue("data_data" in nc_file.variables)
            self.assertEqual(nc_file.sparse_format, "coo")
            
            saved_rows = nc_file.variables["data_row"][:]
            saved_cols = nc_file.variables["data_col"][:]
            saved_data = nc_file.variables["data_data"][:]
            
            np.testing.assert_array_equal(saved_rows, self.test_sparse_matrix.row)
            np.testing.assert_array_equal(saved_cols, self.test_sparse_matrix.col)
            np.testing.assert_array_equal(saved_data, self.test_sparse_matrix.data)

    def test_invalid_matrix_type(self):
        invalid_matrix = "not a matrix"
        with self.assertRaises(ValueError):
            save_matrix_to_netcdf(invalid_matrix, self.test_file_path)

    def test__save_dense_matrix_to_netcdf(self):
        with Dataset(self.test_file_path, "w", format="NETCDF4") as nc_file:
            _save_dense_matrix_to_netcdf(self.test_dense_matrix, nc_file, "test_dense")
            
            self.assertTrue("test_dense" in nc_file.variables)
            self.assertTrue("dim_0" in nc_file.dimensions)
            self.assertTrue("dim_1" in nc_file.dimensions)
            self.assertEqual(nc_file.dimensions["dim_0"].size, self.test_dense_matrix.shape[0])
            self.assertEqual(nc_file.dimensions["dim_1"].size, self.test_dense_matrix.shape[1])
            saved_matrix = nc_file.variables["test_dense"][:]
            np.testing.assert_array_equal(saved_matrix, self.test_dense_matrix)

    def test__save_sparse_matrix_to_netcdf(self):
        with Dataset(self.test_file_path, "w", format="NETCDF4") as nc_file:
            _save_sparse_matrix_to_netcdf(self.test_sparse_matrix, nc_file, "test_sparse")
            
            self.assertTrue("test_sparse_row" in nc_file.variables)
            self.assertTrue("test_sparse_col" in nc_file.variables)
            self.assertTrue("test_sparse_data" in nc_file.variables)
            self.assertTrue("nnz" in nc_file.dimensions)
            self.assertTrue("dim_0" in nc_file.dimensions)
            self.assertTrue("dim_1" in nc_file.dimensions)
            self.assertEqual(nc_file.dimensions["nnz"].size, self.test_sparse_matrix.nnz)
            self.assertEqual(nc_file.dimensions["dim_0"].size, self.test_sparse_matrix.shape[0])
            self.assertEqual(nc_file.dimensions["dim_1"].size, self.test_sparse_matrix.shape[1])
            self.assertEqual(nc_file.sparse_format, "coo")
            
            saved_rows = nc_file.variables["test_sparse_row"][:]
            saved_cols = nc_file.variables["test_sparse_col"][:]
            saved_data = nc_file.variables["test_sparse_data"][:]
            
            np.testing.assert_array_equal(saved_rows, self.test_sparse_matrix.row)
            np.testing.assert_array_equal(saved_cols, self.test_sparse_matrix.col)
            np.testing.assert_array_equal(saved_data, self.test_sparse_matrix.data)

if __name__ == '__main__':
    unittest.main()