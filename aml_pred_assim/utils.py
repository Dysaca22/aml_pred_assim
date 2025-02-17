from scipy.sparse._csr import csr_matrix
from scipy.sparse import coo_matrix
from netCDF4 import Dataset
import numpy as np


def save_matrix_to_netcdf(matrix, file_path, variable_name="data") -> None:
    """
    Save a dense or sparse matrix to a NetCDF (.nc) file.

    Args:
        matrix (numpy.ndarray or scipy.sparse.coo_matrix): 
            The matrix to save. Can be a dense numpy array or a sparse COO matrix.
        file_path (str): 
            The path to the NetCDF file where the matrix will be saved.
        variable_name (str): 
            The base name for the variable(s) to store the data.

    Raises:
        ValueError: If the matrix type is unsupported.
    """
    try:
        with Dataset(file_path, "w", format="NETCDF4") as nc_file:
            if isinstance(matrix, np.ndarray):
                _save_dense_matrix_to_netcdf(matrix, nc_file, variable_name)
                print(f"Dense matrix successfully saved to {file_path}")
            elif isinstance(matrix, coo_matrix) or isinstance(matrix, csr_matrix):
                if isinstance(matrix, csr_matrix):
                    matrix = matrix.tocoo()
                _save_sparse_matrix_to_netcdf(matrix, nc_file, variable_name)
                print(f"Sparse matrix successfully saved to {file_path}")
            else:
                raise ValueError("Unsupported matrix type. Provide a numpy array or scipy.sparse.coo_matrix.")
    except Exception as e:
        raise ValueError(f"Error saving the matrix: {e}")


def _save_dense_matrix_to_netcdf(matrix, nc_file, variable_name):
    """
    Save a dense matrix to a NetCDF file.

    Args:
        matrix (numpy.ndarray): The dense matrix to save.
        nc_file (netCDF4.Dataset): The open NetCDF file object.
        variable_name (str): The name of the variable to store the data.
    """
    dimensions = {}
    for dim_idx, dim_size in enumerate(matrix.shape):
        dim_name = f"dim_{dim_idx}"
        dimensions[dim_name] = nc_file.createDimension(dim_name, dim_size)

    var = nc_file.createVariable(variable_name, matrix.dtype, tuple(dimensions.keys()))
    var[:] = matrix


def _save_sparse_matrix_to_netcdf(sparse_matrix, nc_file, variable_name):
    """
    Save a sparse COO matrix to a NetCDF file.

    Args:
        sparse_matrix (coo_matrix): The sparse matrix to save in COO format.
        nc_file (netCDF4.Dataset): The open NetCDF file object.
        variable_name (str): The base name for the variables storing sparse data.
    """
    nc_file.createDimension("nnz", sparse_matrix.nnz)
    nc_file.createDimension("dim_0", sparse_matrix.shape[0])
    nc_file.createDimension("dim_1", sparse_matrix.shape[1])

    row_var = nc_file.createVariable(f"{variable_name}_row", "i4", ("nnz",))
    row_var[:] = sparse_matrix.row

    col_var = nc_file.createVariable(f"{variable_name}_col", "i4", ("nnz",))
    col_var[:] = sparse_matrix.col

    data_var = nc_file.createVariable(f"{variable_name}_data", sparse_matrix.data.dtype, ("nnz",))
    data_var[:] = sparse_matrix.data

    nc_file.sparse_format = "coo"
