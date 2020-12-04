#isometric game board
#convert game board to be tile based
#code from https://gamedevelopment.tutsplus.com/tutorials/creating-isometric-worlds-a-primer-for-game-developers--gamedev-6511
def cartToIso(cartX, cartY):
    isoX = cartX - cartY
    isoY = (cartX + cartY) / 2
    return isoX, isoY
def isoToCart(isoX, isoY):
    cartX = (2 * isoY + isoX) / 2
    cartY = (2 * isoY - isoX) / 2

def createIsoBoard(board, tileWidth, tileHeight):
    for row in range(board):
        for col in range(board[0]):
            x = col * tileWidth
            y = row * tileHeight
    tileType = levelData[row][col]
    placetile(tileType, carToIso((x, y)))


def placeTile(tileType, point):
    return
#code from CMU https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
from cmu_112_graphics import *
def appStarted(app):
    app.rows = 10
    app.cols = 10
    app.margin = 5 # margin around grid
    app.timerDelay = 250
    app.waitingForFirstKeyPress = True

# getCellBounds from grid-demo.py
def getCellBounds(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill='white')
def redrawAll(app, canvas):
    drawBoard(app,canvas)


runApp(width=400, height=400)

