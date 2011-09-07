# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 16:10:22 2011

@author: pmaurier
"""

import time
import random
import pygame
import sys
from pygame.locals import *

# Game infos
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BLOCKSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = -1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BLOCKSIZE) / 2)
TOPOFBOARD = WINDOWHEIGHT - (BOARDHEIGHT * BLOCKSIZE) - 5

MOVESIDEWAYSFREQ = 0.15


# Some basic colors
#            R    G    B
WHITE =    (255, 255, 255)
BLACK =    (0,     0,   0)
RED =      (155,   0,   0)
GREEN =    (0,   155,   0)
BLUE =     (0,     0, 155)
YELLOW =   (155, 155,   0)
DARKGRAY = (40,   40,  40)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
COLORLIST = (BLUE, GREEN, RED, YELLOW)
colors = COLORLIST[0:3]

# Pieces definition
S_PIECE = [['.....',
            '.....',
            '..01.',
            '.23..',
            '.....'],
           ['.....',
            '..2..',
            '..30.',
            '...1.',
            '.....'],
           ['.....',
            '.....',
            '..32.',
            '.10..',
            '.....'],
           ['.....',
            '..1..',
            '..03.',
            '...2.',
            '.....']]

Z_PIECE = [['.....',
            '.....',
            '.01..',
            '..23.',
            '.....'],
           ['.....',
            '..0..',
            '.21..',
            '.3...',
            '.....'],
           ['.....',
            '.....',
            '.32..',
            '..10.',
            '.....'],
           ['.....',
            '..3..',
            '.12..',
            '.0...',
            '.....']]

I_PIECE = [['..0..',
            '..1..',
            '..2..',
            '..3..',
            '.....'],
           ['.....',
            '.....',
            '3210.',
            '.....',
            '.....'],
           ['..3..',
            '..2..',
            '..1..',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '0123.',
            '.....',
            '.....']]

O_PIECE = [['.....',
            '.....',
            '.01..',
            '.23..',
            '.....'],
           ['.....',
            '.....',
            '.20..',
            '.31..',
            '.....'],
           ['.....',
            '.....',
            '.32..',
            '.10..',
            '.....'],
           ['.....',
            '.....',
            '.13..',
            '.02..',
            '.....']]

J_PIECE = [['.....',
            '.0...',
            '.123.',
            '.....',
            '.....'],
           ['.....',
            '..10.',
            '..2..',
            '..3..',
            '.....'],
           ['.....',
            '.....',
            '.321.',
            '...0.',
            '.....'],
           ['.....',
            '..3..',
            '..2..',
            '.01..',
            '.....']]

L_PIECE = [['.....',
            '...0.',
            '.123.',
            '.....',
            '.....'],
           ['.....',
            '..1..',
            '..2..',
            '..30.',
            '.....'],
           ['.....',
            '.....',
            '.321.',
            '.0...',
            '.....'],
           ['.....',
            '.03..',
            '..2..',
            '..1..',
            '.....']]

T_PIECE = [['.....',
            '..0..',
            '.123.',
            '.....',
            '.....'],
           ['.....',
            '..1..',
            '..20.',
            '..3..',
            '.....'],
           ['.....',
            '.....',
            '.321.',
            '..0..',
            '.....'],
           ['.....',
            '..3..',
            '.02..',
            '..1..',
            '.....']]
            
PIECES = {'S': S_PIECE,
          'Z': Z_PIECE,
          'J': J_PIECE,
          'L': L_PIECE,
          'I': I_PIECE,
          'O': O_PIECE,
          'T': T_PIECE}

# The following lines changes piece[y][x] convention into more common piece[x][y] convention
for p in PIECES: # loop through each piece
    for i in range(len(PIECES[p])): # loop through each rotation of the piece
        shapeData = []
        for x in range(5): # loop through each column of the rotation of the piece
            column = []
            for y in range(5): # loop through each character in the column of the rotation of the piece
                if PIECES[p][i][y][x] == '.':
                    column.append(BLANK)
                else:
                    column.append(int(PIECES[p][i][y][x]))
            shapeData.append(column)
        PIECES[p][i] = shapeData

def main():
    global MAINCLOCK, MAINSURF, BASICFONT
    pygame.init()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    MAINCLOCK = pygame.time.Clock()
    MAINSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Color Compressor')
    
    while True:
        gameloop()

def terminate():
    pygame.quit()
    sys.exit()

def gameloop():
    board = getNewBoard()
    
    lastMoveSidewaysTime = time.time() #Last time when a piece was moved
    lastPushTime = time.time() #Last time when a piece was pushed
    lastFallTime = time.time() #Last time when the line as moved
    
    # Flags for moving pieces when holding the arrow keys    
    movingLeft = False
    movingRight = False  
    
    # Frequency of the push of the piece
    level = 0
    score = 0
    pushfreq = 4-(level*0.25)
    fallfreq = pushfreq/(BOARDHEIGHT*1.5)
    
    currentPiece = getNewPiece()
    currentHeight = 0
    nextPiece = getNewPiece()
    
    pushing = False
    
    while True:
        if (currentPiece == None) and currentHeight > 5:
            currentPiece = nextPiece
            nextPiece = getNewPiece()
#            lastPushTime = time.time()
            
            # No space for a new piece ?
            if not isValidPosition(board, currentPiece):
                break # game over
            
        # handle any input from the player
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
            elif event.type == KEYUP:
                if (event.key == K_LEFT):
                    movingLeft = False
                if (event.key == K_RIGHT):
                    movingRight = False
                    
            elif event.type == KEYDOWN:
                # moving the block sideways  
                if currentPiece != None:
                    if (event.key == K_LEFT) and isValidPosition(board, currentPiece, adjX=-1):
                        currentPiece['x'] -= 1
                        lastMoveSidewaysTime = time.time()
                        movingLeft = True
                        movingRight = False
                        lastMoveSidewaysTime = time.time()
                    if (event.key == K_RIGHT) and isValidPosition(board, currentPiece, adjX=1):
                        currentPiece['x'] += 1
                        movingRight = True
                        movingLeft = False
                        lastMoveSidewaysTime = time.time()

                # rotating the block (if allowed)
                if (event.key == K_UP) and (currentPiece != None):
                    currentPiece['rotation'] = (currentPiece['rotation'] + 1) % len(PIECES[currentPiece['shape']])
                    if not isValidPosition(board, currentPiece):
                        currentPiece['rotation'] = (currentPiece['rotation'] - 1) % len(PIECES[currentPiece['shape']])
                    
                if event.key == K_ESCAPE:
                    terminate()
                    
        # handle moving the block
        if currentPiece != None:
            if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
                if movingLeft and isValidPosition(board, currentPiece, adjX=-1):
                    currentPiece['x'] -= 1
                if movingRight and isValidPosition(board, currentPiece, adjX=1):
                    currentPiece['x'] += 1
                lastMoveSidewaysTime = time.time()
        
        # Push piece if it is time to
        if time.time() - lastPushTime > pushfreq:
            pushing = True
            lastPushTime = time.time()
            
        if (time.time() - lastFallTime > fallfreq) and pushing:
            score += deleteBlocks(board)
            lastFallTime = time.time()
            if hasHitBottom(board, currentHeight):
                currentHeight = 0
#                currentPiece = None
#                lastPushTime = time.time()
                pushing = False
            else:
                if currentHeight <= 5:
                    if currentPiece != None:
                        addToBoard(board, currentPiece)
                        currentPiece = None
                currentHeight += 1
                push(board, currentHeight)

            
        # drawing everything on the screen
        MAINSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if currentPiece != None:
            drawPiece(currentPiece)
        drawLine(currentHeight)
        
        pygame.display.update()
        MAINCLOCK.tick(FPS)

def getNewBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    """When generating a new random piece, first we randomly decide on which shape to use for the new piece. The keys() dictionary method will return a list of all the key values in the dictionary."""
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - 2,
                'y': 0,
                'color': [random.randint(0, len(colors)-1) for a in xrange(4)]}
    return newPiece

def addToBoard(board, piece):
    # fill in the spots on the board based on piece's location, shape, and rotation
    """Once the piece has landed, it needs to be added to the board's data structure. Using nested loops, we go through each of the 25 block spaces in the 5x5 data structure of the piece, and then add it to the corresponding spot on the board."""   
    for x in range(5):
        for y in range(5):
            if PIECES[piece['shape']][piece['rotation']][x][y] != BLANK:
                """Note that PIECES is the large global dictionary that contains all the piece data. piece['shape'] stores the letter that corresponds to the piece type (such as 'S' or 'J'), so PIECES[piece['shape']] returns a list of all the different rotations of that shape. piece['rotation'] contains the index in this list of the specific rotation of a shape.
                So PIECES[piece['shape']][piece['rotation']] contains a value such as this one (remember, -1 (the value in the BLANK constant) represents a blank spot and a 1 value represents a filled spot:

               [[-1, -1, -1, -1, -1],
                [-1,  1,  1, -1, -1],
                [-1, -1,  1,  1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1]]

                (This is after we transformed the block data from this value:)
               ['.....',
                '.OO..',
                '..OO.',
                '.....',
                '.....']

                Then the [x][y] indexes after it get the particular character in this data. If this value is BLANK, the the code continues on. Otherwise, the color integer of the piece is written to the corresponding xy coordinate on the board."""
                board[x + piece['x']][y + piece['y']] = piece['color'][PIECES[piece['shape']][piece['rotation']][x][y]]
                """The actual value that is added to the board is an integer representing the piece's color."""

def push(board, height):
    for x in range(BOARDWIDTH):
        if not isCompleteColumn(board, x, height):
            if board[x][height-1] != BLANK:
                prev = board[x][height-1]
                board[x][height-1] = BLANK
                for y in range(height, BOARDHEIGHT): 
                    next = board[x][y]
                    board[x][y] = prev
                    prev = next
                    if prev == BLANK:
                        break
    return True
                    

def hasHitBottom(board, height):
    if height == BOARDHEIGHT:
        return True
    else:
        # Returns True if one column is full under a certain height    
        for x in range(BOARDWIDTH):
            if isCompleteColumn(board, x, height):
                return True
        return False

def isCompleteColumn(board, x, height):
    # Return True if the xth column from the position of the line is filled with blocks with no gaps.
    for y in range(height, BOARDHEIGHT):
        if board[x][y] == BLANK:
            return False
    return True

def isOnBoard(x, y):
    # Returns True if the xy coordinates point to a block space that is on the board, and returns False if they are outside of the board.
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding with any blocks on the board.
    for x in range(5):
        for y in range(5):
            if y + piece['y'] + adjY < 0 or PIECES[piece['shape']][piece['rotation']][x][y] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def deleteBlocks(board):
    global groupes, visites
    groupes = []
    visites = []
    for i in range(BOARDWIDTH):
        visites.append([False] * BOARDHEIGHT)
    
    # Check all blocks
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if (not visites[i][j]) and (board[i][j] != BLANK):
                groupes.append([])
                visite(board, i, j)

    #On enlève les doubles de chaque groupe
    for i in xrange(len(groupes)):
        groupe = groupes[i]
        groupe2 = []
        for elt in groupe:
            try:
                ind = groupe2.index(elt)
            except:
                groupe2.append(elt)
        groupes[i] = groupe2
    
    score = 0
    for group in groupes:
        nombre = len(group)
        if nombre >= 4:
            for coord in group:
                board[coord[0]][coord[1]] = BLANK
            score += 150+(50*(nombre-4))
    return score

def visite(board, i, j):
    global groupes, visites
    groupes[-1].append([i,j])
    if visites[i][j] == False:
        visites[i][j] = True
        if i+1 < BOARDWIDTH:
            if not (board[i+1][j] == BLANK):
                if board[i][j] == board[i+1][j]:
                    visite(board,i+1,j)
        if i-1 >= 0:
            if not (board[i-1][j] == BLANK):
                if board[i][j] == board[i-1][j]:
                    visite(board,i-1,j)
        if j+1 < BOARDHEIGHT:
            if not (board[i][j+1] == BLANK):
                if board[i][j] == board[i][j+1]:
                    visite(board,i,j+1)
        if j-1 >= 0:
            if not (board[i][j-1] == BLANK):
                if board[i][j] == board[i][j-1]:
                    visite(board,i,j-1)

def convertToPixelCoords(x, y):
    # Convert the given xy coordinates of the board to xy coordinates of the location on the screen.
    return (XMARGIN + (x * BLOCKSIZE)), (TOPOFBOARD + (y * BLOCKSIZE))

def drawBoardBorder():
    # draw the border around the board
    pygame.draw.rect(MAINSURF, BORDERCOLOR, (XMARGIN - 3, TOPOFBOARD - 7, (BOARDWIDTH * BLOCKSIZE) + 8, (BOARDHEIGHT * BLOCKSIZE) + 8), 5)

def drawBoard(board):
    drawBoardBorder()
    # fill the background of the board
    pygame.draw.rect(MAINSURF, BGCOLOR, (XMARGIN, TOPOFBOARD, BLOCKSIZE * BOARDWIDTH, BLOCKSIZE * BOARDHEIGHT))
    # draw the individual blocks on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] != BLANK:
                pixelx, pixely = convertToPixelCoords(x, y)
                pygame.draw.rect(MAINSURF, colors[board[x][y]], (pixelx+1, pixely+1, BLOCKSIZE-1, BLOCKSIZE-1))

def drawPiece(piece, customCoords=(None, None)):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if customCoords == (None, None):
        # if customCoords hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
    else:
        pixelx, pixely = customCoords

    # draw each of the blocks that make up the piece
    for x in range(5):
        for y in range(5):
            if shapeToDraw[x][y] != BLANK:
                pygame.draw.rect(MAINSURF, colors[piece['color'][shapeToDraw[x][y]]], (pixelx + (x * BLOCKSIZE) + 1, pixely + (y * BLOCKSIZE) + 1, BLOCKSIZE-1, BLOCKSIZE-1))

def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, WHITE)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    MAINSURF.blit(nextSurf, nextRect)

    drawPiece(piece, customCoords=(WINDOWWIDTH-120, 100))

def drawLine(y):
    pixelx, pixely = convertToPixelCoords(0, y-1)
    for x in range(BOARDWIDTH):
        pygame.draw.rect(MAINSURF, DARKGRAY, (pixelx + (x * BLOCKSIZE), pixely, BLOCKSIZE, BLOCKSIZE))
        
def drawStatus(score, level):
    # draw the score text
    """The code to render and draw the text is similar to the code in showTextScreen(), except here we do it to display the current score and level that the player is on."""
    scoreSurf = BASICFONT.render('Score: %s' % score, True, WHITE)
    scoreRect = scoreSurf.get_rect()

    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    MAINSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, WHITE)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    MAINSURF.blit(levelSurf, levelRect)
    
if __name__ == '__main__':
    main()
