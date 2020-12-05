#TO DO BY TOMRROW: 
#ANIMATE GAME AI to go thru the necessary path! 
#BE ABLE TO "COMBINE" ingredients into AN APPLIANCE
    #HARDCODE SOME IDEAL COMBINATIONS
    #add to a list that keeps track of ignredients 
    #maybe scale down on number of basket ingredients to just one

#DO WEBSCRAPING
    #access the properties of a website
    #find the ingredients

    #back up plan: look up those ingredients in google and see how mny hits you get back
#draw screen where it presents the final product 
from cmu_112_graphics import *
import classesOfFood as classes 
import webScraping as web
#recurisve function to get from row, col A to row, col B

class CookingMode(Mode):
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
        #TO DO: NEED TO CHECK IF IT"S LEGAL 
        #is this backtracking? 

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
        print((xDir, yDir))

        return CookingMode.generatePath(row0 + xDir, col0 + yDir, row1, col1, moveList)

    #set up game AI properties for use throughout code
    def setUpGameAI(self):
        self.Opponent.randomizeFinalProduct()
        self.finalDish = self.Opponent.finalDish
        self.Opponent.generateApplianceAndGroceriesList()
        self.applianceList = self.Opponent.applianceList
        self.moveList = list()
        CookingMode.gameAIPath(self)
        print(f'this is MOVE LIST: {self.moveList}')
        self.groceries = self.Opponent.groceries
        print(f'this is final dish: {self.finalDish}')
        print(f'this is final appliance list: {self.applianceList}')
        print(f'this is final gtoceries list: {self.groceries}')

        #print(f'this is FINAL DISH: {finalDish}')

    #goes thru all the appliances the gameAI needs to reach
    def gameAIPath(self):
        appliances = self.applianceList
        firstAppliance = appliances[0]
        firstMoveList = list()
        firstAppRow, firstAppCol = self.accessPoints[firstAppliance][0], self.accessPoints[firstAppliance][1]
        #print(f'TESTING GAME AI PATH: {firstAppRow, firstAppCol}')
        self.moveList+=(CookingMode.generatePath(self.oppRow, self.oppCol, firstAppRow, firstAppCol, firstMoveList))
        #go thru every pair:
        for applianceIndex in range(len(appliances)-1):
            appliance = appliances[applianceIndex]
            nextAppliance = appliances[applianceIndex+1]
            row0, col0 = self.accessPoints[appliance][0], self.accessPoints[appliance][1]
            row1, col1 = self.accessPoints[nextAppliance][0], self.accessPoints[nextAppliance][1]
            print(f'this is {row1, col1}')
            #list to hold recursive results
            currMoveList = list()
            print('hello')
            self.moveList+=(CookingMode.generatePath(row0, col0, row1, col1, currMoveList))
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


    def isLegal(self, row, col):
        if self.board[row][col] == 'white':
            return True
        else:
            return False  
    #oveList = list()
    #print(generatePath(0, 0, 4, 5, moveList))
    #keeps track of Mouse pressed 
    def mousePressed(self, event):
        mouseX, mouseY = event.x, event.y 

        #need some kind of case in case it clicks outside the grid 
        color = CookingMode.getColor(self, mouseX, mouseY)
        print(CookingMode.getCell(self, mouseX, mouseY))
        print(color)
        if color !=None and color=='pink':
            (row, col) = CookingMode.getCell(self, mouseX, mouseY)
            currLocation = list((row, col))
            for appliance, location in self.applianceDict.items():
                #print(f'this is cURRENT LOCATION: {currLocation}')
                #print(location)
                if location == currLocation:
                    #print('ur getting here')
                    self.currentAppliance = appliance
                    #print(self.currentAppliance)
            self.isApplianceScreen = True 

            #trigger and open the appliance menu 
        else: 
            #print('im geting here')
            row, col = CookingMode.getInvCell(self, mouseX, mouseY)
            if (row, col) != (-1, -1):
                
                print(self.outlineRowCol)
                #add the ingredientPath of current selected to current selected hand
                #don't add duplicates
                if not self.inventory[row][0] in self.currentSelect:
                    print(f'ths is {self.inventory[row][0]}')
                    if self.inventory[row][0] != None:
                        self.currentSelect.append(self.inventory[row][0])
                        self.outlineRowCol.append((row, col))

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
        
        self.timerDelay = 400
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
        self.cookbooks, self.basket, self.Person, self.Opponent, self.Appliances, self.Ingredients = classes.setUpObjects()
        
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
        CookingMode.setUpInventory(self)
        CookingMode.setUpAppliances(self)
        self.outlineRowCol = list()
        CookingMode.setUpGameAI(self)
        
        self.basket = classes.randomizeBasket(self.cookbooks[0])

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
    
    def setUpAppliances(self):
        self.accessPoints = { 'mix': [1, 3], 
        'bake': [1, 9], 
        'blend': [7, 13],
        'saute': [13, 9],
        'stack': [13, 3]
        #'PLATING': [7, 0],
        }
        self.applianceDict = { 'mix': [0, 3], 
        'bake': [0, 9], 
        'blend': [7, 14],
        'saute': [14, 9],
        'stack': [14, 3]
        #'PLATING': [7, 0],
        }

        CookingMode.setHorizontal(self, 5, 0, 0,'whisk')
        CookingMode.setHorizontal(self, 5, 0, 6, 'oven')        
        CookingMode.setHorizontal(self, 5, self.rows-1, 0, 'blender')        
        CookingMode.setHorizontal(self, 5, self.rows-1, 6, 'stovetop')        
        #CookingMode.setVertical(self, 5, 4, 0, 'plating')
        CookingMode.setVertical(self, 5, 4, self.cols-1, 'stack')


#            for i in range(Appliance.cellsInLength):
#                row = gap * applianceCount + i 
#                col = (self.cols//2 - Appliance.cellsInLength//2) + i 
#                if i == Appliance.cellsInLength//2:
#                    color = 'pink'
#                else:
#                    color = 'gray' 

#                self.board[row][col] = color
#            applianceCount +=1     



    def keyPressed(self, event):
        if event.key =='Up': 
            if CookingMode.isLegal(self, self.charRow -1, self.charCol):
                self.charRow -=1 
            else:
                print('NOT HERE')
        elif event.key == 'Down': 
            if CookingMode.isLegal(self, self.charRow +1, self.charCol):
                self.charRow += 1
            else:
                print('nah')
        elif event.key == 'Left': 
            if CookingMode.isLegal(self, self.charRow, self.charCol-1):
                self.charCol-= 1 
        elif event.key == 'Right': 
            if CookingMode.isLegal(self, self.charRow, self.charCol+1):
                self.charCol += 1
        elif event.key == 'c':
            if self.isApplianceScreen:
                #self.isCombine = True
                if len(self.currentSelect) >= 2:
                    self.combination = CookingMode.combineIngredients(self)
                    self.isCombine = True
                    print('combined!')
        #go to nex mode
        elif event.key == 'n':
            self.app.setActiveMode(self.app.judgingMode)
            
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

    def combineIngredients(self):
        ingredientNames = []
        for item in self.currentSelect:
            ingredientNames.append(item[0])
        firstIngred = ingredientNames[0]
        secondIngred = ingredientNames[1:]
        secondIngredObj = list()
        firstIngredObj = CookingMode.getIngredientObject(self, firstIngred)
        for otherIngred in secondIngred:
            secondIngredObj.append(CookingMode.getIngredientObject(self, otherIngred))
        combination = firstIngredObj.combine(secondIngredObj, 'saute')
        return combination
        #print(ingredientNames)s
    def getIngredientObject(self, ingredient):
        for Ingredient in self.Ingredients:
            if Ingredient.name == ingredient:
                return Ingredient 

    def timerFired(self):
        if self.waitTime ==-1:
            #moveNormally
            CookingMode.moveGameAI(self)
        elif self.waitTime ==0:
            self.moveNum +=1
            CookingMode.moveGameAI(self)
        else: #don't move 
            self.waitTime -=100
        if self.pantryTimer>=0:
            self.pantryTimer -=100
        else:
            self.isTimeUp = True
        
        #run combining methods if ingredients are successfully combined
        #if self.isCombine: 
        #    CookingMode.combineIngredients(self)

            
    def moveGameAI(self):
        #only move if haven't reached goal state
        if not self.moveNum == len(self.moveList): 
            #print(f'THIS IS moveLIST IN MOVE GAME AI: {self.moveList}')
            if not self.moveList == None:
                currMove = self.moveList[self.moveNum]
                if currMove == 'stop':
                    self.waitTime = 500
                else:
                    self.oppRow += currMove[0]
                    self.oppCol += currMove[1]
                    self.moveNum += 1
            

    # getCellBounds from grid-demo.py
    #creds to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellBounds(self, row, col):
        x0 = self.margin + self.gridWidth * col / self.cols
        x1 = self.margin + self.gridWidth * (col+1) / self.cols
        y0 = self.margin + self.gridHeight * row / self.rows
        y1 = self.margin + self.gridHeight * (row+1) / self.rows
        return (x0, y0, x1, y1)
   #creds to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
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
    #based off of https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
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

    # getCellBounds from grid-demo.py
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
        
        Ingredient = CookingMode.getIngredientObject(self, name)
        path = Ingredient.path 
        img = self.loadImage(path)
        scaleFactor = CookingMode.findScaleFactor(self, img, goalWidth)
        img = self.scaleImage(img, scaleFactor)
                
        return name, img #returns the name, loaded image to store in the list in inventory
    #function to set up attributes of inventory for later use
    def setUpInventory(self):
        self.invCols = 1 
        self.invRows = 5
        self.inventoryPage = [self.invCols * [None] for row in range(self.rows)]
        #self.inventory = list()
        #self.inventory.append(classes.Potato)
        #write this into a function
        """

        potatoPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/potato.png'
        potato = self.loadImage(potatoPath)
        scaleFactor1 = CookingMode.findScaleFactor(self, potato, goalWidth)
        potato = self.scaleImage(potato, scaleFactor1)

        milkPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/milk.png'
        milk = self.loadImage(milkPath)
        scaleFactor2 = CookingMode.findScaleFactor(self, milk, goalWidth)
        milk = self.scaleImage(milk, scaleFactor2)
"""
        spot0 = CookingMode.getMidCell(self, 0, 0)
        spot1 = CookingMode.getMidCell(self, 1, 0)
        spot2 = CookingMode.getMidCell(self, 2, 0)
        spot3 = CookingMode.getMidCell(self, 3, 0)
        spot4 = CookingMode.getMidCell(self, 4, 0)
    
        self.inventory = [ [None, spot0], [None, spot1], [None, spot2], [None, spot3],
        [None, spot4] ]

        self.inventory[0][0] = CookingMode.getIngredientImg(self, 'potato')
        self.inventory[1][0] = CookingMode.getIngredientImg(self, 'milk')
        self.inventory[2][0] = CookingMode.getIngredientImg(self, 'butter')

        #self.inventory.append([[potato], [20,20]])
        #self.inventory.append([[milk], [60,60]])
        print(self.inventory)
    #helper function to find the midpoint of the cell to place image in
    def getMidCell(self, row, cell):
        x0,y0, x1, y1 = CookingMode.getInvCellBounds(self,row,cell)
        midX = (x0+x1)//2 
        midY = (y0+y1)//2

        return midX, midY 
    
    #function to call drawCell and draw a table to contain the images it will need
    def drawInventoryTable(self, canvas):
        for row in range(self.invRows):
            for col in range(self.invCols):
                CookingMode.drawInvCell(self, canvas, row, col, 'lightgray')

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
        canvas.create_text(xStart + length - length/6, yStart + width/2, text=f'Press c to cook')
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
        
    #taken from 112 Website
    def getCachedPhotoImage(self, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

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
        print(self.board[row][cell])
        return self.board[row][cell]
    def redrawAll(self, canvas):
    
        CookingMode.drawBoard(self,canvas)
        
        CookingMode.drawGameAI(self, canvas)
        CookingMode.drawPlayer(self, canvas)
        #CookingMode.setUpAppliances(self, canvas)
        CookingMode.drawInventoryScreen(self, canvas)
        CookingMode.drawInventoryTable(self, canvas)
        CookingMode.drawTimer(self, canvas)
        if self.isApplianceScreen:
            CookingMode.drawApplianceScreen(self, canvas)

        #CookingMode.drawButtons(self, canvas)
        #CookingMode.drawIngredientsInInventoryScreen(self, canvas)
        for ingred in self.inventory:
            if ingred[0] != None:
                x, y = ingred[1][0], ingred[1][1]

                img = ingred[0][1]
                canvas.create_image(x, y, image = ImageTk.PhotoImage(img)) 
#modal app code from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
class JudgingMode(Mode):
    def appStarted(self):
        self.finalProductGameAI = self.app.cookingMode.finalDish
    def keyPressed(self, event):
        #launch webScraping for opponent's dish
        finalProduct = ['potatoes', 'milk', 'butter']

        if event.key == 'o':
            self.gameAINum = web.recipeScraper(finalProduct)
            print(self.gameAINum)
        elif event.key == 'p':
            self.playerNum = web.recipeScraper(finalProduct)
    def drawPlayerInfo(self, canvas):
        canvas.create_text(self.width/4, self.height/2.2, text ='Press o to calculate Player', font = 'Verdana 12')
        canvas.create_text(self.width/4, self.height/2, text ='PLAYER SCORE BREAKDOWN:')
    def drawGameAIInfo(self, canvas):
        canvas.create_text(3*self.width/4, self.height/4, text = f'{self.finalProductGameAI}', font = 'Verdana 15 bold')
        canvas.create_text(3* self.width/4, self.height/2.2, text ='Press p to calculate Game AI', font = 'Verdana 12')
        canvas.create_text(3*self.width/4, self.height/2, text = 'GAME AI SCORE BREAKDOWN:')
    def drawScreen(self, canvas):
        canvas.create_rectangle(0,0, self.width, self.height, fill = 'skyblue')
        canvas.create_text(self.width/2, self.height/6, text='JUDGING BEGINS!', font='Arial 26 bold')

    def redrawAll(self, canvas):
        JudgingMode.drawScreen(self, canvas)
        JudgingMode.drawPlayerInfo(self, canvas)
        JudgingMode.drawGameAIInfo(self, canvas)

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

    def getIngredientObject(self, ingredient):
        for Ingredient in self.Ingredients:
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
        self.cookbooks, self.basket, self.Person, self.Opponent, self.Appliances, self.Ingredients = classes.setUpObjects()
        self.shoppingCart+= self.basket 
        
       #self.fridge = [self.cols * [None] for row in range(self.rows)]
        self.ingredientList = classes.ingredientList(self.cookbooks[0])
        print(self.ingredientList)
    
        for i in range(self.rows*self.cols): 
            if i < len(list(self.ingredientList)):
                ingredName = list(self.ingredientList)[i]
                Ingredient = ShoppingMode.getIngredientObject(self, ingredName)
                print(Ingredient)
                print()
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
    def mousePressed(self, event):
        #check if mouse is pressed within the grid 
        
    def drawScreen(self, canvas):
        canvas.create_rectangle(0,0, self.width, self.height, fill = 'pink')
        canvas.create_text(self.width/2, self.height/8, text='GATHER YOUR INGREDIENTS!', font='Arial 26 bold')
        canvas.create_text(self.width/2, 6.7* self.height/8, text = 'You must create a dish incorporating these basket ingredients!')
        canvas.create_text(self.width/2, 7.5*self.height/8, text=f'{self.basket}')
    def keyPressed(self, event):
        #go to next mode 
        if event.key == 'n':
            self.app.setActiveMode(self.app.cookingMode)

    def drawBoard(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                ShoppingMode.drawCell(self,canvas,row,col,self.board[row][col])
                
    def drawCell(self,canvas, row, col, color):
        x0, y0, x1, y1 = ShoppingMode.getCellBounds(self, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = color
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
    def redrawAll(self, canvas):
        ShoppingMode.drawScreen(self, canvas)
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
            print(f'{ingred}: {row, col}')
            x, y = ShoppingMode.getMidCell(self, row, col)
            
            #get loaded img from list 
            img = self.loadedImgList[ingredIndex]

            #reset img to be scale factor 
            canvas.create_image(x, y, image = ImageTk.PhotoImage(img)) 
            #print(ingred)
                #x, y = ingred[1][0], ingred[1][1]
                #img = ingred[0][1]
                #
class MyModalApp(ModalApp):
    def appStarted(app):
        app.shoppingMode = ShoppingMode()
        app.cookingMode = CookingMode()
        app.judgingMode = JudgingMode()
        app.setActiveMode(app.shoppingMode)

        app.timerDelay = 500
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