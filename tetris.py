# imports
from cmu_graphics import *
import math
import random

# Model
def onAppStart(app):
    # the on appStart function initializes the entire app/game.
    
    #game data
    app.background = 'snow'
    
    #Creates the full sized tetris board, 15x10
    app.rows = 15
    app.cols = 10
    
    app.boardLeft = 95
    app.boardTop = 50
    app.boardWidth = 210
    app.boardHeight = 280
    app.cellBorderWidth = 2
    app.board = [[None]*app.cols for row in range(app.rows)]
    app.pieceLeftCol = 0
    app.pieceTopRow = 0
    loadTetrisPieces(app)
    loadPiece(app, random.randrange(len(app.tetrisPieces)))
    
    app.home = True
    app.pause = True
    app.game = False
    app.gameOver = False
    app.step = 0
    app.score = 0
    
    app.slow = False


def loadTetrisPieces(app):
    # initializes tetris pieces and their respective colors
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'aqua', 'aquamarine', 'darkturquoise', 'lime',
                              'lightseagreen', 'mediumspringgreen', 'turquoise']
    #initializes a random piece for the first piece
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))


def loadPiece(app, pieceIndex):
    # loads tetris piece from list of the pieces
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    app.pieceLeftCol = app.cols // 2 - math.ceil(len(app.piece[0]) / 2)
    app.pieceTopRow = 0

def loadNextPiece(app):
    # loads the next tetris piece for the game
    #Randomized Pieces
    loadPiece(app, app.nextPieceIndex)
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))


def rotate2dListClockwise(L):
    # This rotates a 2dList clockwise using a 2dLoop, and this is important
    # for rotating the pieces clockwise
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = [[None for i in range(newCols)] for j in range(newRows)]
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow = oldCol
            newCol = oldRows - oldRow - 1
            M[newRow][newCol] = L[oldRow][oldCol]
    return M

def rotate2dListCounterClockwise(L):
     # This rotates a 2dList counter-clockwise using a 2dLoop, and this is important
    # for rotating the pieces counter-clockwise
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = [[None for i in range(newCols)] for j in range(newRows)]
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow = oldCols - oldCol - 1
            newCol = oldRow
            M[newRow][newCol] = L[oldRow][oldCol]
    return M
    
# view

def redrawAll(app):
    # The view: redraws the entire app
    if app.home:
        drawLabel('Tetris', 200, 30, size=30)
        drawLabel('use arrow keys to navigate the pieces', 200, 80, size=16)
        drawLabel('use Z and X to rotate pieces respectively', 200, 120, size=16)
        drawLabel('Press down to soft drop, press space to hard drop',
                200, 150, size=16)
        drawLabel('Holding up slows down the fall', 200, 180, size=16)

        drawLabel('press P to pause game, press G to start', 200, 200, size=16)
    
    #Game over screen, tells the player to press r to restart and
    #displays score
    elif app.gameOver:
        drawLabel('Game Over!', 200, 30, size=16)
        drawLabel(f'Your score was {app.score}', 200, 60, size = 20)
        drawLabel('Press R to Restart!, Goodluck', 200, 80, size = 20)


    elif app.game:
        drawLabel('Tetris', 200, 30, size=16)
        drawLabel(f'Score: {app.score}', 200, 340, size=16)
        drawBoard(app)
        drawPiece(app)
        drawBoardBorder(app)
        
    elif app.pause and not app.gameOver:
        drawLabel('Game Paused!', 200, 30, size=16)
        drawLabel('use arrow keys to navigate the pieces', 200, 80, size=16)
        drawLabel('use Z and X to rotate pieces respectively', 200, 120, size=16)
        drawLabel('Press down to soft drop, press space to hard drop',
                200, 150, size=16)
        drawLabel('Holding up slows down the fall', 200, 180, size=16)
        drawLabel('press P to pause game, press G to start', 200, 200, size=16)

def drawBoard(app):
    # draws the tetris board (15x10 in this game)
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color)
# functions

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='Black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    # draws a single cell within the tetris board
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color,)

def drawPiece(app):
    # draws current piece on the tetris board
    rows, cols = len(app.piece), len(app.piece[0])
    for i in range(rows):
        for j in range(cols):
            if app.piece[i][j] == True:
                color = app.pieceColor
                drawCell(app, i+app.pieceTopRow, j+app.pieceLeftCol, color)

def getCell(app, x, y):
    # returns the row and column of a cell given its x and y
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None

def getCellLeftTop(app, row, col):
    # returns left and top coordinates of given cell
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    # returns height and width of cell
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

# Helper Functions

def pieceIsLegal(app):
    # checks if piece is in a legal state
    if app.pieceTopRow > len(app.board) - len(app.piece) or \
        app.pieceLeftCol > len(app.board[0]) - len(app.piece[0]) or \
        app.pieceLeftCol < 0 or app.pieceTopRow < 0:
            return False
            
    for i in range(len(app.piece)):
        for j in range(len(app.piece[0])):
            if app.piece[i][j]:
                if app.board[i + app.pieceTopRow][j + app.pieceLeftCol] != None:
                    return False
    return True

def hardDropPiece(app):
    # performs the hard drop of the current piece
    while movePiece(app, +1, 0):
        pass
    
def movePiece(app, drow, dcol):
    # this function moves the current piece by given rows and cols
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    
    if pieceIsLegal(app):
        return True
    else:
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
    
def rotatePieceClockwise(app):
    # rotates entire piece clockwise
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    
    app.piece = rotate2dListClockwise(app.piece)
    
    oldRows, oldCols = len(oldPiece), len(oldPiece[0])
    newRows, newCols = len(app.piece), len(app.piece[0])
    
    centerRow = oldTopRow + oldRows // 2
    centerCol = oldLeftCol + oldCols // 2
    
    app.pieceTopRow = centerRow - newRows // 2
    app.pieceLeftCol = centerCol - newCols // 2
    
    if not pieceIsLegal(app):
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol

def rotatePieceCounterClockwise(app):
    # rotates entire piece counterclockwise
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    
    app.piece = rotate2dListCounterClockwise(app.piece)
    
    oldRows, oldCols = len(oldPiece), len(oldPiece[0])
    newRows, newCols = len(app.piece), len(app.piece[0])
    
    if not pieceIsLegal(app):
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol

def placePieceOnBoard(app):
    # places the entire piece onto the board
    for i in range(len(app.piece)):
        for j in range(len(app.piece[0])):
            if app.piece[i][j]:
                app.board[i+app.pieceTopRow][j+app.pieceLeftCol] = app.pieceColor
                
def removeFullRows(app):
    # removes any full rows from the game board, 
    rowsCleared = 0
    i = 0
    while i < len(app.board):
        j = 0
        full = True
        while j < len(app.board[i]):
            if app.board[i][j] == None: full = False
            j += 1
        if full:
            app.board.pop(i)
            app.board.insert(0, [None] * len(app.board[0]))
            rowsCleared += 1
        i += 1
    updateScore(app, rowsCleared)

def updateScore(app, rowsCleared):
    # updates the score based off the number of cleared rows
    #Keeping player score, this method works with step 4.
    if rowsCleared == 1:
        app.score += 1000
    elif rowsCleared == 2:
        app.score += 3000
    elif rowsCleared == 3:
        app.score += 5000
    elif rowsCleared == 4:
        app.score += 8000

# controller 
def takeStep(app):
    # Takes a singular step within the game
    if not movePiece(app, +1, 0):
        # We could not move the piece, so place it on the board:
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)

def onStep(app):
    # called to update the game state
    # automatic stepping with pause that calls takeStep as long as the game is 
    # running
    
    if app.gameOver:
        app.game = False
        app.step = 0
        app.pause = True
        app.board = [[None]*app.cols for row in range(app.rows)]

        
    app.step += 1
    if not app.pause:
        if not app.slow:
            if app.step % 10 == 0:
                takeStep(app)
        if app.slow:
            if app.step % 20 == 0:
                takeStep(app)
        
        if pieceIsLegal(app) == False:
            app.gameOver = True

        
def onKeyPress(app, key):
    # called when key is pressed
    if app.home == True:
        if key == 'g':
            app.game = True
            app.pause = False
            app.home = False
    if app.pause == False and app.game == True and app.home == False:
        if key == 'left':  
            movePiece(app, 0, -1)
        elif key == 'right':
            movePiece(app, 0, +1)
        elif key == 'space':
            hardDropPiece(app)
        elif key == 'down':
            movePiece(app, +1, 0)
        elif key == 's':
            takeStep(app)
        elif key == 'z': 
            rotatePieceClockwise(app)
        elif key == 'x':
            rotatePieceCounterClockwise(app)
    # Pausing
    if key == 'p' and app.home == False:
        if app.pause == True:
            app.pause = False
            app.game = True
        else:
            app.pause = True
            app.game = False
    # game over screen
    if app.gameOver == True:
        if key == 'r':
            app.pause = False
            app.game = True
            app.gameOver = False
            app.score = 0
            
def onKeyHold(app, keys):
    if app.pause == False and app.game == True and app.home == False:
        if 'up' in keys:
            app.slow = True

def onKeyRelease(app, key):
    if app.pause == False and app.game == True and app.home == False:
        if 'up' in key:
            app.slow = False
        
# Main
def main():
    runApp()

main()
