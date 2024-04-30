import numpy as np
from typing import Tuple


class ICP:
    def __init__(self, map: np.ndarray, data: np.ndarray) -> None:
        self.map = map
        self.data = data
        self.data_size = self.data.shape[0]
        self.c = np.nan
        self.rotation_matrix = np.eye(2)
        self.translation_vector = np.zeros(2)

    # Get nearest neighbour for every data node
    def correspondence(self) -> None:
        correspondences = np.ones((self.data_size, 2))
        for i in range(self.data_size):
            j = min(np.arange(self.data_size), key=lambda x: np.linalg.norm(self.data[i]-self.map[x]))
            correspondences[i][0], correspondences[i][1] = j, i
        self.c = correspondences.astype(np.int16)

    # Get rotation
    def rotation(self) -> np.ndarray:
        # TODO: optimize covariance calculation (may be done by one cov function)
        k = np.cov(np.array([self.map[self.c[:, 0], 0], self.map[self.c[:, 0], 1], 
                             self.data[self.c[:, 1], 0], self.data[self.c[:, 1], 1]]))
        K = np.array([[k[0, 2], k[0, 3]], [k[1, 2], k[1,3]]])
        U, _, V_t = np.linalg.svd(K)
        return U@V_t

    # Get translation
    def translation(self):
        return (self.map[self.c[:, 0], 0].mean() - self.data[self.c[:, 1], 0].mean(),
                self.map[self.c[:, 0], 1].mean() - self.data[self.c[:, 1], 1].mean())

    # Iterate ICP
    def iterate(self, iteration:int) -> None:
        for _ in range(iteration):
            self.correspondence()
            t = self.translation()
            r = self.rotation()
            
            for i in range(self.data_size):
                self.data[i] = r @ self.data[i] + t
                
            self.rotation_matrix = r @ self.rotation_matrix
            self.translation_vector = self.translation_vector + t
    
    # Get final transformation
    def get_transformation(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.rotation_matrix, self.translation_vector
    
    # Get transformed data
    def get_transformed_data(self) -> np.ndarray:
        return self.data
        
            
