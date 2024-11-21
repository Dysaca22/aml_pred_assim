# Library AMLS Pred-Assimilation

A Python library for accessing and processing climate data using two primary data sources:

- ERA5: High-resolution climate data access from the Copernicus Climate Data Store (CDS) via its API[1].
- MPAS: Management of climate prediction data across different spatial scales (Model Prediction Across Scales)[2].

The library processes data structures organized hierarchically into layers. Each main layer represents a height level, associated with an atmospheric pressure level. Within each height layer, there are sublayers corresponding to different climatic variables, such as temperature (T), wind components (U and V), humidity, among others. These sublayers are structured as two-dimensional matrices defined by latitude and longitude.

### Project Structure

```
aml_pred_assim/
│
├── aml_pred_assim/
│   ├── __init__.py                 # Initializes the module
│   ├── core.py                     # Contains the main class `Predecessor`
│   ├── data/                       # Submodule for data storage and management
│   │   ├── __init__.py
│   │   ├── mpas.py                 # `ModelPredictionAcrossScales` model
│   │   ├── cds.py                  # `ClimateDataStorage` handling
│   │   └── utils.py                # Optional utilities
│   ├── utils.py                    # General auxiliary functions (if needed)
│
├── tests/
│   ├── __init__.py
│   ├── test_core.py                # Unit tests for `Predecessor`
│   └── test_data.py                # Tests for the `data` submodule
│
├── setup.py                        # Configuration file to install the library
├── README.md                       # Project documentation
├── LICENSE                         # Library license
└── .gitignore                      # Files and folders to be ignored by Git

```

### Unit Tests

```
python -m unittest discover tests
```

### Publishing on PyPI

```
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*
```

# References
- [1] Copernicus Climate Change Service (C3S). (2017). *ERA5: Fifth generation of ECMWF atmospheric reanalyses of the global climate*. Copernicus Climate Data Store (CDS). Retrieved from https://cds.climate.copernicus.eu/
- [2]Skamarock, W. C., Klemp, J. B., Dudhia, J., Gill, D. O., Liu, Z., Berner, J., Wang, W., Powers, J. G., Duda, M. G., Barker, D. M., Huang, X.-Y., & Grell, G. A. (2012). A Description of the Advanced Research WRF Version 3. National Center for Atmospheric Research. Retrieved from https://www2.mmm.ucar.edu/wrf/users/docs/arw_v3.pdf