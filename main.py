import argparse

import pygame as pg
from pygame.time import Clock

from config import Config
from game import Game
from game_view import GameView


def handle_user_input(game: Game, pause):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.is_running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                game.is_running = False
            elif event.key == pg.K_SPACE:
                pause = not pause
    return pause


def replay(config):
    pg.init()
    game = Game(config.width, config.height, config.seed,
                config.generations, config.top,
                config.selection, config.crossover, config.mutation,
                create=False)
    view = GameView(game, config.tile)
    pause = False
    clock = pg.time.Clock()  # type: Clock
    while game.is_running:
        clock.tick(config.fps)
        pause = handle_user_input(game, pause)
        if not pause:
            game.run()
            if game.is_running:
                view.update(game)
                pg.display.flip()
    pg.quit()


def play(config: Config):
    pg.init()
    game = Game(config.width, config.height, config.seed,
                config.generations, config.population,
                config.selection, config.crossover, config.mutation)
    view = GameView(game, config.tile)
    pause = False
    clock = pg.time.Clock()  # type: Clock
    while game.is_running:
        pause = handle_user_input(game, pause)
        if not pause:
            if game.current_id < config.top:
                clock.tick(config.fps)
                game.run(save=True, save_ann=True)
                if game.is_running:
                    view.update(game)
                    pg.display.flip()
            else:
                game.run(save=True)
    pg.quit()


def run(config: Config):
    game = Game(config.width, config.height, config.seed,
                config.generations, config.population,
                config.selection, config.crossover, config.mutation)
    while game.is_running:
        if game.current_id < config.top:
            game.run(save=True, save_ann=True)
        else:
            game.run(save=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a simulation of snake'
                                                 'game using GA')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--play', action="store_true",
                       help='Run the simulation showing the'
                            ' top snakes of each generation')
    group.add_argument('-r', '--replay', action="store_true",
                       help='Replay the last simulation showing the'
                            ' top snakes of each generation')
    args = parser.parse_args()
    if args.play:
        cfg = Config()
        cfg.save()
        play(config=cfg)
    elif args.replay:
        cfg = Config.load()
        replay(cfg)
    else:
        cfg = Config()
        cfg.mutation = 0.01
        cfg.save()
        run(cfg)
