import pytest

from shared.models.board import Board
from shared.models.piece import Piece
from shared.rules import validate_rook_move


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

# Ладья
def test_rook_valid_mode():
    b = Board()
    b.set_piece(4, 2, Piece("rook", "white"))
    assert validate_rook_move(b, (4, 2), (4, 6), "white")

def test_rook_block_by_own_piece():
    b = Board()
    b.set_piece(4, 2, Piece("rook", "white"))
    b.set_piece(4, 4, Piece("pawn", "white"))
    assert validate_rook_move(b, (4, 2), (4, 6), "white") is False

def test_rook_diagonal_move():
    b = Board()
    b.set_piece(4, 2, Piece("rook", "white"))
    assert validate_rook_move(b, (4, 2), (5, 3), "white") is False

def test_eat_enemy_figure():
    b = Board()
    b.set_piece(4, 2, Piece("rook", "white"))
    b.set_piece(4, 4, Piece("pawn", "black"))
    assert validate_rook_move(b, (4, 2), (4, 4), "white")