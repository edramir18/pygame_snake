from typing import List

import numpy as np


class Brain:
    def __init__(self, seed, generation: int):
        self.state = np.random.default_rng(seed)
        self.seed = seed
        self.inputs = (28, 28)
        self.hidden = (12, 28)
        self.outputs = (4, 12)
        if generation == 0:
            self.syn0 = 2 * self.state.random(size=self.inputs) - 1
            self.syn1 = 2 * self.state.random(size=self.hidden) - 1
            self.syn2 = 2 * self.state.random(size=self.outputs) - 1
        else:
            self.syn0 = np.zeros(self.inputs, dtype=float)
            self.syn1 = np.zeros(self.hidden, dtype=float)
            self.syn2 = np.zeros(self.outputs, dtype=float)
        self.fitness = 0
        self.generation = generation

    def think(self, vision: List[float], direction: List[int]):
        l0 = np.array(vision)
        # print(l0)
        # l0 = self.sigmoid(l0 * 100)
        l0 = np.concatenate((l0, np.array(direction)))
        l0 = l0.reshape((-1, 1))
        l1 = self.sigmoid(np.dot(self.syn0, l0))
        l2 = self.sigmoid(np.dot(self.syn1, l1))
        l3 = self.sigmoid(np.dot(self.syn2, l2))
        idx = np.argmax(l3, axis=0)
        return idx[0]

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def tanh(x):
        return (2 / (1 + np.exp(-2 * x))) - 1
