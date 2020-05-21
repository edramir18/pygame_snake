import pygame as pg

from game import Game
from game_color import GameColor
from snake import Snake


class GameZone:
    def __init__(self, game: Game, tile: int):
        self.width = game.grid.width * tile
        self.height = game.grid.height * tile
        self.canvas = pg.Surface((self.width, self.height))
        self.tile = tile
        self.half = tile // 2
        self.snake = int(tile * 0.8)
        self.m_snake = (tile - self.snake) // 2
        self.cherry = int(tile * 0.4)
        self.wall = int(tile * 0.8)
        self.m_wall = (tile - self.wall) // 2
        self.background = GameColor.BLACK.value
        self.snake_color = GameColor.GREEN.value
        self.cherry_color = GameColor.YELLOW.value
        self.wall_color = GameColor.MAGENTA.value
        self.update(game)

    def update(self, game: Game):
        self.canvas.fill(self.background)
        # for pos, cell in game.grid.cells.items():
        #     x, y = (pos * self.tile).get()
        #     if cell.has_body:
        #         color = GameColor.WHITE.value
        #     elif cell.has_cherry:
        #         color = GameColor.CYAN.value
        #     else:
        #         color = self.wall_color
        #     pg.draw.rect(self.canvas, color, (x, y, self.tile, self.tile), 0)
        lst = [coord for coord, cell in game.grid.cells.items()
               if cell.is_wall() or cell.has_cherry]
        for coord in lst:
            if game.grid.get(coord).has_cherry:
                pos = coord * self.tile + self.half
                pg.draw.circle(self.canvas, self.cherry_color, pos.get(),
                               self.cherry, 0)
            else:
                x, y = (coord * self.tile + self.m_wall).get()
                pg.draw.rect(self.canvas, self.wall_color,
                             (x, y, self.wall, self.wall), 0)
        snake = game.snakes[game.current_id]  # type: Snake
        for pos in snake.body:
            body = pos * self.tile + self.m_snake
            x, y = body.get()
            rect = (x, y, self.snake, self.snake)
            if pos == snake.head:
                pg.draw.rect(self.canvas, GameColor.BLUE.value, rect, 0)
            else:
                pg.draw.rect(self.canvas, self.snake_color, rect, 0)


class GameView:
    def __init__(self, game: Game, tile: int):
        self.zone = GameZone(game, tile)
        self.width = 130 + self.zone.width
        self.height = 20 + self.zone.height
        self.window = pg.display.set_mode((self.width, self.height))
        self.font = pg.font.SysFont(None, 24)
        self.font_color = GameColor.WHITE.value
        self.background = GameColor.BLUE.value
        self.window.fill(self.background)
        _, snake = self.get_text('SNAKE')
        self.window.blit(snake, (20 + self.zone.width, 10))
        _, generation = self.get_text('Generation')
        self.window.blit(generation, (20 + self.zone.width, 70))
        self.update(game)

    def get_text(self, text):
        size = self.font.size(text)
        img = self.font.render(text, True, self.font_color, self.background)
        return size, img

    def update(self, game: Game):
        self.zone.update(game)
        self.window.blit(self.zone.canvas, (10, 10))
        self.window.fill(self.background, (20 + self.width, 40, 100, 30))
        (w, _), text = self.get_text(str(game.points))
        self.window.blit(text, (self.width - 10 - w, 40))
        self.window.fill(self.background, (20 + self.width, 100, 100, 30))
        (w, _), text = self.get_text(str(game.generation))
        self.window.blit(text, (self.width - 10 -w, 100))
