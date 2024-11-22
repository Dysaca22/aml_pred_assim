from sklearn.linear_model import Ridge
from scipy.sparse import coo_matrix
from datetime import datetime as dt
from typing import Tuple, List
import numpy as np
import os

from .mapper.cds import ClimateDataStorage
from .utils import (
    _calculate_positions,
    _calculate_bounds,
    _validate_point,
    _flat_indices,
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