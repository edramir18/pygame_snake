from typing import Set

from coord import Coord


class Snake:
    def __init__(self, pos: Coord):
        self.body = set()  # type: Set[Coord]
        self.body.add(pos)
        self.path = [pos]
        self.head = pos

    def move(self, pos):
        last = self.path.pop()
        if len(self.path) == 0 or last != self.path[-1]:
            self.body.remove(last)
        else:
            last = None
        self.body.add(pos)
        self.path.insert(0, pos)
        self.head = pos
        return last

    def grow(self):
        self.path.append(self.path[-1])
