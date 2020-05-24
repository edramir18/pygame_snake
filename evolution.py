from typing import List
import numpy as np

from brain import Brain


class Evolution:
    def __init__(self, brains: List[Brain], mutation: float,
                 seed: int, generation: int, avg: float):
        self.brains = brains
        self.population = len(brains)
        # self.elite = sum([1 for x in brains if x.fitness >= avg], 0)
        self.elite = int(self.population * 0.1)
        self.children = self.population - self.elite
        self.mutation_rate = mutation
        self.elites = list()  # type: List[Brain]
        self.parent_ids = list()  # type: List[int]
        self.offsprings = list()  # type: List[Brain]
        self.seed = seed
        self.generation = generation
        self.random = np.random.default_rng()

    def selection(self):
        self.brains.sort(key=lambda x: x.fitness, reverse=True)
        self.elites = self.brains[:self.elite]
        total = sum([b.fitness for b in self.brains], 0.0)
        dices = np.sort(self.random.uniform(size=self.children * 2))
        idx = 0
        percent = self.brains[0].fitness / total
        for roll in dices:
            while roll > percent:
                idx += 1
                percent += self.brains[idx].fitness / total
            self.parent_ids.append(idx)
        self.random.shuffle(self.parent_ids)

    def crossover(self):
        a = [True, False]
        l0 = self.brains[0].inputs
        l1 = self.brains[0].outputs
        p = [0.8, 0.2]
        for i in range(self.children):
            p1 = self.brains[self.parent_ids[i]]
            p2 = self.brains[self.parent_ids[i + 1]]
            # p1, p2 = (p1, p2) if p1.fitness > p2.fitness else (p2, p1)
            cross0 = self.random.choice(a, l0, p=p)
            cross1 = self.random.choice(a, l1, p=p)
            offspring = Brain(self.seed * self.population + i, self.generation)
            offspring.syn0 = np.where(cross0, p1.syn0, p2.syn0)
            offspring.syn1 = np.where(cross1, p1.syn1, p2.syn1)
            # offspring.syn0 = np.array(p1.syn0)
            # offspring.syn1 = np.array(p2.syn1)
            self.offsprings.append(offspring)

    def mutation(self):
        a = [True, False]
        l0 = self.brains[0].inputs
        l1 = self.brains[0].outputs
        p = [self.mutation_rate, 1 - self.mutation_rate]
        for i in range(self.children):
            mut0 = self.random.choice(a, l0, p=p)
            cro0 = self.random.uniform(0, 1.0, l0)
            # cro0 = self.random.uniform(-0.3, 0.3, l0)
            mut1 = self.random.choice(a, l1, p=p)
            # cro1 = self.random.uniform(-0.3, 0.3, l1)
            cro1 = self.random.uniform(0, 1.0, l1)
            offspring = self.offsprings[i]
            # offspring.syn0 += np.where(mut0, cro0, np.zeros(l0))
            # offspring.syn1 += np.where(mut1, cro1, np.zeros(l1))
            # offspring.syn0 = np.clip(offspring.syn0, -1, 1)
            # offspring.syn1 = np.clip(offspring.syn1, -1, 1)
            offspring.syn0 = np.where(mut0, cro0, offspring.syn0)
            offspring.syn1 = np.where(mut1, cro1, offspring.syn1)

    def evolve(self):
        self.selection()
        self.crossover()
        self.mutation()
        for i in range(self.elite):
            self.elites[i].generation = self.generation
        return self.elites + self.offsprings
