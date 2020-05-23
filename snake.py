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
        self.directions = list()
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

    def run(self, vision: List[float]):
        if self.life == 0:
            self.is_dead = True
            self.calculate_fitness()
        else:
            self.life -= 1
            self.steps += 1
            # action = self.brain.think(vision, self.get_direction())
            action = self.brain.think(self.encode_vision(vision))
            return self.move(self.get_turn(action), Snake.Direction(action))

    def get_direction(self):
        if self.direction == Snake.Direction.UP:
            return [1, 0, 0, 0]
        if self.direction == Snake.Direction.RIGHT:
            return [0, 1, 0, 0]
        if self.direction == Snake.Direction.DOWN:
            return [0, 0, 1, 0]
        if self.direction == Snake.Direction.LEFT:
            return [0, 0, 0, 1]

    def encode_vision(self, vision: List[int]):
        if self.direction == Snake.Direction.UP:
            return [vision[5], vision[2], vision[3]]
        if self.direction == Snake.Direction.RIGHT:
            return [vision[2], vision[3], vision[4]]
        if self.direction == Snake.Direction.DOWN:
            return [vision[3], vision[4], vision[5]]
        if self.direction == Snake.Direction.LEFT:
            return [vision[4], vision[5], vision[2]]

    def get_turn(self, action):
        adj = Coord.adjacency()
        if action == 0:
            return adj[self.direction.value]
        if self.direction == Snake.Direction.UP:
            if action == 1:
                return adj[Snake.Direction.LEFT.value]
            else:
                return adj[Snake.Direction.RIGHT.value]
        elif self.direction == Snake.Direction.DOWN:
            if action == 1:
                return adj[Snake.Direction.RIGHT.value]
            else:
                return adj[Snake.Direction.LEFT.value]
        elif self.direction == Snake.Direction.RIGHT:
            if action == 1:
                return adj[Snake.Direction.UP.value]
            else:
                return adj[Snake.Direction.DOWN.value]
        elif self.direction == Snake.Direction.LEFT:
            if action == 1:
                return adj[Snake.Direction.DOWN.value]
            else:
                return adj[Snake.Direction.UP.value]

    def grow(self):
        self.life += 100
        self.points += 1
        self.path.append(self.path[-1])

    def calculate_fitness(self):
        fitness = self.steps + (np.power(2, self.points) + 500 * self.points)
        fitness -= 0.25 * np.power(self.steps, 1.3) * np.power(self.points, 1.2)
        # fitness = self.steps * self.steps * np.power(2, self.points)
        self.fitness = fitness
        self.brain.fitness = fitness

    def __str__(self):
        return (f'Snake{self.brain.generation:4}:{self.snk_id:<5} '
                f'{self.points:3} points Life: {self.life:4} '
                f'Score: {self.fitness:10.4f} ')

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
                'generation': self.brain.generation,
                'seed': self.brain.seed,
            }
            json.dump(data, outfile)
            if neural:
                np.savez(f'{basename}.npz',
                         syn0=self.brain.syn0, syn1=self.brain.syn1)

    @staticmethod
    def load(generation, snk_id):
        basename = f'data/{generation}/snake_{snk_id}'
        jsonfile = f'{basename}.json'
        with open(jsonfile) as outfile:
            data = json.load(outfile)
            brain = Brain(data['seed'], data['generation'])
            x, y = data['initial_pos']
            snake = Snake(data['snk_id'], Coord(x, y), brain)
        with np.load(f'{basename}.npz') as data:
            snake.brain.syn0 = data['syn0']
            snake.brain.syn1 = data['syn1']
        return snake
