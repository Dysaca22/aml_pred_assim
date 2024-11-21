"""
MPAS Data Storage Module.

This module provides functionality for downloading and processing MPAS data meshes.
"""

from typing import Optional, List
import os
import requests
import numpy as np
import netCDF4 as nc
from scipy.interpolate import griddata
import tarfile


class MPASDataStorage:
    """A class to handle MPAS mesh data storage and processing.
    
    This class manages the download, storage, and processing of MPAS meshes into standard formats.
    
    Attributes:
        variables (List[str]): List of variables to extract from the MPAS dataset
        target_lat (np.ndarray): Target latitude grid for interpolation
        target_lon (np.ndarray): Target longitude grid for interpolation
        mesh_url (str): URL to the MPAS mesh file
        static_url (str): URL to the MPAS static file
        data (np.ndarray): Processed MPAS data array
    """

    def __init__(
            self,
            variables: Optional[List[str]],
            target_lat: Optional[np.ndarray],
            target_lon: Optional[np.ndarray],
            mesh_url: str,
            static_url: Optional[str] = None,
            path: Optional[str] = None,
        ) -> None:
        self.variables = variables
        self.target_lat = target_lat
        self.target_lon = target_lon
        self.mesh_url = mesh_url
        self.static_url = static_url

        if not path:  # If no local file provided, download and process the mesh
            downloaded_path = self._download_mesh()
            self.data = self._process_data(downloaded_path)
        else:  # Process the provided path
            self.data = self._process_data(path)

    def _download_mesh(self) -> str:
        """Download MPAS mesh and return the extracted file path."""
        os.makedirs("./mpas_data", exist_ok=True)
        archive_path = os.path.join("./mpas_data", os.path.basename(self.mesh_url))

        # Download the mesh
        print("\033[1;33m\nDownloading MPAS mesh...\n\033[0m")
        response = requests.get(self.mesh_url, stream=True)
        with open(archive_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        # Extract the tar.gz file
        extracted_path = None
        if tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(path="./mpas_data")
                # Assume the extracted file is a NetCDF file, find it
                extracted_path = [
                    os.path.join("./mpas_data", member.name)
                    for member in tar.getmembers()
                    if member.name.endswith('.nc')
                ][0]  # Take the first NetCDF file
        else:
            raise Exception(f"Downloaded file is not a valid tar.gz archive: {archive_path}")

        return extracted_path


    def _process_data(self, path: str) -> np.ndarray:
        """Process and extract data from MPAS NetCDF file.
        
        Args:
            path: Path to NetCDF file
            
        Returns:
            np.ndarray: Processed MPAS data array in (layer, variable, lat, lon) format
        """
        print("\033[1;33m\nProcessing MPAS data...\n\033[0m")
        try:
            dataset = nc.Dataset(path)
            lat = dataset.variables["latCell"][:]
            lon = dataset.variables["lonCell"][:]
            data_layers = []  # List of (layer, lat, lon) arrays

            for variable in self.variables:
                variable_data = dataset.variables[variable][:]
                interpolated_data = []

                for level in range(variable_data.shape[1]):  # Assume levels are in dim 1
                    interp_layer = griddata(
                        points=(lat, lon),
                        values=variable_data[:, level],
                        xi=(self.target_lat, self.target_lon),
                        method='linear'
                    )
                    interpolated_data.append(interp_layer)

                data_layers.append(np.stack(interpolated_data, axis=0))  # Stack layers

            return np.array(data_layers)  # Shape: (variable, layer, lat, lon)
        except Exception as e:
            raise Exception(f"\033[1;31mError processing MPAS data:\033[0m {e}")