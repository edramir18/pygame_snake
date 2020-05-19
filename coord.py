from typing import Union


class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coord):
            if self.x != other.x or self.y != other.y:
                return False
        else:
            return False
        return True

    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + self.x
        result = prime * result + self.y
        return result

    def __str__(self):
        return f'({self.x} {self.y})'

    def __repr__(self):
        return self.__str__()

    def manhattan_to(self, other: Union[tuple, 'Coord']) -> int:
        if isinstance(other, Coord):
            x, y = other.x, other.y
        elif isinstance(other, tuple) and len(other) == 2:
            x, y = other
        else:
            raise ValueError
        return abs(self.x - x) + abs(self.y - y)

    def chebyshev_to(self, other: Union[tuple, 'Coord']):
        if isinstance(other, Coord):
            x, y = other.x, other.y
        elif isinstance(other, tuple) and len(other) == 2:
            x, y = other
        else:
            raise ValueError
        return max(abs(self.x - x), abs(self.y - y))

    def get_unit_vector(self) -> 'Coord':
        x = 0 if self.x == 0 else self.x // abs(self.x)
        y = 0 if self.y == 0 else self.y // abs(self.y)
        return Coord(x, y)

    def get(self):
        return self.x, self.y

    def __add__(self, other):
        if isinstance(other, Coord):
            x, y = other.x, other.y
        elif isinstance(other, tuple) and len(other) == 2:
            x, y = other
        elif isinstance(other, int):
            x, y = other, other
        else:
            raise ValueError
        return Coord(self.x + x, self.y + y)

    def __radd__(self, other):
        if isinstance(other, (int, tuple, Coord)):
            self.__add__(other)
        else:
            raise ValueError

    def __sub__(self, other):
        if isinstance(other, Coord):
            x, y = other.x, other.y
        elif isinstance(other, tuple) and len(other) == 2:
            x, y = other
        elif isinstance(other, int):
            x, y = other, other
        else:
            raise ValueError
        return Coord(self.x - x, self.y - y)

    def __mul__(self, other):
        if isinstance(other, Coord):
            x, y = other.x, other.y
        elif isinstance(other, tuple) and len(other) == 2:
            x, y = other
        elif isinstance(other, int):
            x, y = other, other
        else:
            raise ValueError
        return Coord(self.x * x, self.y * y)
    
    def __rmul__(self, other):
        if isinstance(other, (int, tuple, Coord)):
            self.__mul__(other)
        else:
            raise ValueError

    @staticmethod
    def adjacency():
        return [Coord(-1, 0), Coord(1, 0), Coord(0, -1), Coord(0, 1)]
