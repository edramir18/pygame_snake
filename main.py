import random
import sys

import pygame as pg
from pygame.time import Clock

from game import Game
from game_view import GameView

population = 50
top = 10
generations = 200
fps = 6
mutation = 0.10
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
                    game.snakes[i].save()
                game.next_generation()
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
        if sys.argv[1] == '--play':
            play()
        elif sys.argv[1] == '--run':
            run()
