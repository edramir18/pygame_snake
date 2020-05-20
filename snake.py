from typing import Set, List
import numpy as np
from brain import Brain
from coord import Coord


class Snake:
    def __init__(self, snk_id: int, pos: Coord, brain: Brain):
        self.snk_id = snk_id
        self.body = set()  # type: Set[Coord]
        self.body.add(pos)
        self.path = [pos]
        self.head = pos
        self.brain = brain
        self.is_dead = False
        self.life = 100
        self.points = 0
        self.steps = 0
        self.fitness = 0

    def move(self, pos):
        last = self.path.pop()
        if len(self.path) == 0 or last != self.path[-1]:
            if last in self.body:
                self.body.remove(last)
        else:
            last = None
        self.body.add(pos)
        self.path.insert(0, pos)
        self.head = pos
        return last

    def run(self, vision: List[float]):
        if self.life == 0:
            self.is_dead = True
            self.calculate_fitness()
        else:
            self.life -= 1
            self.steps += 1
            action = self.brain.think(vision)
            return self.move(self.head + Coord.adjacency()[action])

    def grow(self):
        self.life += 100
        self.points += 1
        self.path.append(self.path[-1])

    def calculate_fitness(self):
        fitness = self.steps + (np.power(2, self.points) + 500 * self.points)
        fitness -= 0.25 * np.power(self.steps, 1.3) * np.power(self.points, 1.2)
        self.fitness = fitness
        self.brain.fitness = fitness
