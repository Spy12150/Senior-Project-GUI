import numpy as np
import sys

import tensorflow as tf

# convert a piece to a dim 7 one hot vector defined by the piece map
#
# there is an additional flag that indicates whether or not this piece is white
# in order for the machine learning model to better determine what the next move is
# you can flip this entry to indicate if the piece is owned by whose turn it is
def pieceToVector(piece: str, isBlackTurn: bool = False):
    pieceMap = {
        "r": 0,
        "n": 1,
        "b": 2,
        "q": 3,
        "k": 4,
        "p": 5
    }

    vector = np.zeros(7)
    vector[pieceMap[piece.lower()]] = 1

    if ((not isBlackTurn) and piece.isupper()) or (isBlackTurn and piece.islower()):
        vector[6] = 1

    return vector

# convert board fen to 8x8x7 matrix 
# where a piece is given by a dim 7 vector defined in "piece to vector"
#
# additionally in order to distinguish whose turn it is there is an additional flag in the piece vector 
# that defines whether that piece is (1) or is not (0) owned by the player whose turn it currently is
def fenToMatrix(fen: str, isBlackTurn: bool = False):
    matrix = np.zeros((8,8,7))
    x = 0
    y = 0
    for char in fen:
        if char.isnumeric():
            x += int(char)
        elif char == "/":
            x = 0
            y += 1
        elif char == " ":
            break
        else:
            matrix[x,y,:] = pieceToVector(char, isBlackTurn)
            x += 1
    return matrix

@tf.function
def moveIndexToMoveCoord(index):
    fromIndex = index // 64
    toIndex = index % 64

    fromX = fromIndex % 8
    fromY = fromIndex // 8

    toX = toIndex % 8
    toY = toIndex // 8

    return tf.stack([fromX,fromY,toX,toY])


# converts the 64*64 dim one hot move vector to "to" and "from" move coordinates on an 8x8 grid
@tf.function
def movePredictionToMoveList(oneHotVector):
    maxEntry = tf.reduce_max(oneHotVector)

    moves = tf.where(oneHotVector > maxEntry/2)

    return tf.map_fn(moveIndexToMoveCoord, moves)

@tf.function
def dotRowElement(row):
    dotVec = tf.constant([1.0,1.0,1.0,1.0,1.0,1.0,-1.0], dtype=tf.float64)
    return tf.map_fn(lambda e: tf.tensordot(e,dotVec,axes = 1), row)


boardVariable = tf.Variable(tf.zeros((8,8,7), dtype= tf.float64))

# flips all white pieces to black pieces and black pieces to white pieces. 
# this is used to determine whose turn it is
@tf.function
def flipBoard(boardMatrix):
    ownershipFlip = tf.map_fn(dotRowElement, boardMatrix)

    boardVariable.assign(boardMatrix)
    boardVariable[:,:,6].assign(ownershipFlip)

    return tf.convert_to_tensor(boardVariable)

@tf.function
def preformMove(board, move):
    xFrom = move[0,0]
    yFrom = move[1,0]
    xTo = move[2,0]
    yTo = move[3,0]

    piece = board[xFrom,yFrom,:]

    boardVariable.assign(board)

    boardVariable[xFrom,yFrom,:].assign(tf.zeros(7, dtype= tf.float64))
    boardVariable[xTo,yTo].assign(piece)

    # flip the board so it is in the perspective of the next player
    ownershipFlip = tf.map_fn(dotRowElement, tf.convert_to_tensor(boardVariable))
    boardVariable[:,:,6].assign(ownershipFlip)

    return tf.convert_to_tensor(boardVariable)



class AndersBot:


    def __init__(self, depth):
        self.depth = depth
        self.evalModel = tf.keras.models.load_model("anders_bot/evaluator.h5")
        self.moveGenerator = tf.keras.models.load_model("anders_bot/movePredictor.h5")


    def depthSearch(self,board,depth,isBlackTurn):

        if depth <= 0:
            if isBlackTurn:
                board = flipBoard(board)
            return self.evalModel.predict(np.array([board]))[0]
    
        moves = movePredictionToMoveList(
            self.moveGenerator.predict(np.array([board]))[0]
        )


        # should filter moves for those that are valid
        evaluatedMoves = tf.map_fn(
            lambda move: self.depthSearch(preformMove(board,move),depth-1,not isBlackTurn),
            moves
        )

        if isBlackTurn:
            return tf.reduce_min(evaluatedMoves)
        else:
            return tf.reduce_max(evaluatedMoves)




    def getUciMove(self, board, move, turn):
        letterCoords = "abcdefgh"
        xFrom = tf.get_static_value(move[0,0])
        yFrom = tf.get_static_value(move[1,0])
        xTo = tf.get_static_value(move[2,0])
        yTo = tf.get_static_value(move[3,0])

        try: 
            if board.is_valid_move(7 - yFrom,xFrom,7 - yTo,xTo,turn):
                return letterCoords[xFrom] + str(yFrom + 1) + letterCoords[xTo] + str(yTo + 1)
            else:
                return None
        except:
            print("move validation failed")
            print([xFrom,yFrom,xTo,yTo])
            print(letterCoords[xFrom] + str(yFrom + 1) + letterCoords[xTo] + str(yTo + 1))




    def backup(self, board, turn ):
        print("failed to be smart, choosing first legal move")
        return board.get_legal_moves(turn)[0]



    def get_best_move(self,board, turn):

        isBlackTurn = turn == "b"
        boardMatrix = fenToMatrix(board.toFen(), isBlackTurn)

        moves = movePredictionToMoveList(
            self.moveGenerator.predict(np.array([boardMatrix]))[0]
        )

        if moves.shape[0] == 1:
            move = moves[0]

            uci = self.getUciMove(board,move,turn)

            return uci if uci is not None else self.backup(board,turn)
            
        evaluatedMoves = tf.map_fn(
            lambda move: self.depthSearch(preformMove(boardMatrix,move),self.depth,not isBlackTurn),
            moves
        )

        maxToMin = tf.argsort(evaluatedMoves)
        
        adjustment = -1 if isBlackTurn else 1

        length = len(maxToMin)

        index = length -1 if isBlackTurn else 0

        while(index < length and index >= 0):
            arg = maxToMin[index]
            print(arg)
            move = moves[arg]
            uci = self.getUciMove(board,move,turn)

            if uci:
                return uci

            index += adjustment

        return self.backup(board, turn)



        


            
            
        


        
        




