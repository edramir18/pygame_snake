from random import Random
from typing import Set, Dict, List


from cell import Cell
from coord import Coord


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

    def get_vision(self, pos: Coord, cherry: Coord):
        x, y = (cherry - pos).get()
        vision = [x, y]  # type: List[int]
        for adj in Coord.adjacency(True):
            last = pos + adj
            if last not in self.cells or self.cells[last].is_wall():
                vision.append(1)
            elif self.cells[last].has_body:
                vision.append(1)
            # elif self.cells[last].has_cherry:
            #     vision += [0, 1]
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
