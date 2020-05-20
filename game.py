import random
from typing import Set, List, Dict

from brain import Brain
from coord import Coord
from evolution import Evolution
from grid import Grid
from snake import Snake
from node import find_route


class Game:
    def __init__(self, width: int, height: int, seed: int,
                 snakes: int, mutation: float):
        self.points = 0
        self.seed = seed
        self.random = random.Random()
        self.random.seed(seed)
        # self.grid.build_walls(self.random)
        self.grid = Grid(width, height)
        self.cherry = self.grid.get_next_cherry(self.random)
        self.current_id = 0
        self.generation = 0
        self.population = snakes
        self.snakes = dict()  # type: Dict[int, Snake]
        self.mutation = mutation
        self.create_all_snakes()
        self.best_fitness = 0

    def run(self):
        snake = self.snakes[self.current_id]
        vision = self.grid.get_vision(snake.head)
        snake.run(vision)
        head = self.grid.get(snake.head)
        if head is None or head.is_wall() or head.has_player or snake.is_dead:
            if not snake.is_dead:
                snake.is_dead = True
                snake.calculate_fitness()
            if snake.fitness > self.best_fitness:
                self.best_fitness = snake.fitness
            print(f'Snake {snake.brain.generation:3}:{snake.snk_id:<5}'
                  f'Score: {snake.fitness:10.4f} Best: {self.best_fitness:.4f}')
            self.reset_game()
        elif head.has_cherry:
            self.eat_cherry()

    def create_all_snakes(self):
        pos = self.random.choice(self.grid.get_free_cells())
        for snk_id in range(self.population):
            brain = Brain(self.seed * self.population + snk_id, 0)
            snake = Snake(snk_id, pos, brain)
            self.snakes[snk_id] = snake
        self.grid.get(pos).has_player = True

    def eat_cherry(self):
        self.grid.get(self.cherry).has_cherry = False
        self.snakes[self.current_id].grow()
        self.points += 1
        self.cherry = self.grid.get_next_cherry(self.random)

    def reset_game(self):
        self.random.seed(self.seed)
        self.points = 0
        self.grid = Grid(self.grid.width, self.grid.height)
        self.cherry = self.grid.get_next_cherry(self.random)
        self.current_id += 1

    def next_generation(self):
        brains = [snake.brain for snake in self.snakes.values()]
        self.generation += 1
        generation = Evolution(brains, self.mutation,
                               self.seed, self.generation)
        brains = generation.evolve()
        self.random.seed(self.seed)
        self.points = 0
        self.grid = Grid(self.grid.width, self.grid.height)
        self.cherry = self.grid.get_next_cherry(self.random)
        pos = self.random.choice(self.grid.get_free_cells())
        self.current_id = 0
        self.snakes = dict()
        for snk_id in range(self.population):
            snake = Snake(snk_id, pos, brains[snk_id])
            self.snakes[snk_id] = snake
        self.grid.get(pos).has_player = True




