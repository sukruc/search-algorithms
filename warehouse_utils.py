"""Warehouse helper functions."""

from typing import List, Tuple

MOVEMENT_SYMBOL = {(1, 0): 'v', (-1, 0): '^', (0, 1): '>', (0, -1): '<'}


def parse_warehouse(warehouse: List[str]) -> List[List[str]]:
    """Convert warehouse map to a usable list of lists structure."""
    return [list(row) for row in warehouse]


def apply_move(square: Tuple[int], move: Tuple[int]) -> Tuple[int]:
    """Apply move in current square and return next position."""
    return square[0] + move[0], square[1] + move[1]


def inbound(warehouse_parsed: List[List[str]], square: Tuple[int]) -> bool:
    """Return if square is within warehouse bounds."""
    x = len(warehouse_parsed)
    y = len(warehouse_parsed[0])
    return (0 <= square[0] < x) and (0 <= square[1] < y)


def allowed(warehouse_parsed: List[List[str]], square: Tuple[int]) -> bool:
    """Return if square is blocked or not."""
    return warehouse_parsed[square[0]][square[1]] != '#'


def arrived(warehouse_parsed: List[List[str]], square: Tuple[int]) -> bool:
    """Return if arrived at destination."""
    return warehouse_parsed[square[0]][square[1]] == '+'


def get_symbol_pos(warehouse_parsed: List[List[str]], symbol: str) -> Tuple[int]:
    """Return symbol position."""
    m = len(warehouse_parsed)
    n = len(warehouse_parsed[0])
    for i in range(m):
        for j in range(n):
            if warehouse_parsed[i][j] == symbol:
                return (i, j)


def get_start_pos(warehouse_parsed: List[List[str]]) -> Tuple[int]:
    """Return starting position."""
    return get_symbol_pos(warehouse_parsed, '@')


def get_target_pos(warehouse_parsed: List[List[str]]) -> Tuple[int]:
    """Return target position."""
    return get_symbol_pos(warehouse_parsed, '+')


def check_solution(warehouse: List[str], moves: List[Tuple[int]], expected_turns=None, print_path=False):
    """Check validity of solution."""
    warehouse_parsed = parse_warehouse(warehouse)
    if expected_turns is None:
        expected_turns = len(warehouse_parsed) * len(warehouse_parsed[0])
    turn = 0
    cost = 0
    position = get_start_pos(warehouse_parsed)
    k0, k1 = position
    for move in moves:
        turn += 1
        i, j = position
        warehouse_parsed[i][j] = MOVEMENT_SYMBOL[move]
        position = apply_move(position, move)
        i, j = position
        cost += ord(warehouse[i][j])
        if turn > expected_turns:
            print('Timeout.')
            return False
        if not inbound(warehouse_parsed, position):
            print(position)
            print('Out of bounds.')
            return False
        if not allowed(warehouse_parsed, position):
            print(position)
            print('Walked into the wall.')
            return False
        if arrived(warehouse_parsed, position):
            print('Success')
            warehouse_parsed[k0][k1] = '@'
            print('Total cost:', cost)
            print('Followed path:')
            if print_path:
                for row in warehouse_parsed:
                    print(''.join(row))
            return True
    return False
