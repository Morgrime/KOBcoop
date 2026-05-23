import pytest

from shared.models.board import Board
from shared.models.piece import Piece

def test_board_set_piece():
    b = Board()
    b.set_piece(3, 4, Piece("knight", "white"))

    assert b.get_piece(3, 4).piece_type == "knight"

    # фигуры поставлены не туда
    with pytest.raises(IndexError):
        assert b.get_piece(-1, 5)

    with pytest.raises(IndexError):
        assert b.get_piece(15, 5)

    with pytest.raises(IndexError):
        assert b.get_piece(0, 15)    

def test_copy():
    b = Board()
    b.set_piece(3, 4, Piece("knight", "white"))

    b2 = b.copy()
    b2.set_piece(3, 4, Piece("pawn", "black"))
    assert b.get_piece(3, 4).color == "white", "Копирование сломало оригинал"