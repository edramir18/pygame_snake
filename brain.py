import numpy as np


class Brain:
    def __init__(self, seed, generation: int):
        self.state = np.random.RandomState(seed)
        self.inputs = 24
        self.hidden = 16
        self.outputs = 4
        if generation == 0:
            self.syn0 = 2 * self.state.random((24, 4)) - 1  # type: np.ndarray
            # self.syn1 = 2 * self.state.random((16, 16)) - 1  # type: np.ndarray
            # self.syn2 = 2 * self.state.random((16, 4)) - 1  # type: np.ndarray
        else:
            self.syn0 = np.zeros((24, 4), dtype=float)
            # self.syn1 = np.zeros((16, 16), dtype=float)
            # self.syn2 = np.zeros((16, 4), dtype=float)
        self.fitness = 0
        self.generation = generation

    def think(self, data):
        l0 = np.array(data)
        np.reshape(l0, (1, -1))
        l1 = self.sigmoid(np.dot(l0, self.syn0))
        # l2 = self.sigmoid(np.dot(l1, self.syn1))
        # l3 = self.sigmoid(np.dot(l2, self.syn2))
        idx, _ = max([(k, w) for k, w in enumerate(l1)], key=lambda x: x[1])
        return idx

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
