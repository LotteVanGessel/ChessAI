import pygame 
import sys
from const import WIDTH, HEIGHT, SQUARESIZE
from game import Game
from square import Square
from move import Move


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()


    def main_loop(self) -> None:
        while True:
            self.game.show_bg(surface = self.screen)
            self.game.show_last_move(surface=self.screen)
            self.game.show_moves(self.screen)
            self.game.show_hover(self.screen)
            self.game.show_pieces(surface=self.screen)
            if self.game.dragger.dragging:
                self.game.dragger.update_blit(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game.dragger.update_mouse(event.pos)
                    clicked_row = self.game.dragger.mouseY // SQUARESIZE
                    clicked_col = self.game.dragger.mouseX // SQUARESIZE
                    if self.game.board.squares[clicked_row][clicked_col].has_piece():
                        piece = self.game.board.squares[clicked_row][clicked_col].piece
                        if piece.color == self.game.next_player:
                            self.game.board.calc_moves(piece, clicked_row, clicked_col)
                            self.game.dragger.save_inital(event.pos)
                            self.game.dragger.drag_piece(piece)
                            self.game.show_bg(self.screen)
                            self.game.show_moves(self.screen)
                            self.game.show_pieces(self.screen)

                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUARESIZE
                    motion_col = event.pos[0] // SQUARESIZE
                    self.game.set_hover(motion_row, motion_col)
                    if self.game.dragger.dragging:
                        self.game.dragger.update_mouse(event.pos)
                        self.game.show_bg(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_hover(self.screen)
                        self.game.show_pieces(self.screen)
                        self.game.dragger.update_blit(self.screen) 


                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.game.dragger.dragging:
                        self.game.dragger.update_mouse(event.pos)
                        clicked_row = self.game.dragger.mouseY // SQUARESIZE
                        clicked_col = self.game.dragger.mouseX // SQUARESIZE     
                        initial = Square(self.game.dragger.initial_row, self.game.dragger.initial_col)
                        final = Square(clicked_row, clicked_col)
                        move = Move(initial, final)
                        if self.game.board.valid_move(self.game.dragger.piece, move):
                            capture = self.game.board.squares[clicked_row][clicked_col].has_piece()
                            self.game.board.move(self.game.dragger.piece, move)
                            self.game.sound_effect(capture)
                            self.game.show_bg(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_pieces(self.screen)
                            self.game.next_turn()
                        self.game.dragger.undrag_piece()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.game.change_theme()
                    elif event.key == pygame.K_r:
                        self.game.reset()
                    
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main() 
main.main_loop()
 