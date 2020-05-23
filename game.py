import random
from typing import Set, List, Dict

from brain import Brain
from coord import Coord
from evolution import Evolution
from grid import Grid
from snake import Snake
import numpy as np
from node import find_route


class Game:
    def __init__(self, width: int, height: int, seed: int,
                 snakes: int, mutation: float, create=True):
        self.points = 0
        self.current_id = 0
        self.generation = 0
        self.mutation = mutation
        self.best_fitness = 0
        self.avg_fitness = 0
        self.seed = seed
        self.random = np.random.default_rng(seed)
        self.grid = Grid(width, height)
        self.grid.build_walls(self.random)
        # for i in range(int(width * height * 0.05)):
        self.cherry = self.grid.get_next_cherry(self.random)
        self.population = snakes
        self.snakes = dict()  # type: Dict[int, Snake]
        self.initial_pos = self.random.choice(self.grid.get_free_cells())
        if create:
            self.create_all_snakes()

    def run(self):
        snake = self.snakes[self.current_id]
        vision = self.grid.get_vision(snake.head, cherry=self.cherry)
        last = snake.run(vision)
        head = self.grid.get(snake.head)
        if head is None or head.is_wall() or head.has_body or snake.is_dead:
            if not snake.is_dead:
                snake.is_dead = True
                snake.calculate_fitness()
            if snake.fitness > self.best_fitness:
                self.best_fitness = snake.fitness
            self.avg_fitness += snake.fitness
            print(f'{self.generation}> {snake}'
                  f'Best: {self.best_fitness:10.4f} '
                  f'AVG: {self.avg_fitness/(self.current_id + 1):10.4f}')
            self.reset_game()
            self.current_id += 1
            if self.current_id < self.population:
                snake = self.snakes[self.current_id]
                self.grid.get(snake.head).has_body = True
        else:
            head.has_body = True
            if last is not None:
                self.grid.get(last).has_body = False
            if head.has_cherry:
                self.eat_cherry()

    def create_all_snakes(self):
        for snk_id in range(self.population):
            brain = Brain(self.seed * self.population + snk_id, 0)
            snake = Snake(snk_id, self.initial_pos, brain)
            self.snakes[snk_id] = snake
        self.grid.get(self.initial_pos).has_body = True

    def eat_cherry(self):
        snake = self.snakes[self.current_id]
        self.grid.get(snake.head).has_cherry = False
        snake.grow()
        self.points += 1
        self.cherry = self.grid.get_next_cherry(self.random)

    def reset_game(self):
        # self.random = np.random.default_rng(self.seed)
        self.points = 0
        self.grid = Grid(self.grid.width, self.grid.height)
        self.grid.build_walls(self.random)
        # for i in range(int(self.grid.width * self.grid.height * 0.05)):
        self.cherry = self.grid.get_next_cherry(self.random)

    def next_generation(self, create=True):
        self.generation += 1
        self.current_id = 0
        self.avg_fitness = 0
        self.reset_game()
        if create:
            brains = [snake.brain for snake in self.snakes.values()]
            generation = Evolution(brains, self.mutation,
                                   self.seed, self.generation, self.avg_fitness)
            brains = generation.evolve()
            self.snakes = dict()
            for snk_id in range(self.population):
                snake = Snake(snk_id, self.initial_pos, brains[snk_id])
                self.snakes[snk_id] = snake
        self.grid.get(self.initial_pos).has_body = True




