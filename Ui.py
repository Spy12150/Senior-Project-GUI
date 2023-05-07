
from turtle import color
import pygame
from Board import Board
from TreeEngine import TreeEngine
import time
from MovesList import MovesList
import random

# Set up the Pygame window
pygame.init()
WIDTH = HEIGHT = 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
HAZEL = (240, 217, 181)
BROWN = (181, 136, 99)

# Load chess piece images
images = {}
images["wK"] = pygame.transform.scale(pygame.image.load('data/imgs/wK.png'), (80, 80))
images["wQ"] = pygame.transform.scale(pygame.image.load('data/imgs/wQ.png'), (80, 80))
images["wR"] = pygame.transform.scale(pygame.image.load('data/imgs/wR.png'), (80, 80))
images["wB"] = pygame.transform.scale(pygame.image.load('data/imgs/wB.png'), (80, 80))
images["wN"] = pygame.transform.scale(pygame.image.load('data/imgs/wN.png'), (80, 80))
images["wP"] = pygame.transform.scale(pygame.image.load('data/imgs/wP.png'), (80, 80))
images["bK"] = pygame.transform.scale(pygame.image.load('data/imgs/bK.png'), (80, 80))
images["bQ"] = pygame.transform.scale(pygame.image.load('data/imgs/bQ.png'), (80, 80))
images["bR"] = pygame.transform.scale(pygame.image.load('data/imgs/bR.png'), (80, 80))
images["bB"] = pygame.transform.scale(pygame.image.load('data/imgs/bB.png'), (80, 80))
images["bN"] = pygame.transform.scale(pygame.image.load('data/imgs/bN.png'), (80, 80))
images["bP"] = pygame.transform.scale(pygame.image.load('data/imgs/bP.png'), (80, 80))

# Define the chess board
board = Board()
# Define the square size and font
SQUARE_SIZE = HEIGHT // 8
FONT = pygame.font.SysFont('calibri', 30)

scriptedmoves=[]
list = MovesList()

#  "c8g4", "g1f3", "b8c6", "d2d3", "e7e6", "c1g5", "f8b4", "b1c3", "g8f6"]

# Draw the chess board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = HAZEL if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.board[row][col]
            if piece != '':
                if piece != '':
                    img = images[piece]
                    img_x = col*SQUARE_SIZE + (SQUARE_SIZE-img.get_width())//2
                    img_y = row*SQUARE_SIZE + (SQUARE_SIZE-img.get_height())//2
                    win.blit(img, (img_x, img_y))


# Draw the coordinates on the board
def draw_coordinates():
    for i in range(8):
        text = FONT.render(str(8 - i), True, BLACK)
        win.blit(text, (5, i * SQUARE_SIZE + 10))

        text = FONT.render(chr(97 + i), True, BLACK)
        win.blit(text, (i * SQUARE_SIZE + 80, HEIGHT - 30))



# Main game loop
running = True

print("enter moves in the notation: e2e4 (start pos + end pos_")
turn = "w"
movenum = 0
randommove = TreeEngine(5)

while running:
    time.sleep(.02)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

     # Draw the board and pieces
    draw_board()
    draw_coordinates()

    # Check if the game is over
    pygame.display.update()
    
            

    
    Moved = False
    while(not Moved):
        moves = list.get_legal_moves(board, turn)
        if movenum < len(scriptedmoves):
            move = scriptedmoves[movenum]
            movenum += 1
            Moved = board.move(move, turn, moves)
        else:

            
            if(list.is_king_in_check(board, turn)):
                
                print(turn + "king in check")
                
            
            
            if(moves == [] and list.is_king_in_check(board, turn)):
                if turn == "b":
                    print("game is over by checkmate")
                    print("w" + " Wins!")
                else:
                    print("game is over by checkmate")
                    print("w" + " Wins!")
                running = False
                time.sleep(30)
            elif(moves == []):
                print("The game is a draw")
                running = False
                time.sleep(30)
            elif(list.is_stalemate(turn, moves, board)):
                print("The game is a draw")
                running = False
                time.sleep(30)

            if(turn == "b"):

                Moved = board.move(moves[random.randint(0, len(moves) - 1)], turn, moves)
            else:
                print("your legal moves are: ")
                print(moves)
                Moved = board.move(input("move in the manor of 'e2e4': "), turn, moves)
            
             
        
        
    movenum += 1
    if(turn == "w"):
        turn = "b"
    else:
        turn = "w"
    
    

    
   

pygame.quit()
