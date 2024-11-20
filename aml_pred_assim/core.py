from datetime import datetime as dt
from typing import Tuple, List
import numpy as np
import os

from .data.cds import ClimateDataStorage
from .utils import (
    _calculate_positions,
    _calculate_bounds,
    _validate_point,
    _get_indices,
)


def get_climate_data_from_api(variables: List[str], datetime: dt, pressure_levels: List[str], api_key: str) -> np.ndarray:
    """
    Retrieves climate data using the API.
    
    Args:
        variables: List of climate variables to retrieve
        datetime: Date and time for the data
        pressure_levels: List of pressure levels to consider
        api_key: Authentication key for the API
        
    Returns:
        Climate data as numpy array
        
    Raises:
        ValueError: If variables list is empty or invalid
        TypeError: If datetime is not a datetime object
        ValueError: If pressure_levels list is empty or invalid
        ValueError: If api_key is empty or invalid
    """
    if not variables or not isinstance(variables, list):
        raise ValueError("Variables list must be non-empty and valid")
    
    if not isinstance(datetime, dt):
        raise TypeError("datetime must be a datetime object")
        
    if not pressure_levels or not isinstance(pressure_levels, list):
        raise ValueError("Pressure levels list must be non-empty and valid")
        
    if not api_key or not isinstance(api_key, str):
        raise ValueError("API key must be non-empty and valid")

    climate_storage = ClimateDataStorage(
        variables=variables,
        years=datetime.year,
        months=datetime.month,
        days=datetime.day,
        hours=datetime.hour,
        pressure_levels=pressure_levels,
        key=api_key,
    )
    return climate_storage.data


def get_climate_data_from_file(variables: List[str], file_path: str) -> np.ndarray:
    """
    Retrieves climate data from a static file.
    
    Args:
        variables: List of climate variables to retrieve
        file_path: Path to the data file
        
    Returns:
        Climate data as numpy array
        
    Raises:
        ValueError: If variables list is empty or invalid
        ValueError: If file_path is empty or invalid
        FileNotFoundError: If the specified file does not exist
    """
    if not variables or not isinstance(variables, list):
        raise ValueError("Variables list must be non-empty and valid")
        
    if not file_path or not isinstance(file_path, str):
        raise ValueError("File path must be non-empty and valid")
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    climate_storage = ClimateDataStorage(
        variables=variables,
        path=file_path
    )
    return climate_storage.data


def get_predecessors(matrix: np.ndarray, point: Tuple[int, int, int, int], radius: int, 
                    x_bound: bool = True, y_bound: bool = True) -> np.ndarray:
    """
    Get predecessors for a given point in a 4D matrix.

    Args:
        matrix: 4D numpy array representing climate data
        point: Tuple of 4 integers representing (layer, variable, latitude, longitude)
        radius: Radius for neighborhood calculation
        x_bound: Whether to respect x-axis boundaries
        y_bound: Whether to respect y-axis boundaries

    Returns:
        numpy array of predecessor values
        
    Raises:
        ValueError: If point coordinates are invalid for the given matrix
        TypeError: If matrix is not a numpy array
        ValueError: If matrix is not 4-dimensional
        ValueError: If point is not a tuple of 4 integers
        ValueError: If radius is negative or zero
        TypeError: If x_bound or y_bound are not boolean values
    """
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Matrix must be a numpy array")
        
    if len(matrix.shape) != 4:
        raise ValueError("Matrix must be 4-dimensional")
        
    if not isinstance(point, tuple) or len(point) != 4 or not all(isinstance(x, int) for x in point):
        raise ValueError("Point must be a tuple of 4 integers")
        
    if not isinstance(radius, int) or radius <= 0:
        raise ValueError("Radius must be a positive integer")
        
    if not isinstance(x_bound, bool) or not isinstance(y_bound, bool):
        raise TypeError("x_bound and y_bound must be boolean values")

    if not _validate_point(matrix, point):
        return np.array([])

    layer, variable, latitude, longitude = point
    matrix_shape = matrix.shape

    lat_min, lat_max, lon_min, lon_max = _calculate_bounds(matrix_shape, point, radius, x_bound, y_bound)
    lat_indices, lon_indices = _get_indices(matrix_shape, lat_min, lat_max, lon_min, lon_max, latitude)
    positions = _calculate_positions(layer, variable, matrix_shape, lat_indices, lon_indices, lat_min, latitude, lon_min, longitude)

    return matrix[tuple(positions.T)]