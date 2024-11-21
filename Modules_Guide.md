# ClimateDataStorage Class

`ClimateDataStorage` is a class designed to download, process, and store climate data from the **Copernicus Climate Data Store (CDS)**. It is a useful tool for working with ERA5 reanalysis data, allowing users to download specific variables and organize them into a ready-to-analyze data structure.

---

## Key Features

1. **Data Download**: Uses the CDS API to fetch climate data in NetCDF format.
2. **Variable Mapping**: Translates standard variable names like "temperature" or "wind" to their internal identifiers (e.g., `t` for temperature).
3. **File Processing**: Extracts structured data from existing NetCDF files.

---

## Main Methods

#### Key Parameters
- **`variables`**: List of climate variables to include, such as `"temperature"` or `"wind"`.
- **`years`, `months`, `days`, `hours`**: Dates and times to filter the data.
- **`pressure_levels`**: Pressure levels to include (e.g., `"1000"`, `"850"`).
- **`key`**: API key for accessing CDS.
- **`path`**: Path to a NetCDF file if you want to process local data.

#### What it does
- If you provide an API key, it will download data from CDS.
- If you provide a file, it will extract and process its data.

---

### Parameter Validation: `_validate`

#### Description
This internal method ensures that all required parameters are properly defined.

---

### Variable Mapping: `_get_hardcoded_variables`

#### Description
Translates climate variable names into internal identifiers defined in a configuration file (`cds_variables.json`).

#### Example
- `"temperature"` → `"t"`
- `"u_component_of_wind"` → `"u"`

---

### Data Download: `_download_ensemble`

#### Description
Downloads data from CDS using the API and saves it as a NetCDF file.

---

### File Processing: `_get_data`

#### Description
Extracts and organizes data from a NetCDF file into a multidimensional array.

#### Array Structure
- `[Layers | Variables | Ensembles | Latitude | Longitude]`

---

## How to Use

### Create an Instance

You can create a `ClimateDataStorage` instance to download data or process an existing file:

```python
from aml_pred_assim.data.cds import ClimateDataStorage

# Example 1: Download data from the API
climate_storage = ClimateDataStorage(
    variables=["temperature", "u_component_of_wind"],
    years=["2023"],
    months=["11"],
    days=["20"],
    hours=["12"],
    pressure_levels=["1000", "850"],
    key="YOUR_API_KEY"
)

# Example 2: Process an existing NetCDF file
climate_storage = ClimateDataStorage(
    variables=["temperature", "u_component_of_wind"],
    path="climate_data.nc"
)

```
# Climate Data Processing Functions

## Overview

This module provides three core functions for retrieving and analyzing climate data:
1. **`get_climate_data_from_api`**: Retrieves data using the Copernicus Climate Data Store (CDS) API.
2. **`get_climate_data_from_file`**: Loads climate data from a local NetCDF file.
3. **`get_predecessors`**: Finds neighboring values (predecessors) in a 4D climate data matrix.

---

## Function: `get_climate_data_from_api`

### Purpose
Fetches climate data from the **CDS API**, specifying the variables, date, and pressure levels.

### Parameters
- **`variables`** (`List[str]`): List of climate variables to retrieve (e.g., `"temperature"`, `"u_component_of_wind"`).
- **`datetime`** (`datetime`): Date and time for the data.
- **`pressure_levels`** (`List[str]`): Pressure levels to include (e.g., `"1000"`, `"850"`).
- **`api_key`** (`str`): API key for CDS access.

### Returns
- **`np.ndarray`**: Climate data as a multidimensional NumPy array.

### Raises
- **`ValueError`**: If `variables`, `pressure_levels`, or `api_key` are invalid.
- **`TypeError`**: If `datetime` is not a `datetime` object.

### Example Usage
```python
from aml_pred_assim.data.core import get_climate_data_from_api
from datetime import datetime as dt

# Retrieve data for November 20, 2023, at 12:00
data = get_climate_data_from_api(
    variables=["temperature", "u_component_of_wind"],
    datetime=dt(2023, 11, 20, 12),
    pressure_levels=["1000", "850"],
    api_key="YOUR_API_KEY"
)
```

## Function: `get_climate_data_from_file`

### Purpose

The `get_climate_data_from_file` function retrieves climate data from a local NetCDF file. It uses the `ClimateDataStorage` class to process the file and extract the requested variables.

---

### Parameters

- **`variables`** (`List[str]`): 
  List of climate variables to retrieve (e.g., `"temperature"`, `"u_component_of_wind"`).

- **`file_path`** (`str`): 
  The path to the NetCDF file containing the climate data.

---

### Returns

- **`np.ndarray`**: 
  A multidimensional NumPy array containing the requested climate data.

---

### Raises

- **`ValueError`**:
  - If `variables` is empty or not a list.
  - If `file_path` is empty or not a string.

- **`FileNotFoundError`**:
  - If the specified file does not exist at the given path.

---

### How It Works

1. **Validation**:
   - Ensures `variables` is a non-empty list.
   - Checks that `file_path` is a valid string and the file exists.

2. **Processing**:
   - Initializes a `ClimateDataStorage` instance, passing the `variables` and `file_path`.
   - Calls the `ClimateDataStorage` class to extract and process the data from the file.

3. **Data Retrieval**:
   - Returns the processed data as a NumPy array.

---

### Example Usage

```python
from aml_pred_assim.data.core import get_climate_data_from_file

# Load climate data from a local NetCDF file
data = get_climate_data_from_file(
    variables=["temperature", "u_component_of_wind"],
    file_path="climate_data.nc"
)

# Access the data
print(data)
```

## Function: `get_predecessors`

### Purpose

The `get_predecessors` function identifies neighboring values (predecessors) around a specific point in a 4D climate data matrix. 

---

### Parameters

- **`matrix`** (`np.ndarray`): 
  A 4D NumPy array representing climate data. The array must follow the structure:
  - `[Layers | Variables | Latitude | Longitude]`.
  
- **`point`** (`Tuple[int, int, int, int]`): 
  A tuple specifying the location in the matrix. The format is `(layer, variable, latitude, longitude)`.
  
- **`radius`** (`int`): 
  Defines the size of the neighborhood to analyze. Represents the range around the specified `point` for which neighboring values will be retrieved.
  
- **`x_bound`** (`bool`, optional): 
  Indicates whether x-axis boundaries (longitude) should be respected. Defaults to `True`.
  
- **`y_bound`** (`bool`, optional): 
  Indicates whether y-axis boundaries (latitude) should be respected. Defaults to `True`.

---

### Returns

- **`np.ndarray`**: 
  A NumPy array containing the values of the neighbors (predecessors) around the specified point.

---

### Raises

- **`TypeError`**:
  - If `matrix` is not a NumPy array.
  - If `x_bound` or `y_bound` are not boolean values.

- **`ValueError`**:
  - If `matrix` is not 4-dimensional.
  - If `point` is not a tuple of 4 integers.
  - If `radius` is not a positive integer.
  - If `point` coordinates are invalid for the given `matrix`.

---

### How It Works

1. **Validation**:
   - Ensures the input matrix is 4D and the `point` is within the matrix bounds.
   - Checks that the `radius` is positive and that the boundary flags (`x_bound`, `y_bound`) are boolean.

2. **Neighborhood Calculation**:
   - Uses `_calculate_bounds` to determine the latitude and longitude range based on the specified `radius`.
   - Retrieves indices for neighbors using `_get_indices` while respecting boundary conditions.

3. **Position Extraction**:
   - Calls `_calculate_positions` to compute the exact positions of the neighbors based on the `matrix` shape and `point` location.

4. **Value Retrieval**:
   - Extracts the neighboring values from the matrix and returns them as a NumPy array.

---

### Example Usage

```python
import numpy as np
from aml_pred_assim.data.core import get_predecessors

# Create a simulated 4D climate data matrix
matrix = np.random.rand(10, 5, 100, 100)  # Layers, Variables, Latitude, Longitude

# Define the point and neighborhood radius
point = (2, 1, 50, 50)  # (layer, variable, latitude, longitude)
radius = 3

# Extract neighboring values
neighbors = get_predecessors(matrix, point, radius)
print(neighbors)
```
# Utils Module

The `utils.py` module provides auxiliary functions for validating points, calculating bounds, and generating indices in multidimensional arrays, specifically tailored for climate data analysis. These utility functions are crucial for spatial operations in 4D data structures.

---

## Function:`_validate_point`

#### Purpose
Validates whether a given point is within the bounds of a 4D matrix.

#### Parameters
- **`matrix`** (`np.ndarray`): The 4D matrix to check.
- **`point`** (`Tuple[int, int, int, int]`): The point to validate, formatted as `(layer, variable, latitude, longitude)`.

#### Returns
- **`bool`**: `True` if the point is valid, `False` otherwise.

#### Example
```python
matrix = np.random.rand(10, 5, 100, 100)
point = (2, 1, 50, 50)
is_valid = _validate_point(matrix, point)
print(is_valid)  # True
```

## Function: `_calculate_bounds`

### Purpose

The `_calculate_bounds` function computes the latitude and longitude boundaries around a specific point in a 4D matrix. It considers the radius of the neighborhood and whether to enforce boundaries (x-axis and y-axis).

---

### Parameters

- **`shape`** (`Tuple[int, int, int, int]`): 
  The shape of the 4D matrix, typically `(layers, variables, latitude, longitude)`.

- **`point`** (`Tuple[int, int, int, int]`): 
  The point of interest in the matrix, given as `(layer, variable, latitude, longitude)`.

- **`r`** (`int`): 
  The radius for neighborhood calculation.

- **`x_bound`** (`bool`): 
  Whether to respect longitude boundaries (x-axis).

- **`y_bound`** (`bool`): 
  Whether to respect latitude boundaries (y-axis).

---

### Returns

- **`Tuple[int, int, int, int]`**: 
  A tuple containing the computed bounds:
  - `k_min`: Minimum latitude index.
  - `k_max`: Maximum latitude index.
  - `l_min`: Minimum longitude index.
  - `l_max`: Maximum longitude index.

---

### How It Works

1. **Latitude Bounds**:
   - If `y_bound` is `True`, ensures the latitude indices are within `[0, shape[2]-1]`.
   - If `y_bound` is `False`, allows latitude indices to extend beyond the matrix bounds.

2. **Longitude Bounds**:
   - If `x_bound` is `True`, ensures the longitude indices are within `[0, shape[3]-1]`.
   - If `x_bound` is `False`, allows longitude indices to extend beyond the matrix bounds.

3. **Adjustments**:
   - Adds or subtracts the radius (`r`) from the current latitude (`k`) and longitude (`l`) to compute the bounds.

---

### Example Usage

```python
shape = (10, 5, 100, 100)  # 4D matrix shape
point = (2, 1, 50, 50)     # Target point: layer=2, variable=1, latitude=50, longitude=50
radius = 3
x_bound = True
y_bound = True

bounds = _calculate_bounds(shape, point, radius, x_bound, y_bound)
print(bounds)  # Output: (47, 54, 47, 54)
```

## Function: `_calculate_positions`

### Purpose

The `_calculate_positions` function computes the exact positions of neighboring points around a given target point in a 4D matrix. This is useful for retrieving specific data points or analyzing spatial relationships within the matrix.

---

### Parameters

- **`i`** (`int`): 
  The current layer index in the matrix.

- **`j`** (`int`): 
  The current variable index in the matrix.

- **`shape`** (`Tuple[int, int, int, int]`): 
  The shape of the 4D matrix, typically `(layers, variables, latitude, longitude)`.

- **`k_ind`** (`np.ndarray`): 
  Array of latitude indices generated for the neighborhood.

- **`l_ind`** (`np.ndarray`): 
  Array of longitude indices generated for the neighborhood.

- **`k_min, k`** (`int`): 
  Minimum latitude bound and current latitude.

- **`l_min, l`** (`int`): 
  Minimum longitude bound and current longitude.

---

### Returns

- **`np.ndarray`**: 
  A 2D array where each row represents a position `(layer, variable, latitude, longitude)` within the neighborhood.

---

### How It Works

1. **Position Meshgrid**:
   - Generates position grids for the neighborhood using `np.meshgrid`, ensuring all possible combinations of neighboring indices are considered.

2. **Concatenate Positions**:
   - Combines different grids into a single array representing all valid neighboring positions in the 4D matrix.

3. **Edge Cases**:
   - Handles boundary conditions using the provided bounds and ensures valid positions are returned.

---

### Example Usage

```python
import numpy as np
from aml_pred_assim.utils import _calculate_positions

# Define matrix shape and neighborhood indices
shape = (10, 5, 100, 100)  # 4D matrix shape
k_indices = np.array([47, 48, 49])
l_indices = np.array([50, 51, 52])
k_min, k, l_min, l = 47, 50, 50, 53

# Compute positions
positions = _calculate_positions(
    i=2, 
    j=1, 
    shape=shape, 
    k_ind=k_indices, 
    l_ind=l_indices, 
    k_min=k_min, 
    k=k, 
    l_min=l_min, 
    l=l
)

print(positions.shape)  # Output: (number of positions, 4)
```