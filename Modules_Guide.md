
# **Modules Guide**

This guide provides a detailed overview of the key modules, classes, and functions within the `aml_pred_assim` package. Each section outlines the purpose, main methods, and example usage of the components.

---

# **1. ClimateDataStorage Class**

The `ClimateDataStorage` class handles downloading, processing, and storing climate data from the **Copernicus Climate Data Store (CDS)**.

---

## **Key Methods**

### **`_validate`**
Ensures all required parameters are defined and valid.

---

### **`_get_hardcoded_variables`**
Maps human-readable climate variable names (e.g., `"temperature"`) to internal identifiers (e.g., `"t"`) using the configuration file `cds_variables.json`.

---

### **`_download_ensemble`**
Downloads data from the CDS API and saves it in NetCDF format.

---

### **`get_data`**
Processes NetCDF files into a multidimensional array with the structure `[Layers | Variables | Ensembles | Latitude | Longitude]`.

---

## **Example Usage**
```python
from aml_pred_assim.Mapper.cds import ClimateDataStorage

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
data = climate_storage.get_data()
print(data.shape)

# Example 2: Process an existing NetCDF file
climate_storage = ClimateDataStorage(
    variables=["temperature", "u_component_of_wind"],
    path="climate_data.nc"
)
data = climate_storage.get_data()
print(data)
```

---

# **2. Core Functions**

## **Overview**
Core functions provide utilities for retrieving and processing climate data.

---

### **Function: `get_climate_data_from_api`**
Fetches climate data from the CDS API.

#### **Parameters**:
- **`variables`** (`List[str]`): List of climate variables.
- **`datetime`** (`datetime`): Date and time for the data.
- **`pressure_levels`** (`List[str]`): Pressure levels to include.
- **`api_key`** (`str`): API key for accessing CDS.

#### **Returns**:
- A multidimensional NumPy array.

---

### **Function: `get_climate_data_from_file`**
Loads climate data from a local NetCDF file.

#### **Parameters**:
- **`variables`** (`List[str]`): Climate variables to retrieve.
- **`file_path`** (`str`): Path to the NetCDF file.

#### **Returns**:
- A multidimensional NumPy array.

---

## **Example Usage**
```python
from aml_pred_assim.core import get_climate_data_from_api, get_climate_data_from_file
from datetime import datetime

# Retrieve data from the API
data = get_climate_data_from_api(
    variables=["temperature"],
    datetime=datetime(2024, 11, 25, 12),
    pressure_levels=["1000"],
    api_key="YOUR_API_KEY"
)
print(data)

# Load data from a file
data = get_climate_data_from_file(
    variables=["temperature"],
    file_path="climate_data.nc"
)
print(data)
```

---

# **3. Predecessor Class**

The `Predecessor` class analyzes spatial relationships within a 4D climate data matrix.

---

## **Key Methods**

### **`get_point_predecessors`**
Finds neighboring points for a specific point in the matrix.

---

### **`get_all_predecessors`**
Computes predecessors for all points in the matrix.

---

### **Example Usage**
```python
from aml_pred_assim.Predecessor import Predecessor
import numpy as np

matrix = np.random.rand(2, 3, 10, 10)  # Example 4D data
predecessor = Predecessor(matrix)

# Find neighbors for a specific point
point = (1, 2, 5, 5)
neighbors = predecessor.get_point_predecessors(point, radius=2)
print(neighbors)

# Compute predecessors for all points
all_predecessors = predecessor.get_all_predecessors(radius=2)
print(all_predecessors[0])  # Predecessors for the first point
```

---

# **4. PrecisionMatrix Class**

The `PrecisionMatrix` class computes precision covariance matrices using Ridge regression.

---

## **Key Methods**

### **`store_T`**
Saves the `T` matrix in a NetCDF file.

---

### **Example Usage**
```python
from aml_pred_assim.PrecisionMatrix import PrecisionMatrix
import numpy as np

Xb = np.random.rand(100, 10)  # Input data (100 samples, 10 features)
pred = [np.array([0, 1, 2]) for _ in range(10)]  # Example predecessors

# Create the precision matrix
matrix = PrecisionMatrix(Xb, pred, n=10, alpha=0.1)

# Store and visualize the T matrix
matrix.store_T("T_matrix.nc")
matrix.show_T()
```

---

# **5. Utils Module**

The `utils.py` module provides auxiliary functions for matrix handling, including saving dense and sparse matrices to NetCDF files.

---

## **Key Functions**

### **`save_matrix_to_netcdf`**
Saves a dense or sparse matrix to a NetCDF file.

---

## **Example Usage**
```python
from aml_pred_assim.utils import save_matrix_to_netcdf
import numpy as np

# Save a dense matrix
dense_matrix = np.random.rand(5, 5)
save_matrix_to_netcdf(dense_matrix, "dense_matrix.nc")

# Save a sparse matrix
from scipy.sparse import coo_matrix
sparse_matrix = coo_matrix([[0, 1], [2, 0]])
save_matrix_to_netcdf(sparse_matrix, "sparse_matrix.nc", variable_name="sparse_data")
```

---

# **6. Testing**

The `tests` directory includes unit tests for validating core functionalities.

Run all tests:
```bash
python -m unittest discover tests
```

---
