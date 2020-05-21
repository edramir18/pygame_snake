from typing import List
import numpy as np

from brain import Brain


class Evolution:
    def __init__(self, brains: List[Brain], mutation: float,
                 seed: int, generation: int):
        self.brains = brains
        self.population = len(brains)
        self.elite = int(self.population * 0.2)
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
        l1 = self.brains[0].hidden
        l2 = self.brains[0].outputs
        p = [0.75, 0.25]
        for i in range(self.population - self.elite):
            p1 = self.brains[self.parent_ids[i]]
            p2 = self.brains[self.parent_ids[i + 1]]
            cross0 = self.random.choice(a, l0, p=p)
            cross1 = self.random.choice(a, l1, p=p)
            cross2 = self.random.choice(a, l2, p=p)
            offspring = Brain(self.seed * self.population + i, self.generation)
            offspring.syn0 = np.where(cross0, p1.syn0, p2.syn0)
            offspring.syn1 = np.where(cross1, p1.syn1, p2.syn1)
            offspring.syn2 = np.where(cross2, p1.syn2, p2.syn2)
            self.offsprings.append(offspring)

    def mutation(self):
        a = [True, False]
        l0 = self.brains[0].inputs
        l1 = self.brains[0].hidden
        l2 = self.brains[0].outputs
        p = [self.mutation_rate, 1 - self.mutation_rate]
        for i in range(self.population - self.elite):
            mut0 = self.random.choice(a, l0, p=p)
            cro0 = 2 * self.random.random(l0) - 1
            mut1 = self.random.choice(a, l1, p=p)
            cro1 = 2 * self.random.random(l1) - 1
            mut2 = self.random.choice(a, l2, p=p)
            cro2 = 2 * self.random.random(l2) - 1
            offspring = self.offsprings[i]
            offspring.syn0 = np.where(mut0, cro0, offspring.syn0)
            offspring.syn1 = np.where(mut1, cro1, offspring.syn1)
            offspring.syn2 = np.where(mut2, cro2, offspring.syn2)

    def evolve(self):
        self.selection()
        self.crossover()
        self.mutation()
        for i in range(self.elite):
            self.elites[i].generation = self.generation
        return self.elites + self.offsprings
