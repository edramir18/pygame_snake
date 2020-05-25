import json
import os
from enum import Enum
from typing import Set, List
import numpy as np
from brain import Brain
from coord import Coord


class Snake:
    class Direction(Enum):
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    def __init__(self, snk_id: int, pos: Coord, brain: Brain):
        self.snk_id = snk_id
        self.body = set()  # type: Set[Coord]
        self.body.add(pos)
        self.path = [pos, pos, pos]
        self.direction = Snake.Direction.UP
        self.directions = [Snake.Direction.UP]
        self.head = pos
        self.brain = brain
        self.is_dead = False
        self.life = 200
        self.points = 0
        self.steps = 0
        self.fitness = 0
        self.initial_pos = pos

    def move(self, delta: Coord, direction: 'Snake.Direction'):
        pos = self.head + delta
        last = self.path.pop()
        if len(self.path) == 0 or last != self.path[-1]:
            if last in self.body:
                self.body.remove(last)
        else:
            last = None
        if len(self.directions) > len(self.path):
            self.directions.pop()
        self.body.add(pos)
        self.path.insert(0, pos)
        self.head = pos
        self.direction = direction
        self.directions.insert(0, direction)
        return last

    def run(self, vision: List[int]):
        if self.life == 0:
            self.is_dead = True
            self.calculate_fitness()
        else:
            self.life -= 1
            self.steps += 1
            action = self.brain.think(vision + self.get_direction())
            adj, direction = Coord.adjacency()[action], Snake.Direction(action)
            return self.move(adj, direction)

    def get_direction(self):
        if self.direction == Snake.Direction.UP:
            return [0, 0]
        elif self.direction == Snake.Direction.RIGHT:
            return [0, 1]
        elif self.direction == Snake.Direction.DOWN:
            return [1, 0]
        else:
            return [1, 1]

    def encode_vision(self, vision: List[int]):
        gene = self.brain.gene
        r_vision = vision[:gene * 4]
        if self.direction == Snake.Direction.UP:
            return r_vision[-gene:] + r_vision[:gene * 2]
        if self.direction == Snake.Direction.RIGHT:
            return r_vision[:gene * 3]
        if self.direction == Snake.Direction.DOWN:
            return r_vision[gene:]
        if self.direction == Snake.Direction.LEFT:
            return (r_vision[-2 * gene:-gene] + r_vision[-gene:]
                    + r_vision[:gene])

    def get_turn(self, action):
        adj = Coord.adjacency()
        if action == 0 or action == 3:
            return adj[self.direction.value], self.direction
        if self.direction == Snake.Direction.UP:
            if action == 2:
                return adj[Snake.Direction.LEFT.value], Snake.Direction.LEFT
            else:
                return adj[Snake.Direction.RIGHT.value], Snake.Direction.RIGHT
        elif self.direction == Snake.Direction.DOWN:
            if action == 2:
                return adj[Snake.Direction.RIGHT.value], Snake.Direction.RIGHT
            else:
                return adj[Snake.Direction.LEFT.value], Snake.Direction.LEFT
        elif self.direction == Snake.Direction.RIGHT:
            if action == 2:
                return adj[Snake.Direction.UP.value], Snake.Direction.UP
            else:
                return adj[Snake.Direction.DOWN.value], Snake.Direction.DOWN
        elif self.direction == Snake.Direction.LEFT:
            if action == 2:
                return adj[Snake.Direction.DOWN.value], Snake.Direction.DOWN
            else:
                return adj[Snake.Direction.UP.value], Snake.Direction.UP

    def grow(self):
        self.life += 100
        self.points += 1
        self.path.append(self.path[-1])

    def calculate_fitness(self):
        # fitness = self.steps + np.power(2, self.points)
        # fitness += 500 * np.power(self.points, 2.1)
        # fitness -= 0.25 * np.power(self.steps, 1.3) * np.power(self.points, 1.2)
        fitness = self.steps * self.steps * np.power(2, self.points)
        self.fitness = fitness
        self.brain.fitness = fitness

    def __str__(self):
        return (f'Snake{self.brain.age:4}:{self.snk_id:<5} '
                f'{self.points:3} points Life: {self.life:4} '
                f'Score: {self.fitness:8.2f} ')

    def save(self, neural=True):
        basename = f'data/{self.brain.generation}/snake_{self.snk_id}'
        jsonfile = f'{basename}.json'
        os.makedirs(os.path.dirname(jsonfile), exist_ok=True)
        with open(jsonfile, 'w') as outfile:
            data = {
                'snk_id': self.snk_id,
                'fitness': int(self.fitness),
                'steps': int(self.steps),
                'points': int(self.points),
                'initial_pos': self.initial_pos.get(),
                'generation': int(self.brain.generation),
                'seed': int(self.brain.seed),
                'gene': int(self.brain.gene),
                'size': int(self.brain.size),
                'age': int(self.brain.age)
            }
            if neural:
                data['chromosome'] = ''.join(str(x)
                                             for x in self.brain.chromosome)
            json.dump(data, outfile)

    @staticmethod
    def load(generation, snk_id):
        basename = f'data/{generation}/snake_{snk_id}'
        jsonfile = f'{basename}.json'
        with open(jsonfile) as outfile:
            data = json.load(outfile)
            brain = Brain(data['seed'], data['generation'],
                          data['gene'], data['size'], data['age'],
                          [int(x) for x in data['chromosome']])
            x, y = data['initial_pos']
            snake = Snake(data['snk_id'], Coord(x, y), brain)
        return snake
111