from enum import Enum


class Cell:
    class CellType(Enum):
        WALL = '#'
        FLOOR = ' '

        def __str__(self):
            return str(self.value)

        def __repr__(self):
            return self.__str__()

    def __init__(self):
        self.celltype = Cell.CellType.WALL
        self.has_cherry = False
        self.has_pellet = False
        self.has_player = False

    def __str__(self):
        return str(self.celltype)

    def __repr__(self):
        return self.__str__()

    def is_wall(self):
        return self.celltype == Cell.CellType.WALL

    def is_floor(self):
        return self.celltype == Cell.CellType.FLOOR

    def is_empty(self):
        if self.celltype == Cell.CellType.WALL:
            return False
        return not (self.has_pellet or self.has_cherry or self.has_player)
