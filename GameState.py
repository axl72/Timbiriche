from typing import NamedTuple
from numpy import ndarray
import numpy as np


class GameState(NamedTuple):
    """
    board_status: int[][]
        For each element, if its absolute element is four, then
        the square has been taken by a player. If element's sign
        is negative, then it has been taken by player 1. Otherwise,
        it has been taken by player 2.
        Access: board_status[y, x]

    row_status: int[][]
        Represent the horizontal line mark status: 1 for marked, 0 for not.
        Access: row_status[y, x]

    col_status: int[][]
        Represent the vertical line mark status: 1 for marked, 0 for not.
        Access: col_status[y, x]

    player1_turn: bool
        True if it is player 1 turn, False for player 2.
    """

    board_status: ndarray
    row_status: ndarray
    col_status: ndarray
    player1_turn: bool

    def get_id(self) -> str:
        return "".join(str(value) for value in self.board_status)

    def is_terminal(self) -> bool:
        posibles = list(filter(lambda x: False if x == 4 else True, [
                        abs(value) for row in self.board_status for value in row]))
        return len(posibles) == 0


if __name__ == "__main__":
    board_status1 = np.zeros(shape=(5 - 1, 5 - 1))
    board_status2 = np.zeros(shape=(4 - 1, 5 - 1))
    row_status1 = np.zeros(shape=(5, 5 - 1))
    col_status1 = np.zeros(shape=(5 - 1, - 1))
    row_status2 = np.zeros(shape=(4 - 1, 1))
    col_status2 = np.zeros(shape=(4 - 1, 5))
    estado1 = GameState(board_status1, row_status1, col_status2, True)
    estado2 = GameState(board_status2, row_status2, col_status2, False)
    print(estado1.board_status)
    print()
    print(estado2.board_status)
