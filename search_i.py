"""Contains searching robot implementations."""

import sys
from typing import Tuple, List
import heapq
from warehouse_utils import (
    parse_warehouse,
    get_start_pos,
    get_target_pos,
    check_solution,
    apply_move,
    allowed,
    inbound
    )


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
        self.append(obj)

    def pop(self):
        return super().pop(0)



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

    @staticmethod
    def apply_move(square: Tuple[int], move: Tuple[int], warehouse: List[str] = None) -> Tuple[Tuple[int], float]:
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

    def _recursive_search(self, warehouse: List[str], start_pos: Tuple[int], target_pos: Tuple[int], seen=None):
        """Perform recursive depth first search."""
        self.increase_counter()
        if seen is None:
            seen = {start_pos}
        moves = self.moves.copy()
        np.random.shuffle(moves)
        for move in moves:
            new_square, cost = self.apply_move(start_pos, move, warehouse)

            if new_square == target_pos:
                return [move]

            if new_square in seen:
                continue

            seen.add(new_square)

            if not inbound(warehouse, new_square):
                continue
            if not allowed(warehouse, new_square):
                continue

            path = self._recursive_search(warehouse, new_square, target_pos, seen)
            if path:
                return [move] + path
            else:
                continue
        return []


    def _flat_search(self, warehouse: List[str], start_pos: Tuple[int], target_pos: Tuple[int], explored=None):
        """Perform flat depth first search."""
        return []


class RobotBFS(Robot):
    def _search(self, warehouse, start_pos, target_pos):
        explored = {start_pos: []}  #  {(3, 3): [(0, 1), (0, 1), (-1, 0)]}
        frontiers = Queue([start_pos])

        while True:
            if not frontiers:
                return []

            frontier = frontiers.pop()
            self.increase_counter()

            if frontier == target_pos:
                return explored[target_pos]

            for move in self.moves:
                new_square, cost = self.apply_move(frontier, move, warehouse)

                if new_square in explored:
                    continue
                explored[new_square] = explored[frontier] + [move]

                if not inbound(warehouse, new_square):
                    continue
                if not allowed(warehouse, new_square):
                    continue
                frontiers.push(new_square)

# heap

# heapq

class PriorityQueue(list):
    """Regardless of push order, minimum out."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        heapq.heapify(self)

    def push(self, obj: Tuple[float, Tuple[int, int]]):
        """Push object into PriorityQueue while retaining order."""
        heapq.heappush(self, obj)

    def pop(self):
        """Pop object from PriorityQueue while retaining order."""
        obj = heapq.heappop(self)
        return obj

    def remove(self, location: Tuple[int, int]):
        """Remove object from PriorityQueue while retaining order."""
        for i, obj in enumerate(self):
            if obj[1] == location:
                super().pop(i)
                heapq.heapify(self)
                break


class RobotUCS(Robot):
    def _search(self, warehouse, start_pos, target_pos):
        explored = {start_pos: ([], 0)}  #  {(3, 3): ([(0, 1), (0, 1), (-1, 0)], 8)}
        frontiers = PriorityQueue([(0, start_pos)])  # (8, (4,5))

        while True:
            if not frontiers:
                return []

            _, frontier = frontiers.pop()
            self.increase_counter()

            path_here, cost_here = explored[frontier]

            if frontier == target_pos:
                return path_here

            for move in self.moves:
                new_square, cost = self.apply_move(frontier, move, warehouse)

                if new_square in explored:
                    if explored[new_square][1] <= cost_here + cost:
                        continue
                    else:
                        frontiers.remove(new_square)

                # explored[new_square] = explored[frontier] + [move]
                explored[new_square] = path_here + [move], cost_here + cost

                if not inbound(warehouse, new_square):
                    continue
                if not allowed(warehouse, new_square):
                    continue
                frontiers.push((cost, new_square))


class RobotAstar(Robot):
    @staticmethod
    def heuristic(pos1, pos2, p=1):
        """Calculate heuristic for given two points on the grid."""
        return 0.0

    def _search(self, warehouse, start_pos, target_pos):
        return []


if __name__ == '__main__':
    from test_tracks import WAREHOUSES

    import numpy as np

    try:
        track_number = [i for i in sys.argv if i.isnumeric()]
        track_number = int(track_number[0])
        WAREHOUSES[track_number]
    except IndexError:
        print(f'Enter a warehouse number {list(range(len(WAREHOUSES)))} to run robots.')
        sys.exit(1)

    recursion = '-r' in sys.argv
    print_path = '-v' in sys.argv

    moves = [
        (-1, 0),  # up
        (0, 1),  # right
        (1, 0),  # down
        (0, -1),  # left
        ]

    robots = [RobotBFS, RobotUCS, RobotAstar, RobotDFS]
    print()
    print()
    for cls in robots:
        print('Running', cls.__name__)
        kwargs = {'recursive': True} if cls is RobotDFS and recursion else {}
        robot = cls(moves, **kwargs)

        for warehouse in [WAREHOUSES[track_number]]:
            with RecursionLimit(2500):
                path = robot.find_moves(warehouse)
            print('Total explored:', robot.count_explored)
            try:
                assert check_solution(warehouse, path, print_path=print_path), "Test failed."
            except AssertionError as e:
                print(e)

            print()
