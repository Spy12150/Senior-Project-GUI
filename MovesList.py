import copy
class MovesList:
    def __init__(self):
        something = 0
        

    def is_stalemate(self, color, moves, board):
        if(self.is_king_in_check(board, color)):
            return False

        
        if (len(moves) == 0):
            return True

        pieces = []
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece != '' and piece[1] != "K":
                    pieces.append("piece")
                    if(len(pieces) > 2):
                        return False
        if(len(pieces) == 0):
            return True
        if(len(pieces) == 1 and (pieces[0][1] == "N" or pieces[0][1] == "B")):
            return True
        if(len(pieces) == 1 and (pieces[0][1] == "N" and pieces[1][1] == "N")):
            return True

        return False

    def get_king_pos(self, color, board):
        for row in range(8):
            for col in range(8):
                if board.board[row][col] == color + 'K':
                    return str(row) + str(col)
        return "1234"
    def is_king_in_check(self, board, color):
        king_pos = self.get_king_pos(color, board)
        opponent_color = 'b' if color == 'w' else 'w'
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece != '' and piece[0] == opponent_color:
                    
                    if self.is_valid_move(row, col, int(king_pos[0]), int(king_pos[1]), opponent_color, board):
                        return True
        return False
    
    def isTempo(self, piece, start_row, start_col,  board):
        color = piece[0]
        if piece[1] == "P" and color == "w":
            movesopt = {(-1,-1), (-1,1)}
            for movenums in movesopt:
                end_row, end_col = start_row + movenums[0],start_col + movenums[1]
                
                if end_row >= 0 and end_col >= 0:
                    move = chr(ord('a') + start_col) + str(8 - start_row)+ chr(ord('a') + end_col) + str(8 - end_row )
                    
                    
                    
                    if self.capture(move, color, board):
                        return True
                    return False
                    

        elif piece[1] == "P" and color == "b":
            movesopt = {(1,-1), (1,1), (1,0), (2,0)}
            for movenums in movesopt:
                end_row, end_col = start_row + movenums[0],start_col + movenums[1]
                
                if end_row >= 0 and end_col >= 0:
                    move = chr(ord('a') + start_col) + str(8 - start_row)+ chr(ord('a') + end_col) + str(8 - end_row )
                    
                    
                    
                    if self.capture(move, color, board):
                        return True
                    return False
        elif piece[1] == "R" and piece[0] == color:
            movesopt = []
            for i in range(17):
                movesopt.append((0,i - 8))
            for i in range(17):
                movesopt.append((i - 8,0))
            for movenums in movesopt:
                end_row, end_col = start_row + movenums[0],start_col + movenums[1]
                
                if end_row >= 0 and end_col >= 0:
                    move = chr(ord('a') + start_col) + str(8 - start_row)+ chr(ord('a') + end_col) + str(8 - end_row )
                    
                    
                    
                    if self.capture(move, color, board):
                        return True
                    return False
        elif piece[1] == "N" and piece[0] == color:
            movesopt = {(-2,-1), (-1,-2),(-2,1),(1,-2),(2,-1),(-1,2),(2,1),(1,2)}
            for movenums in movesopt:
                end_row, end_col = start_row + movenums[0],start_col + movenums[1]
                
                if end_row >= 0 and end_col >= 0:
                    move = chr(ord('a') + start_col) + str(8 - start_row)+ chr(ord('a') + end_col) + str(8 - end_row )
                    
                    
                    
                    if self.capture(move, color, board):
                        return True
                    return False
        elif piece[1] == "K" and piece[0] == color:
            movesopt = []
            for i in [-1,0,1]:
                for j in [-1, 0, 1]:
                    movesopt.append((i,j))
            
            for movenums in movesopt:
                end_row, end_col = start_row + movenums[0],start_col + movenums[1]
                
                if end_row >= 0 and end_col >= 0:
                    move = chr(ord('a') + start_col) + str(8 - start_row)+ chr(ord('a') + end_col) + str(8 - end_row )
                    
                    
                    
                    if self.capture(move, color, board):
                        return True
                    return False
        elif piece[1] == "B" and piece[0] == color:
            movesopt = []
            for i in range(17):
                movesopt.append((i-8,i - 8))
            for i in range(17):
                movesopt.append((i - 8,-i + 8))
            for movenums in movesopt:
                end_row, end_col = start_row + movenums[0],start_col + movenums[1]
                
                if end_row >= 0 and end_col >= 0:
                    move = chr(ord('a') + start_col) + str(8 - start_row)+ chr(ord('a') + end_col) + str(8 - end_row )
                    
                    
                    
                    if self.capture(move, color, board):
                        return True
                    return False
        elif piece[1] == "Q" and piece[0] == color:
            movesopt = []
            for i in range(17):
                movesopt.append((0,i - 8))
            for i in range(17):
                movesopt.append((i - 8,0))
            for i in range(17):
                movesopt.append((i-8,i - 8))
            for i in range(17):
                movesopt.append((i - 8,-i + 8))
            for movenums in movesopt:
                end_row, end_col = start_row + movenums[0],start_col + movenums[1]
                
                if end_row >= 0 and end_col >= 0:
                    move = chr(ord('a') + start_col) + str(8 - start_row)+ chr(ord('a') + end_col) + str(8 - end_row )
                    
                    
                    
                    if self.capture(move, color, board):
                        return True
                    return False
    
    def get_captures(self, board, color):
        moves = []
        boardcopy = board  # create a copy of the board to avoid modifying the original
        for row in range(8):
            for col in range(8):
                boardcopy = board
                piece = boardcopy.board[row][col]
                if piece != '' and piece[0] == color:
                    if piece[1] == "P" and color == "w":
                        movesopt = {(-1,-1), (-1,1), (-1,0), (-2,0)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                
                                
                                if self.capture(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "P" and color == "b":
                        movesopt = {(1,-1), (1,1), (1,0), (2,0)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                if self.capture(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "R" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((0,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,0))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                if self.capture(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "N" and piece[0] == color:
                        movesopt = {(-2,-1), (-1,-2),(-2,1),(1,-2),(2,-1),(-1,2),(2,1),(1,2)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                
                                if self.capture(move, color, boardcopy):
                                    moves.append(move)
                                    
                                    boardcopy = board
                    elif piece[1] == "K" and piece[0] == color:
                        movesopt = []
                        if(boardcopy.board[7][4] == "wK"):
                            
                            if self.capture("e1g1", color, boardcopy):
                                    
                                    moves.append("e1g1")
                                    boardcopy = board
                            if self.capture("e1c1", color, boardcopy):
                                    moves.append("e1c1")
                                    boardcopy = board
                        if(boardcopy.board[0][4] == "bK"):
                            if self.capture("e8g8", color, boardcopy):
                                    moves.append("e8g8")
                                    boardcopy = board
                            if self.capture("e8c8", color, boardcopy):
                                    moves.append("e8c8")
                                    boardcopy = board
                        for i in [-1,0,1]:
                            for j in [-1, 0, 1]:
                                movesopt.append((i,j))
                        
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                if self.capture(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "B" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((i-8,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,-i + 8))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                            
                            if self.capture(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "Q" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((0,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,0))
                        for i in range(17):
                            movesopt.append((i-8,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,-i + 8))
                        for movenums in movesopt:
                            move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + col + movenums[1]) + str(8 - row + movenums[0])
                            
                            if self.capture(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board

        

        return moves
    
    def capture(self, move, color, boardcopy):
        board = copy.deepcopy(boardcopy)
        if(len(move) != 4):
            
            return False
        
        start_col = ord(move[0]) - ord('a')
        start_row = 7 - (int(move[1]) - 1)
        end_col = ord(move[2]) - ord('a')
        end_row = 7- (int(move[3]) - 1)
        

        

        if(len(str(start_col) + str(start_row) + str(end_col) + str(end_row)) != 4):
            
            return False

        

        if str(start_col) not in '01234567' or str(end_col) not in '01234567' or str(start_row) not in '01234567' or str(end_row) not in '01234567':
            
            return False

        piece = board.board[start_row][start_col]

        if piece == '':
            
            
            return False
        if(board.board[end_row][end_col] != ''):
            if(board.board[end_row][end_col][0] == color):
                
                
                
                return False


        if (board.board[start_row][start_col][0] != color):
            
            
            return False


        if (self.is_valid_move(start_row, start_col, end_row, end_col, color, board)):
            swapped = board.board[end_row][end_col]
            if color == "w":
                othercolor = "b"
            else:
                othercolor = "w"
            
            board.board[start_row][start_col] = ''
            board.board[end_row][end_col] = piece
            if(swapped == '' ):
                if not self.is_king_in_check(board, othercolor):
                    return False
            
            if((piece == "wP" and end_row == 0) or (piece == "bP" and end_row == 7)):
                board.board[end_row][end_col] = piece[0] + "Q"

            if(self.get_king_pos == "1234"):
                board.board[start_row][start_col] = piece
                board.board[end_row][end_col] = swapped
                return False
            if(self.is_king_in_check(board, color)):
                board.board[start_row][start_col] = piece
                board.board[end_row][end_col] = swapped
                
                
                return False
            board.board[start_row][start_col] = piece
            board.board[end_row][end_col] = swapped

        else: 
            
            
            return False
        
        

        
        
        return True
        
    def get_legal_moves(self, board, color):
        moves = []
        boardcopy = board  # create a copy of the board to avoid modifying the original
        for row in range(8):
            for col in range(8):
                boardcopy = board
                piece = boardcopy.board[row][col]
                if piece != '' and piece[0] == color:
                    if piece[1] == "P" and color == "w":
                        movesopt = {(-1,-1), (-1,1), (-1,0), (-2,0)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                
                                
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "P" and color == "b":
                        movesopt = {(1,-1), (1,1), (1,0), (2,0)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "R" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((0,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,0))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "N" and piece[0] == color:
                        movesopt = {(-2,-1), (-1,-2),(-2,1),(1,-2),(2,-1),(-1,2),(2,1),(1,2)}
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    
                                    boardcopy = board
                    elif piece[1] == "K" and piece[0] == color:
                        movesopt = []
                        if(boardcopy.board[7][4] == "wK"):
                            
                            if self.move("e1g1", color, boardcopy):
                                    
                                    moves.append("e1g1")
                                    boardcopy = board
                            if self.move("e1c1", color, boardcopy):
                                    moves.append("e1c1")
                                    boardcopy = board
                        if(boardcopy.board[0][4] == "bK"):
                            if self.move("e8g8", color, boardcopy):
                                    moves.append("e8g8")
                                    boardcopy = board
                            if self.move("e8c8", color, boardcopy):
                                    moves.append("e8c8")
                                    boardcopy = board
                        for i in [-1,0,1]:
                            for j in [-1, 0, 1]:
                                movesopt.append((i,j))
                        
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            if end_row >= 0 and end_col >= 0:
                                move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                                
                                if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "B" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((i-8,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,-i + 8))
                        for movenums in movesopt:
                            end_row, end_col = row + movenums[0], col + movenums[1]
                            move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + end_col) + str(8 - end_row )
                            
                            if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board
                    elif piece[1] == "Q" and piece[0] == color:
                        movesopt = []
                        for i in range(17):
                            movesopt.append((0,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,0))
                        for i in range(17):
                            movesopt.append((i-8,i - 8))
                        for i in range(17):
                            movesopt.append((i - 8,-i + 8))
                        for movenums in movesopt:
                            move = chr(ord('a') + col) + str(8 - row)+ chr(ord('a') + col + movenums[1]) + str(8 - row + movenums[0])
                            
                            if self.move(move, color, boardcopy):
                                    moves.append(move)
                                    boardcopy = board

        

        return moves

    def move(self, move, color, boardcopy):
        board = copy.deepcopy(boardcopy)
        if(len(move) != 4):
            
            return False
        
        start_col = ord(move[0]) - ord('a')
        start_row = 7 - (int(move[1]) - 1)
        end_col = ord(move[2]) - ord('a')
        end_row = 7- (int(move[3]) - 1)
        

        

        if(len(str(start_col) + str(start_row) + str(end_col) + str(end_row)) != 4):
            
            return False

        

        if str(start_col) not in '01234567' or str(end_col) not in '01234567' or str(start_row) not in '01234567' or str(end_row) not in '01234567':
            
            return False

        piece = board.board[start_row][start_col]

        if piece == '':
            
            
            return False
        if(board.board[end_row][end_col] != ''):
            if(board.board[end_row][end_col][0] == color):
                
                
                
                return False


        if (board.board[start_row][start_col][0] != color):
            
            
            return False


        if (self.is_valid_move(start_row, start_col, end_row, end_col, color, board)):
            swapped = board.board[end_row][end_col]
            board.board[start_row][start_col] = ''
            board.board[end_row][end_col] = piece
            
            
            if((piece == "wP" and end_row == 0) or (piece == "bP" and end_row == 7)):
                board.board[end_row][end_col] = piece[0] + "Q"

            if(self.get_king_pos == "1234"):
                board.board[start_row][start_col] = piece
                board.board[end_row][end_col] = swapped
                return False
            if(self.is_king_in_check(board, color)):
                board.board[start_row][start_col] = piece
                board.board[end_row][end_col] = swapped
                
                
                return False
            board.board[start_row][start_col] = piece
            board.board[end_row][end_col] = swapped

        else: 
            
            
            return False
        
        

        
        
        return True
    def is_valid_move(self, start_row, start_col, end_row, end_col, color, board):
        piece = board.board[start_row][start_col]
        if(piece[1] == "P"):
            if(color == "w"):
                
                if(board.board[end_row][end_col] == '' and start_row-end_row == 1 and start_col == end_col):
                    board.enPassantable = None
                    return True
                if(start_row == 6):
                    
                    if(board.board[end_row][end_col] == '' and board.board[end_row+1][end_col] == '' and start_row-end_row == 2 and start_col == end_col and start_row == 6):
                        board.enPassantable = end_col
                        return True
                if(board.board[end_row][end_col] != '' and start_row-end_row == 1 and (start_col - 1 == end_col or start_col + 1 == end_col)):
                    board.enPassantable = None
                    return True
                if end_row == start_row - 1 and abs(end_col - start_col) == 1 and board.board[end_row][end_col] == '' and end_col == board.enPassantable:
                    board.enPassantable = None
                    # board.board[start_row][end_col] = ''
                    return True
            elif(color == "b"):
                if(board.board[end_row][end_col] == '' and start_row-end_row == -1 and start_col == end_col):
                    board.enPassantable = None
                    return True
                if(start_row == 1):
                    if(board.board[end_row][end_col] == '' and board.board[end_row-1][end_col] == '' and start_row-end_row == -2 and start_col == end_col and start_row == 1):
                        board.enPassantable = end_col
                        return True
                if(board.board[end_row][end_col] != '' and start_row-end_row == -1 and (start_col - 1 == end_col or start_col + 1 == end_col)):
                    board.enPassantable = None
                    return True
                if end_row == start_row + 1 and abs(end_col - start_col) == 1 and board.board[end_row][end_col] == '' and end_col == board.enPassantable:
                    board.enPassantable = None
                    # board.board[start_row][end_col] = ''
                    return True
            
            return False
            
        elif(piece[1] == "N"):
            
            if(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 2):
                board.enPassantable = None
                return True
            elif(abs(start_row-end_row) == 2 and abs(start_col-end_col) == 1):
                board.enPassantable = None
                return True
            
            return False
        elif(piece[1] == "K"):
            if(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 1):
                
                board.enPassantable = None
                
                return True
            elif(abs(start_row-end_row) == 0 and abs(start_col-end_col) == 1):
                
                board.enPassantable = None
                
                return True
            elif(abs(start_row-end_row) == 1 and abs(start_col-end_col) == 0):
                
                board.enPassantable = None
                
                return True
            elif(start_col - end_col == 2 and start_row == end_row and start_row == 7 and board.wqCastle and color == "w"):
                
                for i in [0, 1, 2]:
                    opponent_color = 'b' if color == 'w' else 'w'
                    if(board.board[start_row][start_col - i]!= '' and i!= 0):
                        return False
                    for row in range(8):
                        for col in range(8):
                            piece = board.board[row][col]
                            if piece != '' and piece[0] == opponent_color:
                                if self.is_valid_move(row, col, start_row, start_col - i, opponent_color, board):
                                    return False
                
                
                return True
            elif(end_col - start_col == 2 and start_row == end_row and start_row == 7 and board.wkCastle and color == "w"):
                
                for i in [0, 1, 2]:
                    if(board.board[start_row][start_col + i] != '' and i!= 0):
                        
                        return False
                    opponent_color = 'b' if color == 'w' else 'w'
                    for row in range(8):
                        for col in range(8):
                            piece = board.board[row][col]
                            if piece != '' and piece[0] == opponent_color:
                                if self.is_valid_move(row, col, start_row, start_col + i, opponent_color, board):
                                    
                                    return False
                
                
                return True
            elif(start_col - end_col == 2 and start_row == end_row and start_row == 0 and board.bqCastle and color == "b"):
                for i in [0, 1, 2]:
                    opponent_color = 'b' if color == 'w' else 'w'
                    if(board.board[start_row][start_col - i] != '' and i!= 0):
                        return False
                    for row in range(8):
                        for col in range(8):
                            piece = board.board[row][col]
                            if piece != '' and piece[0] == opponent_color:
                                if self.is_valid_move(row, col, start_row, start_col - i, opponent_color, board):
                                    return False
                
                
                return True
            elif(end_col - start_col == 2 and start_row == end_row and start_row == 0 and board.bkCastle and color == "b"):
                for i in [0, 1, 2]:
                    if(board.board[start_row][start_col + i] != '' and i!= 0):
                        return False
                    opponent_color = 'b' if color == 'w' else 'w'
                    for row in range(8):
                        for col in range(8):
                            piece = board.board[row][col]
                            if piece != '' and piece[0] == opponent_color:
                                if self.is_valid_move(row, col, start_row, start_col + i, opponent_color, board):
                                    return False
               
                
                return True

            else:
                return False
        elif(piece[1] == "R"):
            if(start_row-end_row == 0):

                if(end_col - start_col >= 0):
                    for i in range(0, (end_col - start_col)):
                        if(board.board[start_row][start_col + i] != '' and i != 0 and i != (end_col - start_col)):
                            return False
                else:
                    for i in range(0, (start_col - end_col)):
                        if(board.board[start_row][start_col - i] != '' and i != 0 and i != (start_col - end_col)):
                            return False
            elif(start_col-end_col == 0):
                if(end_row - start_row >= 0):
                    for i in range(0, (end_row - start_row)):
                        if(board.board[start_row + i][start_col] != '' and i != 0 and i != (end_row - start_row)):
                            return False
                else:
                    for i in range(0, (start_row - end_row)):
                        if(board.board[start_row - i][start_col] != '' and i != 0 and i != (start_row - end_row)):
                            return False
            else:
                return False
                
            board.enPassantable = None
           


            return True
        elif(piece[1] == "B"):
            diffrow = end_row - start_row
            diffcol = end_col - start_col
            if(abs(diffrow) != abs(diffcol)):
                return False
            elif(diffrow >= 0 and diffcol >=0):
                for i in range(0, (diffcol)):
                    if(board.board[start_row + i][start_col + i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow <= 0 and diffcol <=0):
                for i in range(0, abs(diffcol)):
                    if(board.board[start_row - i][start_col - i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow >= 0 and diffcol <=0):
                for i in range(0, abs(diffcol)):
                    if(board.board[start_row + i][start_col - i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow <= 0 and diffcol >=0):
                for i in range(0, abs(diffcol)):
                    if(board.board[start_row - i][start_col + i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            board.enPassantable = None
            return True
        elif(piece[1] == "Q"):
            diffrow = end_row - start_row
            diffcol = end_col - start_col
            if(start_row-end_row == 0):

                if(end_col - start_col >= 0):
                    for i in range(0, (end_col - start_col)):
                        if(board.board[start_row][start_col + i] != '' and i != 0 and i != (end_col - start_col)):
                            return False
                else:
                    for i in range(0, (start_col - end_col)):
                        if(board.board[start_row][start_col - i] != '' and i != 0 and i != (start_col - end_col)):
                            return False
            elif(start_col-end_col == 0):
            
                if(end_row - start_row >= 0):
                    for i in range(0, (end_row - start_row)):
                        if(board.board[start_row + i][start_col] != '' and i != 0 and i != (end_row - start_row)):
                            return False
                else:
                    for i in range(0, (start_row - end_row)):
                        if(board.board[start_row - i][start_col] != '' and i != 0 and i != (start_row - end_row)):
                            return False
            
            elif(abs(diffrow) != abs(diffcol)):
                return False
            elif(diffrow >= 0 and diffcol >=0):
                for i in range(0, (diffcol)):
                    if(board.board[start_row + i][start_col + i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow <= 0 and diffcol <=0):
                for i in range(0, abs(diffcol)):
                    if(board.board[start_row - i][start_col - i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow >= 0 and diffcol <=0):
                for i in range(0, abs(diffcol)):
                    if(board.board[start_row + i][start_col - i] != '' and i != 0 and i != abs(diffcol)):
                        return False
            elif(diffrow <= 0 and diffcol >=0):
                for i in range(0, abs(diffcol)):
                    if(board.board[start_row - i][start_col + i] != '' and i != 0 and i != abs(diffcol)):
                        return False

            board.enPassantable = None
            return True
            
                
            

                
        else:
            return False

