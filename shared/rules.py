from .models.board import Board


def validate_rook_move(board: Board, from_pos: tuple[int, int], to_pos: tuple[int, int], color: str) -> bool:
    """Валидация хода ладьи"""
    piece = board.get_piece(*from_pos)
    fr, fc = from_pos
    tr, tc = to_pos

    if not piece:
        return False
    
    if piece.color != color:
        return False
    
    # Если тип не ладья
    if piece.piece_type != "rook":
        return False
    
    # Проверка что ход не по прямой или фигура стоит на месте
    if fr != tr and fc != tc:
        return False
    if fr == tr and fc == tc:
        return False
    
    # Проверка что на целевой клетке нет своей фигуры
    target = board.get_piece(tr, tc)
    if target is not None and target.color == color:
        return False
    
    # Вычисляем направление шага (0, 1 или -1)
    dr = 0 if fr == tr else (1 if tr > fr else -1)
    dc = 0 if fc == tc else (1 if tc > fc else -1)
    
    # Проверка пути между стартом и финишем
    curr_r, curr_c = fr + dr, fc + dc
    while (curr_r, curr_c) != (tr, tc):
        if board.get_piece(curr_r, curr_c) is not None:
            return False
        curr_r += dr
        curr_c += dc

    return True
    

    
