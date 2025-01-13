import numpy as np


class Position:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def asArray(self):
        return np.array([self.x, self.y, self.z], dtype=np.float32)

    def __str__(self):
        return f'Position({self.x}, {self.y}, {self.z})'
