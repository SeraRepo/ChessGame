"""
This is our main driver file. It will be responsible for handling user input and displaying the current
GameState object.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512  # 400 works too
DIMENSION = 8  # Dimension of a chessboard are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For animation
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main 
'''


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(""
                                                       "images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # We can access an image by saying 'IMAGES['wp']


'''
The main driver for our code. This will handle user input and updating the graphics
'''


def main():
    p.init()

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()
    # print(gs.board)

    loadImages()  # only do this once, before the while loop
    running = True

    validMoves = gs.getValidMoves()
    #print(validMoves)
    moveMade = False #flag variable for when a move is made

    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of the mouse
                col = location[0] // SQ_SIZE  # get the column where the user clicked
                row = location[1] // SQ_SIZE  # get the row where the user clicked

                if sqSelected == (row, col):  # if the user click the same square twice only unselect the piece clicked
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                if len(playerClicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    #print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]


            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo if 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade: #Reset the list of valid moves when a move is done
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all the graphics within a current game state.
'''


def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, gs.board)  # draw pieces on top of the board


'''
Draw the squares on the board. The top left square is always light.
'''


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the current GameState.board
'''


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
