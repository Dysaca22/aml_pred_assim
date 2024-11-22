from sklearn.linear_model import Ridge
from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt
from typing import Tuple
import numpy as np

from .utils import save_matrix_to_netcdf


class PrecisionMatrix:
    def __init__(self, Xb: np.ndarray, pred: list, n: int, alpha: float = 1):
        """
        Initialize the PrecisionMatrixCalculator with the input data.

        Args:
            Xb: Input data matrix of shape (samples, features)
            pred: Array of predecessor indices for each feature
            n: Number of features/variables
            alpha: Ridge regression regularization parameter (default=1)
        """
        if not isinstance(Xb, np.ndarray) or len(Xb.shape) != 2:
            raise ValueError("Xb must be a 2D numpy array")
        if not isinstance(pred, list):
            raise TypeError("pred must be a list")
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer")
        if not isinstance(alpha, (int, float)) or alpha <= 0:
            raise ValueError("alpha must be a positive number")
        if len(pred) != n:
            raise ValueError("pred length must match n")

        self.Xb = Xb
        self.pred = pred
        self.n = n
        self.alpha = alpha
        self.value = self.__calculate_precision_matrix()


    def __calculate_precision_matrix(self) -> Tuple[coo_matrix, coo_matrix]:
        """
        Private method to calculate the precision matrix using Ridge regression.

        Returns:
            T: Sparse matrix (COO format) containing coefficients
            D: Sparse diagonal matrix (COO format) with precision values
        """
        Xb_ = self.Xb
        lr = Ridge(fit_intercept=False, alpha=self.alpha)
        T, D, I, J = [], [], [], []

        for i, p in enumerate(self.pred):
            I.append(i)
            J.append(i)
            T.append(1)
            if i == 0:
                D.append(1 / np.var(Xb_[:, i]))
            else:
                y = Xb_[:, i]
                X = Xb_[:, p]
                lr.fit(X, y)
                residuals = y - lr.predict(X)
                I.extend([i] * p.size)
                J.extend(p.tolist())
                T.extend((-lr.coef_).tolist())
                D.append(1 / np.var(residuals))

        i = np.array(I, dtype='int32')
        j = np.array(J, dtype='int32')
        id = np.arange(self.n)
        T_matrix = coo_matrix((T, (i, j)))
        D_matrix = coo_matrix((D, (id, id)))
        return T_matrix, D_matrix


    def get_decomposition_matrix(self) -> Tuple[coo_matrix, coo_matrix]:
        return self.value


    def show_T(self) -> None:
        T, _ = self.value
        plt.figure(figsize=(20, 20))
        plt.spy(T, marker='.')
        plt.show()


    def show_D(self) -> None:
        _, D = self.value
        plt.figure(figsize=(20, 20))
        plt.spy(D, marker='.')
        plt.show()


    def get_matrix(self) -> coo_matrix:
        T, D = self.value
        Binv = T.T @ T + D
        return Binv

    
    def store_T(self, filename: str = "T.nc") -> None:
        """
        Store the T matrix in a NetCDF file.
        """
        T, _ = self.value
        save_matrix_to_netcdf(T, filename)


    def store_D(self, filename: str = "D.nc") -> None:
        """
        Store the D matrix in a NetCDF file.
        """
        _, D = self.value
        save_matrix_to_netcdf(D, filename)


    def store_matrix(self, filename: str = "Binv.nc") -> None:
        """
        Store the precision matrix in a NetCDF file.
        """
        Binv = self.get_matrix()
        save_matrix_to_netcdf(Binv, filename)