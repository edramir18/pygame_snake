from typing import Dict

import numpy as np

from brain import Brain
from cell import Cell
from coord import Coord
from evolution import Evolution
from grid import Grid
from snake import Snake


class Game:
    def __init__(self, width: int, height: int, seed: int, generations: int,
                 population: int, selection: float, crossover: float,
                 mutation: float, create=True):
        self.seed = seed
        self.points = 0
        self.current_id = 0
        self.generation = 0
        self.generations = generations
        self.population = population
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.best_fitness = 0
        self.avg_fitness = 0
        self.is_running = True
        self.random = np.random.default_rng(seed)
        self.snakes = dict()  # type: Dict[int, Snake]
        self.grid = Grid(width, height)
        self.cherry = self.grid.get_next_cherry(self.random)
        self.initial_pos = self.random.choice(self.grid.get_free_cells())
        self.create = create
        self.create_all_snakes()

    def run_snake(self, snake: Snake):
        vision = self.grid.get_vision(snake.head)
        tail = snake.run(vision)  # type: Coord
        head = self.grid.get(snake.head)  # type: Cell
        if head is None or head.is_wall() or head.has_body or snake.is_dead:
            if not snake.is_dead:
                snake.is_dead = True
                snake.calculate_fitness()
        else:
            head.has_body = True
            if tail is not None:
                self.grid.get(tail).has_body = False
            if head.has_cherry:
                self.eat_cherry(snake)

    def print_score_by_snake(self, snake: Snake):
        print(f'{self.generation}> {snake}'
              f'Best: {self.best_fitness:10.4f} '
              f'AVG: {self.avg_fitness / (self.current_id + 1):10.4f}')

    def run(self, save=False, save_ann=False):
        snake = self.snakes[self.current_id]
        self.run_snake(snake)
        if snake.is_dead:
            if save:
                snake.save(save_ann)
            self.avg_fitness += snake.fitness
            self.print_score_by_snake(snake)
            if snake.fitness > self.best_fitness:
                self.best_fitness = snake.fitness
            self.current_id += 1
            if self.current_id == self.population:
                self.generation += 1
                if self.generation == self.generations:
                    self.is_running = False
                else:
                    self.next_generation()
            self.reset_game()

    def create_all_snakes(self):
        if self.create:
            for snk_id in range(self.population):
                brain = Brain(self.seed * self.population + snk_id, 0)
                snake = Snake(snk_id, self.initial_pos, brain)
                self.snakes[snk_id] = snake
            self.grid.get(self.initial_pos).has_body = True
        else:
            for snk_id in range(self.population):
                snake = Snake.load(0, snk_id)
                self.snakes[snk_id] = snake

    def eat_cherry(self, snake: Snake):
        self.grid.get(snake.head).has_cherry = False
        snake.grow()
        self.points += 1
        self.cherry = self.grid.get_next_cherry(self.random)

    def reset_game(self):
        self.random = np.random.default_rng(self.seed)
        self.points = 0
        self.grid = Grid(self.grid.width, self.grid.height)
        self.cherry = self.grid.get_next_cherry(self.random)
        self.grid.get(self.initial_pos).has_body = True

    def next_generation(self):
        self.current_id = 0
        self.avg_fitness = 0
        if self.create:
            # TODO Cambiar todo la parte de Brain y evolucion
            brains = [snake.brain for snake in self.snakes.values()]
            generation = Evolution(brains, self.mutation,
                                   self.seed, self.generation, self.avg_fitness)
            brains = generation.evolve()
            self.snakes = dict()
            for snk_id in range(self.population):
                snake = Snake(snk_id, self.initial_pos, brains[snk_id])
                self.snakes[snk_id] = snake
        else:
            for snk_id in range(self.population):
                snake = Snake.load(self.generation, snk_id)
                self.snakes[snk_id] = snake
        self.reset_game()
