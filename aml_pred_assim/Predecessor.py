from typing import List, Tuple
import numpy as np


class Predecessor:
    def __init__(self, matrix: np.ndarray):
        """
        Initialize the Predecessor with a 4D matrix.

        Args:
            matrix: 4D numpy array representing climate data.
        """
        if not isinstance(matrix, np.ndarray):
            raise TypeError("Matrix must be a numpy array")
        if len(matrix.shape) != 4:
            raise ValueError("Matrix must be 4-dimensional")
        
        self.matrix = matrix
        self.all_predecessors = None


    def __validate_point(self, point: Tuple[int, int, int, int]) -> bool:
        """
        Validate if a point is within matrix bounds.

        Args:
            matrix: 4D numpy array
            point: Tuple of 4 integers representing (layer, variable, latitude, longitude)

        Returns:
            bool indicating if point is valid
        """
        i, j, k, l = point
        shape = self.matrix.shape
        return all(0 <= idx < dim for idx, dim in zip((i, j, k, l), shape))


    def __calculate_bounds(self, shape: Tuple[int, int, int, int], point: Tuple[int, int, int, int], 
                        r: int, x_bound: bool, y_bound: bool) -> Tuple[int, int, int, int]:
        """
        Calculate bounds for latitude and longitude.

        Args:
            shape: Shape of the matrix
            point: Tuple of 4 integers representing (layer, variable, latitude, longitude)
            r: Radius for neighborhood calculation
            x_bound: Whether to respect x-axis boundaries
            y_bound: Whether to respect y-axis boundaries

        Returns:
            Tuple of (k_min, k_max, l_min, l_max)
        """
        _, _, k, l = point
        k_min = max(k-r, 0) if y_bound else k-r
        k_max = min(shape[2], k+r+1) if y_bound else k+r+1
        l_min = max(l-r, 0) if x_bound else l-r
        l_max = min(shape[3], l+r+1) if x_bound else l+r+1
        return k_min, k_max, l_min, l_max


    def __get_indices(self, shape: Tuple[int, int, int, int], k_min: int, k_max: int, 
                    l_min: int, l_max: int, k: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get unique indices considering periodic boundaries.

        Args:
            shape: Shape of the matrix
            k_min, k_max: Latitude bounds
            l_min, l_max: Longitude bounds
            k: Current latitude point

        Returns:
            Tuple of (k_indices, l_indices)
        """
        
        k_ind = np.unique(np.arange(k_min, k_max) % shape[2])
        l_ind = np.unique(np.arange(l_min, l_max) % shape[3])

        if k_ind.size == 0:
            k_ind = np.array([k])
        
        return k_ind, l_ind


    def __calculate_positions(self, i: int, j:int, shape: Tuple[int, int, int, int], k_ind: np.ndarray, 
                            l_ind: np.ndarray, k_min: int, k: int, l_min: int, l: int) -> np.ndarray:
        """
        Calculate predecessor positions.

        Args:
            i: Current layer
            shape: Shape of the matrix
            k_ind, l_ind: Latitude and longitude indices
            k_min, k: Latitude values
            l_min, l: Longitude values

        Returns:
            Array of positions
        """
        positions = []
        positions.append(np.array(np.meshgrid(np.arange(i), np.arange(shape[1]), k_ind, l_ind)).T.reshape(-1, 4))
        positions.append(np.array(np.meshgrid([i], np.arange(j), k_ind, l_ind)).T.reshape(-1, 4))
        positions.append(np.array(np.meshgrid([i], [j], k_ind, np.arange(l_min, l))).T.reshape(-1, 4))
        positions.append(np.array(np.meshgrid([i], [j], np.arange(k_min, k), [l])).T.reshape(-1, 4))
        return np.concatenate(positions)


    def __flat_indices(self, positions, matrix) -> List:
        """
        Convert multi-dimensional array positions to flattened indices.

        Args:
            positions: Array of position tuples (i, j, k, l)
            matrix: Input matrix to get shape information

        Returns:
            List of flattened indices corresponding to the input positions
        """
        indices = []
        for pred in positions:
            i, j, k, l = pred
            index = l * matrix.shape[1] * matrix.shape[2] * matrix.shape[0] + k * matrix.shape[1] * matrix.shape[0] + j * matrix.shape[0] + i
            indices.append(index)
        return indices


    def get_point_predecessors(self, point: Tuple[int, int, int, int], radius: int, x_bound: bool = True, y_bound: bool = True) -> np.ndarray:
        """
        Get predecessors for a given point in the matrix.
        """
        if not isinstance(point, tuple) or len(point) != 4 or not all(isinstance(x, int) for x in point):
            raise ValueError("Point must be a tuple of 4 integers")
        if not isinstance(radius, int) or radius <= 0:
            raise ValueError("Radius must be a positive integer")
        if not isinstance(x_bound, bool) or not isinstance(y_bound, bool):
            raise TypeError("x_bound and y_bound must be boolean values")
        if not self.__validate_point(point):
            return np.array([])

        lat_min, lat_max, lon_min, lon_max = self.__calculate_bounds(self.matrix.shape, point, radius, x_bound, y_bound)
        lat_indices, lon_indices = self.__get_indices(self.matrix.shape, lat_min, lat_max, lon_min, lon_max, point[2])
        positions = self.__calculate_positions(point[0], point[1], self.matrix.shape, lat_indices, lon_indices, lat_min, point[2], lon_min, point[3])
        return self.__flat_indices(positions, self.matrix)


    def get_all_predecessors(self, radius: int, x_bound: bool = True, y_bound: bool = True) -> np.ndarray:
        """
        Get all predecessors for all points in the matrix.

        Args:
            radius: Radius for neighborhood calculation.
            x_bound: Whether to respect x-axis boundaries.
            y_bound: Whether to respect y-axis boundaries.

        Returns:
            numpy array of predecessors for all points.
        """
        if self.all_predecessors is not None:
            return self.all_predecessors
        results = []
        for layer in range(self.matrix.shape[0]):
            for variable in range(self.matrix.shape[1]):
                for longitude in range(self.matrix.shape[3]):
                    for latitude in range(self.matrix.shape[2]):
                        point = (layer, variable, latitude, longitude)
                        predecessors = self.get_point_predecessors(point, radius, x_bound, y_bound)
                        results.append(np.array(predecessors))
        self.all_predecessors = results
        return results