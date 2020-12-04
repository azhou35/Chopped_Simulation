from cmu_112_graphics import *
import classesOfFood as classes 
#recurisve function to get from row, col A to row, col B
class MyApp(App):
    #recursive game ai function 
    def generatePath(row0, col0, row1, col1, moveList):
        xDir = 0
        yDir = 0

        #base case: you have reached the end position
        if (row0==row1 and col0==col1):
            return moveList

        #if avatar needs to move up, yDir is -1, if down, 1
        if col1-col0 >0: yDir = 1
        else: yDir = -1

        #chck if avatar needs to move right 
        if (row1-row0 >0): xDir = 1 
        else: xDir = -1

        moveList.append((xDir, yDir))
        #TO DO: NEED TO CHECK IF IT"S LEGAL 
        #is this backtracking? 

        #default move is to keep on moving diagonally until either 
        #your row0 matches row1 or col0 value matches with col1, 
        #in that case you just move in that lateral direction
        if (row0==row1 and col0!=col1):
            return MyApp.generatePath(row0, col0 + yDir, row1, col1, moveList)
        elif (row0!= row1 and col0==col1):
            return MyApp.generatePath(row0 + xDir, col0, row1, col1, moveList)

        else:
            return MyApp.generatePath(row0 + xDir, col0 + yDir, row1, col1, moveList)

    def isLegal(self, row, col):
        if self.board[row][col] != 'white':
            return True
        else:
            return False  
    #oveList = list()
    #print(generatePath(0, 0, 4, 5, moveList))
    #keeps track of Mouse pressed 
    def mousePressed(self, event):
        mouseX, mouseY = event.x, event.y 

        #need some kind of case in case it clicks outside the grid 
        color = MyApp.getColor(self, mouseX, mouseY)
        if color !=None and 'pink':
            row, cell = MyApp.getCell(self, mouseX, mouseY)
            self.isApplianceScreen = True 
            #trigger and open the appliance menu 
        else: 
            #check if it's in boundaries of appliance grid or somethng
            #if in inventory grid boundaries 
            #getInvCellBounds 
            print()
        #if mouseX in image and mouseY in image:
        # trigger your pop up menu 
        #self.messages.append((mouseX, mouseY))
        """
        if mouseX <= self.width/2 and mouseY <= self.height/2:
            self.isIngredientScreen = True 
        if self.isCookingMode==True and mouseX<= self.width/2 and mouseY <= self.height/2:
            self.isApplianceScreen = True
        """


    def appStarted(self):
        self.rows = 15
        self.cols = 15

        self.margin = 20 # margin around grid
        self.bottomMargin = self.height//4
        self.rightMargin = self.width//4

        #self.timerDelay = 250
        #taken from my HW7 Tetris homework
        #keep track which parts of board are filled
        self.board = [self.cols * ['white'] for row in range(self.rows)]

        self.oppRow = 0 
        self.oppCol = 0 

        self.goalRow = 5
        self.goalCol = 5 
        #call helper function for list of moves it will need to take
        self.moves = MyApp.generatePath(self.oppRow, self.oppCol, self.goalRow, self.goalCol, [])
        self.moveNum = 0 

        self.charRow = self.rows-1
        self.charCol = self.cols - 1 
        self.cookbooks, self.basket, self.Person, self.Opponent, self.Appliances, self.Ingredients = classes.setUpObjects()

        #booleans for different modes 
        self.isApplianceScreen = False
        self.isInventoryScreen = True 
        self.isTimeUp = False
        self.pantryTimer = 20000 #start with 1 minute = 180000

        MyApp.setUpInventory(self)

    def setUpAppliances(self, canvas):
        gap = 3 #gap of 3 rows between everything 
        applianceCount = 0
        
        for Appliance in self.Appliances:
            for i in range(Appliance.cellsInLength):
                row = gap * applianceCount
                col = (self.cols//2 - Appliance.cellsInLength//2) + i 
                if i == Appliance.cellsInLength//2:
                    color = 'pink'
                else:
                    color = 'gray' 

                self.board[row][col] = color
            applianceCount +=1     

    def keyPressed(self, event):
        if event.key =='Up': self.charRow -=1
        elif event.key == 'Down': self.charRow += 1
        elif event.key == 'Left': self.charCol-= 1 
        elif event.key == 'Right': self.charCol += 1

    def convertMilli(self, milli):
        seconds=(milli//1000)%60
        minutes=(milli//(1000*60))%60
        return seconds, minutes
    def drawTimer(self, canvas):
        seconds, minutes = MyApp.convertMilli(self, self.pantryTimer)
        if self.isTimeUp:
            minutes = '00'
            seconds = '00'
        elif seconds <10:
            seconds = '0' + str(seconds)
        canvas.create_text(7* self.width/8, self.height/8, text = f'Time Left: {minutes}:{seconds}')

    def timerFired(self):
        MyApp.moveGameAI(self)
        if self.pantryTimer>=0:
            self.pantryTimer -=100
        else:
            self.isTimeUp = True


            
    def moveGameAI(self):
        #only move if haven't reached goal state
        if not self.moveNum == len(self.moves) -1: 
            currMove = self.moves[0]
            self.oppRow += currMove[0]
            self.oppCol += currMove[1]
            self.moveNum += 1
        

    # getCellBounds from grid-demo.py
    def getCellBounds(self, row, col):
        self.gridWidth  = self.width - self.margin - self.rightMargin
        self.gridHeight = self.height - self.margin - self.bottomMargin
        x0 = self.margin + self.gridWidth * col / self.cols
        x1 = self.margin + self.gridWidth * (col+1) / self.cols
        y0 = self.margin + self.gridHeight * row / self.rows
        y1 = self.margin + self.gridHeight * (row+1) / self.rows
        return (x0, y0, x1, y1)
   
    def getCell(self, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        gridWidth  = self.width - self.margin - self.rightMargin
        gridHeight = self.height - self.margin - self.bottomMargin
        self.cellWidth  = gridWidth / self.cols
        self.cellHeight = gridHeight / self.rows

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, app.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - self.margin) / self.cellHeight)
        col = int((x - self.margin) / self.cellWidth)

        return (row, col)

    # getCellBounds from grid-demo.py
    def getInvCellBounds(self, row, col):
        xStart = self.width - self.rightMargin + self.margin
        yStart = self.height/5

        width = self.rightMargin - 2 * self.margin 
        length = self.height - self.bottomMargin 
        margin = width / 4.5
        self.invGridWidth  = width - 2 * margin
        self.invGridHeight = length - 2 * margin

        x0 = xStart+ margin + self.invGridWidth * col / self.invCols
        x1 = xStart+ margin + self.invGridWidth * (col+1) / self.invCols
        y0 = yStart + margin + self.invGridHeight * row / self.invRows
        y1 = yStart +margin + self.invGridHeight * (row+1) / self.invRows
        return (x0, y0, x1, y1)
    
    #function to set up attributes of inventory for later use
    def setUpInventory(self):
        self.invCols = 1 
        self.invRows = 5
        self.inventoryPage = [self.invCols * [None] for row in range(self.rows)]
        self.inventory = list()
        #self.inventory.append(classes.Potato)
        self.inventory.append('/Users/az/Documents/GitHub/Chopped_Simulation/images/potato.png')
    def drawIngredientsInInventoryScreen(self, canvas):
        #loop thru index of everything in ur current inventory
        for ingredIndex in range(len(self.inventory)): #inventory
            #only show as many images as there r rows
            """
            if ingredIndex < self.invRows: 
                Ingredient = self.inventory[ingredIndex]
                path = Ingredient.path 
                drawImage(self, path, midRow, midCol)
"""
            ingredientPath = self.inventory[ingredIndex]
            drawImage(self,ingredientPath, 0, 0)
    #function to call drawCell and draw a table to contain the images it will need
    def drawInventoryTable(self, canvas):
        for row in range(self.invRows):
            for col in range(self.invCols):
                MyApp.drawInvCell(self, canvas, row, col, 'lightgray')

    def drawInvCell(self,canvas, row, col, color):

        x0, y0, x1, y1 = MyApp.getInvCellBounds(self, row, col)
        
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline='gray')

    def drawBoard(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                MyApp.drawCell(self,canvas,row,col,self.board[row][col])


    #taken from my HW7, Tetris
    #function to create each cell and fill with its respective color 
    
    def drawApplianceScreen(self, canvas):
        width = 2*self.bottomMargin/3
        length = self.width - self.margin - self.rightMargin
        xStart = self.margin
        yStart = self.height-self.bottomMargin+self.margin
        canvas.create_rectangle(xStart, yStart, xStart + length, yStart + width, fill = 'skyblue')
        canvas.create_text((2*xStart+length)/2, yStart + length/35, text = 'APPLIANCE')
    
    def drawInventoryScreen(self, canvas):
        self.invWidth = self.rightMargin - 2 * self.margin 
        self.invLength = self.height - self.bottomMargin 
        xStart = self.width - self.rightMargin + self.margin
        yStart = self.height/5
        canvas.create_rectangle(xStart, yStart, xStart + self.invWidth, yStart + self.invLength, fill = 'pink')
        canvas.create_text((2*xStart+self.invWidth)/2, yStart + self.invLength/35, text = 'INVENTORY')

    def drawCell(self,canvas, row, col, color):
        x0, y0, x1, y1 = MyApp.getCellBounds(self, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = color
                                 )

    def drawGameAI(self, canvas):
        (x0, y0, x1, y1) = MyApp.getCellBounds(self, self.oppRow, self.oppCol)
        canvas.create_oval(x0, y0, x1, y1, fill='red')

    def drawPlayer(self, canvas):
        (x0, y0, x1, y1) = MyApp.getCellBounds(self, self.charRow, self.charCol)
        canvas.create_oval(x0, y0, x1, y1, fill='blue')

    #heavily based on code from PIL optional lecture, link: https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4c852dc1-658a-42dc-a8c0-ac790004263c   
    def scaleImage(self, image, goalWidth):
        width, height = image.size 
        scaleFactor = goalWidth / width 
        return scaleFactor    
    
    #given path of image and which row, col it should be centered in, draw image

    def drawImage(self, path, midRow, midCol, grid):
        img = self.loadImage(path)
        #draw image to be based on where the inventory is
        if grid == 'inventory':
            x0, x1, y0, y1 = MyApp.getInvCellBounds(self, midRow, midCol)
            self.invcellWidth  = self.invGridWidth / self.invcols
            scaleFactor = MyApp.scaleImage(self, img, self.invGridWidth)

        else:
            x0, x1, y0, y1 = MyApp.getCellBounds(self, midRow, midCol)
            scaleFactor = MyApp.scaleImage(self, img, self.cellWidth)

        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(img)) 
        
    #taken from 112 Website
    def getCachedPhotoImage(self, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    def getImageDim(self, image, cx, cy):
        width = image.width 
        height = image.height
        leftX = cx - image.width/2 
        rightX = cx + image.width/2
        topY = cy + image.height/2
        bottomY = cy - image.height/2 
        nwX, nwY = leftX, topY
        neX, neY = rightX, topY
        swX, swY = leftX, bottomY
        seX, seY = rightX, bottomY
        return ((nwX, nwY), (neX, neY), (swX, swY), (seX, seY))
    
    def convertMilli(self, milli):
        seconds=(milli//1000)%60
        minutes=(milli//(1000*60))%60
        return seconds, minutes

    def drawTimer(self, canvas):
        seconds, minutes = MyApp.convertMilli(self, self.pantryTimer)
        if self.isTimeUp:
            minutes = '00'
            seconds = '00'
        elif seconds <10:
            seconds = '0' + str(seconds)
        canvas.create_text(7* self.width/8, self.height/8, text = f'Time Left: {minutes}:{seconds}')

    #this check is taken from example 10 of https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by app.
        return ((self.margin <= x <= self.width-self.margin-self.rightMargin) and
                (self.margin <= y <= self.height-self.margin-self.bottomMargin))

    def getColor(self, x, y):
        #this check is taken from example 10 of https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        if (not MyApp.pointInGrid(self, x, y)):
            return None
        row, cell = MyApp.getCell(self, x, y)
        print(self.board[row][cell])
        return self.board[row][cell]

    def redrawAll(self, canvas):
        MyApp.drawBoard(self,canvas)
        MyApp.drawGameAI(self, canvas)
        MyApp.drawPlayer(self, canvas)
        MyApp.setUpAppliances(self, canvas)
        MyApp.drawInventoryScreen(self, canvas)
        MyApp.drawInventoryTable(self, canvas)
        MyApp.drawTimer(self, canvas)
        MyApp.drawIngredientsInInventoryScreen(self, canvas)

        if self.isApplianceScreen:
            MyApp.drawApplianceScreen(self, canvas)

MyApp(width = 600, height = 600)
"""
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

    #see if row has color in it at any point, thus being illegal to approach
    
function to set up dimensions
def playChopped():
    rows, cols, cellSize, margin = gameDimensions()
    #calculate width of screen using game dimensions
    width = cols * cellSize + 2*margin
    #calculate height of screen using game dimensions
    height = rows * cellSize + 2*margin
    MyApp(width = width, height = height)

#main 
def main():
    playChopped()

if __name__ == '__main__':
    main()

""" 