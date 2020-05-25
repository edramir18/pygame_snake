from typing import List

import numpy as np


class Brain:
    def __init__(self, seed, generation: int, gene: int, size: int, age=0,
                 chromosome=None):
        self.state = np.random.default_rng(seed)
        self.seed = seed
        if chromosome is None:
            self.chromosome = list(self.state.integers(0, gene, (size,)))
        else:
            self.chromosome = chromosome  # type: List[int]
        self.fitness = 0
        self.age = age
        self.generation = generation
        self.gene = gene  # type: int
        self.size = size  # type: int

    def think(self, vision: List[int]):
        code = self.decode(vision) * self.gene
        lst = self.chromosome[code:code + self.gene]
        return self.decode(lst)

    @staticmethod
    def decode(code: List[int]):
        size = len(code) - 1
        value = sum((code[size - k] * np.power(2, k)
                     for k in range(size, -1, -1)), 0)
        return value

    def __str__(self):
        return f'{self.fitness}'

    def __repr__(self):
        return f'Brain {self.generation}:{self.fitness}'
