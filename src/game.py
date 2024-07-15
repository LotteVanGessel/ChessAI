import pygame

from const import ROWS, COLS, SQUARESIZE, HEIGHT
from board import Board
from dragger import Dragger
from config import Config
from square import Square
class Game:

    def __init__(self) -> None:
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = "white"
        self.hovered_sqr = None
        self.config = Config()


    def next_turn(self):
        self.next_player = "black" if self.next_player == "white" else "white"

    # show methods
    def show_bg(self, surface)->None:
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQUARESIZE, row *SQUARESIZE, SQUARESIZE, SQUARESIZE)
                pygame.draw.rect(surface, color, rect)

                if col == 0:
                    color = theme.bg.dark if row % 2 ==0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS - row), 1 , color)
                    lbl_pos = (5, 5 + row * SQUARESIZE)
                    surface.blit(lbl, lbl_pos)
                
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1 , color)
                    lbl_pos = (col * SQUARESIZE + SQUARESIZE - 20, HEIGHT - 20)
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(COLS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece 
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme 
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = theme.moves.light if  (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQUARESIZE, move.final.row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        move = self.board.last_move
        if move:
           initial = move.initial
           final = move.final
           for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 else theme.trace.dark
                rect = (pos.col * SQUARESIZE, pos.row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQUARESIZE, self.hovered_sqr.row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, capture = False):
        if capture:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()