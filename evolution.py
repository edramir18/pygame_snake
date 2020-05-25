from typing import List
import numpy as np

from brain import Brain


class Evolution:
    def __init__(self, brains: List[Brain], selection: float, crossover: float,
                 mutation: float, seed: int, generation: int):
        self.brains = brains
        self.population = len(brains)
        self.elite = int(self.population * selection)
        self.children = self.population - self.elite
        self.mutation_rate = mutation
        self.crossover_rate = crossover
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
        percent = self.brains[idx].fitness / total
        for roll in dices:
            while roll > percent:
                idx += 1
                percent += self.brains[idx].fitness / total
            self.parent_ids.append(idx)
        self.random.shuffle(self.parent_ids)

    def crossover(self):
        a = [True, False]
        p = [self.crossover_rate, 1 - self.crossover_rate]
        size = self.brains[0].size // self.brains[0].gene
        gene = self.brains[0].gene
        for i in range(self.children):
            p1 = self.brains[self.parent_ids[i]]
            p2 = self.brains[self.parent_ids[i + 1]]
            cross = list(self.random.choice(a, (size,), p=p))
            seed = self.seed * self.population + i + self.elite
            crom = list()
            for k in range(size):
                m, n = k * gene, k * gene + gene
                crom += p1.chromosome[m:n] if cross[k] else p2.chromosome[m:n]
            offspring = Brain(seed, self.generation, p1.gene, p1.size, 0, crom)
            self.offsprings.append(offspring)

    def mutation(self):
        a = [True, False]
        size = (self.brains[0].size,)
        p = [self.mutation_rate, 1 - self.mutation_rate]
        for i in range(self.children):
            mut = self.random.choice(a, size, p=p)
            offspring = self.offsprings[i]
            crom = [1 if k == 0 else 0 for k in offspring.chromosome]
            mut_crom = list(np.where(mut, crom, offspring.chromosome))
            offspring.chromosome = mut_crom

    def evolve(self):
        self.selection()
        self.crossover()
        self.mutation()
        for i in range(self.elite):
            self.elites[i].generation = self.generation
            self.elites[i].age += 1
        return self.elites + self.offsprings
