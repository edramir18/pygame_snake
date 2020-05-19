from typing import Dict

from cell import Cell
from coord import Coord
from grid import Grid


class Node:
    def __init__(self, src: Coord, dst: Coord, parent:'Node' = None):
        self.position = src
        self.h = src.manhattan_to(dst)
        self.g = 0 if parent is None else parent.g + 1
        self.f = self.h + self.g
        self.parent = parent

    def get_path(self):
        lst = []
        node = self
        while node is not None:
            lst.append(node.position)
            node = node.parent
        lst.reverse()
        return lst

    def update_parent(self, parent: 'Node', g: int):
        self.g = g
        self.f = self.h + self.g
        self.parent = parent

    def __str__(self):
        return f'f:{self.f} g:{self.g}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.position == other.position


def find_route(start: Coord, end: Coord, grid: Grid):
    lst_open = dict()  # type: Dict[Coord, Node]
    lst_closed = dict()  # type: Dict[Coord, Node]
    begin = Node(start, end)
    lst_open[start] = begin
    while len(lst_open) > 0:
        current_pos = min(lst_open, key=lambda k: lst_open[k].f)
        current = lst_open.pop(current_pos)
        lst_closed[current_pos] = current
        if current_pos == end:
            return current.get_path()
        for pos in grid.get_neighbourds(current_pos):
            cell = grid.get(pos)
            if cell.is_wall() or cell.has_player:
                continue
            node = Node(pos, end, current)
            if pos in lst_closed:
                continue
            if pos in lst_open and node.g < lst_open[pos].g:
                lst_open[pos].update_parent(current, node.g)
            else:
                lst_open[pos] = node
    return list()
