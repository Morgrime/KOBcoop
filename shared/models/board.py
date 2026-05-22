from typing import Optional, List
from copy import deepcopy
from .piece import Piece

class Board:
    def __init__(self):
        self.grid: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]

    def get_piece(self, r: int, c: int) -> Optional[Piece]:
        if not self.is_on_board(r, c):
            raise IndexError("Координаты r и c вне доски")
        return self.grid[r][c]
        
    def set_piece(self, r: int, c: int, piece: Optional[Piece]) -> None:
        if not self.is_on_board(r, c):
            raise IndexError("Координаты r и c вне доски")
        self.grid[r][c] = piece

    def is_on_board(self, r: int, c: int) -> bool:
        """
        r - row
        c - column
        """
        return 0 <= r < 8 and 0 <= c < 8
    
    def copy(self) -> "Board":
        """
        Возврат глубокой копии. Нужно для валидации ходов.
        """
        new_board = Board()
        new_board.grid = deepcopy(self.grid)
        return new_board