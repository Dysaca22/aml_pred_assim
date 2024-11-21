# ClimateDataStorage Class

## What is `ClimateDataStorage`?

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