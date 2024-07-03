from const import COLS, ROWS
from square import Square
from piece import * 
from move import Move

class Board:

    def __init__(self) -> None:
        self.squares = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece, move):
        initial = move.initial
        final = move.final 
        
        self.squares[initial.row][initial.col].piece = None 
        self.squares[final.row][final.col].piece = piece 

        piece.moved = True

        piece.clear_moves()
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):
        def pawn_moves():
            steps = 1 if piece.moved else 2

            start = row + piece.dir 
            end = row + (piece.dir) * (1 + steps)
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: break
                else: break
            move_row = row + piece.dir
            move_cols = [col + 1, col - 1]
            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def king_knight_moves(directions):
            adjecent = [(row + i, col +j) for i,j in directions]
            for possible_move in adjecent:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                move_row = row + row_incr
                move_col = col + col_incr
                while True:
                    if Square.in_range(move_row, move_col):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        move = Move(initial, final)
                        if self.squares[move_row][move_col].isempty():
                            piece.add_move(move)
                        if self.squares[move_row][move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break
                        if self.squares[move_row][move_col].has_team_piece(piece.color):
                            break
                    else: break
                    move_row, move_col = move_row + row_incr, move_col + col_incr
        
        if isinstance(piece, Pawn):     pawn_moves()
        elif isinstance(piece, Knight): king_knight_moves([(- 2, 1),(- 2, - 1),(2, 1),(2, - 1),(- 1, 2),(1, 2),(- 1, - 2),(1, - 2)])
        elif isinstance(piece, Bishop): straight_line_moves([(-1, 1), (1, 1), (1, -1), (-1, -1)])
        elif isinstance(piece, Rook):   straight_line_moves([(1, 0), (-1, 0), (0, 1), (0, -1)])
        elif isinstance(piece, Queen):  straight_line_moves([(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)])
        elif isinstance(piece, King):   king_knight_moves([(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)])

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)          

    def _add_pieces(self, color):
        row_pawn, row_other = (6,7) if color == "white" else (1,0)

        # pawns 
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn,col, Pawn(color))

        # knights 
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishop 
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks 
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen and King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))