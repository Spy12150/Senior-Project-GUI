import pygame
import random
from MovesList import MovesList
from Board import Board
import copy
import time
from TranspositionTable import TranspositionTable
import tensorflow as tf
import numpy as np
class bob:
    def __init__(self, depth):
        self.depth = depth
        self.list = MovesList()
        self.transposition_table = TranspositionTable()
        self.model = tf.keras.models.load_model('blobfish1.12.h5')
        self.converter = ChessConverter()
        self.moves = 0
        self.guess = tf.keras.models.load_model('guesser1.h5')

    def get_best_move(self, board, color):
        moves = self.list.get_legal_moves(board, color)
        n = len(moves)
        i = 0
        self.moves += 1

        if color == "w":
            best_move = None
            max_evaluation = -float('inf')
            alpha = -float('inf')
            beta = float('inf')

            aiMove = self.AImove(board, color)
            if(aiMove in moves):
                return aiMove

            for move in moves:
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                if (self.list.get_legal_moves(boardcopy, "b") == [] and self.list.is_king_in_check(boardcopy, "b")):
                    return move
                if self.piecesonboard(boardcopy) < 4:
                    evaluation = self.minimax(boardcopy, 6, "b", alpha, beta)
                else:
                    evaluation = self.minimax(boardcopy, 1, "b", alpha, beta)
                i += 1
                print(f"\rProgress: {(i/n)*100}%", end='')

                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    best_move = move

                alpha = max(alpha, max_evaluation)

                if beta <= alpha:
                    break

            return best_move
        else:
            best_move = None
            min_evaluation = float('inf')
            alpha = -float('inf')
            beta = float('inf')
            aiMove = self.AImove(board, color)
            if(aiMove in moves):
                return aiMove
            

            for move in moves:
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                if (self.list.get_legal_moves(boardcopy, "w") == [] and self.list.is_king_in_check(boardcopy, "w")):
                    return move

                if self.piecesonboard(boardcopy) < 4:
                    evaluation = self.minimax(boardcopy, 6, "w", alpha, beta)
                else:
                    evaluation = self.minimax(boardcopy, 1, "w", alpha, beta)

                i += 1
                print(f"\rProgress: {(i/n)*100}%", end='')

                if evaluation < min_evaluation:
                    min_evaluation = evaluation
                    best_move = move

                beta = min(beta, min_evaluation)

                if beta <= alpha:
                    break

            return best_move

        
    
    def AIevaluate(self, board, color):
        fen = self.transposition_table.board_to_fen(board, color)
        input_data = np.array([int(j) for j in (self.converter.boardtofen(fen))])
        input_data = np.reshape(input_data, (-1, 449))
        predictions = self.model.predict(input_data, verbose = 0)

        return predictions
    
    def AImove(self, board, color):
        fen = self.transposition_table.board_to_fen(board, color)
        input_data = np.array([int(j) for j in (self.converter.boardtofen(fen))])
        input_data = np.reshape(input_data, (-1, 449))
        predictions3 = self.guess.predict(input_data)
        rounded_predictions = tf.round(predictions3)
        move = tf.cast(rounded_predictions, dtype=tf.int32)

        # Access the individual elements of the NumPy array
        start_col = chr(ord('a') + int(move[0, 0]))
        start_row = str(8 - int(move[0, 1]))
        end_col = chr(ord('a') + int(move[0, 2]))
        end_row = str(8 - int(move[0, 3]))

        # Combine the elements to form the move in algebraic notation
        algebraic_move = start_col + start_row + end_col + end_row

        return str(algebraic_move)


    def minimax(self, board, depth, color, alpha, beta):
        board = board
        if color == "w":
            otherplayer = "b"
        else:
            otherplayer = "w"
        tt_entry = self.transposition_table.lookup(board, color)
        if tt_entry is not None and tt_entry[1] >= depth:
            return tt_entry[0]

        legalmoves = self.list.get_legal_moves(board, color)

        if len(legalmoves) == 0 and self.list.is_king_in_check(board, color):
            if color == "w":
                return -9999999
            else:
                return 9999999

        if depth == 0 or len(legalmoves) == 0:
            return self.AIevaluate(board, color)

        if color == "w":
            max_evaluation = -float('inf')
            for move in legalmoves:
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                evaluation = self.minimax(boardcopy, depth - 1, "b", alpha, beta)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, max_evaluation)

                if beta <= alpha:
                    break
            
                self.transposition_table.store(board, max_evaluation, depth, color)

            return max_evaluation
        else:
            min_evaluation = float('inf')
            for move in legalmoves:
                boardcopy = self.Test_Move(move, copy.deepcopy(board))
                evaluation = self.minimax(boardcopy, depth - 1, "w", alpha, beta)
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, min_evaluation)

                if beta <= alpha:
                    break
                self.transposition_table.store(board, min_evaluation, depth, color) 
            return min_evaluation

    def piecesonboard(self, board):
        pieces = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if(piece != ''):
                    pieces +=1

        return pieces

    def evaluate(self, board):

        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if(piece == "wP"):
                    score += pawnEvalWhite[row][col]
                    score+= 100
                elif(piece == "bP"):
                    score -= pawnEvalBlack[row][col]
                    score -= 100
                elif(piece == "wQ"):
                    score += queenEval[row][col]
                    score +=900
                elif(piece == "bQ"):
                    score -= queenEval[row][col]
                    score -=900
                elif(piece == "wR"):
                    score += rookEvalWhite[row][col]
                    score +=500
                elif(piece == "bR"):
                    score -=  rookEvalBlack[row][col]
                    score -=500
                elif(piece == "wB"):
                    score += bishopEvalWhite[row][col]
                    score +=300
                elif(piece == "wN"):
                    score += knightEval[row][col]
                    score +=300
                elif(piece == "bB"):
                    score -= bishopEvalBlack[row][col]
                    score -= 300
                elif(piece == "bN"):
                    score -= knightEval[row][col]
                    score -=300
                elif(piece == "wK"):
                    if(self.piecesonboard(board) < 9):
                        score += kingEvalEndGameWhite[row][col]
                    else:
                        score += kingEvalWhite[row][col]
                elif(piece == "bK"):
                    if(self.piecesonboard(board) < 9):
                        score -= kingEvalEndGameBlack[row][col]
                    else:
                        score -= kingEvalBlack[row][col]

        
                    
        if(self.list.get_legal_moves(copy.deepcopy(board), "b") == [] and self.list.is_king_in_check(copy.deepcopy(board), "b")):
            score = 999999
        elif(self.list.get_legal_moves(copy.deepcopy(board), "w") == [] and self.list.is_king_in_check(copy.deepcopy(board), "w")):
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
pawnEvalBlack = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, -20, -20, 10, 10,  5],
    [5, -5, -10,  10,  10, -10, -5,  5],
    [0,  -10,  -10, 20, 20,  -10,  -10,  0],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [500, 500, 500, 500, 500, 500, 500, 500]
]
pawnEvalWhite = list(reversed(pawnEvalBlack))

knightEval = [
    [-50, -20, -30, -30, -30, -30, -20, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -20, -30, -30, -30, -30, -20, -50]
]

bishopEvalBlack = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]
bishopEvalWhite = list(reversed(bishopEvalBlack))

rookEvalBlack = [
    [0, 0, 0, 5, 5, 0, 0, 0],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
rookEvalWhite = list(reversed(rookEvalBlack))

queenEval = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

kingEvalBlack = [
    [20, 30, 10, 0, 0, 10, 30, 20],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, -30, -30, -40, -40, -30, -30, -20],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30]
]
kingEvalWhite = list(reversed(kingEvalBlack))

kingEvalEndGameBlack = [
    [50, -30, -30, -30, -30, -30, -30, -50,],
    [-30, -30,  0,  0,  0,  0, -30, -30,],
    [-30, -10, 20, 30, 30, 20, -10, -30,],
    [-30, -10, 30, 40, 40, 30, -10, -30,],
    [-30, -10, 30, 40, 40, 30, -10, -30,],
    [-30, -10, 20, 30, 30, 20, -10, -30,],
    [-30, -20, -10,  0,  0, -10, -20, -30,],
    [-50, -40, -30, -20, -20, -30, -40, -50]
]
kingEvalEndGameWhite = list(reversed(kingEvalEndGameBlack))
# fmt: on

class ChessConverter:
    @staticmethod
    def boardtofen(fen):
        binary = ''
        for element in fen:
            if(element == "P"):
                binary += "0100000"
            elif(element == "R"):
                binary += "0010000"
            elif(element == "N"):
                binary += "0001000"
            elif(element == "B"):
                binary += "0000100"
            elif(element == "Q"):
                binary += "0000010"
            elif(element == "K"):
                binary += "0000001"
            elif(element == "p"):
                binary += "1100000"
            elif(element == "r"):
                binary += "1010000"
            elif(element == "n"):
                binary += "1001000"
            elif(element == "b"):
                binary += "1000100"
            elif(element == "q"):
                binary += "1000010"
            elif(element == "k"):
                binary += "1000001"

            elif(element == "1"):
                binary += "0000000"
            elif(element == "2"):
                binary += "0000000"
                binary += "0000000"
                
            elif(element == "3"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "4"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "5"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "6"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                
            elif(element == "7"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "8"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "w"):
                binary += "0"
            elif(element == "b"):
                binary += "1"

        return binary[:449]
    
    def result_to_binary(self, result):
        if(result == "1-0"):
            return 1
        elif(result == "0-1"):
            return -1
        else:
            return 0