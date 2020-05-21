import random

import pygame as pg
from pygame.time import Clock

from game import Game
from game_view import GameView

population = 1000
generations = 200
fps = 60
mutation = 0.10
width = 40
height = 40
seed = 2040
tile = 10
top = 3


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
                for i in range(top):
                    game.snakes[i].save()
                game.next_generation()
    pg.quit()


if __name__ == '__main__':
    # offline()
    run()
