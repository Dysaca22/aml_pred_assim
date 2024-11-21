from setuptools import setup, find_packages

setup(
    name='aml_pred_assim',
    version='0.1.0',
    description='Una librería para cálculos básicos',
    author='Tu Nombre',
    author_email='tu_email@example.com',
    packages=find_packages(),
    install_requires=[
        'setuptools==75.5.0',
        'wheel==0.45.0',
        'scikit-learn==1.5.2',
        'numpy==2.1.3',
        'scipy==1.14.1'
    ],  # Dependencias externas
    python_requires='>=3.12.2',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
