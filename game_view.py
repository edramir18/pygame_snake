import pygame as pg

from game import Game
from game_color import GameColor


class GameZone:
    def __init__(self, width, height, tile, game):
        self.width = width
        self.height = height
        self.canvas = pg.Surface((width, height))
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
        pos = game.cherry * self.tile + self.half
        pg.draw.circle(self.canvas, self.cherry_color, pos.get(),
                       self.cherry, 0)
        lst = [coord for coord, cell in game.grid.cells.items()
               if cell.is_wall()]
        for coord in lst:
            x, y = (coord * self.tile + self.m_wall).get()
            pg.draw.rect(self.canvas, self.wall_color,
                         (x, y, self.wall, self.wall), 0)
        for pos in game.snake.body:
            body = pos * self.tile + self.m_snake
            x, y = body.get()
            rect = (x, y, self.snake, self.snake)
            pg.draw.rect(self.canvas, self.snake_color, rect, 0)


class GameView:
    def __init__(self, game: Game):
        self.width = 740
        self.height = 490
        self.window = pg.display.set_mode((self.width, self.height))
        self.font = pg.font.SysFont(None, 30)
        self.font_color = GameColor.WHITE.value
        self.background = GameColor.BLUE.value
        self.zone = GameZone(470, 470, 10, game)
        snake = self.get_text('SNAKE')
        self.window.fill(self.background)
        self.window.blit(snake, (495, 10))
        self.update(game)

    def get_text(self, text):
        return self.font.render(text, True, self.font_color, self.background)

    def update(self, game: Game):
        self.zone.update(game)
        self.window.blit(self.zone.canvas, (15, 10))
        self.window.fill(self.background, (495, 40, 230, 40))
        w, _ = self.font.size(str(game.points))
        text = self.get_text(str(game.points))
        self.window.blit(text, (725 - w, 40))
