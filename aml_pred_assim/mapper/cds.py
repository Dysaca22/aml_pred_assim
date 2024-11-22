"""
Climate Data Storage Module.

This module provides functionality for downloading and processing climate data from the Copernicus Climate Data Store (CDS).
"""

from typing import List, Optional
import os, cdsapi, json
import netCDF4 as nc
import numpy as np


class ClimateDataStorage:
    """A class to handle climate data storage and processing.
    
    This class manages the download, storage, and processing of climate data from ERA5 reanalysis.
    
    Attributes:
        variables (List[str]): List of climate variables to process
        years (List[str]): List of years to consider
        months (List[str]): List of months to consider
        days (List[str]): List of days to consider
        hours (List[str]): List of hours to consider
        pressure_levels (List[str]): List of pressure levels to consider
        hardcoded_variables (List[str]): Mapped variable names from configuration
        data (np.ndarray): Processed climate data array
    """
    
    def __init__(
            self, 
            variables: Optional[List[str]] = None,
            years: Optional[List[str]] = None,
            months: Optional[List[str]] = None,
            days: Optional[List[str]] = None,
            hours: Optional[List[str]] = None,
            pressure_levels: Optional[List[str]] = None,
            key: Optional[str] = None,
            path: Optional[str] = None,
        ) -> None:
        """Initialize the ClimateDataStorage instance.
        
        Args:
            variables: List of climate variables to process
            years: List of years to consider
            months: List of months to consider
            days: List of days to consider
            hours: List of hours to consider
            pressure_levels: List of pressure levels to consider
            key: API key for CDS access
            path: Optional path to existing NetCDF file
            
        Raises:
            ValueError: If required parameters are missing
        """
        if not path:
            self._validate(variables, years, months, days, hours, pressure_levels, key)
            self.hardcoded_variables = self.__get_hardcoded_variables(variables)
            
            self.variables = variables
            self.years = years
            self.months = months
            self.days = days
            self.hours = hours
            self.pressure_levels = pressure_levels
            
            self.__download_ensemble(key)
        else:
            if not variables:
                raise ValueError("No variables provided")
            self.hardcoded_variables = self.__get_hardcoded_variables(variables)
            self.variables = variables

        self.data = self.get_data(path)


    @staticmethod
    def _validate(variables: List[str], years: List[str], months: List[str], 
                days: List[str], hours: List[str], pressure_levels: List[str], 
                key: str) -> None:
        """Validate input parameters.
        
        Args:
            variables: List of climate variables
            years: List of years
            months: List of months
            days: List of days
            hours: List of hours
            pressure_levels: List of pressure levels
            key: API key
            
        Raises:
            ValueError: If any required parameter is None
        """
        if variables is None:
            raise ValueError("No variables provided")
        if years is None:
            raise ValueError("No years provided")
        if months is None:
            raise ValueError("No months provided")
        if days is None:
            raise ValueError("No days provided")
        if hours is None:
            raise ValueError("No hours provided")
        if pressure_levels is None:
            raise ValueError("No pressure levels provided")
        if key is None:
            raise ValueError("No key provided")
    

    def __get_hardcoded_variables(self, variables: List[str]) -> List[str]:
        """Get mapped variable names from configuration file.
        
        Args:
            variables: List of variable names to map
            
        Returns:
            List[str]: Mapped variable names
            
        Raises:
            Exception: If error occurs reading configuration file
        """
        print("\033[1;33m\nReading hardcoded data...\n\033[0m")
        try:
            with open(os.path.join(os.path.dirname(__file__), "cds_variables.json"), "r", encoding="utf-8") as f:
                hardcoded_variables = json.load(f)
            return [hardcoded_variables[var] for var in variables]
        except Exception as e:
            raise Exception(f"\033[1;31mError reading hardcoded data:\033[0m {e}")


    def __download_ensemble(self, key: str) -> None:
        """Download climate data ensemble from CDS.
        
        Args:
            key: API key for CDS access
            
        Raises:
            Exception: If error occurs during download
        """
        print("\033[1;33m\nDownloading ensemble...\n\033[0m")
        try:
            dataset = "reanalysis-era5-pressure-levels"
            request = {
                "product_type": ["ensemble_members"],
                "variable": self.variables,
                "year": self.years,
                "month": self.months,
                "day": self.days,
                "time": self.hours,
                "pressure_level": self.pressure_levels,
                "data_format": "netcdf",
                "download_format": "unarchived"
            }

            client = cdsapi.Client(url="https://cds.climate.copernicus.eu/api", key=key)
            client.retrieve(dataset, request).download("./ensemble.nc")
            print("\033[1;33m\nDownloaded ensemble\n\033[0m")
        except Exception as e:
            raise Exception(f"\033[1;31mError downloading ensemble:\033[0m {e}")            


    def get_data(self, path: Optional[str]) -> np.ndarray:
        """Process and extract data from NetCDF file.
        
        Args:
            path: Optional path to existing NetCDF file
            
        Returns:
            np.ndarray: Processed climate data array
            
        Raises:
            Exception: If error occurs during data processing
        """
        print("\033[1;33m\nGetting and extracting data...\n\033[0m")
        try:
            dataset = nc.Dataset(path if path else "./ensemble.nc")
            pressure_levels = dataset.variables["pressure_level"].shape[0]
            ensembles = dataset.variables[self.hardcoded_variables[0]].shape[0]

            data_layers = []  # Ensemble | Layer | Variable | Latitude | Longitude
            for ensemble_index in range(ensembles):
                ensemble_data = []
                for i_layer in range(pressure_levels):
                    layer = []
                    for variable in self.hardcoded_variables:
                        level = dataset.variables[variable][ensemble_index, 0, i_layer, :, :].data
                        layer.append(level)
                    ensemble_data.append(np.array(layer))
                data_layers.append(np.array(ensemble_data))
            
            return np.array(data_layers)  # Ensemble is now the first dimension
        except Exception as e:
            raise Exception(f"\033[1;31mError getting or extracting data:\033[0m {e}")
