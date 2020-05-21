from typing import List

import numpy as np


class Brain:
    def __init__(self, seed, generation: int):
        self.state = np.random.RandomState(seed)
        self.seed = seed
        self.inputs = (28,29)
        self.hidden = (12, 29)
        self.outputs = (4, 13)
        if generation == 0:
            self.syn0 = 2 * self.state.random(self.inputs) - 1
            self.syn1 = 2 * self.state.random(self.hidden) - 1
            self.syn2 = 2 * self.state.random(self.outputs) - 1
        else:
            self.syn0 = np.zeros(self.inputs, dtype=float)
            self.syn1 = np.zeros(self.hidden, dtype=float)
            self.syn2 = np.zeros(self.outputs, dtype=float)
        self.fitness = 0
        self.generation = generation

    def think(self, vision: List[float], direction: List[int]):
        one = np.ones((1, 1))
        l0 = np.array(vision)
        l0 = self.tanh(l0)
        l0 = np.concatenate((l0, np.array(direction)))
        l0 = l0.reshape((-1, 1))
        l0 = np.concatenate((l0, one))
        l1 = self.sigmoid(np.dot(self.syn0, l0))
        l1 = np.concatenate((l1, one))
        l2 = self.sigmoid(np.dot(self.syn1, l1))
        l2 = np.concatenate((l2, one))
        l3 = self.sigmoid(np.dot(self.syn2, l2))
        idx = np.argmax(l3, axis=0)
        return idx[0]

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def tanh(x):
        return (2 / (1 + np.exp(-2 * x))) - 1
