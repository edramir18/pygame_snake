from typing import List

import numpy as np


class Brain:
    def __init__(self, seed, generation: int):
        self.state = np.random.default_rng(seed)
        self.seed = seed
        self.inputs = (20, 21)
        self.outputs = (4, 21)
        if generation == 0:
            self.syn0 = self.state.uniform(-1, 1, self.inputs)
            self.syn1 = self.state.uniform(-1, 1, self.outputs)
        else:
            self.syn0 = np.zeros(self.inputs, dtype=float)
            self.syn1 = np.zeros(self.outputs, dtype=float)
        self.fitness = 0
        self.generation = generation

    def think(self, vision: List[float], direction: List[int]):
        one = np.ones((1, 1))
        l0 = np.array(vision)
        l0 = np.concatenate((l0, np.array(direction)))
        l0 = l0.reshape((-1, 1))
        l0 = np.concatenate((l0, one))
        l1 = self.sigmoid(np.dot(self.syn0, l0))
        l1 = np.concatenate((l1, one))
        l2 = self.sigmoid(np.dot(self.syn1, l1))
        idx = np.argmax(l2, axis=0)
        return idx[0]

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def tanh(x):
        return (2 / (1 + np.exp(-2 * x))) - 1
