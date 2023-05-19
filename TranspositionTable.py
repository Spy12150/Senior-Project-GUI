import copy
class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, board, score, depth):
        fen = self.board_to_fen(board)
        self.table[fen] = (score, depth)

    def lookup(self, board):
        fen = self.board_to_fen(board)
        if fen in self.table:
            return self.table[fen]
        else:
            return None
        
    def board_to_fenBoard(self, copy_board):
        board = copy.deepcopy(copy_board)
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if(piece == "wP"):
                    board.board[row][col] = "P"
                elif(piece == "bP"):
                    board.board[row][col] = "p"
                elif(piece == "wQ"):
                    board.board[row][col] = "Q"
                elif(piece == "bQ"):
                    board.board[row][col] = "q"
                elif(piece == "wR"):
                    board.board[row][col] = "R"
                elif(piece == "bR"):
                    board.board[row][col] = "r"
                elif(piece == "wB"):
                    board.board[row][col] = "B"
                elif(piece == "wN"):
                    board.board[row][col] = "N"
                elif(piece == "bB"):
                    board.board[row][col] = "b"
                elif(piece == "bN"):
                    board.board[row][col] = "n"
                elif(piece == "wK"):
                    board.board[row][col] = "K"
                elif(piece == "bK"):
                    board.board[row][col] = "k"
        return board.board
    def board_to_fen(self, board_array_copy, color):
        board_array = self.board_to_fenBoard(board_array_copy)

        # Convert the board array to a FEN string
        fen_parts = []

        # Loop through the rows of the board array from the top to the bottom
        for row in range(8):
            fen_row = ''
            empty_squares = 0

            # Loop through the columns of the board array from left to right
            for col in range(8):
                piece = board_array[row][col]

                if piece == '':
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        fen_row += str(empty_squares)
                        empty_squares = 0

                    fen_row += piece

            if empty_squares > 0:
                fen_row += str(empty_squares)

            fen_parts.append(fen_row)

        fen = '/'.join(fen_parts)

        # Add the side to move, castling rights, en passant square, and halfmove clock
        # Assuming you have the necessary variables to retrieve this information
        side_to_move = color  # Example: 'w' for white to move, 'b' for black to move

        fen += f' {side_to_move}'

        return fen


