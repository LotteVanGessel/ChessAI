class Move:

    def __init__(self, initial, final, final_piece = None) -> None:
        self.initial = initial
        self.final = final 
        self.final_piece = final_piece
        

    def __eq__(self, value) -> bool:
        return value.initial == self.initial and value.final == self.final