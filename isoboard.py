from cmu_112_graphics import *
#http://clintbellanger.net/articles/isometric_math/
#isometric game board
#convert game board to be tile based
#code from https://gamedevelopment.tutsplus.com/tutorials/creating-isometric-worlds-a-primer-for-game-developers--gamedev-6511
#code from https://stackoverflow.com/questions/892811/drawing-isometric-game-worlds
def cartToIso(cartX, cartY):
    isoX = cartX - cartY
    isoY = (cartX + cartY) / 2
    return isoX, isoY

def isoToCart(isoX, isoY):
    cartX = (2 * isoY + isoX) / 2
    cartY = (2 * isoY - isoX) / 2
    return cartX, cartY 
def pixelToMap(app, x, y):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    tileWidthHalf = (gridWidth//app.rows) / 2 
    row = (x / tileWidthHalf + y / tileWildthHalf) / 2
    col = (y / tileWidthHalf - (x / tileWidthHalf)) /2
def isLegal(app, row, col):
    if 0<= row <=app.rows-1 and 0<=col <=app.cols-1:
        return True
#i dont think i need this
def createIsoBoard(board, tileWidth, tileHeight):
    for row in range(board):
        for col in range(board[0]):
            x = col * tileWidth
            y = row * tileHeight
    tileType = levelData[row][col]
    placetile(tileType, carToIso((x, y)))

    return x, y
def keyPressed(app, event):
    if event.key =='Up':
        if isLegal(app, app.charRow-1, app.charCol):
            app.img = app.upImg
            app.charRow -=1 
    elif event.key =='Down':
        if isLegal(app, app.charRow+1, app.charCol):
            app.img = app.downImg

            app.charRow +=1 
    if event.key =='Left':
        if isLegal(app, app.charRow, app.charCol-1):

            app.img = app.leftImg

            app.charCol -=1 
    elif event.key =='Right':
        if isLegal(app, app.charRow, app.charCol+1):
            app.img = app.rightImg

            app.charCol +=1 
def placeTile(tileType, point):
    return
#code from CMU https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def appStarted(app):
    app.rows = 6
    app.cols = 6
    app.margin = 60 # margin around grid
    app.timerDelay = 250
    app.waitingForFirstKeyPress = True
    app.charRow = 0
    app.charCol = 0 
    app.tileWidth = 64
    app.tileHeight = 64
    setUpCharImages(app)

def setUpCharImages(app):    
    app.imgPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/icons8-cake-96.png'
    app.kitchenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/kitchen.png'
    #app.img = app.loadImage(app.imgPath)
    app.imgKitchen = app.loadImage(app.kitchenPath)
    app.leftPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/left.png'
    app.rightPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/right.png'
    app.downPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/down.png'
    app.upPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/up.png'
    app.leftImg = app.loadImage(app.leftPath)
    scaleFactor = findScaleFactor(app.leftImg, app.width//8)
    app.leftImg = app.scaleImage(app.loadImage(app.leftPath), scaleFactor)

    app.rightImg = app.scaleImage(app.loadImage(app.rightPath), scaleFactor)
    app.downImg = app.scaleImage(app.loadImage(app.downPath), scaleFactor)
    app.upImg = app.scaleImage(app.loadImage(app.upPath), scaleFactor)

    app.img = app.leftImg 
    #heavily based on code from PIL optional lecture, link: https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4c852dc1-658a-42dc-a8c0-ac790004263c   
def findScaleFactor(image, goalWidth):
    width, height = image.size 
    scaleFactor = goalWidth / width 
    return scaleFactor    


def getIsoCellBounds(app, row, col):
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    startX, startY = cartToIso(x0, y0) 
    endX, endY = cartToIso(x1, y1)
    return startX, startY, endX, endY
# getCellBounds from grid-demo.py
def getCellBounds(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width 
    gridHeight = app.height 
    x0 = gridWidth * col / app.cols
    x1 =gridWidth * (col+1) / app.cols
    y0 = gridHeight * row / app.rows
    y1 = gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def drawChar(app, canvas):
    x0,y0,x1, y1 = getIsoCellBounds(app, app.charRow, app.charCol)
    #canvas.create_oval(x0,y0,x1, y1, fill = 'red')
    canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(app.img)) 
    


def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            startx0, starty0 = cartToIso(x0, y0)
            endx1, endy1 = cartToIso(x1, y1)
            midx1, midy1 = startx0 +(endy1-starty0)/2, starty0 + (endy1-starty0)/2
            r = 5
            canvas.create_oval(x0-r, y0-r, x0+r, y0+r, fill = 'pink')
            canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill = 'pink')

def drawKitchen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.imgKitchen))
def redrawAll(app, canvas):
    drawKitchen(app, canvas)
    drawBoard(app,canvas)
    drawChar(app, canvas)


runApp(width=600, height=600)

