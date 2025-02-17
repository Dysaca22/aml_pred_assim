from setuptools import setup, find_packages

setup(
    name='aml_pred_assim',
    version='0.1.0',
    description='A package for predictive assimilation',
    author='Nino-Ruiz, Elias D',
    author_email='enino@uninorte.edu.co',
    packages=find_packages(),
    install_requires=[
        'setuptools==75.5.0',
        'wheel==0.45.0',
        'scikit-learn==1.5.2',
        'numpy==2.1.3',
        'scipy==1.14.1',
        'cdsapi==0.7.4',
        'netCDF4==1.7.2'
    ],  # Dependencias externas
    python_requires='>=3.12.2',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md', encoding="utf8").read(),
    long_description_content_type='text/markdown',
)
