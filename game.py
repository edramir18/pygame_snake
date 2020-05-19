import random
from typing import Set, List

from coord import Coord
from grid import Grid
from snake import Snake
from node import find_route


class Game:
    def __init__(self, width, height, seed):
        self.points = 0
        self.seed = seed
        self.random = random.Random()
        self.random.seed(seed)
        self.grid = Grid(width, height)
        self.grid.build_walls(self.random)
        self.cherry = self.grid.get_next_cherry(self.random)  # type: Coord
        self.snake = self.create_snake()  # type: Snake

    def run(self):
        paths = find_route(self.snake.head, self.cherry, self.grid)
        if len(paths) == 0:
            print('SNAKE DIEEEE')
            self.points = 0
            for pos in self.snake.body:
                self.grid.get(pos).has_player = False
            self.snake = self.create_snake()
        else:
            pos = paths[1]
            self.move_snake(pos)
            if pos == self.cherry:
                self.eat_cherry()

    def create_snake(self):
        pos = self.random.choice(self.grid.get_free_cells())
        self.grid.get(pos).has_player = True
        snake = Snake(pos)
        return snake

    def eat_cherry(self):
        self.grid.get(self.cherry).has_cherry = False
        self.snake.grow()
        self.points += 1
        self.cherry = self.grid.get_next_cherry(self.random)

    def move_snake(self, pos: Coord):
        self.grid.get(pos).has_player = True
        last = self.snake.move(pos)
        if last is not None:
            self.grid.get(last).has_player = False
