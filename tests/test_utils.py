import numpy as np
import unittest

from aml_pred_assim.utils import (
    _validate_point,
    _calculate_bounds,
    _get_indices,
    _calculate_positions
)


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_matrix = np.zeros((2, 3, 4, 5))
        self.test_shape = (2, 3, 4, 5)
    

    def test_validate_point(self):
        # Test valid point
        self.assertTrue(_validate_point(self.test_matrix, (1, 2, 3, 4)))
        # Test invalid points
        self.assertFalse(_validate_point(self.test_matrix, (2, 2, 3, 4)))
        self.assertFalse(_validate_point(self.test_matrix, (-1, 2, 3, 4)))
        self.assertFalse(_validate_point(self.test_matrix, (1, 3, 3, 4)))
        self.assertFalse(_validate_point(self.test_matrix, (1, 2, 4, 4)))
        self.assertFalse(_validate_point(self.test_matrix, (1, 2, 3, 5)))


    def test_calculate_bounds(self):
        point = (1, 2, 2, 3)
        r = 1
        
        # Test with boundaries respected
        bounds = _calculate_bounds(self.test_shape, point, r, True, True)
        self.assertEqual(bounds, (1, 3, 2, 4))
        
        # Test with no boundaries
        bounds = _calculate_bounds(self.test_shape, point, r, False, False)
        self.assertEqual(bounds, (1, 4, 2, 5))
        
        # Test edge cases
        point_edge = (1, 2, 0, 0)
        bounds_edge = _calculate_bounds(self.test_shape, point_edge, r, True, True)
        self.assertEqual(bounds_edge, (0, 2, 0, 2))


    def test_get_indices(self):
        # Test normal case
        k_ind, l_ind = _get_indices(self.test_shape, 1, 3, 2, 4, 2)
        np.testing.assert_array_equal(k_ind, np.array([1, 2]))
        np.testing.assert_array_equal(l_ind, np.array([2, 3]))
        
        # Test periodic boundaries
        k_ind, l_ind = _get_indices(self.test_shape, -1, 1, 4, 6, 0)
        np.testing.assert_array_equal(k_ind, np.array([0, 3]))
        np.testing.assert_array_equal(l_ind, np.array([0, 4]))
        
        # Test empty case
        k_ind, l_ind = _get_indices(self.test_shape, 2, 2, 2, 3, 2)
        np.testing.assert_array_equal(k_ind, np.array([2]))
        np.testing.assert_array_equal(l_ind, np.array([2]))


    def test_calculate_positions(self):
        k_ind = np.array([1, 2])
        l_ind = np.array([2, 3])
        positions = _calculate_positions(1, 2, self.test_shape, k_ind, l_ind, 1, 2, 2, 3)
        
        # Test shape of output
        self.assertEqual(positions.shape[1], 4)
        
        # Test if positions are within bounds
        self.assertTrue(np.all(positions[:, 0] <= self.test_shape[0]))
        self.assertTrue(np.all(positions[:, 1] <= self.test_shape[1]))
        self.assertTrue(np.all(positions[:, 2] <= self.test_shape[2]))
        self.assertTrue(np.all(positions[:, 3] <= self.test_shape[3]))
        
        # Test if positions are non-negative
        self.assertTrue(np.all(positions >= 0))


if __name__ == '__main__':
    unittest.main()
