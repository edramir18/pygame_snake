from typing import List
import numpy as np

from brain import Brain


class Evolution:
    def __init__(self, brains: List[Brain], mutation: float,
                 seed: int, generation: int):
        self.brains = brains
        self.population = len(brains)
        self.elite = int(self.population * 0.2)
        self.mutation_rate = mutation
        self.parents = list()  # type: List[Brain]
        self.parent_ids = list()  # type: List[int]
        self.offsprings = list()  # type: List[Brain]
        self.seed = seed
        self.generation = generation

    def selection(self):
        self.brains.sort(key=lambda x: x.fitness, reverse=True)
        self.parents = self.brains[:self.elite]
        total = sum([b.fitness for b in self.parents], 0.0)
        dices = np.sort(np.random.sample((self.population - self.elite) * 2))
        idx = 0
        percent = self.parents[0].fitness / total
        for roll in dices:
            while roll > percent:
                idx += 1
                percent += self.parents[idx].fitness / total
            self.parent_ids.append(idx)
        np.random.shuffle(self.parents)

    def crossover(self):
        a = [True, False]
        inputs = (self.brains[0].inputs, self.brains[0].hidden)
        # layer0 = (self.brains[0].hidden, self.brains[0].hidden)
        outputs = (self.brains[0].hidden, self.brains[0].outputs)
        p = [0.5, 0.5]
        for i in range(self.elite):
            self.offsprings.append(self.parents[i])
        for i in range(self.population - self.elite):
            p1 = self.parents[self.parent_ids[i]]
            p2 = self.parents[self.parent_ids[i + 1]]
            cross0 = np.random.choice(a, inputs, p=p)
            # cross1 = np.random.choice(a, layer0, p=p)
            cross2 = np.random.choice(a, outputs, p=p)
            offspring = Brain(self.seed * self.population + i, self.generation)
            offspring.syn0 = np.where(cross0, p1.syn0, p2.syn0)
            # offspring.syn0 = np.array(p1.syn0)
            # offspring.syn1 = np.where(cross1, p1.syn1, p2.syn1)
            offspring.syn2 = np.where(cross2, p1.syn2, p2.syn2)
            # offspring.syn2 = np.array(p2.syn2)
            self.offsprings.append(offspring)

    def mutation(self):
        a = [True, False]
        inputs = (self.brains[0].inputs, self.brains[0].hidden)
        # layer0 = (self.brains[0].hidden, self.brains[0].hidden)
        outputs = (self.brains[0].hidden, self.brains[0].outputs)
        p = [self.mutation_rate, 1 - self.mutation_rate]
        for i in range(self.population):
            mut0 = np.random.choice(a, inputs, p=p)
            cro0 = 2 * np.random.random(inputs) - 1
            # mut1 = np.random.choice(a, layer0, p=p)
            # cro1 = 2 * np.random.random(layer0) - 1
            mut2 = np.random.choice(a, outputs, p=p)
            cro2 = 2 * np.random.random(outputs) - 1
            offspring = self.offsprings[i]
            offspring.syn0 = np.where(mut0, cro0, offspring.syn0)
            # offspring.syn1 = np.where(mut1, cro1, offspring.syn1)
            offspring.syn2 = np.where(mut2, cro2, offspring.syn2)

    def evolve(self):
        self.selection()
        self.crossover()
        self.mutation()
        return self.offsprings
