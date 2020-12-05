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
    #set up game AI properties for use throughout code
    def setUpGameAI(self):
        self.Opponent.randomizeFinalProduct()
        self.finalDish = self.Opponent.finalDish
        self.Opponent.generateApplianceAndGroceriesList()
        self.applianceList = self.Opponent.applianceList
        self.moveList = list()
        MyApp.gameAIPath(self)
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
        firstAppRow, firstAppCol = self.applianceDict[firstAppliance][0], self.applianceDict[firstAppliance][1]
        #print(f'TESTING GAME AI PATH: {firstAppRow, firstAppCol}')
        self.moveList+=(MyApp.generatePath(self.oppRow, self.oppCol, firstAppRow, firstAppCol, firstMoveList))
        #go thru every pair:
        for applianceIndex in range(len(appliances)):
            if not applianceIndex == len(appliances)-1: #if not at the last index
                appliance = appliances[applianceIndex]
                nextAppliance = appliances[applianceIndex+1]
                row0, col0 = self.applianceDict[appliance][0], self.applianceDict[appliance][1]
                row1, col1 = self.applianceDict[nextAppliance][0], self.applianceDict[nextAppliance][1]
                #list to hold recursive results
                currMoveList = list()
                self.moveList+=(MyApp.generatePath(row0, col0, row1, col1, currMoveList))
                self.moveList+=['stop']
                applianceIndex+=1 
            #if starting at the list, start accumulating moves with the game Ai's initial starting row, col
            #if applianceIndex == 0: 
            #    row0, col0 = self.oppRow, self.oppCol
            #    row1, col1 = self.applianceDict[appliance][0], self.applianceDict[appliance][1]
            #else:
            #    nextAppliance = appliances[applianceIndex+1]
            #    row0, col0 = self.applianceDict[appliance][0], self.applianceDict[appliance][1]
            #    row1, col1 = self.applianceDict[nextAppliance][0], self.applianceDict[nextAppliance][1]
            #currentMoveList = list()
            #self.moveList+=(MyApp.generatePath(row0, col0, row1, col1, currentMoveList))


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
        color = MyApp.getColor(self, mouseX, mouseY)
        print(MyApp.getCell(self, mouseX, mouseY))
        print(color)
        if color !=None and color=='pink':
            (row, col) = MyApp.getCell(self, mouseX, mouseY)
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
            row, col = MyApp.getInvCell(self, mouseX, mouseY)
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
        
        self.timerDelay = 250
        #taken from my HW7 Tetris homework
        #keep track which parts of board are filled
        self.board = [self.cols * ['white'] for row in range(self.rows)]
        self.waitTime = -1
        self.oppRow = 4 
        self.oppCol = 0 

        #self.goalRow = 5
        #self.goalCol = 5 
        #call helper function for list of moves it will need to take
        #self.moves = MyApp.generatePath(self.oppRow, self.oppCol, self.goalRow, self.goalCol, [])
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
        MyApp.setUpInventory(self)
        MyApp.setUpAppliances(self)
        self.outlineRowCol = list()
        self.currentAppliance = ''
        MyApp.setUpGameAI(self)
        
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
        self.applianceDict = { 'mix': [0, 3], 
        'bake': [0, 9], 
        'blend': [7, 14],
        'saute': [14, 9],
        'stack': [14, 3]
        #'PLATING': [7, 0],
        }

        MyApp.setHorizontal(self, 5, 0, 0,'whisk')
        MyApp.setHorizontal(self, 5, 0, 6, 'oven')        
        MyApp.setHorizontal(self, 5, self.rows-1, 0, 'blender')        
        MyApp.setHorizontal(self, 5, self.rows-1, 6, 'stovetop')        
        #MyApp.setVertical(self, 5, 4, 0, 'plating')
        MyApp.setVertical(self, 5, 4, self.cols-1, 'stack')


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
            if MyApp.isLegal(self, self.charRow -1, self.charCol):
                self.charRow -=1 
            else:
                print('NOT HERE')
        elif event.key == 'Down': 
            if MyApp.isLegal(self, self.charRow +1, self.charCol):
                self.charRow += 1
            else:
                print('nah')
        elif event.key == 'Left': 
            if MyApp.isLegal(self, self.charRow, self.charCol-1):
                self.charCol-= 1 
        elif event.key == 'Right': 
            if MyApp.isLegal(self, self.charRow, self.charCol+1):
                self.charCol += 1
        elif event.key == 'c':
            if self.isApplianceScreen:
                #self.isCombine = True
                if len(self.currentSelect) >= 2:
                    self.combination = MyApp.combineIngredients(self)
                    self.isCombine = True
                    print('combined!')
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

    def combineIngredients(self):
        ingredientNames = []
        for item in self.currentSelect:
            ingredientNames.append(item[0])
        firstIngred = ingredientNames[0]
        secondIngred = ingredientNames[1:]
        secondIngredObj = list()
        firstIngredObj = MyApp.getIngredientObject(self, firstIngred)
        for otherIngred in secondIngred:
            secondIngredObj.append(MyApp.getIngredientObject(self, otherIngred))
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
            MyApp.moveGameAI(self)
        elif self.waitTime ==0:
            self.moveNum +=1
            MyApp.moveGameAI(self)
        else: #don't move 
            self.waitTime -=100
        if self.pantryTimer>=0:
            self.pantryTimer -=100
        else:
            self.isTimeUp = True
        
        #run combining methods if ingredients are successfully combined
        #if self.isCombine: 
        #    MyApp.combineIngredients(self)

            
    def moveGameAI(self):
        #only move if haven't reached goal state
        if not self.moveNum == len(self.moveList) -1: 
            print(f'THIS IS moveLIST IN MOVE GAME AI: {self.moveList}')
            if not self.moveList == None:
                currMove = self.moveList[self.moveNum]
                if currMove == 'stop':
                    self.waitTime = 500
                else:
                    self.oppRow += currMove[0]
                    self.oppCol += currMove[1]
                    self.moveNum += 1
            

    # getCellBounds from grid-demo.py
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
        if (not MyApp.pointInInvGrid(self, x, y)):
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
        
        Ingredient = MyApp.getIngredientObject(self, name)
        path = Ingredient.path 
        img = self.loadImage(path)
        scaleFactor = MyApp.findScaleFactor(self, img, goalWidth)
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
        scaleFactor1 = MyApp.findScaleFactor(self, potato, goalWidth)
        potato = self.scaleImage(potato, scaleFactor1)

        milkPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/milk.png'
        milk = self.loadImage(milkPath)
        scaleFactor2 = MyApp.findScaleFactor(self, milk, goalWidth)
        milk = self.scaleImage(milk, scaleFactor2)
"""
        spot0 = MyApp.getMidCell(self, 0, 0)
        spot1 = MyApp.getMidCell(self, 1, 0)
        spot2 = MyApp.getMidCell(self, 2, 0)
        spot3 = MyApp.getMidCell(self, 3, 0)
        spot4 = MyApp.getMidCell(self, 4, 0)
    
        self.inventory = [ [None, spot0], [None, spot1], [None, spot2], [None, spot3],
        [None, spot4] ]

        self.inventory[0][0] = MyApp.getIngredientImg(self, 'potato')
        self.inventory[1][0] = MyApp.getIngredientImg(self, 'milk')
        self.inventory[2][0] = MyApp.getIngredientImg(self, 'butter')

        #self.inventory.append([[potato], [20,20]])
        #self.inventory.append([[milk], [60,60]])
        print(self.inventory)
    #helper function to find the midpoint of the cell to place image in
    def getMidCell(self, row, cell):
        x0,y0, x1, y1 = MyApp.getInvCellBounds(self,row,cell)
        midX = (x0+x1)//2 
        midY = (y0+y1)//2

        return midX, midY 
    
    #function to call drawCell and draw a table to contain the images it will need
    def drawInventoryTable(self, canvas):
        for row in range(self.invRows):
            for col in range(self.invCols):
                MyApp.drawInvCell(self, canvas, row, col, 'lightgray')

    def drawInvCell(self,canvas, row, col, color):
        if (row, col) in self.outlineRowCol:
            outline = 'red'
        else:
            outline = 'gray'
        x0, y0, x1, y1 = MyApp.getInvCellBounds(self, row, col)
        
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, width=2, outline = outline)


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
    def findScaleFactor(self, image, goalWidth):
        width, height = image.size 
        scaleFactor = goalWidth / width 
        return scaleFactor    
    
    #given path of image and which row, col it should be centered in, draw image

    def drawImage(self, img, midRow, midCol, grid):
        #draw image to be based on where the inventory is
        if grid == 'inventory':
            x0, x1, y0, y1 = MyApp.getInvCellBounds(self, midRow, midCol)
            #self.invcellWidth  = self.invGridWidth / self.invcols
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
            #print('THIS IS FALSE')
            return None
        row, cell = MyApp.getCell(self, x, y)
        print(self.board[row][cell])
        return self.board[row][cell]
    def redrawAll(self, canvas):
    
        MyApp.drawBoard(self,canvas)
        
        MyApp.drawGameAI(self, canvas)
        MyApp.drawPlayer(self, canvas)
        #MyApp.setUpAppliances(self, canvas)
        MyApp.drawInventoryScreen(self, canvas)
        MyApp.drawInventoryTable(self, canvas)
        MyApp.drawTimer(self, canvas)
        if self.isApplianceScreen:
            MyApp.drawApplianceScreen(self, canvas)

        #MyApp.drawButtons(self, canvas)
        #MyApp.drawIngredientsInInventoryScreen(self, canvas)
        for ingred in self.inventory:
            if ingred[0] != None:
                x, y = ingred[1][0], ingred[1][1]

                img = ingred[0][1]
                canvas.create_image(x, y, image = ImageTk.PhotoImage(img)) 
    
        
MyApp(width = 600, height = 600)




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