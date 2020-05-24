from typing import List

import numpy as np


class Brain:
    def __init__(self, seed, generation: int):
        self.state = np.random.default_rng(seed)
        self.seed = seed
        self.inputs = (25, 32)
        self.outputs = (3, 25)
        if generation == 0:
            self.syn0 = self.state.uniform(0, 1, self.inputs)
            self.syn1 = self.state.uniform(0, 1, self.outputs)
        else:
            self.syn0 = np.zeros(self.inputs, dtype=float)
            self.syn1 = np.zeros(self.outputs, dtype=float)
        self.fitness = 0
        self.generation = generation

    def think(self, vision: List[float]):
        # ones = np.ones((1,1))
        l0 = np.array(vision)
        l0 = l0.reshape((-1, 1))
        l1 = self.reul(np.dot(self.syn0, l0))
        # l1 = self.sigmoid(np.dot(self.syn0, l0))
        # l1 = np.concatenate((l1, ones))
        l2 = np.exp(np.dot(self.syn1, l1))
        sum_l2 = sum(l2)
        l2 = l2 / sum_l2
        # l2 = self.sigmoid(np.dot(self.syn1, l1))
        idx = np.argmax(l2, axis=0)
        return idx[0]

    def __str__(self):
        return f'{self.fitness}'

    def __repr__(self):
        return f'Brain {self.generation}:{self.fitness}'

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def tanh(x):
        return (2 / (1 + np.exp(-2 * x))) - 1

    @staticmethod
    def reul(x):
        return np.maximum(x, 0)
