from dataclasses import dataclass
from typing import Literal

PieceType = Literal["king", "queen", "rook", "bishop", "knight", "pawn"]
Color = Literal["white", "black"]

@dataclass
class Piece:
    piece_type: PieceType
    color: Color
    has_moved: bool = False


