
import pygame
import random
from MovesList import MovesList
from Board import Board
import copy

class TreeEngine:
    def __init__(self, depth):
        self.depth = depth
        self.list = MovesList()
        self.permeableboard = Board()


    def generate_move(self, board, color):
        copy_board = copy.deepcopy(board)
        initial = self.get_x_best_moves(copy_board, color, 5)
        print(initial)
        print("50%")
        if(color == "w"):
            othercolor = "b"
        else:
            othercolor = "w"
        movescores = []
        i = 0
        for move in initial:
            movescores.append(self.searchtree(copy_board, othercolor, move, 5))
            copy_board = copy.deepcopy(board)
            i += 1

        print(initial)
        print(movescores)
        
        if(color == "w"):
            return initial[movescores.index(max(movescores))]
        else:
            
            return initial[movescores.index(min(movescores))]


        
            
    def new_search_tree(self, board, color, initialMove, depth):
        copy_board = copy.deepcopy(board)
        if(depth == 0):
            return self.evaluate(board)
        if(color == "w"):
            othercolor = "b"
        else:
            othercolor = "w"



    def get_only_best_move(self, board, color):
        copy_board = copy.deepcopy(board) # create a copy of the board object
        self.permeableboard.board = copy_board.board
        if(color == "w"):
            othercolor = "b"
        else:
            othercolor = "w"
        depth = self.depth
        
        moves = self.list.get_legal_moves(copy_board, color)
        rand = random.randint(0,len(moves) - 1)
        bestboard = copy.deepcopy(self.Test_Move(moves[rand], copy_board))
        
        self.permeableboard.board = copy_board.board
        
        bestmove = moves[rand]
        for move in moves:
            if(color == "w"):
                
                if(self.evaluate(bestboard) < self.evaluate(self.Test_Move(move, copy_board))):
                    copy_board = copy.deepcopy(board)
                    
                    bestboard = self.Test_Move(move, copy_board)
                    copy_board = copy.deepcopy(board)
                    bestmove = move
            else:
                
                if(self.evaluate(bestboard) > self.evaluate(self.Test_Move(move, copy_board))):
                    copy_board = copy.deepcopy(board)
                    
                    bestboard = self.Test_Move(move, copy_board)
                    copy_board = copy.deepcopy(board)
                    
                    bestmove = move

        return bestmove

        

        
        
    def searchtree(self, board, color, initialMove, depth):
        copy_board = copy.deepcopy(board)
        if depth == 0:
            print("it gets here")
            return (self.get_best_move(copy_board, color)[0])
        if(color == "w"):
            othercolor = "b"
        else:
            othercolor = "w"

        newboard = copy.deepcopy(self.get_best_move(copy_board, color)[1])
        
        if(newboard == None):
            
            if(color == "b"):
                return 99999
            elif(color == "w"):
                return -99999
        return self.searchtree(newboard, othercolor, initialMove, depth - 1)

       
        


        
        
    def get_best_move(self, board, color):
        copy_board = copy.deepcopy(board)
        if(color == "w"):
            othercolor = "b"
        else:
            othercolor = "w"
        depth = self.depth
        moves = self.list.get_legal_moves(copy_board, color)
        copy_board = copy.deepcopy(board)
        good_moves = []
        boards = []
        i = 0
        for move in moves:
            boards.append(copy.deepcopy(self.Test_Move(move, copy_board)))
            copy_board = copy.deepcopy(board)
            i+=1
        boardscores = []
        i = 0
        for movedboard in boards:
            boardscores.append(self.evaluate(movedboard))
            if(self.list.get_legal_moves(movedboard, othercolor) == [] and self.list.is_king_in_check(movedboard, othercolor)):
                if color == "b":
                    
                    boardscores[i] = -999998
                else:
                    boardscores[i] = 9999999
            i+= 1
            
            
        i = 0
        bestnum = 0
        for score in boardscores:
            if(color == "w"):  
                if(score > boardscores[bestnum]):
                    bestnum = i
            else:
                if(score < boardscores[bestnum]):
                    bestnum = i
            i += 1

        if len(moves) == 0:
            
            return (0, None)
        
        
        return (boardscores[bestnum], boards[bestnum])
        
            
        
        
    def get_x_best_moves(self, board, color, x):
        copy_of_board = copy.deepcopy(board)
        if(color == "w"):
            othercolor = "b"
        else:
            othercolor = "w"
        depth = self.depth
        moves = self.list.get_legal_moves(copy_of_board, color)
        copy_of_board = copy.deepcopy(board)
        good_moves = []
        good_boards = []
        boards = []
        i = 0
        for move in moves: #generate boards to evaluate

            boards.append(self.get_best_move(self.Test_Move(move, copy_of_board), othercolor)[1])
            copy_of_board = copy.deepcopy(board)
            i+=1
        boardscores = []
        
        print(moves)
        i = 0
        for boardlist in boards: #evaluate boards
            if boardlist == None:
                if color == "b":
                    
                    boardscores[i] = -999999
                else:
                    boardscores[i] = 9999999
            else:
                boardscores.append(self.evaluate(boardlist))
                boardlist = copy.deepcopy(board)
                i+= 1
                if(self.list.get_legal_moves(boardlist, othercolor) == [] and self.list.is_king_in_check(boardlist, othercolor)):
                    if color == "b":
                        
                        boardscores[i] = -999999
                    else:
                        boardscores[i] = 9999999
                boardlist = copy.deepcopy(board)
        
        i = 0
        print(boardscores)
        bestnum = random.randint(0, len(moves) - 1)
        if(len(moves) < x):
            return moves
        while(len(good_moves) < x or len(good_moves) == len(moves)):
            
            i+= 1
            if(i == len(moves) - 1):
                i = 0
                good_moves.append(moves[bestnum])
                print(moves[bestnum])
                print(boardscores[bestnum])
                del moves[bestnum]
                del boardscores[bestnum]
                del boards[bestnum]
                bestnum = 0
                
            if(color == "w"):  
                if(boardscores[i] > boardscores[bestnum]):
                    bestnum = i
            else:
                if(boardscores[i] < boardscores[bestnum]):
                    
                    bestnum = i
        
        # return (good_moves,good_boards)
        return(good_moves)
        


        

    


    

    def dist_from_center(self, row, col):
        return abs(3.5 - row) + abs(3.5-col)

    def evaluate(self, board):
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if(piece == "wP"):
                    score +=100
                    # if(row == 4 and (col == 3 or col == 4)):
                    #     score += 20
                elif(piece == "bP"):
                    score -=100
                    # if(row == 3 and (col == 3 or col == 4)):
                    #     score += 20
                elif(piece == "wQ"):
                    score +=900
                elif(piece == "bQ"):
                    score -=900
                elif(piece == "wR"):
                    score +=500
                elif(piece == "bR"):
                    score -=500
                elif(piece == "wB" or piece == "wN"):
                    # score += 100 * (5 - self.dist_from_center(row, col))
                    score +=300
                elif(piece == "bB" or piece == "bN"):
                    # score -= 100 * (5 - self.dist_from_center(row, col))
                    score -=300

        
                    
        if(self.list.get_legal_moves(board, "b") == [] and self.list.is_king_in_check(board, "b")):
            score = 999999
        elif(self.list.get_legal_moves(board, "w") == [] and self.list.is_king_in_check(board, "w")):
            score = -999999
            
        
        return score
    def Test_Move(self, move, board):
        boardcopy = board
        start_col = ord(move[0]) - ord('a')
        start_row = 7 - (int(move[1]) - 1)
        end_col = ord(move[2]) - ord('a')
        end_row = 7- (int(move[3]) - 1)
        piece = boardcopy.board[start_row][start_col]
        if(start_row == 7 and start_col == 0):
            board.wqCastle = False
        if(start_row == 7 and start_col == 7):
            board.wkCastle = False
        if(start_row == 0 and start_col == 0):
            board.bqCastle = False
        if(start_row == 0 and start_col == 7):
            board.bkCastle = False
        boardcopy.board[start_row][start_col] = ''
        boardcopy.board[end_row][end_col] = piece
        if(piece=="wK"):
            board.wkCastle = False
            board.wqCastle = False
            
        if(piece == "bK"):
            board.bkCastle = False
            board.bqCastle = False

        if(piece=="wK" and move == "e1g1"):
            boardcopy.board[7][7] = ''
            boardcopy.board[7][5] = "wR"
        if(piece=="wK" and move == "e1c1"):
            boardcopy.board[7][0] = ''
            boardcopy.board[7][3] = "wR"
        
        if(piece=="bK" and move == "e8g8"):
            boardcopy.board[0][7] = ''
            boardcopy.board[0][5] = "wR"
        if(piece=="wK" and move == "e8c8"):
            boardcopy.board[0][0] = ''
            boardcopy.board[0][3] = "wR"
        return boardcopy
    