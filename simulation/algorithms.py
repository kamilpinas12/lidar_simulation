import numpy as np
from typing import Tuple, Dict


class ICP:
    def __init__(self, map: np.ndarray, data: np.ndarray):
        self.map = map
        self.data = data
        self.data_size = self.data.shape[1]
        self.c = np.nan

    # Get nearest neighbour for every data node
    def correspondence(self):
        correspondences = np.ones((self.data_size + 1, 2))
        for i in range(self.data_size + 1):
            j = min(np.arange(self.data_size + 1), key=lambda x: np.linalg.norm(self.data[i]-self.map[x]))
            correspondences[i][0], correspondences[i][1] = i, j
        self.c = correspondences.astype(np.int16)

    # Get rotation
    def rotation(self):
        k11 = np.cov(self.map[self.c[:, 0], 0], self.data[self.c[:, 1], 0])
        k12 = np.cov(self.map[self.c[:, 0], 0], self.data[self.c[:, 1], 1])
        k21 = np.cov(self.map[self.c[:, 0], 1], self.data[self.c[:, 1], 0])
        k22 = np.cov(self.map[self.c[:, 0], 1], self.data[self.c[:, 1], 1])
        K = np.array([[k11, k12], [k21, k22]])
        U, S, V_t = np.linalg.svd(K)
        return U@V_t

    # Get translation
    def translation(self):
        return (self.map[self.c[:, 0], 0].mean() - self.data[self.c[:, 1], 0].mean(),
                self.map[self.c[:, 0], 1].mean() - self.data[self.c[:, 1], 1].mean())
