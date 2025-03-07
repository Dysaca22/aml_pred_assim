![Logo](https://aml-cs.github.io/images/logo.jpg)

# Statistical Package for Computing Precision Covariance Matrices via Modified Cholesky Decomposition 🌍📊

This statistical package provides a method to compute precision covariance matrices using a **modified Cholesky decomposition** [1, 2] for **Atmospheric General Circulation Models (AGCMs)**. The technique takes advantage of a **pre-defined localization radius** structure to generate a **sparse estimator** of the precision matrix. This is achieved by leveraging an **ensemble of model realizations** to improve accuracy while reducing computational complexity.

### Key Features 🌟
- **Precision Matrix Estimation**: The method estimates the precision covariance matrices, which are essential for understanding the underlying relationships between variables in AGCMs.
- **Sparse Estimation**: The approach uses sparse matrix techniques to **save memory** and **reduce computation time**, making it scalable and efficient for large atmospheric models.
- **Localization Radius**: A predefined **localization radius** is used to structure the precision matrix, ensuring relevant correlations are captured while maintaining sparsity.
- **Ensemble Modeling**: The technique exploits an ensemble of model realizations, enhancing the robustness and reliability of the estimator.

### Applications and Use Cases 🌍💡
This estimator is particularly useful in the context of **Data Assimilation**, where it aids in efficiently solving the linear systems involved in the **assimilation step of observations** [3]. By exploiting the **special structure** of the estimated precision background, it allows for **more efficient solutions** and better performance in assimilation tasks.

### Optimization for Speed and Memory ⚡💾
We utilize **sparse libraries in Python** to ensure the method is both **memory-efficient** and **computationally fast** during the computation of precision matrices. This makes it suitable for large-scale atmospheric models that would otherwise be too demanding on resources.

### Easy Precision Matrix Building for Popular Models 🔧💻
As an additional feature, this package includes a **wrapper** to easily build precision matrices for the following well-known models in the context of weather forecast and climate prediction:
- **ERA5**: High-resolution climate data access from the **Copernicus Climate Data Store (CDS)** via its API [4].

These integrations simplify the process of incorporating real-world climate data into your model and precision matrix computations.

The library processes data organized into hierarchical layers. Each primary layer corresponds to a specific **height level**, which is associated with a corresponding **atmospheric pressure level**. Within each height layer, there are **sublayers** representing various **climatic variables** such as temperature ($T$), wind components ($u$ and $v$), humidity, and more. These sublayers are structured as **two-dimensional matrices** defined by **latitude** and **longitude**, allowing for detailed spatial representation of each variable.

### Developers
- Elías D. Niño-Ruiz, Ph.D. - Director of the Applied Math and Computer Science Lab (www.aml-cs.org), Universidad del Norte, Colombia - https://enino84.github.io/ - enino@uninorte.edu.co
- Giuliano Raffaele Frieri Quiroz, Computer Engineer, Universidad del Norte, Colombia - https://gfrieri.github.io/ - gfrieri@uninorte.edu.co
- Dylan Cantillo Arrieta, System Engineer, Universidad del Norte, Colombia - dilanc@uninorte.edu.co
- Nicolas Quintero Quintero, MSc. - PhD student in civil engineering, Universidad del Norte, Colombia - qnicolas@uninorte.edu.co

### Project Structure

```
aml_pred_assim/
│
├── aml_pred_assim/
│   ├── __init__.py                 # Initializes the module
│   ├── core.py                     # Contains core functions for climate data handling
│   ├── Predecessor.py              # Implements the `Predecessor` class
│   ├── PrecisionMatrix.py          # Implements the `PrecisionMatrix` class for matrix calculations
│   ├── mapper/                     # Submodule for data storage and management
│   │   ├── __init__.py
│   │   ├── cds.py                  # Handles climate data download and processing from CDS
│   │   ├── cds_variables.json      # Mapping of climate variable names
│   ├── utils.py                    # General auxiliary functions (if needed)
│   ├── tests/
│       ├── test_core.py                # Unit tests for `basic`
│       └── test_utils.py               # Tests for the `utils` submodule
│
├── setup.py                        # Configuration file to install the library
├── README.md                       # Project documentation
├── LICENSE                         # Library license
└── .gitignore                      # Files and folders to be ignored by Git

```

### Installation

Create a  virtual environment and activate it:
```
py -m venv venv
source venv/Scripts/activate
```
Install the library:
```
pip install -e .
```
Setup the environment:
```
py setup.py install
```

### Unit Tests

```
py -m unittest discover tests
```

### Publishing on PyPI

```
pip install twine
py setup.py sdist bdist_wheel
twine upload dist/*
```

### Modules guide and usage

https://github.com/Dysaca22/aml_pred_assim/blob/main/Modules_Guide.md

# References
- [1] Nino-Ruiz, Elias D., Adrian Sandu, and Xinwei Deng. "A parallel implementation of the ensemble Kalman filter based on modified Cholesky decomposition." Journal of Computational Science 36 (2019): 100654.
- [2] Nino-Ruiz, Elias D., Adrian Sandu, and Xinwei Deng. "An ensemble Kalman filter implementation based on modified Cholesky decomposition for inverse covariance matrix estimation." SIAM Journal on Scientific Computing 40.2 (2018): A867-A886.
- [3] Nino-Ruiz, Elias D., Luis G. Guzman-Reyes, and Rolando Beltran-Arrieta. "An adjoint-free four-dimensional variational data assimilation method via a modified Cholesky decomposition and an iterative Woodbury matrix formula." Nonlinear Dynamics 99.3 (2020): 2441-2457.
- [4] Copernicus Climate Change Service (C3S). (2017). *ERA5: Fifth generation of ECMWF atmospheric reanalyses of the global climate*. Copernicus Climate Data Store (CDS). Retrieved from https://cds.climate.copernicus.eu/


