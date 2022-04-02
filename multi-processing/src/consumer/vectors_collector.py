import numpy as np
from numpy.typing import NDArray

class VectorsCollector:
    row: int
    matrix: NDArray

    def __init__(self, capacity: int, vector_size: int):
        self.row = 0
        self.matrix = np.zeros((capacity, vector_size))

    def reset(self):
        self.row = 0

    def add_vector(self, vector: NDArray):

        if self.row >= self.matrix.shape[0]:
            raise IndexError("Vectors has reached the matrix capacity")

        self.matrix[self.row] = vector
        self.row += 1

    def is_full(self):
        return self.row >= self.matrix.shape[0]