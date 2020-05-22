import random
import sys

import pygame as pg
from pygame.time import Clock

from game import Game
from game_view import GameView
from snake import Snake

population = 10000
top = 20
generations = 50
fps = 60
mutation = 0.05
width = 10
height = 10
seed = 1981
tile = 40


def run():
    pg.init()
    game = Game(width, height, seed, population, mutation)
    view = GameView(game, tile)
    running = True
    pause = False
    clock = pg.time.Clock()  # type: Clock
    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    pause = not pause
        if not pause:
            game.run()
            if game.current_id == population:
                if game.generation == generations:
                    running = False
                else:
                    print(f'Generation: {game.generation:5} '
                          f'Fitness {game.best_fitness}')
                    game.next_generation()
            else:
                view.update(game)
                pg.display.flip()
    pg.quit()


def offline():
    game = Game(width, height, seed, population, mutation)
    running = True
    while running:
        game.run()
        if game.current_id == population:
            if game.generation == generations:
                running = False
            else:
                print(f'Generation: {game.generation:5} '
                      f'Fitness {game.best_fitness}')
                for i in range(population):
                    game.snakes[i].save(game.generation == generations - 1
                                        or i < top)
                game.next_generation()


def replay():
    pg.init()
    game = Game(width, height, seed, top, mutation, False)
    for i in range(top):
        snake = Snake.load(0, i)
        game.snakes[i] = snake
    game.grid.get(game.initial_pos).has_body = True
    view = GameView(game, tile)
    running = True
    pause = False
    clock = pg.time.Clock()  # type: Clock
    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    pause = not pause
        if not pause:
            game.run()
            if game.current_id == top:
                if game.generation == generations:
                    running = False
                else:
                    for i in range(top):
                        snake = Snake.load(game.generation, i)
                        game.snakes[i] = snake
                    game.next_generation(create=False)
            else:
                view.update(game)
                pg.display.flip()
    pg.quit()


def play():
    pg.init()
    game = Game(width, height, seed, population, mutation)
    view = GameView(game, tile)
    running = True
    pause = False
    clock = pg.time.Clock()  # type: Clock
    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    pause = not pause
        if not pause:
            if game.current_id == population:
                if game.generation == generations:
                    running = False
                else:
                    print(f'Generation: {game.generation:5} '
                          f'Fitness {game.best_fitness}')
                    game.next_generation()
            elif game.current_id < top:
                game.run()
                if game.current_id < population:
                    view.update(game)
                    pg.display.flip()
            else:
                while game.current_id < population:
                    game.run()
    pg.quit()


if __name__ == '__main__':
    n_args = len(sys.argv)
    if n_args == 1:
        offline()
    elif n_args == 2:
        _, arg = sys.argv
        if arg == '--play':
            play()
        elif arg == '--run':
            run()
        elif arg == '--replay':
            replay()
