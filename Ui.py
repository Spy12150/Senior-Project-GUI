from ast import Import
import pygame
from Board import Board

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

while running:
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
         move = str(input("what move do you want to make: "))
         Moved = board.move(move, turn)
        
    
    if(turn == "w"):
        turn = "b"
    else:
        turn = "w"

    if (board.is_checkmate(turn)):
        print("Game over by checkmate")
        running = False

    print("turn: ")
    print(turn)
   

pygame.quit()
