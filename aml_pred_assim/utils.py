from typing import Tuple
import numpy as np


def _validate_point(matrix: np.ndarray, point: Tuple[int, int, int, int]) -> bool:
    """
    Validate if a point is within matrix bounds.

    Args:
        matrix: 4D numpy array
        point: Tuple of 4 integers representing (layer, variable, latitude, longitude)

    Returns:
        bool indicating if point is valid
    """
    i, j, k, l = point
    shape = matrix.shape
    return all(0 <= idx < dim for idx, dim in zip((i, j, k, l), shape))


def _calculate_bounds(shape: Tuple[int, int, int, int], point: Tuple[int, int, int, int], 
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
    k_max = min(shape[2]-1, k+r+1) if y_bound else k+r+1
    l_min = max(l-r, 0) if x_bound else l-r
    l_max = min(shape[3]-1, l+r+1) if x_bound else l+r+1
    return k_min, k_max, l_min, l_max


def _get_indices(shape: Tuple[int, int, int, int], k_min: int, k_max: int, 
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


def _calculate_positions(i: int, j:int, shape: Tuple[int, int, int, int], k_ind: np.ndarray, 
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
    positions.append(np.array(np.meshgrid([i], [j], np.arange(k_min, k), l)).T.reshape(-1, 4))
    return np.concatenate(positions)


def _flat_indices(positions, matrix):
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