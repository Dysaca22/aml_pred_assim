# Library AMLS Pred-Assimilation

A Python library for accessing and processing climate data using two primary data sources:

- ERA5: High-resolution climate data access from the Copernicus Climate Data Store (CDS) via its API[1].
- MPAS: Management of climate prediction data across different spatial scales (Model Prediction Across Scales)[2].

The library processes data structures organized hierarchically into layers. Each main layer represents a height level, associated with an atmospheric pressure level. Within each height layer, there are sublayers corresponding to different climatic variables, such as temperature (T), wind components (U and V), humidity, among others. These sublayers are structured as two-dimensional matrices defined by latitude and longitude.

### Estructura del proyecto

```
aml_pred_assim/
│
├── aml_pred_assim/
│   ├── __init__.py                 # Inicializa el módulo
│   ├── core.py                     # Contiene la clase principal `Predecessor`
│   ├── data/                       # Submódulo para almacenamiento y manejo de datos
│   │   ├── __init__.py
│   │   ├── mpas.py                 # Modelo `ModelPredictionAcrossScales`
│   │   ├── cds.py                  # Almacenamiento `ClimateDataStorage`
│   │   └── utils.py                # Utilidades opcionales
│   ├── utils.py                    # Funciones auxiliares generales (si se necesitan)
│
├── tests/
│   ├── __init__.py
│   ├── test_core.py                # Pruebas unitarias para `Predecessor`
│   └── test_data.py                # Pruebas para el submódulo `data`
│
├── setup.py                        # Archivo de configuración para instalar la librería
├── README.md                       # Documentación del proyecto
├── LICENSE                         # Licencia de la librería
└── .gitignore                      # Archivos y carpetas a ignorar por Git
```

### Pruebas unitarias

```
python -m unittest discover tests
```

### Publicación en PyPI

```
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*
```

# References
- [1] Copernicus Climate Change Service (C3S). (2017). *ERA5: Fifth generation of ECMWF atmospheric reanalyses of the global climate*. Copernicus Climate Data Store (CDS). Retrieved from https://cds.climate.copernicus.eu/
- [2]Skamarock, W. C., Klemp, J. B., Dudhia, J., Gill, D. O., Liu, Z., Berner, J., Wang, W., Powers, J. G., Duda, M. G., Barker, D. M., Huang, X.-Y., & Grell, G. A. (2012). A Description of the Advanced Research WRF Version 3. National Center for Atmospheric Research. Retrieved from https://www2.mmm.ucar.edu/wrf/users/docs/arw_v3.pdf