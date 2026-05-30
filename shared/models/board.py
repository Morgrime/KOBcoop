from dataclasses import asdict
from typing import Optional, List
from copy import deepcopy
from .piece import Piece


class Board:
    def __init__(self):
        self.grid: List[List[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

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

    def display(self) -> str:
        """
        Заглавные - белые
        строчные - черные
        """
        symbols = {
            "king": "K",
            "queen": "Q",
            "rook": "R",
            "bishop": "B",
            "knight": "K",
            "pawn": "P",
        }
        rows = []
        for row in self.grid:
            chars = []
            for cell in row:
                if cell is None:
                    chars.append("·")
                else:
                    sym = symbols[cell.piece_type]
                    chars.append(sym if cell.color == "white" else sym.lower())
            rows.append(" | ".join(chars))
            
        return "\n".join(rows)

    def apply_move(self, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> None:
        piece = self.get_piece(*from_pos)
        self.set_piece(*from_pos, None)
        self.set_piece(*to_pos, piece)
        if piece:
            piece.has_moved = True

    def to_dict(self) -> dict:
        """
        Заворачивание состояния доски в json чтобы отображать при подключении
        """
        grid = []
        for row in self.grid:
            grid.append([asdict(cell) if cell else None for cell in row])
        return {"grid": grid}
    
    @classmethod
    def from_dict(cls, data: dict) -> "Board":
        """
        Создание доски из JSON
        """
        board = cls()
        grid_data = data["grid"]
        for r, row in enumerate(grid_data):
            for c, cell in enumerate(row):
                if cell is not None:
                    board.set_piece(r, c, Piece(**cell))

        return board