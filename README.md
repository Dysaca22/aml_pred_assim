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