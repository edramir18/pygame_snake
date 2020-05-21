from typing import List

import numpy as np


class Brain:
    def __init__(self, seed, generation: int):
        self.state = np.random.RandomState(seed)
        self.hidden = (16, 25)
        self.outputs = (4, 17)
        if generation == 0:
            self.syn0 = 2 * self.state.random(self.hidden) - 1
            # type: np.ndarray
            self.syn1 = 2 * self.state.random(self.outputs) - 1
            # type: np.ndarray
        else:
            self.syn0 = np.zeros(self.hidden, dtype=float)
            self.syn1 = np.zeros(self.outputs, dtype=float)
        self.fitness = 0
        self.generation = generation

    def think(self, data: List[float]):
        data.append(1.0)
        l0 = np.array(data)
        l0 = l0.reshape((-1, 1))
        l1 = self.sigmoid(np.dot(self.syn0, l0))
        one = np.ones((1, 1))
        l1 = np.concatenate((l1, one))
        l2 = self.sigmoid(np.dot(self.syn1, l1))
        idx = np.argmax(l2, axis=0)
        return idx[0]

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
