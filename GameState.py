import pygame
class Game:
    def __init__(self):
        # Initialize the board and other variables
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.turn = 'w'
        self.en_passant = None
        self.castling_rights = 'KQkq'
        self.halfmove_clock = 0
        self.fullmove_number = 1

    def is_game_over(self):
        # Check if the game is in a state where it is over, such as checkmate or stalemate
        if self.is_checkmate(self.turn) or self.is_stalemate(self.turn):
            return True
        else:
            return False

    def get_color(self, piece):
        if piece == '':
            return None
        elif piece[0] == 'w':
            return 'w'
        else:
            return 'b'

    def get_king_pos(self, color):
        """Return the position of the king of the specified color."""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == color + 'K':
                    return (row, col)


    def is_in_check(self, player, kingPos):
        """Check if the given player is in check"""
        king_pos = kingPos
        
        # Check if any of the opponent's pieces can attack the king
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '' and self.get_color(piece) != player:
                    if king_pos in self.get_moves((row, col)):
                        return True
        
        return False


    def is_checkmate(self, color):
        king_pos = self.get_king_pos(color)
        if not self.is_in_check(king_pos, color):
            return False
        
        # Check if any move can get the king out of check
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '' and self.get_color(piece) == color:
                    for move in piece.get_valid_moves((row, col), self):
                        # Make the move and check if the king is still in check
                        new_state = self.copy()
                        new_state.move_piece((row, col), move)
                        new_king_pos = new_state.get_king_pos(color)
                        if not new_state.is_in_check(new_king_pos, color):
                            return False
        
        return True

    def is_stalemate(self, turn):
        """
        Returns True if the game is in stalemate, False otherwise.
        """
        # Check if the player is in stalemate
        if not self.is_in_check(turn):
            for piece in self.get_pieces(turn):
                for move in self.get_legal_moves(self):
                    # If the player has a legal move, the game is not in stalemate
                    if not self.is_in_check(self.get_color(piece), move):
                        return False
            return True
        return False



    def ask_for_move():
        """
        Asks the user for a move in chess notation (e.g. "e2e4").

        Returns:
            tuple: A tuple representing the start and end positions of the move.
        """
        while True:
            move_str = input("Enter your move in chess notation (e.g. 'e2e4'): ")
            if len(move_str) != 4:
                print("Invalid move. Please enter a move in the format 'e2e4'.")
                continue
            start_col, start_row, end_col, end_row = move_str[0], move_str[1], move_str[2], move_str[3]
            if start_col not in 'abcdefgh' or end_col not in 'abcdefgh' or \
                    start_row not in '12345678' or end_row not in '12345678':
                print("Invalid move. Please enter a move in the format 'e2e4'.")
                continue
            start_pos = (int(start_row) - 1, ord(start_col) - ord('a'))
            end_pos = (int(end_row) - 1, ord(end_col) - ord('a'))
            return start_pos, end_pos
        
    
    
    def is_valid_move(piece, start_pos, end_pos, self, board):
        # Check if the ending position is a valid square
        if not self.is_valid_square(end_pos):
            return False

        # Check if the starting position contains the specified piece
        if board[start_pos[0]][start_pos[1]] != piece:
            return False

        # Check if the ending position is one of the legal moves for the piece
        legal_moves = self.get_legal_moves(piece, start_pos)
        if end_pos not in legal_moves:
            return False

        # Check if the move would leave the king in check
        if self.is_check_after_move(piece, start_pos, end_pos):
            return False

        # All checks passed, so the move is valid
        return True

    

    
    def move_piece(board, move, self):
        start_col = ord(move[0]) - ord('a')
        start_row = int(move[1]) - 1
        end_col = ord(move[2]) - ord('a')
        end_row = int(move[3]) - 1
        
        start_pos = (start_row, start_col)
        end_pos = (end_row, end_col)
        
        piece = board[start_row][start_col]
        
        # Check if the starting position contains a piece
        if piece == '':
            return False
        
        # Check if the piece can legally move to the ending position
        if not self.is_valid_move(piece, start_pos, end_pos, board):
            return False
        
        # Move the piece
        board[start_row][start_col] = ''
        board[end_row][end_col] = piece
        
        return True
        
    def get_legal_moves(self):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == '':
                    continue
                if piece[0] == self.turn:
                    for move in self.get_moves((row, col)):
                        if self.is_valid_move((row, col), move):
                            legal_moves.append((row, col, move[0], move[1]))
        return legal_moves

    def get_moves(self, pos):
        row, col = pos
        piece = self.board[row][col]
        if piece[1] == 'P':
            return self.get_pawn_moves(pos)
        elif piece[1] == 'R':
            return self.get_rook_moves(self.board, row, col)
        elif piece[1] == 'N':
            return self.get_knight_moves(pos)
        elif piece[1] == 'B':
            return self.get_bishop_moves(pos)
        elif piece[1] == 'Q':
            return self.get_queen_moves(pos)
        elif piece[1] == 'K':
            return self.get_king_moves(pos)

    def get_king_moves(row, col, board, self):
        """Get all legal moves for a king at a given position on the board"""
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            end_row = row + direction[0]
            end_col = col + direction[1]
            if self.is_valid_square(end_row, end_col) and (board[end_row][end_col] == '' or self.is_opponent(board[row][col], board[end_row][end_col])):
                moves.append((end_row, end_col))
        return moves
    def is_opponent_checking(board, king_pos, opponent_color, self):
        for row in range(8):
            for col in range(8):
                if board[row][col] != '' and self.get_piece_color(board[row][col]) == opponent_color:
                    legal_moves = self.get_legal_moves((row, col))
                    if king_pos in legal_moves:
                        return True
        return False

    def get_piece_color(piece):
        if piece[0] == 'w':
            return 'white'
        elif piece[0] == 'b':
            return 'black'
        else:
            return None
    def is_valid_square(row, col):
        """Check if a given row and column are valid coordinates on a chess board"""
        return 0 <= row < 8 and 0 <= col < 8

    def is_opponent(piece1, piece2):
        """Check if piece1 and piece2 belong to opposite players"""
        if piece1 == '' or piece2 == '':
            return False
        return piece1[0] != piece2[0]
    
    def get_queen_moves(row, col, board,self):
        """Get all legal moves for a queen at a given position on the board"""
        return self.get_rook_moves(row, col, board) + self.get_bishop_moves(row, col, board)

    def get_knight_moves(board, row, col, self):
        """
        Given the current board and knight position, returns a list of all possible moves that the knight can make.
        """
        moves = []

        # Possible moves for a knight
        possible_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

        # Generate all possible moves for the knight
        for move in possible_moves:
            new_row = row + move[0]
            new_col = col + move[1]

            # Check if the new position is within the board
            if new_row < 0 or new_row > 7 or new_col < 0 or new_col > 7:
                continue

            # Check if the new position is empty or contains an opponent's piece
            if board[new_row][new_col] == '' or self.is_opponent(board[row][col], board[new_row][new_col]):
                moves.append((new_row, new_col))

        return moves
    def get_rook_moves(board, row, col, self):
        """
        Given the current board and rook position, returns a list of all possible moves that the rook can make.
        """
        moves = []

        # Check moves to the right
        for i in range(col + 1, 8):
            if board[row][i] == '':
                moves.append((row, i))
            elif self.is_opponent(board[row][col], board[row][i]):
                moves.append((row, i))
                break
            else:
                break

        # Check moves to the left
        for i in range(col - 1, -1, -1):
            if board[row][i] == '':
                moves.append((row, i))
            elif self.is_opponent(board[row][col], board[row][i]):
                moves.append((row, i))
                break
            else:
                break

        # Check moves up
        for i in range(row - 1, -1, -1):
            if board[i][col] == '':
                moves.append((i, col))
            elif self.is_opponent(board[row][col], board[i][col]):
                moves.append((i, col))
                break
            else:
                break

        # Check moves down
        for i in range(row + 1, 8):
            if board[i][col] == '':
                moves.append((i, col))
            elif self.is_opponent(board[row][col], board[i][col]):
                moves.append((i, col))
                break
            else:
                break

        return moves
    def get_pawn_moves(board, row, col, self):
        """
        Given the current board and pawn position, returns a list of all possible moves that the pawn can make.
        """
        moves = []

        piece = board[row][col]
        color = piece[0]

        # Check moves for white pawns
        if color == 'w':
            # Check move one square up
            if row > 0 and board[row-1][col] == '':
                moves.append((row-1, col))

                # Check move two squares up (only allowed from starting position)
                if row == 6 and board[row-2][col] == '':
                    moves.append((row-2, col))

            # Check captures to the upper right and left diagonals
            if row > 0 and col < 7 and self.is_opponent(piece, board[row-1][col+1]):
                moves.append((row-1, col+1))

            if row > 0 and col > 0 and self.is_opponent(piece, board[row-1][col-1]):
                moves.append((row-1, col-1))

        # Check moves for black pawns
        if color == 'b':
            # Check move one square down
            if row < 7 and board[row+1][col] == '':
                moves.append((row+1, col))

                # Check move two squares down (only allowed from starting position)
                if row == 1 and board[row+2][col] == '':
                    moves.append((row+2, col))

            # Check captures to the lower right and left diagonals
            if row < 7 and col < 7 and self.is_opponent(piece, board[row+1][col+1]):
                moves.append((row+1, col+1))

            if row < 7 and col > 0 and self.is_opponent(piece, board[row+1][col-1]):
                moves.append((row+1, col-1))

        return moves
    def get_bishop_moves(row, col, board, self):
        """Get all legal moves for a bishop at a given position on the board"""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            for i in range(1, 8):
                end_row = row + i * direction[0]
                end_col = col + i * direction[1]
                if not self.is_valid_square(end_row, end_col):
                    break
                if board[end_row][end_col] == '':
                    moves.append((end_row, end_col))
                elif self.is_opponent(board[row][col], board[end_row][end_col]):
                    moves.append((end_row, end_col))
                    break
                else:
                    break
        return moves
    
        




