from sklearn.linear_model import Ridge
from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt
import numpy as np
import sparse
import h5py


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


    def __calculate_precision_matrix(self):
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


    def get_decomposition_matrix(self):
        return self.value


    def show_T(self):
        T, _ = self.value
        plt.figure(figsize=(20, 20))
        plt.spy(T, marker='.')
        plt.show()


    def show_D(self):
        _, D = self.value
        plt.figure(figsize=(20, 20))
        plt.spy(D, marker='.')
        plt.show()


    def get_matrix(self):
        T, D = self.value
        Binv = T.T @ T + D
        return Binv


    def save_as_nc(self, filename: str):
        """
        Save the calculated precision matrix and diagonal matrix to an HDF5 file.

        Args:
            filename: Path to save the HDF5 file
        """
        T_matrix, D_matrix = self.value
        
        # Convert sparse matrices to dense tensors using the `sparse` library
        T_tensor = sparse.COO.from_scipy_sparse(T_matrix)
        D_tensor = sparse.COO.from_scipy_sparse(D_matrix)

        # Save tensors in HDF5 format
        with h5py.File(filename, 'w') as f:
            f.create_dataset('T_data', data=T_tensor.data)
            f.create_dataset('T_coords', data=T_tensor.coords)
            f.create_dataset('D_data', data=D_tensor.data)
            f.create_dataset('D_coords', data=D_tensor.coords)
            f.attrs['n'] = self.n

        print(f"HDF5 file saved as {filename}")
