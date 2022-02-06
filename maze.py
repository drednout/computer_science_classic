from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from generic_search import dfs, Node, node_to_path


class Cell(str, Enum):
    BLOCKED = "x"
    EMPTY = " "
    PATH = "*"
    START = "S"
    FINISH = "F"



class MazePos(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, rows: int = 10, columns: int = 10, density: float = 0.2, 
                 start: MazePos = MazePos(0, 0), finish: MazePos = MazePos(9, 9)) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazePos = start
        self.finish: MazePos = finish

        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for c in range(self._columns)] for r in range(self._rows)
        ]
        self._fill_cells(density)
        self._grid[start.row][start.column] = Cell.START
        self._grid[finish.row][finish.column] = Cell.FINISH

    def _fill_cells(self, density: int) -> None:
        for i, row in enumerate(self._grid):
            for j, _ in enumerate(row):
                if random.random() <= density:
                    self._grid[i][j] = Cell.BLOCKED

    def __str__(self):
        out_strlist = []
        out_strlist.append("=" * (self._columns + 2) + "\n")
        for row in self._grid:
            column_str = "|" + "".join([c for c in row]) + "|\n"
            out_strlist.append(column_str)
        out_strlist.append("=" * (self._columns + 2) + "\n")

        return "".join(out_strlist)

    def is_goal_achieved(self, pos: MazePos) -> bool:
        return pos == self.finish

    def is_pos_valid(self, row: int, column: int) -> bool:
        if row < 0 or column < 0:
            return False
        if row >= self._rows or column >= self._columns:
            return False

        return True

    def get_possible_neighbours(self, pos: MazePos) -> List[MazePos]:
        out_positions : MazePos = []
        possible_neighbours = [
            (pos.row - 1, pos.column),
            (pos.row + 1, pos.column),
            (pos.row, pos.column - 1),
            (pos.row, pos.column + 1),
        ]

        for i, j in possible_neighbours:
            if self.is_pos_valid(i, j) and self._grid[i][j] != Cell.BLOCKED:
                out_positions.append(MazePos(i, j))

        return out_positions

    def mark(self, path: List[MazePos]) -> None:
        for maze_pos in path:
            self._grid[maze_pos.row][maze_pos.column] = Cell.PATH

        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.finish.row][self.finish.column] = Cell.FINISH

    def clear(self, path: List[MazePos]) -> None:
        for maze_pos in path:
            self._grid[maze_pos.row][maze_pos.column] = Cell.EMPTY

        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.finish.row][self.finish.column] = Cell.FINISH


if __name__ == "__main__":
    maze = Maze()
    print(maze)

    solution_dfs: Optional[Node[MazePos]] = dfs(maze.start, maze.is_goal_achieved, maze.get_possible_neighbours)

    if solution_dfs is None:
        print("No path found using DFS algo")
    else:
        path: List[MazePos] = node_to_path(solution_dfs)
        maze.mark(path)
        print(maze)
        maze.clear(path)

