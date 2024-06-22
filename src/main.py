import pygame 
import sys
from const import WIDTH, HEIGHT, SQUARESIZE
from game import Game


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()


    def main_loop(self) -> None:
        while True:
            self.game.show_bg(surface = self.screen)
            self.game.show_moves(self.screen)
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
                        self.game.board.calc_moves(piece, clicked_row, clicked_col)
                        self.game.dragger.save_inital(event.pos)
                        self.game.dragger.drag_piece(piece)
                        self.game.show_bg(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)

                elif event.type == pygame.MOUSEMOTION:
                    if self.game.dragger.dragging:
                        self.game.dragger.update_mouse(event.pos)
                        self.game.show_bg(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)
                        self.game.dragger.update_blit(self.screen) 


                elif event.type == pygame.MOUSEBUTTONUP:
                    self.game.dragger.undrag_piece()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main() 
main.main_loop()
 