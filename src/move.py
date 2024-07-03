class Move:

    def __init__(self, initial, final) -> None:
        self.initial = initial
        self.final = final 
        

    def __eq__(self, value) -> bool:
        return value.initial == self.initial and value.final == self.final