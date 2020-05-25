from typing import Dict, List

from cell import Cell
from coord import Coord
from snake import Snake


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = dict()  # type: Dict[Coord, Cell]
        for y in range(height):
            for x in range(width):
                coord = Coord(x, y)
                cell = Cell()
                cell.celltype = Cell.CellType.FLOOR
                self.cells[coord] = cell

    def get(self, pos: Coord):
        if pos in self.cells:
            return self.cells[pos]
        return None

    def get_free_cells(self):
        return [coord for coord, cell in self.cells.items() if cell.is_empty()]

    def get_next_cherry(self, rand):
        free_cells = self.get_free_cells()
        pos = rand.choice(free_cells)  # type: Coord
        self.cells[pos].has_cherry = True
        return pos

    def get_neighbourds(self, coord):
        return [coord + adj for adj in Coord.adjacency()
                if coord + adj in self.cells]

    def get_vision(self, direction: Snake.Direction, pos: Coord, cherry: Coord):
        vision = list()
        r_pos = Coord(pos.x, pos.y)
        adj = [(-1, 0), (0, -1), (1, 0)]
        for i in range(direction.value):
            adj = [(-y, x) for x, y in adj]
            r_pos.x, r_pos.y = -r_pos.y, r_pos.x
        x, y = (cherry - r_pos).get_unit_vector().get()
        if x == 0:
            vision += [0, 0, 0] if y == -1 else [1, 0, 0]
        elif x == 1:
            if y == 0:
                vision += [0, 1, 0]
            else:
                vision += [0, 0, 1] if y == -1 else [0, 1, 1]
        elif x == -1:
            if y == 0:
                vision += [1, 1, 0]
            else:
                vision += [1, 1, 1] if y == -1 else [1, 0, 1]
        for vector in adj:
            last = pos + vector
            if last not in self.cells or self.cells[last].is_wall():
                vision.append(1)
            elif self.cells[last].has_body:
                vision.append(1)
            elif self.cells[last].has_cherry:
                vision.append(0)
            else:
                vision.append(0)
        return vision

    def build_walls(self, rand):
        for cell in self.cells.values():
            if rand.random() < 0.15:
                cell.celltype = Cell.CellType.WALL
        free_cells = self.get_free_cells()
        islands = list()
        computed = set()
        for coord in free_cells:
            if coord in computed:
                continue
            else:
                computed.add(coord)
            island = list()
            path = [coord]
            while len(path) > 0:
                first = path.pop(0)
                island.append(first)
                for adj in self.get_neighbourds(first):
                    if (adj in self.cells and adj not in computed
                            and self.cells[adj].is_floor()):
                        path.append(adj)
                        computed.add(adj)
            islands.append(island)
        islands.sort(key=lambda k: len(k), reverse=True)
        for island in islands[1:]:
            for coord in island:
                self.cells[coord].celltype = Cell.CellType.WALL
