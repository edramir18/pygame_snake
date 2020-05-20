import random

import pygame as pg
from pygame.time import Clock

from game import Game
from game_view import GameView


def run():
    population = 100
    fps = 60
    generations = 200
    mutation = 0.05
    pg.init()
    game = Game(47, 47, 1981, population, mutation)
    view = GameView(game)
    running = True
    clock = pg.time.Clock()  # type: Clock
    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
        game.run()
        if game.current_id == population:
            if game.generation == generations:
                running = False
            else:
                game.next_generation()
        else:
            view.update(game)
            pg.display.flip()
    pg.quit()


def offline():
    population = 100
    generations = 200
    mutation = 0.15
    game = Game(47, 47, 1981, population, mutation)
    running = True
    while running:
        game.run()
        if game.current_id == population:
            if game.generation == generations:
                running = False
            else:
                game.next_generation()
    pg.quit()


if __name__ == '__main__':
    # offline()
    run()
