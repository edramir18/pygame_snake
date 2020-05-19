import random

import pygame as pg
from pygame.time import Clock

from game import Game
from game_view import GameView


def run():
    pg.init()
    game = Game(47, 47, 1981)
    view = GameView(game)
    running = True
    clock = pg.time.Clock()  # type: Clock
    while running:
        clock.tick(24)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
        game.run()
        view.update(game)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    run()
