from cmu_112_graphics import *
#http://clintbellanger.net/articles/isometric_math/
#isometric game board
#convert game board to be tile based
#code from https://gamedevelopment.tutsplus.com/tutorials/creating-isometric-worlds-a-primer-for-game-developers--gamedev-6511
#code from https://stackoverflow.com/questions/892811/drawing-isometric-game-worlds
def cartToIso(self, cartX, cartY, scalingFactor):
    cartX -= self.offsetX 
    cartY -= self.offsetY 
    cartX = cartX / scalingFactor
    cartY = cartY / scalingFactor 
    isoX = cartX - cartY
    isoY = (cartX + cartY) / 2
    return isoX, isoY

def isoToCart(self, isoX, isoY, scalingFactor):
    cartX = (2 * isoY + isoX) / 2
    cartY = (2 * isoY - isoX) / 2
    cartX = cartX / scalingFactor
    cartY = cartY / scalingFactor
    cartX += offsetX 
    cartY += offsetY 
    return cartX, cartY 

def pixelToMap(self, x, y):
    gridWidth  = self.width - 2*self.margin
    gridHeight = self.height - 2*self.margin
    tileWidthHalf = (gridWidth//self.rows) / 2 
    row = (x / tileWidthHalf + y / tileWildthHalf) / 2
    col = (y / tileWidthHalf - (x / tileWidthHalf)) /2
    return row, col
def isLegal(self, row, col):
    if 0<= row <=self.rows-1 and 0<=col <=self.cols-1:
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
def keyPressed(self, event):
    if event.key =='Up':
        if isLegal(self, self.charRow-1, self.charCol):
            self.img = self.upImg
            self.charRow -=1 
    elif event.key =='Down':
        if isLegal(self, self.charRow+1, self.charCol):
            self.img = self.downImg

            self.charRow +=1 
    if event.key =='Left':
        if isLegal(self, self.charRow, self.charCol-1):

            self.img = self.leftImg

            self.charCol -=1 
    elif event.key =='Right':
        if isLegal(self, self.charRow, self.charCol+1):
            self.img = self.rightImg

            self.charCol +=1 
def placeTile(tileType, point):
    return
#code from CMU https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def appStarted(self):
    #representative 2D board 
    self.rows = 10
    self.cols = 10
    self.margin = 60 # margin around grid
    self.timerDelay = 250
    self.waitingForFirstKeyPress = True
    self.charRow = 4
    self.charCol = 4
    self.tileWidth = 128
    self.tileHeight = 64
    setUpIsometric(self)
    setUpCharImages(self)
    print(mapToScreen(self, 2, 1))
    print(screenToMap(self, 64, 96))
    self.board = [self.cols * ['white'] for row in range(self.rows)]
    self.blendPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/blender.png'
    self.blendRow = 0
    self.blendCol = 0 
    self.blendImg = self.loadImage(self.blendPath)
    self.blendScale = findScaleFactor(self.blendImg, self.width//2)
    self.blendImg= self.scaleImage(self.blendImg, self.blendScale)
def setUpIsometric(self):
    self.tileWidthHalf = self.tileWidth//2
    self.tileHeightHalf = self.tileHeight//2
    self.offsetX = -1000
    self.offsetY = -270
    self.scalingFactor = 2.5
def mapToScreen(self, row, col):
    x0 = (row - col) * self.tileWidth /2 
    y0 = (row + col) * self.tileHeight / 2 
    return x0, y0
#returns pixel to pointon screen
def screenToMap(self, x, y):
    
    row = (x // self.tileWidthHalf) + (y //self.tileHeightHalf)
    row = row//2 
    col = (y// self.tileHeightHalf)- (x // self.tileWidthHalf)
    col = col//2

    return row, col
def setUpCharImages(self):    
    self.imgPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/icons8-cake-96.png'
    self.kitchenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/kitchen.png'
    #self.img = self.loadImage(self.imgPath)
    self.imgKitchen = self.loadImage(self.kitchenPath)
    self.leftPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/left.png'
    self.rightPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/right.png'
    self.downPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/down.png'
    self.upPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/up.png'
    self.leftImg = self.loadImage(self.leftPath)
    scaleFactor = findScaleFactor(self.leftImg, self.width//8)
    self.leftImg = self.scaleImage(self.loadImage(self.leftPath), scaleFactor)

    self.rightImg = self.scaleImage(self.loadImage(self.rightPath), scaleFactor)
    self.downImg = self.scaleImage(self.loadImage(self.downPath), scaleFactor)
    self.upImg = self.scaleImage(self.loadImage(self.upPath), scaleFactor)

    self.img = self.leftImg 
    #heavily based on code from PIL optional lecture, link: https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4c852dc1-658a-42dc-a8c0-ac790004263c   
def findScaleFactor(image, goalWidth):
    width, height = image.size 
    scaleFactor = goalWidth / width 
    return scaleFactor    


def getIsoCellBounds(self, row, col):
    x0, y0, x1, y1 = getCellBounds(self, row, col)
    startX, startY = cartToIso(self, x0, y0, self.scalingFactor) 
    endX, endY = cartToIso(self, x1, y1, self.scalingFactor)
    return startX, startY, endX, endY
# getCellBounds from grid-demo.py
def getCellBounds(self, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = self.width
    gridHeight = self.height
    x0 = gridWidth * col / self.cols
    x1 =gridWidth * (col+1) / self.cols
    y0 = gridHeight * row / self.rows
    y1 = gridHeight * (row+1) / self.rows
    return (x0, y0, x1, y1)

def drawChar(self, canvas):
    x0,y0,x1, y1 = getIsoCellBounds(self, self.charRow, self.charCol)
    #canvas.create_oval(x0,y0,x1, y1, fill = 'red')
    canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(self.img)) 
    
def drawAppliances(self, canvas):
    x0, y0, x1, y1 = getIsoCellBounds(self,self.blendRow, self.blendCol)
    canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(self.blendImg)) 

def drawBoard(self, canvas):
    for row in range(self.rows):
        for col in range(self.cols):
            (x0, y0, x1, y1) = getCellBounds(self, row, col)
            startx0, starty0 = cartToIso(self, x0, y0)
            endx1, endy1 = cartToIso(self, x1, y1)
            midx1, midy1 = startx0 +(endy1-starty0)/2, starty0 + (endy1-starty0)/2
            r = 5
            canvas.create_oval(x0-r, y0-r, x0+r, y0+r, fill = 'pink')
            canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill = 'pink')

def drawKitchen(self, canvas):
    canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.imgKitchen))
def redrawAll(self, canvas):
    drawKitchen(self, canvas)
    #drawBoard(self,canvas)
    drawAppliances(self, canvas)
    drawChar(self, canvas)


runApp(width=600, height=600)

