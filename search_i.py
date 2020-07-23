"""Contains searching robot class implementations."""

import sys
from typing import Tuple, List
import heapq
from warehouse_utils import (parse_warehouse, get_start_pos, get_target_pos,
                             check_solution, apply_move, allowed, inbound)


class RecursionLimit:
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, val, tb):
        sys.setrecursionlimit(self.old_limit)


class Queue(list):
    """First in, first out."""
    def push(self, obj):
        pass

    def pop(self):
        pass


class Robot:
    """Base class for warehouse searching robots."""
    def __init__(self, moves):
        self.moves = moves
        self.count_explored = 0

    def increase_counter(self):
        self.count_explored += 1

    def _search(self, warehouse, start_pos, target_pos):
        """Search warehouse to find a way to given target position."""
        raise NotImplementedError

    def apply_move(self, square: Tuple[int], move: Tuple[int], warehouse: List[str] = None) -> Tuple[Tuple[int], float]:
        """Apply move and return next square on the grid.

        If a warehouse list is passed, cost is also calculated and returned,
        else cost is 1 by default.

        If next square is out of bounds, cost defaults to 1e+9.
        """
        i, j = apply_move(square, move)
        if warehouse is not None:
            try:
                cost = ord(warehouse[i][j])
            except IndexError:
                cost = 1e9
        else:
            cost = 1
        return (i, j), cost

    def find_moves(self, warehouse):
        """Search warehouse to find a way to package denoted by + on the grid."""
        parsed_warehouse = parse_warehouse(warehouse)
        start_pos = get_start_pos(parsed_warehouse)
        target_pos = get_target_pos(parsed_warehouse)
        return self._search(parsed_warehouse, start_pos, target_pos)


class RobotBFS(Robot):
    def _search(self, warehouse, start_pos, target_pos):
        return []

class PriorityQueue(list):
    """Regardless of push order, minimum out."""
    def push(self, *args):
        """Push object into PriorityQueue while retaining order."""
        pass

    def pop(self, *args):
        """Pop object from PriorityQueue while retaining order."""
        pass

    def remove(self, *args):
        """Remove object from PriorityQueue while retaining order."""
        pass


class RobotUCS(Robot):
    def _search(self, warehouse, start_pos, target_pos):
        return []

class RobotAstar(Robot):
    @staticmethod
    def heuristic(pos1, pos2, p=1):
        """Calculate heuristic for given two points on the grid."""
        return 0.0

    def _search(self, warehouse, start_pos, target_pos):
        return []

class RobotDFS(Robot):
    def __init__(self, *args, recursive=False , **kwargs):
        super().__init__(*args, **kwargs)
        if recursive:
            print('Performing recursive search')
            self._search = self._recursive_search
        else:
            print('Performing flat search')
            self._search = self._flat_search

    @staticmethod
    def _negate_move(move: Tuple[int]):
        """Negate move."""
        i, j = move
        return (-i, -j)

    def _recursive_search(self, warehouse: List[str], start_pos: Tuple[int], target_pos: Tuple[int], explored=None):
        """Perform recursive depth first search."""
        return []


    def _flat_search(self, warehouse: List[str], start_pos: Tuple[int], target_pos: Tuple[int], explored=None):
        """Perform flat depth first search."""
        return []


if __name__ == '__main__':
    from test_tracks import warehouse

    moves = [
        (-1, 0),  # up
        (0, 1),  # right
        (1, 0),  # down
        (0, -1),  # left
        ]

    robots = [RobotBFS, RobotUCS, RobotAstar, RobotDFS]

    print()
    for row in warehouse:
        print(row)
    print()
    for cls in robots:
        print('Running', cls.__name__)
        kwargs = {'recursive': True} if cls is RobotDFS and '-r' in sys.argv else {}
        robot = cls(moves, **kwargs)
        with RecursionLimit(1200):
            path = robot.find_moves(warehouse)
        # print(path)
        print('Total explored:', robot.count_explored)
        assert check_solution(warehouse, path, print_path='-v' in sys.argv), "Test failed."
        print()
        # for p in path:
        #     print(p)
