class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, board, score, depth):
        self.table[hash(board)] = (score, depth)

    def lookup(self, board):
        if hash(board) in self.table:
            return self.table[hash(board)]
        else:
            return None