#CITATION: CMU GRAPHICS FRAMEWORK CREDS TO: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#this includes CMU Graphics file, so functions like "appStarted" and such
#TP 3: work on ui: which one is player, which one is game ai, kitchen appliances
#make it more explicit how to combine ingredients 


from cmu_112_graphics import *
#my own files
import classesOfFood as classes 
import webScraping as web
#CITATION: RANDOM MODULE FROM https://docs.python.org/3/library/random.html
import random
#cooking mode class with user control
#CITATION: MODAL CODE FRAMEWORK CREDS TO: https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
class CookingMode(Mode):
    #recurisve game AI function to get from row, col A to row, col B
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
        #default move is to keep on moving diagonally until either 
        #your row0 matches row1 or col0 value matches with col1, 
        #in that case you just move in that lateral direction

        if (row0==row1 and col0!=col1):
            #return CookingMode.generatePath(row0, col0 + yDir, row1, col1, moveList)
            xDir = 0 
        elif (row0!= row1 and col0==col1):
            #return CookingMode.generatePath(row0 + xDir, col0, row1, col1, moveList)
        #else:
            yDir = 0
        moveList.append((xDir, yDir))

        return CookingMode.generatePath(row0 + xDir, col0 + yDir, row1, col1, moveList)

    #set up game AI properties for use throughout code
    def setUpGameAI(self):
        self.Opponent.randomizeFinalProduct()
        self.finalDish = self.Opponent.finalDish
        self.Opponent.generateApplianceAndGroceriesList()
        self.applianceList = self.Opponent.applianceList
        self.moveList = list()
        CookingMode.gameAIPath(self)
        self.groceries = self.Opponent.groceries
        #print(f'this is FINAL DISH: {finalDish}')

    #goes thru all the appliances the gameAI needs to reach
    def gameAIPath(self):
        appliances = self.applianceList
        firstAppliance = appliances[0]
        firstMoveList = list()
        #print(f'THIS IS ACCESS {self.accessPoints} and THIS IS THE FIRST ONE {self.accessPoints[firstAppliance][0]}')
        firstAppRow, firstAppCol = self.accessPoints[firstAppliance][0], self.accessPoints[firstAppliance][1]
        self.moveList+=(CookingMode.generatePath(self.oppRow, self.oppCol, firstAppRow, firstAppCol, firstMoveList))
        #add arbitrary number to indicate wait time 
        self.moveList.append((20, 20))
        #self.endingRow, self.endingCol = 0, 0
        #go thru every pair:
        print(appliances)
        for applianceIndex in range(len(appliances)-1):
            
            appliance = appliances[applianceIndex]
            nextAppliance = appliances[applianceIndex+1]
            row0, col0 = self.accessPoints[appliance][0], self.accessPoints[appliance][1]
            row1, col1 = self.accessPoints[nextAppliance][0], self.accessPoints[nextAppliance][1]
            currMoveList = list()
            self.moveList+=(CookingMode.generatePath(row0, col0, row1, col1, currMoveList))
            self.moveList.append((20, 20))
            #self.endingRow, self.endingCol = row1, col1
        #after all steps, move game ai to vibe in the middle C:
        lastAppliance = appliances[-1]
        moveList = list()
        lastRow, lastCol = self.accessPoints[lastAppliance][0], self.accessPoints[lastAppliance][1]
        vibeRow, vibeCol = self.rows//2, self.cols//2
        self.moveList+=(CookingMode.generatePath(lastRow, lastCol, vibeRow, vibeCol, moveList))
        print(self.moveList)
        #calculate path to wait in the middle
        #finalMoveList = list()
        #self.moveList += CookingMode.generatePath(self.endingRow, self.endingCol, self.rows//2, self.cols//2, finalMoveList)
                #self.moveList+=['stop']
                #applianceIndex+=1 
            #if starting at the list, start accumulating moves with the game Ai's initial starting row, col
            #if applianceIndex == 0: 
            #    row0, col0 = self.oppRow, self.oppCol
            #    row1, col1 = self.applianceDict[appliance][0], self.applianceDict[appliance][1]
            #else:
            #    nextAppliance = appliances[applianceIndex+1]
            #    row0, col0 = self.applianceDict[appliance][0], self.applianceDict[appliance][1]
            #    row1, col1 = self.applianceDict[nextAppliance][0], self.applianceDict[nextAppliance][1]
            #currentMoveList = list()
            #self.moveList+=(CookingMode.generatePath(row0, col0, row1, col1, currentMoveList))

    def getIndex(self, row, col, rows):
        index = ((row * rows) + col)
        return index 

    def isLegal(self, row, col):
        if self.board[row][col] == 'white':
            if not (self.oppRow == row and self.oppCol == col): 
                return True
        else:
            return False  
    #oveList = list()
    #keeps track of Mouse pressed 
    def mousePressed(self, event):
        mouseX, mouseY = event.x, event.y 

        #need some kind of case in case it clicks outside the grid 
        color = CookingMode.getColor(self, mouseX, mouseY)
        if color !=None and color=='pink':
            (row, col) = CookingMode.getCell(self, mouseX, mouseY)
            currLocation = list((row, col))
            for appliance, location in self.applianceDict.items():
                if location == currLocation:
                    self.currentAppliance = appliance
                    #print(self.currentAppliance)
            self.isApplianceScreen = True 

            #trigger and open the appliance menu 
        else: 
            #print('im geting here')
            row, col = CookingMode.getInvCell(self, mouseX, mouseY)
            if (row, col) != (-1, -1):
                
                #add the ingredientPath of current selected to current selected hand
                #don't add duplicates
                if not self.displayInventory[row][0] in self.currentSelect:
                    if self.displayInventory[row][0] != None:
                        self.currentSelect.append(self.inventory[row])
                        self.outlineRowCol.append((row, col))
                        #index = CookingMode.getIndex(self, row, col, 5)
                        #print(index)
                        #self.ingredientHistory.append(self.inventory[index])

                    #print(self.currentSelect)
                    #print(self.currentSelect)
            #check if it's clicked within the appliance grid 
        #else: click within the aplliance screen
        
    def appStarted(self):
        self.rows = 15
        self.cols = 15

        self.margin = 20 # margin around grid
        self.bottomMargin = self.height//4
        self.rightMargin = self.width//4
        
        #self.timerDelay = 400
        #taken from my HW7 Tetris homework
        #keep track which parts of board are filled
        self.board = [self.cols * ['white'] for row in range(self.rows)]
        self.waitTime = -1
        self.oppRow = 4 
        self.oppCol = 0 

        #self.goalRow = 5
        #self.goalCol = 5 
        #call helper function for list of moves it will need to take
        #self.moves = CookingMode.generatePath(self.oppRow, self.oppCol, self.goalRow, self.goalCol, [])
        self.moveNum = 0 
        self.charRow = self.rows-4
        self.charCol = 0
        #self.app.cookingMode.finalDish
        (self.cookbooks, self.basket, self.Person, self.Opponent, self.Appliances, self.IngredientObjects) = (self.app.basketMode.cookbooks, self.app.basketMode.basket, self.app.basketMode.Person,
                                                                                    self.app.basketMode.Opponent, self.app.basketMode.Appliances, self.app.basketMode.Ingredients)

        self.invWidth = self.rightMargin - 2 * self.margin 
        self.invLength = self.height - self.bottomMargin 
        width = self.rightMargin - 2 * self.margin 
        length = self.height - self.bottomMargin 
        margin = width / 4.5
        self.invGridWidth  = width - 2 * margin
        self.invGridHeight = length - 2 * margin
        self.gridWidth  = self.width - self.margin - self.rightMargin
        self.gridHeight = self.height - self.margin - self.bottomMargin

        #booleans for different modes 
        self.isApplianceScreen = False
        self.isInventoryScreen = True 
        self.isTimeUp = False
        self.isCombine = False
        self.pantryTimer = 20000 #start with 1 minute = 180000
        self.combination = ''
        self.currentSelect = list()
        self.ingredientHistory = list()
        CookingMode.setUpInventory(self)
        #CookingMode.setUpAppliances(self)
        CookingMode.randomizeAppliances(self)
        self.outlineRowCol = list()
        CookingMode.setUpGameAI(self)
        CookingMode.placeImage(self)
        #self.basket = classes.randomizeBasket(self.cookbooks[0])
        self.playerFinalDish = ''
        self.complexity = 0 
        self.recipeCounter = 0
    def convertMoveToAppliance(self):
        for item in self.applianceList:
            if item=='stack': 
                item = 'plating'
    def setHorizontal(self, length, row, col, appliance):
        for i in range(length):
            col += 1 
            if i == 5//2:
                color = 'pink'
                #self.applianceLocation[appliance] = [row, col]
            else:
                color = 'gray'

            self.board[row][col] = color

    def setVertical(self, length, row, col, appliance):
        for i in range(length):
            row += 1 
            if i == 5//2:
                color = 'pink'
                #self.applianceLocation[appliance] = [row, col]
            else:
                color = 'gray'
            self.board[row][col] = color
    #place appliances on board
    def placeAppliance(self, length, startingPoint, side, orientation, appliance):
        tableLocation = list()
        applianceLocation = list()
        accessPoint = list()

        if orientation == 'vert':
            row = startingPoint
            col = side #stays constant
        else: 
            col = startingPoint
            row = side #stays constant 
        

        for i in range(length):
            #check orientation for which way it moves
            if orientation == 'vert':
                if i!=0:
                    row += 1 #add by whichever part of the appliance you're on
            else: 
                if i!=0:
                    col += 1
#first check if there's not something already in the path, otherwise, return false
            if self.board[row][col] != 'white':
                return False 
            applianceLocation = [row, col] #set current row, col applicane location
            #this is appliance location!
            if i == 5//2:
                color = 'pink'
                if side == 0: #this means its on top or on left, meaning u should either increase  
                    if orientation == 'vert': 
                        accessPoint = [row, col+1]
                    else:
                        accessPoint= [row+1, col]
                #self.applianceLocation[appliance] = [row, col]
                else: #this means its on right or bottom, so u need to be either to the left or above 
                    if orientation == 'vert': 
                        accessPoint = [row, col-1]
                    else:
                        accessPoint = [row-1, col]
            else: 
                color = 'gray'
    #only add items if everything is ok and legal!
            tableLocation.append([(row, col), color])
        for item in tableLocation:
            #print(item)
            self.board[item[0][0]][item[0][1]] = item[1]
        self.accessPoints[appliance] = accessPoint
        self.applianceDict[appliance] = applianceLocation
        print(f'this is access points{self.accessPoints}')

        return True 

    def generateRandom(self, appliances, length): 
        orientation = random.choice(['hor', 'vert'])
        #top or bottom / left or right
        side = random.choice([0, self.cols-1])
            #randomize starting point
        startingPoint = random.randint(0, self.cols - length - 1) #ending opint is so it doesnt go past the end of the board
        return orientation, side, startingPoint

    #function to randomly place appliances on different areas on the board! 
    def randomizeAppliances(self):
        appliances = ['whisk', 'bake', 'blend', 'saute', 'stack']
        #randomly choose if vertical or horizontal
        length = 5
        self.accessPoints = dict()
        self.applianceDict = dict()
        isLegal = False
        for i in range(len(appliances)):
            #should keep redoing this until you get a legal appliance setting :^))) 
            #inspo for randomization from snake https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
            while isLegal == False:  
                orientation, side, startingPoint = CookingMode.generateRandom(self, appliances, length)
                isLegal = CookingMode.placeAppliance(self, length, startingPoint, side, orientation, appliances[i])
    
    def setUpAppliances(self):
        self.accessPoints = { 'mix': [1, 3], 
        'bake': [1, 9], 
        'blend': [7, 13],
        'saute': [13, 9],
        'stack': [13, 3]
        }
        self.applianceDict = { 'mix': [0, 3], 
        'bake': [0, 9], 
        'blend': [7, 14],
        'saute': [14, 9],
        'stack': [14, 3]
        }

        CookingMode.setHorizontal(self, 5, 0, 0,'whisk')
        CookingMode.setHorizontal(self, 5, 0, 6, 'oven')        
        CookingMode.setHorizontal(self, 5, self.rows-1, 0, 'blender')        
        CookingMode.setHorizontal(self, 5, self.rows-1, 6, 'stovetop')        
        #CookingMode.setVertical(self, 5, 4, 0, 'plating')
        CookingMode.setVertical(self, 5, 4, self.cols-1, 'stack')

    
    def keyPressed(self, event):
        if event.key =='Up': 
            if CookingMode.isLegal(self, self.charRow -1, self.charCol):
                self.charRow -=1 
        elif event.key == 'Down': 
            if CookingMode.isLegal(self, self.charRow +1, self.charCol):
                self.charRow += 1
        elif event.key == 'Left': 
            if CookingMode.isLegal(self, self.charRow, self.charCol-1):
                self.charCol-= 1 
        elif event.key == 'Right': 
            if CookingMode.isLegal(self, self.charRow, self.charCol+1):
                self.charCol += 1
        elif event.key == 'c':
            if self.isApplianceScreen:
                #self.isCombine = True
                if len(self.currentSelect) >= 1:
                    self.combination = CookingMode.combineIngredients(self)
                    self.playerFinalDish = self.combination
                    self.isCombine = True
                    self.complexity += 1 
        #go to nex mode
        elif event.key == 'n':
            self.app.setActiveMode(self.app.judgingMode)
        
        elif event.key == 'x':
            self.inventory.append(self.combination)
            self.isApplianceScreen = False
            self.combination = ''
        #this is where the loaded List might function differently, so call here
        CookingMode.placeImage(self)
#CITATION: convertMilli and drawTimer code based off of https://stackoverflow.com/questions/35989666/convert-milliseconds-to-hours-min-and-seconds-python
    def convertMilli(self, milli):
        seconds=(milli//1000)%60
        minutes=(milli//(1000*60))%60
        return seconds, minutes
    def drawTimer(self, canvas):
        seconds, minutes = CookingMode.convertMilli(self, self.pantryTimer)
        if self.isTimeUp:
            minutes = '00'
            seconds = '00'
        elif seconds <10:
            seconds = '0' + str(seconds)
        canvas.create_text(7* self.width/8, self.height/8, text = f'Time Left: {minutes}:{seconds}')

    #function to combine ingredients in current select using object properties
    def combineIngredients(self):
        ingredientNames = []
        #print(f'this is current select: {self.currentSelect}')
        for item in self.currentSelect:
            if (isinstance(item, classes.Staples)):
                ingredObject = item
                self.ingredientHistory.append(ingredObject.name)
            else:
                self.ingredientHistory.append(item)
                ingredObject = CookingMode.getIngredientObject(self, item)
            #print(isinstance(ingredObject, classes.Staples))
            ingredientNames.append(ingredObject)
        firstIngred = ingredientNames[0]
        secondIngred = ingredientNames[1:]
        combination = firstIngred.combine(secondIngred, self.currentAppliance)
        return combination
        
    def getIngredientObject(self, ingredient):
        for ingredObject in self.IngredientObjects:
            if ingredObject.name == ingredient:
                #print(f'within GET INGREDIENT OBJECT {isinstance(ingredObject, classes.Staples)}')

                return ingredObject

    def timerFired(self):
        print(self.waitTime)
        #print(f'THIS IS MOVE NUM: {self.moveNum}')
        if self.waitTime ==-1:
            #moveNormally
            CookingMode.moveGameAI(self)
        elif self.waitTime ==0:
            self.moveNum +=1 #you can start moving again
            CookingMode.moveGameAI(self)
            self.waitTime = -1
        else: #when you hit stop time, don't move 
            self.waitTime -=100
            print(self.oppRow, self.oppCol)
        if self.pantryTimer>=0:
            self.pantryTimer -=100
        else:
            self.isTimeUp = True
        
        #run combining methods if ingredients are successfully combined
        #if self.isCombine: 
        #    CookingMode.combineIngredients(self)
        CookingMode.placeImage(self)
        CookingMode.displayImagesInInventory(self)    

    def moveGameAI(self):
        #only move if haven't reached goal state
        if not self.moveNum == len(self.moveList): 
            #print(f'THIS IS moveLIST IN MOVE GAME AI: {self.moveList}')
            if not self.moveList == None:
                currMove = self.moveList[self.moveNum]
                if currMove[0] == 20:
                    self.waitTime = 500
                else:
                    self.oppRow += currMove[0]
                    self.oppCol += currMove[1]
                    self.moveNum += 1
                    #print('move added')
        

    # getCellBounds from grid-demo.py
    #CITATION: CREDS to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellBounds(self, row, col):
        x0 = self.margin + self.gridWidth * col / self.cols
        x1 = self.margin + self.gridWidth * (col+1) / self.cols
        y0 = self.margin + self.gridHeight * row / self.rows
        y1 = self.margin + self.gridHeight * (row+1) / self.rows
        return (x0, y0, x1, y1)
   #CITATION: CREDS to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
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
    #CITATION: CREDS to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getInvCell(self, x, y):
        if (not CookingMode.pointInInvGrid(self, x, y)):
            return (-1, -1)

        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        xStart = self.width - self.rightMargin + self.margin
        yStart = self.height/5

        width = self.rightMargin - 2 * self.margin 
        length = self.height - self.bottomMargin 
        margin = width / 4.5
        self.invCellWidth  = width - 2 * margin
        self.invCellHeight = (length - 2 * margin) // self.invRows

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, app.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - yStart) / self.invCellHeight)
        col = int((x - xStart) / self.invCellWidth)
        #print(f'this is row col: {row, col}')
        
        return (row, col)

#CITATION: CREDS getCellBounds from grid-demo.py, CREDS to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getInvCellBounds(self, row, col):
        xStart = self.width - self.rightMargin + self.margin
        yStart = self.height/5

        width = self.rightMargin - 2 * self.margin 
        length = self.height - self.bottomMargin 
        margin = width / 4.5

        x0 = xStart+ margin + self.invGridWidth * col / self.invCols
        x1 = xStart+ margin + self.invGridWidth * (col+1) / self.invCols
        y0 = yStart + margin + self.invGridHeight * row / self.invRows
        y1 = yStart +margin + self.invGridHeight * (row+1) / self.invRows
        return (x0, y0, x1, y1)
    #funcion to go into instance and set it up for image loading
    
    def getIngredientImg(self, name):
        width = self.rightMargin - 2 * self.margin 
        length = self.height - self.bottomMargin 
        margin = width / 4.5
        goalWidth  = width - 2 * margin

        path = ''
        img = None
        if (isinstance(name, classes.Staples)):
            Ingredient = name
        else:
            Ingredient = CookingMode.getIngredientObject(self, name)
        #print(f'this is ingredient in getingredientimg: {Ingredient}')
        if Ingredient != None:
            path = Ingredient.path
            #keep track of howmany successful recipes you made
            if self.isCombine: 
                self.recipeCounter +=1 
        else:
            #if havent set up image for this, set default "gunk" image
            path = '/Users/az/Documents/GitHub/Chopped_Simulation/images/gunk.png'
            
        
#CITATION: ALL IMAGE LOADING CODE TAKEN FROM PIL OPTION LECTURE https://scs.hosted.panopto.com/Panopto/Pages/Auth/Login.aspx
#https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        img = self.loadImage(path)
        scaleFactor = CookingMode.findScaleFactor(self, img, goalWidth)
        img = self.scaleImage(img, scaleFactor)
                    
        return img #returns the  loaded image to store in the list in ingredientObject
    #function to set up attributes of inventory for later use
    def setUpInventory(self):
        self.invCols = 1 
        self.invRows = 5
        self.inventoryPage = [self.invCols * [None] for row in range(self.rows)]

        spot0 = CookingMode.getMidCell(self, 0, 0)
        spot1 = CookingMode.getMidCell(self, 1, 0)
        spot2 = CookingMode.getMidCell(self, 2, 0)
        spot3 = CookingMode.getMidCell(self, 3, 0)
        spot4 = CookingMode.getMidCell(self, 4, 0)

        #load the inventory into this mode
        self.inventory = list()
        self.inventory+=self.basket

        self.inventory+=self.app.shoppingMode.hand
        
        #self.ingredientObjects = list()
#        for name in self.inventory:
#            self.ingredientObjects(CookingMode.getIngredientImg(self, name)) 

        #this is the inventory that shows up on the screen, limit of 5
        self.displayInventory = [ [None, spot0], [None, spot1], [None, spot2], [None, spot3],
        [None, spot4] ]
        CookingMode.displayImagesInInventory(self)

    def displayImagesInInventory(self):
        for i in range(len(self.inventory)):
            name = self.inventory[i]
                #if i < len(self.displayInventory) - 2:
            loadedImg = CookingMode.getIngredientImg(self, name)
            self.displayInventory[i][0] = loadedImg 

#        self.inventory[0][0] = CookingMode.getIngredientImg(self, 'potato')
#        self.inventory[1][0] = CookingMode.getIngredientImg(self, 'milk')
#        self.inventory[2][0] = CookingMode.getIngredientImg(self, 'butter')
    
        #self.inventory.append([[potato], [20,20]])
        #self.inventory.append([[milk], [60,60]])
        #print(f'this IS MY cuRRENT INVNEORY: {self.inventory}')
    #helper function to find the midpoint of the cell to place image in
    def getMidCell(self, row, cell):
        x0,y0, x1, y1 = CookingMode.getInvCellBounds(self,row,cell)
        midX = (x0+x1)//2 
        midY = (y0+y1)//2

        return midX, midY 
    #heavily based on code from PIL optional lecture, link: https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4c852dc1-658a-42dc-a8c0-ac790004263c   
    def findScaleFactor(self, image, goalWidth):
        width, height = image.size 
        scaleFactor = goalWidth / width 
        return scaleFactor    

    #function to call drawCell and draw a table to contain the images it will need
    def drawInventoryTable(self, canvas):
        for row in range(self.invRows):
            for col in range(self.invCols):
                CookingMode.drawInvCell(self, canvas, row, col, 'lightgray')
#CITATION: DRAW CELL CODE FROM
    def drawInvCell(self,canvas, row, col, color):
        if (row, col) in self.outlineRowCol:
            outline = 'red'
        else:
            outline = 'gray'
        x0, y0, x1, y1 = CookingMode.getInvCellBounds(self, row, col)
        
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, width=2, outline = outline)


    def drawBoard(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                CookingMode.drawCell(self,canvas,row,col,self.board[row][col])


    #taken from my HW7, Tetris
    #function to create each cell and fill with its respective color 
    
    def drawApplianceScreen(self, canvas):
        width = 2*self.bottomMargin/3
        length = self.width - self.margin - self.rightMargin
        xStart = self.margin
        yStart = self.height-self.bottomMargin+self.margin
        canvas.create_rectangle(xStart, yStart, xStart + length, yStart + width, fill = 'skyblue')
        canvas.create_text((2*xStart+length)/2, yStart + length/35, text = f'{self.currentAppliance}')
        canvas.create_text(xStart + length - length/6, yStart + width/2, text=f'Press c to {self.currentAppliance}')
        canvas.create_text(xStart + length/6, yStart + length/35, text = 'Press x to add')
        if self.isCombine:
            canvas.create_text(xStart + length/3, yStart + width/2, text=f'You have made: {self.combination}')
            
    def drawInventoryScreen(self, canvas):
        xStart = self.width - self.rightMargin + self.margin
        yStart = self.height/5
        canvas.create_rectangle(xStart, yStart, xStart + self.invWidth, yStart + self.invLength, fill = 'pink')
        canvas.create_text((2*xStart+self.invWidth)/2, yStart + self.invLength/35, text = 'INVENTORY')

    #this check is taken from example 10 of https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def pointInInvGrid(self, x, y):
        xStart = self.width - self.rightMargin + self.margin
        yStart = self.height/5
        xEnd = xStart + self.invWidth
        yEnd = yStart + self.invLength

        # return True if (x, y) is inside the grid defined by app.
        inBounds = ((xStart <= x <= xEnd) and
                (yStart <= y <= yEnd))
        return inBounds
#CITATION: from CMU https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    def drawCell(self,canvas, row, col, color):
        x0, y0, x1, y1 = CookingMode.getCellBounds(self, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = color
                                 )

    def drawGameAI(self, canvas):
        (x0, y0, x1, y1) = CookingMode.getCellBounds(self, self.oppRow, self.oppCol)
        canvas.create_oval(x0, y0, x1, y1, fill='red')

    def drawPlayer(self, canvas):
        (x0, y0, x1, y1) = CookingMode.getCellBounds(self, self.charRow, self.charCol)
        canvas.create_oval(x0, y0, x1, y1, fill='blue')
        
    #given path of image and which row, col it should be centered in, draw image
#CITATION: SCALE IMAGE FROM https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def drawImage(self, img, midRow, midCol, grid):
        #draw image to be based on where the inventory is
        if grid == 'inventory':
            x0, x1, y0, y1 = CookingMode.getInvCellBounds(self, midRow, midCol)
            #self.invcellWidth  = self.invGridWidth / self.invcols
            scaleFactor = CookingMode.scaleImage(self, img, self.invGridWidth)

        else:
            x0, x1, y0, y1 = CookingMode.getCellBounds(self, midRow, midCol)
            scaleFactor = CookingMode.scaleImage(self, img, self.cellWidth)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(img)) 
#CITATION: convertMilli and drawTimer code based off of https://stackoverflow.com/questions/35989666/convert-milliseconds-to-hours-min-and-seconds-python
    def convertMilli(self, milli):
        seconds=(milli//1000)%60
        minutes=(milli//(1000*60))%60
        return seconds, minutes

    def drawTimer(self, canvas):
        seconds, minutes = CookingMode.convertMilli(self, self.pantryTimer)
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
        if (not CookingMode.pointInGrid(self, x, y)):
            #print('THIS IS FALSE')
            return None
        row, cell = CookingMode.getCell(self, x, y)
        #print(self.board[row][cell])
        return self.board[row][cell]
    #helper function to "place" loaed image into displayinventory, changes if user needs to display more ingredients 
    
    def placeImage(self):
        #run thru 
        for i in range(len(self.displayInventory)):
            # check that i is within currnet list of ingredients in inventory
            if i < len(self.inventory):
                ingredName = self.displayInventory[i]
                ingredName = CookingMode.getIngredientObject(self, ingredName)
                if ingredName != None:
                    loadedImg = CookingMode.getIngredientImg(self, ingredName)
                    #load default None to be image instead 
                    self.displayInventory[i][0] = loadedImg
                    #print(f'TTHIS IS DISPLAY INVNETORY {self.displayInventory}')
    #helper function to draw the currently loaded images in displayInventory
#CITATION: DRAW IMAGE FROM https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
    def drawInventoryIngredients(self, canvas):
        for i in range(len(self.displayInventory)): 
            #as long as there's the objected loaded in that inventory, proceed
            if self.displayInventory[i][0] != None:
                x, y = self.displayInventory[i][1][0], self.displayInventory[i][1][1]
                #this should be the already loaded image 
                img = self.displayInventory[i][0]
                #print(ingred)
                canvas.create_image(x, y, image = ImageTk.PhotoImage(img)) 
    def drawInstructions(self, canvas):
        canvas.create_text(self.width/2, self.height-20, text = f'Go around and click different pink boxes and select ingreds to cook!')
    def redrawAll(self, canvas):
    
        CookingMode.drawBoard(self,canvas)
        
        CookingMode.drawGameAI(self, canvas)
        CookingMode.drawPlayer(self, canvas)
        #CookingMode.setUpAppliances(self, canvas)
        CookingMode.randomizeAppliances(self, canvas)
        CookingMode.drawInventoryScreen(self, canvas)
        CookingMode.drawInventoryTable(self, canvas)
        CookingMode.drawTimer(self, canvas)
        if self.isApplianceScreen:
            CookingMode.drawApplianceScreen(self, canvas)

        #CookingMode.drawButtons(self, canvas)
        CookingMode.drawInventoryIngredients(self, canvas)
        CookingMode.drawInstructions(self, canvas)
        """
        for ingred in self.inventory:
            if ingred[0] != None:
                x, y = ingred[1][0], ingred[1][1]
                img = ingred[0][1]
                print(ingred)
                """
                #canvas.create_image(x, y, image = ImageTk.PhotoImage(img)) 
#modal app code from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
class JudgingMode(Mode):
    def appStarted(self):
        self.finalProductGameAI = self.app.cookingMode.finalDish
        self.finalProductPlayer = self.app.cookingMode.playerFinalDish
        self.playerIngredients = self.app.cookingMode.ingredientHistory
        self.gameAIIngredients = self.app.cookingMode.groceries
        self.playerWebScore = ''
        self.gameAIWebScore = ''
        print(self.gameAIIngredients)
        self.numberCalculated = 0
        self.isWinnerCalculated=False
    def keyPressed(self, event):
        #launch webScraping for opponent's dish

        if event.key == 'o':
            playerNum = web.recipeScraper(self.playerIngredients)
            self.playerWebScore = JudgingMode.calculateScore(self, playerNum)
            self.numberCalculated+=1
            #rint(self.gameAINum)
        elif event.key == 'p':
            gameAINum = web.recipeScraper(self.gameAIIngredients)
            self.gameAIWebScore = JudgingMode.calculateScore(self, gameAINum)
            self.numberCalculated+=1
        elif event.key == 'w':
            self.isWinnerCalculated = True

    def calculateScore(self, num):
        #case where there are no recipes bc combo is so bizzarre
        if num < 5: 
            webScore = 3
        #standard number of recipes, this is a complex, complete recipe
        elif 5< num < 20:
            webScore = 8
        else:
            webScore = 6 
        return webScore


    def drawPlayerInfo(self, canvas):
        canvas.create_text(self.width/4, self.height/4, text = f'{self.finalProductPlayer}', font = 'Verdana 15 bold')
        canvas.create_text(self.width/4, self.height/2.2, text ='Press o to calculate Player', font = 'Verdana 12')
        canvas.create_text(self.width/4, self.height/2, text ='PLAYER SCORE BREAKDOWN:')
        canvas.create_text(self.width/4, 4*self.height/5, text=f'SCORE IS: {self.playerWebScore}', font = 'Verdana 14 bold')
    def drawGameAIInfo(self, canvas):
        canvas.create_text(3*self.width/4, self.height/4, text = f'{self.finalProductGameAI}', font = 'Verdana 15 bold')
        canvas.create_text(3* self.width/4, self.height/2.2, text ='Press p to calculate Game AI', font = 'Verdana 12')
        canvas.create_text(3*self.width/4, self.height/2, text = 'GAME AI SCORE BREAKDOWN:')
        canvas.create_text(3*self.width/4, 4*self.height/5, text=f'SCORE IS: {self.gameAIWebScore}', font = 'Verdana 14 bold')


    def drawScreen(self, canvas):
        canvas.create_rectangle(0,0, self.width, self.height, fill = 'skyblue')
        canvas.create_text(self.width/2, self.height/6, text='JUDGING BEGINS!', font='Arial 26 bold')

    def drawWin(self,canvas):
        if self.playerWebScore > self.gameAIWebScore:
            winner = 'PLAYER'
        elif self.playerWebScore<self.gameAIWebScore:
            winner = 'GAME AI'
        else:
            winner = 'TIE! NEITHER'
        canvas.create_text(self.width/2, 5*self.height-6, text = f'{winner} WINS THE COOKING COMPETITION')
    def redrawAll(self, canvas):
        JudgingMode.drawScreen(self, canvas)
        JudgingMode.drawPlayerInfo(self, canvas)
        JudgingMode.drawGameAIInfo(self, canvas)
        if self.isWinnerCalculated:
            JudgingMode.drawWin(self, canvas)

    
class ShoppingMode(Mode):
    def appStarted(self):
        self.rows = 4
        self.cols = 4 
        self.margin = self.width/5
        self.gridWidth  = self.width - 2 * self.margin
        self.gridHeight = self.height - 2* self.margin
        self.board = [self.cols * ['lightgray'] for row in range(self.rows)]
        #self.fridge = list()
        self.shoppingCart = list()
        self.fridge = list()
        ShoppingMode.setUpFridge(self)
        self.loadedImgList = list()
        #load images into list for later use
        for i in range(len(self.fridge)):
            name = self.fridge[i].name
            self.loadedImgList.append(ShoppingMode.getIngredientImg(self, name))
        self.currentSelect = list() 
        self.hand = list() 
        shoppingScreenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/shoppingscreen.png'  
        self.shoppingScreen = self.loadImage(shoppingScreenPath)
        shelfPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/shelf.png'
        self.shelf = self.loadImage(shelfPath)

    def getIngredientObject(self, ingredient):
        for Ingredient in self.IngredientObjects:
            if Ingredient.name == ingredient:
                return Ingredient 
    def setUpFridge(self):
        """
        self.board = list()
        for row in range(self.rows):
            currCol = list()
            for col in range(self.cols): 
                location = ShoppingMode.getMidCell(self, row, col)
                currCol.append(['lightgray', None, location])
            self.board.append(currCol)
"""
        (self.cookbooks, self.basket, self.Person, self.Opponent, self.Appliances, self.IngredientObjects) = (self.app.basketMode.cookbooks, self.app.basketMode.basket, self.app.basketMode.Person,
                                                                                    self.app.basketMode.Opponent, self.app.basketMode.Appliances, self.app.basketMode.Ingredients)

        self.shoppingCart+= self.basket 
        
       #self.fridge = [self.cols * [None] for row in range(self.rows)]
        self.ingredientList = classes.ingredientList(self.cookbooks[0])
        #print(self.ingredientList)
    
        for i in range(self.rows*self.cols): 
            if i < len(list(self.ingredientList)):
                ingredName = list(self.ingredientList)[i]
                Ingredient = ShoppingMode.getIngredientObject(self, ingredName)
                #print(Ingredient)
                #print()
                self.fridge.append(Ingredient)
        
        #print(self.fridge)
        """        
        spot0 = ShoppingMode.getMidCell(self, 0, 0)
        spot1 = ShoppingMode.getMidCell(self, 1, 0)
        spot2 = ShoppingMode.getMidCell(self, 2, 0)
        spot3 = ShoppingMode.getMidCell(self, 3, 0)
        spot4 = ShoppingMode.getMidCell(self, 4, 0)
    
        self.fridge = [ [None, spot0], [None, spot1], [None, spot2], [None, spot3],
        [None, spot4] ]
        """
    def getMidCell(self, row, cell):
        x0,y0, x1, y1 = ShoppingMode.getCellBounds(self,row,cell)
        midX = (x0+x1)//2 
        midY = (y0+y1)//2

        return midX, midY 
        #converts row, col to list 
    def getIndex(self, row, col):
        index = ((row * self.rows) + col)
        return index 
    def mousePressed(self, event):
        #check if mouse is pressed within the grid 
        mouseX, mouseY = event.x, event.y
        row, col = ShoppingMode.getCell(self, mouseX, mouseY)
        if not (row, col) == (-1, -1):
            #print('added!')
            self.currentSelect.append((row, col))
            index = ShoppingMode.getIndex(self, row, col)
            self.hand.append(self.fridge[index])
            
    def drawScreen(self, canvas):
        canvas.create_rectangle(0,0, self.width, self.height, fill = 'pink')
        canvas.create_text(self.width/2, self.height/8, text='GATHER YOUR INGREDIENTS!', font='Arial 26 bold')
        canvas.create_text(self.width/2, 6.7* self.height/8, text = 'You must create a dish incorporating these basket ingredients!')
        canvas.create_text(self.width/2, 7*self.height/8, text = 'Press n to move on to cooking mode')
        canvas.create_text(self.width/2, 7.5*self.height/8, text=f'{self.basket}')
    def keyPressed(self, event):
        #go to next mode 
        if event.key == 'n':
            #add all currently selected to your inventory 
            self.app.setActiveMode(self.app.cookingMode)

    def drawBoard(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                ShoppingMode.drawCell(self,canvas,row,col,self.board[row][col])
                
    def drawCell(self,canvas, row, col, color):
        x0, y0, x1, y1 = ShoppingMode.getCellBounds(self, row, col)
        imgY = y1 - self.height/22
        imgX = self.width/2 
        #if box is currently selected, change outline
        if (row, col) in self.currentSelect:
            outline = 'red'
            width = 3
        else:
            outline = ''
            width=0
        canvas.create_image(imgX, imgY, image = ImageTk.PhotoImage(self.shelf))
    
        canvas.create_rectangle(x0, y0, x1, y1, fill = '', outline = outline, width = width
                                 )

    #heavily based on code from PIL optional lecture, link: https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4c852dc1-658a-42dc-a8c0-ac790004263c   
    def findScaleFactor(self, image, goalWidth):
        width, height = image.size 
        scaleFactor = goalWidth / width 
        return scaleFactor    
    
    def getCellBounds(self, row, col):
        x0 = self.margin + self.gridWidth * col / self.cols
        x1 = self.margin + self.gridWidth * (col+1) / self.cols
        y0 = self.margin + self.gridHeight * row / self.rows
        y1 = self.margin + self.gridHeight * (row+1) / self.rows
        return (x0, y0, x1, y1)
    def getRowColFrom1D(self, list, index):
        row = index//self.cols 
        col = index%self.rows
        return row, col 
    def getIngredientImg(self, name):
        """
        width = self.rightMargin - 2 * self.margin 
        length = self.height - self.bottomMargin 
        margin = width / 4.5
        goalWidth  = width - 2 * margin
"""
        x0, y0, x1, y1 = ShoppingMode.getCellBounds(self, 0, 0)
        goalWidth = x1-x0
        
        path = ''
        img = None
        
        Ingredient = ShoppingMode.getIngredientObject(self, name)
        path = Ingredient.path 
        img = self.loadImage(path)
        scaleFactor = ShoppingMode.findScaleFactor(self, img, goalWidth)
        img = self.scaleImage(img, scaleFactor)

        return img #returns the loaded image to store in the list in inventory
   #creds to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by app.
        return ((self.margin <= x <= self.width-self.margin) and
                (self.margin <= y <= self.height-self.margin))

   #creds to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCell(self, x, y):
        if not ShoppingMode.pointInGrid(self, x, y):
            return (-1, -1)
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        gridWidth  = self.width - 2*self.margin
        gridHeight = self.height - 2*self.margin
        cellWidth  = gridWidth / self.cols
        cellHeight = gridHeight / self.rows

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, app.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - self.margin) / cellHeight)
        col = int((x - self.margin) / cellWidth)

        return (row, col)

    def drawImageScreen(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.shoppingScreen))
    def redrawAll(self, canvas):
        #ShoppingMode.drawScreen(self, canvas)
        ShoppingMode.drawImageScreen(self, canvas)
        ShoppingMode.drawBoard(self, canvas)
        """
        for ingred in self.fridge:
            #as long as there an image
            if ingred != None:
                x,y = ingred[0], ingred[1]
                img = ingred[1]
                canvas.create_image(x, y , image = ImageTk.PhotoImage(img))
        """
        for ingredIndex in range(len(self.fridge)):
            ingred = self.fridge[ingredIndex] #returningredient object
            path = ingred.path
            row, col = ShoppingMode.getRowColFrom1D(self, self.fridge, ingredIndex)
            #print(f'{ingred}: {row, col}')
            x, y = ShoppingMode.getMidCell(self, row, col)
            
            #get loaded img from list 
            img = self.loadedImgList[ingredIndex]

            #reset img to be scale factor 
            canvas.create_image(x, y, image = ImageTk.PhotoImage(img)) 
                #x, y = ingred[1][0], ingred[1][1]
                #img = ingred[0][1]
                #

#since tp2: new classes 
#modal app code from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
#KNIFE IMAGE: https://www.google.com/url?sa=i&url=https%3A%2F%2Fstreak.club%2Fp%2F24520%2Fknife-by-notapollogising&psig=AOvVaw0W2y9LLiM9dUCHHf33DfJp&ust=1607356088117000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOinhqXaue0CFQAAAAAdAAAAABAD
class TitleMode(Mode):
    def appStarted(self):
        #citation: image from here https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.bravespacebiz.com%2Fblog%2F2017%2F9%2F22%2Fshow-up-or-get-chopped&psig=AOvVaw3JPc_fH-7rRKOdpFiLx63d&ust=1607354864940000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMjGuNTVue0CFQAAAAAdAAAAABAI
        #self.logo = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/chopped.png')
        self.cookingScreen = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingScreen.png')
        
    def keyPressed(self, event):
        if event.key == 'Space':
            self.app.setActiveMode(self.app.basketMode)
            

    
    def drawTitleScreen(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = 'orange')
        canvas.create_text(self.width/2, self.height/8, font = 'Verdana 24 bold', text='WELCOME TO THE CHOPPED SIMULATION')
        canvas.create_text(self.width/2, 2* self.height/3, text = 'Press space to start.')
        #canvas.create_image(self.width/2, self.height/3, image = ImageTk.PhotoImage(self.logo)) 
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.cookingScreen))

    def redrawAll(self, canvas):
        TitleMode.drawTitleScreen(self, canvas)

class BasketMode(Mode):
    def appStarted(self):
        #call your ingedients!! EVERYTHING MUST REFEENCE HERE FO INITIAL BASKET CALL! 
        self.cookbooks, self.basket, self.Person, self.Opponent, self.Appliances, self.Ingredients = classes.setUpObjects()
        #call its basket function
        self.basket = classes.randomizeBasket(self.cookbooks[0])
        self.isDisplayBasket = False
        #CITATION: self created on canva
        self.screenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/basketScreen.png'
        self.screenImg = self.loadImage(self.screenPath)
        self.basketLoadedIngredients = list()
        BasketMode.loadBasketIngreds(self)
    def keyPressed(self, event):
        if event.key == 'Space':
            self.isDisplayBasket = True
        elif event.key == 'n':
            self.app.setActiveMode(self.app.shoppingMode)

    def getIngredientObject(self, item):
        for Ingredient in self.Ingredients:
            if Ingredient.name == item:
                return Ingredient 
    
    def loadBasketIngreds(self):
        for item in self.basket:
            ingredObject = BasketMode.getIngredientObject(self, item)
            path = ingredObject.path 
            self.ingredImg = self.loadImage(path)
            #print(self.ingredImg)
            self.scaledImg = self.scaleImage(self.ingredImg, self.width/6)
            self.basketLoadedIngredients.append(self.scaledImg)

    def drawScreen(self,canvas):
        canvas.create_rectangle(0,0, self.width, self.height, fill = 'pink')
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.screenImg))
    #function to go thru basket loaded images and draw it 
    def drawBasket(self, canvas):
        #for item in self.basket:
     
        canvas.create_image(self.width/4, self.height/2, image = ImageTk.PhotoImage(self.basketLoadedIngredients[0]))
        canvas.create_image(3*self.width/4, self.height/2, image = ImageTk.PhotoImage(self.basketLoadedIngredients[1]))

    """
       i = 0 
        gap = self.width/3
        for item in self.basketLoadedIngredients:
            x  = gap + i*gap
    """
    def redrawAll(self, canvas):
        BasketMode.drawScreen(self, canvas)
        BasketMode.drawBasket(self, canvas)
        


class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleMode = TitleMode()
        app.shoppingMode = ShoppingMode()
        app.cookingMode = CookingMode()
        app.judgingMode = JudgingMode()
        app.setActiveMode(app.titleMode)
        app.basketMode = BasketMode()
        #app.timerDelay = 500

app = MyModalApp(width = 600, height = 600)




"""


    def drawButtons(self, canvas):
        xStart = self.width - self.rightMargin + self.margin
        yStart = self.height/5

        width = self.rightMargin - 2 * self.margin 
        length = self.height - self.bottomMargin 

        #center button in middle
        width = width/2 
        xCenter += width
        yCenter = self.height - self.yStart - self.yStart//2

        canvas.create_rectangle(xStart, yStart, xEnd, yEnd, fill = 'blue')


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
    
""" 