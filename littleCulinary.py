#CITATION: CMU GRAPHICS FRAMEWORK CREDS TO: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#this includes CMU Graphics file, so functions like "appStarted" and such
from cmu_112_graphics import *
#my own files
import classesOfFood as classes 
import webScraping as web
import characterInformation as charInfo
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
        #catch bugs
        if len(appliances)==0:
            self.finalDish = 'mashedPotatoes'
            self.grocries = ['potato', 'milk', 'butter']
            appliances = ['saute']
        firstAppliance = appliances[0]
        firstMoveList = list()
        #print(f'THIS IS ACCESS {self.accessPoints}')
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
        if 0<=row<=self.rows-1 and 0<=col<=self.cols-1:
            if self.board[row][col] == 'white':
                if not (self.oppRow == row and self.oppCol == col): 
                    if 0<= row <=self.rows-1 and 0<=col <=self.cols-1:
                        return True
            else:
                return False  
    #oveList = list()
    #keeps track of Mouse pressed 
    def mousePressed(self, event):
        mouseX, mouseY = event.x, event.y 
        #need some kind of case in case it clicks outside the grid 
        print(mouseX, mouseY)
        color = CookingMode.getColor(self, mouseX, mouseY)

        if color !=None and color=='pink':
            (row, col) = CookingMode.getCell(self, mouseX, mouseY)
            currLocation = list((row, col))
            for appliance, location in self.applianceDict.items():
                #check that the location u clicked on is in the dictionary of appliance dicts
                if location == currLocation:
                    #check that you can only click when ur in the right access point
                    if [self.charRow, self.charCol] == self.accessPoints[appliance]:
                        self.currentAppliance = appliance
                        #print(self.currentAppliance)
                        self.isApplianceScreen = True 

            #trigger and open the appliance menu 
        else: 
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

        self.margin = 0 # margin around grid
        self.bottomMargin = 0
        self.rightMargin = 0
        
        #self.timerDelay = 400
        #taken from my HW7 Tetris homework
        #keep track which parts of board are filled
        self.board = [self.cols * ['white'] for row in range(self.rows)]
        self.waitTime = -1
        #self.oppRow = 4 
        #self.oppCol = 0 

        #self.goalRow = 5
        #self.goalCol = 5 
        #call helper function for list of moves it will need to take
        #self.moves = CookingMode.generatePath(self.oppRow, self.oppCol, self.goalRow, self.goalCol, [])
        self.moveNum = 0 
        #self.charRow = self.rows-4
        #self.charCol = 0
        
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
        self.pantryTimer = 300000
        #self.pantryTimer = 150000 #start with 1 minute = 180000
        self.combination = ''
        self.currentSelect = list()
        self.ingredientHistory = list()
        CookingMode.setUpInventory(self)
        #CookingMode.setUpAppliances(self)
        CookingMode.randomizeAppliances(self)
        self.outlineRowCol = list()
        CookingMode.randomStarting(self)
        CookingMode.setUpGameAI(self)
        CookingMode.placeImage(self)
        #self.basket = classes.randomizeBasket(self.cookbooks[0])
        self.playerFinalDish = ''
        self.complexity = 0 
        self.recipeCounter = 0
        CookingMode.setUpCooking(self)
        CookingMode.setUpIsometric(self)
        self.miniGameRectX0 = 80
        self.isHard = self.app.titleMode.isHard #get bool 
        if self.isHard:
            self.miniGameRectWidth = 20
            self.gap = 80 #it moves faster
        else:
            self.miniGameRectWidth = 20
            self.gap = 20
        self.miniGameRectX1 =self.miniGameRectX0+self.miniGameRectWidth
        self.thresholdLeft = 210
        self.thresholdRight = 270
        self.isMiddleClick = False
        self.isSpaceClick = False
        self.skill = 0
        self.combinationScreenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/combinationScreen.png'
        self.combinationScreenLength = 0 
        self.imgCombinationScreen = self.loadImage(self.combinationScreenPath)
        self.combinationScreenScaleFactor = 0
        self.cookbookScreen = '/Users/az/Documents/GitHub/Chopped_Simulation/images/cookbookScreen.png'
        self.imgcookbookScreen = self.loadImage(self.cookbookScreen)
        self.isExitCombination = False 
        self.youMadePath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/youMade.png'
        self.imgYouMade = self.loadImage(self.youMadePath)
        self.combinationImg = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/cookedRice.png')
        self.timerDelay = 200
        try:
            self.isCasual = self.app.customizeMode.isCasual #default is false, unless u click is casual
        except:
            self.isCasual = self.app.profileMode.isCasual #check the other possible place for casual
        self.isCookbook = False 
        CookingMode.setUpCharImages(self)
        self.recipeDict = classes.accessRecipes(self.inventory, self.cookbooks)
        self.isSorry = False 
#CITATION: code math from https://gamedevelopment.tutsplus.com/tutorials/creating-isometric-worlds-a-primer-for-game-developers--gamedev-6511
#CITATION: code math from https://stackoverflow.com/questions/892811/drawing-isometric-game-worlds
#CITATION: CODE MATH FROM http://clintbellanger.net/articles/isometric_math/ 
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

    def setUpIsometric(self):
        #self.tileWidthHalf = self.tileWidth//2
        #self.tileHeightHalf = self.tileHeight//2
        self.offsetX = -1000
        self.offsetY = -270
        self.scalingFactor = 2.5
        self.blenderPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/blender.png'
        self.blenderImg = self.loadImage(self.blenderPath)
        self.blenderScale = CookingMode.findScaleFactor(self, self.blenderImg, self.width//2)
        self.blenderImg= self.scaleImage(self.blenderImg, self.blenderScale)
        
        self.whiskPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/whisk.png'
        self.whiskImg = self.loadImage(self.whiskPath)
        self.whiskImg= self.scaleImage(self.whiskImg, self.blenderScale)


        self.ovenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/oven.png'
        self.ovenImg = self.loadImage(self.ovenPath)
        self.ovenImg= self.scaleImage(self.ovenImg, self.blenderScale)


        self.stovetopPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/stovetop.png'
        self.stovetopImg = self.loadImage(self.stovetopPath)
        self.stovetopImg= self.scaleImage(self.stovetopImg, self.blenderScale)


        self.platingPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/plating.png'
        self.platingImg = self.loadImage(self.platingPath)
        self.platingImg= self.scaleImage(self.platingImg, self.blenderScale)

        self.cupboardPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/Screen_Shot_2020-12-07_at_5.47.26_PM-removebg-preview.png'
        self.cupboardImg = self.loadImage(self.cupboardPath)
        self.cupboardImg= self.scaleImage(self.cupboardImg, self.blenderScale)

    def setUpCharImages(self):    
        self.imgPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/icons8-cake-96.png'
        if self.isCasual:
            self.kitchenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/casualScreen.png'
        else:
            self.kitchenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/competitionScreen.png'
        #self.img = self.loadImage(self.imgPath)
        self.imgKitchen = self.loadImage(self.kitchenPath)
        self.leftPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/left.png'
        self.rightPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/right.png'
        self.downPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/down.png'
        self.upPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/up.png'
        self.leftImg = self.loadImage(self.leftPath)

        scaleFactor = CookingMode.findScaleFactor(self, self.leftImg, self.width//8)
        
        self.leftImg = self.scaleImage(self.loadImage(self.leftPath), scaleFactor)
        self.hatLoadedImgs = dict()
        self.hatPaths = {'chef': '/Users/az/Documents/GitHub/Chopped_Simulation/images/chef.png', 
                    'santa': '/Users/az/Documents/GitHub/Chopped_Simulation/images/santa.png',   
                    'octopus': '/Users/az/Documents/GitHub/Chopped_Simulation/images/octopus.png',
                    'hat': '/Users/az/Documents/GitHub/Chopped_Simulation/images/hat.png' ,
                    'stem': '/Users/az/Documents/GitHub/Chopped_Simulation/images/stem.png'
                    }        #set up hat loaded images which is different than in customize mode cuz diff scale factor
        for hat, path in self.hatPaths.items():
            self.hatPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/' + hat + '.png'
            self.loadedHatImg = self.loadImage(self.hatPath)
            scaleFactor = CookingMode.findScaleFactor(self, self.loadedHatImg, self.leftImg.size[0])
            self.loadedHatImg = self.scaleImage(self.loadedHatImg, scaleFactor)
            self.hatLoadedImgs[hat] = self.loadedHatImg

        try:
            self.hat = self.app.customizeMode.hat #get the chosen hat 
        except:
            self.hat = 'chef' #default
        #scaleFactor = CookingMode.findScaleFactor(self, self.leftImg, self.width//8)
        self.leftImg = self.scaleImage(self.loadImage(self.leftPath), scaleFactor)
        self.leftImg = CookingMode.combineCharImg(self, self.leftImg, self.hatLoadedImgs[self.hat])

        self.rightImg = self.scaleImage(self.loadImage(self.rightPath), scaleFactor)
        self.rightImg = CookingMode.combineCharImg(self, self.rightImg, self.hatLoadedImgs[self.hat])

        self.downImg = self.scaleImage(self.loadImage(self.downPath), scaleFactor)
        self.downImg = CookingMode.combineCharImg(self, self.downImg, self.hatLoadedImgs[self.hat])

        self.upImg = self.scaleImage(self.loadImage(self.upPath), scaleFactor)
        self.upImg = CookingMode.combineCharImg(self, self.upImg, self.hatLoadedImgs[self.hat])

        #initialize ai character
        self.img = self.leftImg 
        
        img = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIUp.png')
        scaleFactor = CookingMode.findScaleFactor(self, img, self.width//6)

        self.gameAIDir = self.scaleImage(self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIUp.png'), scaleFactor)
         
    def setUpCooking(self):
        self.blendImg = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingscreen/blend.png')
        self.bakeImg = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingscreen/bake.png')
        self.sauteImg = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingscreen/saute.png')
        self.stackImg = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingscreen/stack.png')
        self.mixImg = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingscreen/mix.png')
        

    def randomStarting(self):
        #CITATION: inspired by randomization here https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
        while True:
            side = random.choice(['top', 'left', 'right', 'up'])
            if side == 'top':
                self.oppRow = 0 
                self.oppCol = random.randint(0, self.cols - 1)
                self.charRow = 0 
                self.charCol = random.randint(0, self.cols-1)
            
            elif side == 'left':
                self.oppRow = random.randint(0, self.rows - 1)
                self.oppCol = 0
                self.charRow = random.randint(0, self.rows - 1)
                self.charCol = 0     
            elif side == 'right':
                self.oppRow = random.randint(0, self.rows - 1)
                self.oppCol = self.cols-1 
                self.charRow = random.randint(0, self.rows - 1)
                self.charCol = self.cols-1 

            else: #bottom
                self.oppRow = self.rows-1
                self.oppCol = random.randint(0, self.cols - 1)
                self.charRow = self.rows-1
                self.charCol = random.randint(0, self.cols - 1)
            #check that this is legal
            if not (self.oppRow, self.oppCol) == (self.charRow, self.charCol):
                if self.board[self.charRow][self.charCol] == 'white' and self.board[self.oppRow][self.oppCol] == 'white':
                    return 


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
            
            #this is appliance location!
            if i == 5//2:
                color = 'pink'
                applianceLocation = [row, col] #set current row, col applicane location
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

        return True 

    def generateRandom(self, appliances, length): 
        orientation = random.choice(['hor', 'vert'])
        #top or bottom / left or right
        side = random.choice([0, self.cols-1])
            #randomize starting point
        startingPoint = random.randint(0, self.cols - length - 1) #ending opint is so it doesnt go past the end of the board
        #add legality check here?
        
        return orientation, side, startingPoint

    #function to randomly place appliances on different areas on the board! 
    def randomizeAppliances(self):
        appliances = ['mix', 'bake', 'blend', 'saute', 'stack']
        #randomly choose if vertical or horizontal
        length = 5
        self.accessPoints = dict()
        self.applianceDict = dict()
        for i in range(len(appliances)):
            isLegal = False
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
                self.img = self.upImg
                self.charRow -=1 

        elif event.key == 'Down': 
            if CookingMode.isLegal(self, self.charRow +1, self.charCol):
                self.img = self.downImg
                self.charRow += 1
        elif event.key == 'Left': 
            if CookingMode.isLegal(self, self.charRow, self.charCol-1):
                self.img = self.leftImg

                self.charCol-= 1 
        elif event.key == 'Right': 
            if CookingMode.isLegal(self, self.charRow, self.charCol+1):
                self.img = self.rightImg

                self.charCol += 1
        #GET BACK HERE POTATO
        elif event.key == 'o':
            print(self.charRow, self.charCol)
            #check if person is at an access point
            for appliance, location in self.accessPoints.items():
                #add a genrous filter of when you can click 'o' to compensate for isometric view
                if [self.charRow, self.charCol] == location:
                    self.currentAppliance = appliance
                    self.isApplianceScreen = True 
                elif (self.charRow, self.charCol) == (location[0] - 1, location[1] -1):
                    self.currentAppliance = appliance
                    self.isApplianceScreen = True    
                                
                elif (self.charRow, self.charCol) == (location[0] + 1, location[1] -1):
                    self.currentAppliance = appliance
                    self.isApplianceScreen = True 

                                
                elif (self.charRow, self.charCol) == (location[0] + 2, location[1]):
                    self.currentAppliance = appliance
                    self.isApplianceScreen = True 
                elif (self.charRow, self.charCol) == (location[0] , location[1]+2):
                    self.currentAppliance = appliance
                    self.isApplianceScreen = True 


                elif (self.charRow, self.charCol) == (location[0] + 1, location[1] +1):
                    self.currentAppliance = appliance
                    self.isApplianceScreen = True 

                elif (self.charRow, self.charCol) == (location[0] - 1, location[1] +1):
                    self.currentAppliance = appliance
                    self.isApplianceScreen = True 

        elif event.key == 'c':
            if self.isApplianceScreen:
                #self.isCombine = True
                if len(self.currentSelect) >= 1:
                    self.combination = CookingMode.combineIngredients(self)
                    self.playerFinalDish = self.combination
                    self.isCombine = True
                    #add to complexity each time something is combined
                    self.complexity += 1 
        #go to nex mode
        elif event.key == 'n':
            if self.isCasual:
                self.app.setActiveMode(self.app.titleMode)
            else:
                self.app.setActiveMode(self.app.judgingMode)
        elif event.key == 'Space':
            if len(self.currentSelect)!=0: #only do this if there r actually ingreds to combine
                if self.miniGameRectX0>= self.thresholdLeft and self.miniGameRectX1 <= self.thresholdRight:
                    self.isSpaceClick = True 
                    self.isMiddleClick = True
                    #reset rect 
                    self.miniGameRectX0 = 80
                    self.miniGameRectX1 = self.miniGameRectX0+self.miniGameRectWidth
                    
                else: 
                    self.isSpaceClick = True 
                    self.isMiddleClick = False 
                    self.miniGameRectX0 = 80 
                    self.miniGameRectX1 = self.miniGameRectX0+self.miniGameRectWidth
                self.isExitCombination = False

                self.combination = CookingMode.combineIngredients(self)
                self.playerFinalDish = self.combination
                self.isCombine = True
                        #add to complexity each time something is combined
                self.complexity += 1 
                self.inventory.append(self.combination) #either way, add combination to inventory
                #load image here
                self.combinationImg = self.getIngredientImg(self.combination)
                self.combinationImg = self.scaleImage(self.combinationImg, CookingMode.findScaleFactor(self, self.combinationImg, self.height//4))
        elif event.key == 'x':
            if self.isSpaceClick:
                print('ur getting here ')
                self.combination = '' #reset combination 
                for item in self.currentSelect:
                    self.outlineRowCol = list()
                self.currentSelect = list()
                
                self.isExitCombination = True
            #check cookbook first so u can return to appliance screen
            elif self.isCookbook:
                self.isCookbook = False 
            elif self.isSorry:
                self.isSorry = False
            elif self.isApplianceScreen:
                self.isApplianceScreen = False
            
        elif event.key == 'i':
            if self.isCasual:
                if self.isApplianceScreen: #ur on the appliance screen
                    self.isCookbook = True 
            else:
                self.isSorry = True    
        #this is where the loaded List might function differently, so call here
        CookingMode.placeImage(self)
#CITATION: https://www.google.com/search?q=image.paste+python&oq=image.paste+python&aqs=chrome.0.0i457j0i22i30l7.3209j0j4&sourceid=chrome&ie=UTF-8 
    #referenced for usage of pil 
    def combineCharImg(self, sprite, hat):
        updatedChar = Image.new('RGBA', (sprite.width, max(sprite.height, hat.height)))
        updatedChar.paste(sprite, (0,0))
        updatedChar.paste(hat, (0, 0), hat.convert('RGBA'))
        return updatedChar
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
        canvas.create_text(7* self.width/8, self.height/12, text = f'Time Left: {minutes}:{seconds}', font = 'Verdana bold 12', fill = 'white')

    def drawCookbookRecipes(self, canvas):
        i = 0
        for dish, item in self.recipeDict.items():
            canvas.create_text(self.width/2, self.height/3 + i *self.height/10, text = f'{dish}: {item[0]} using {item[1]}', font = 'Verdana 10')
            i +=1
        #self.recipeDict = classes.accessRecipes(self.inventory, self.cookbooks)
        #print(recipeDict)
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
        if not '+' in combination:
            self.recipeCounter+=1
        return combination
        
    def getIngredientObject(self, ingredient):
        for ingredObject in self.IngredientObjects:
            if ingredObject.name == ingredient:
                #print(f'within GET INGREDIENT OBJECT {isinstance(ingredObject, classes.Staples)}')

                return ingredObject

    def timerFired(self):
        if self.isApplianceScreen:
            if not self.isSpaceClick:
                #incorporate wrap around
                if (self.miniGameRectX1 >= 400):
                    self.miniGameRectX0 = 80
                    self.miniGameRectX1 = 100 
                else:
                    self.miniGameRectX0 = (self.miniGameRectX0 + self.gap) 
                    self.miniGameRectX1 = ( self.miniGameRectX1+self.gap )  
            else: 
                if 0<=self.combinationScreenLength<self.width:
                    if self.isMiddleClick:
                        self.skill += 10/12 #add points to skill for cooking well
                    else:
                        if self.skill>=1:
                            self.skill -= 10/12 #takes 12 timer fired, so scor changes by 10 
                    self.combinationScreenLength += 50 
                    self.combinationScreenScaleFactor = CookingMode.findScaleFactor(self, self.imgCombinationScreen, self.combinationScreenLength)
                    self.imgCombinationScreen = self.scaleImage(self.imgCombinationScreen, self.combinationScreenScaleFactor)
                else:
                    if self.isExitCombination:
                        self.combinationScreenLength = 0 
                        self.isSpaceClick = False

                      
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
        if not self.isCasual:
            if self.pantryTimer>=0:
                    self.pantryTimer -=150 #slightly faster cuz of timer delay
            else:
                self.isTimeUp = True
            
        #run combining methods if ingredients are successfully combined
        #if self.isCombine: 
        #    CookingMode.combineIngredients(self)
        CookingMode.placeImage(self)
        CookingMode.displayImagesInInventory(self)    

    def moveGameAI(self):
        #only move if haven't reached goal state
        if not self.isCasual:
            if not self.moveNum == len(self.moveList): 
                #print(f'THIS IS moveLIST IN MOVE GAME AI: {self.moveList}')
                if not self.moveList == None:
                    currMove = self.moveList[self.moveNum]
                    img = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIUp.png')
                    scaleFactor = CookingMode.findScaleFactor(self, img, self.width//6)
                    if currMove == (0, 1) or currMove == (1, -1) or currMove == (-1, 0):
                        self.gameAIDir = self.scaleImage(self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIUp.png'), scaleFactor)
                    elif currMove == (0, 1): 
                        self.gameAIDir = self.scaleImage(self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIRight.png'), scaleFactor)
                    elif currMove == (0, -1):
                        self.gameAIDir = self.scaleImage(self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AILeft.png'), scaleFactor)
                    elif currMove == (1, 0):
                        self.gameAIDir = self.scaleImage(self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIDown.png'), scaleFactor)
                    elif currMove == (-1, -1):
                        self.gameAIDir = self.scaleImage(self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIdiagonalLeft.png'), scaleFactor)
                    elif currMove == (1, 1):
                        self.gameAIDir = self.scaleImage(self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIdiagonalRight.png'), scaleFactor)
                    else:
                        self.gameAIDir = self.scaleImage(self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/AIUp.png'), scaleFactor)
                        print(currMove)
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
        xStart = 468 
        invGridWidth = 541 - xStart
        yStart = 107
        invGridHeight = 513 - yStart
        invCellHeight = invGridHeight/self.invRows
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
  

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, app.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - yStart) / invCellHeight)
        col = int((x - xStart) / invGridWidth)
        #print(f'this is row col: {row, col}')
        
        return (row, col)

#CITATION: CREDS getCellBounds from grid-demo.py, CREDS to https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getInvCellBounds(self, row, col):
        """
        margin = 20 # margin around grid
        bottomMargin = self.height//4
        rightMargin = self.width//4
        
        invWidth = rightMargin - 2 * margin 
        invLength = self.height - bottomMargin 
        width = rightMargin - 2 * self.margin 
        length = self.height - self.bottomMargin 
        margin = width / 4.5

        invGridWidth  = width - 2 * margin
        invGridHeight = length - 2 * margin

        xStart = self.width - rightMargin 
        yStart = self.height/7

        width = rightMargin - 2 * margin 
        length = self.height - bottomMargin 
        margin = width / 4.5
        """
        xStart = 468 
        invGridWidth = 541 - xStart
        yStart = 107
        invGridHeight = 513 - yStart
        
        x0 = xStart + invGridWidth * col / self.invCols
        x1 = xStart+  invGridWidth * (col+1) / self.invCols
        y0 = yStart + invGridHeight * row / self.invRows
        y1 = yStart + invGridHeight * (row+1) / self.invRows
        return (x0, y0, x1, y1)
      

    #funcion to go into instance and set it up for image loading
    
    def getIngredientImg(self, name):
        margin = 20 # margin around grid
        bottomMargin = self.height//4
        rightMargin = self.width//4

        width = rightMargin - 2 * margin 
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
            #if self.isCombine: 
            #    self.recipeCounter +=1 #successful recipe being made
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

        #load the inventory into this mode
        self.inventory = list()
        self.inventory+=self.basket

        self.inventory+=self.app.shoppingMode.hand
        
        #self.ingredientObjects = list()
#        for name in self.inventory:
#            self.ingredientObjects(CookingMode.getIngredientImg(self, name)) 
        spot0 = CookingMode.getMidCell(self, 0, 0)
        spot1 = CookingMode.getMidCell(self, 1, 0)
        spot2 = CookingMode.getMidCell(self, 2, 0)
        spot3 = CookingMode.getMidCell(self, 3, 0)
        spot4 = CookingMode.getMidCell(self, 4, 0)
    

        #this is the inventory that shows up on the screen, limit of 5
        self.displayInventory = [ [None, spot0], [None, spot1], [None, spot2], [None, spot3],
        [None, spot4] ]
        CookingMode.displayImagesInInventory(self)
        
        """
        spot0 = (6.7*self.width/8, self.height/4.5)
        spot1 = (6.7*self.width/8, 1.75*self.height/4.7)
        spot2 = (6.7*self.width/8, 3*self.height/4.7)
        spot3 = (6.7*self.width/8, 4*self.height/4.7)
        spot4 = (6.7*self.width/8, 5*self.height/4.7)
        """
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
            outline = 'white'
        else:
            outline = ''
        x0, y0, x1, y1 = CookingMode.getInvCellBounds(self, row, col)
        
        canvas.create_rectangle(x0, y0, x1, y1, fill = '', width=2, outline = outline)


    def drawBoard(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                CookingMode.drawCell(self,canvas,row,col,self.board[row][col])
                if self.board[row][col] == 'pink':
                    for appliance, locations in self.applianceDict.items():
                        #print(self.applianceDict)
                        if locations == [row, col]:
                            x0, y0, x1, y1 = CookingMode.getIsoCellBounds(self, row, col)
                            canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f'{appliance}', font = 'Verdana 10')
                            #display appropriate image
                            if appliance == 'saute':
                                applianceImg = self.stovetopImg
                            elif appliance == 'mix':
                                applianceImg = self.whiskImg
                            elif appliance == 'bake':
                                applianceImg = self.ovenImg
                            elif appliance == 'blend':
                                applianceImg = self.blenderImg
                            elif appliance == 'stack':
                                applianceImg = self.platingImg
                            canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(applianceImg))
                """
                elif self.board[row][col] == 'gray': #cupboards
                    x0, y0, x1, y1 = CookingMode.getIsoCellBounds(self, row, col)
                    applianceImg = self.cupboardImg
                    canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(applianceImg))
                """
    #taken from my HW7, Tetris
    #function to create each cell and fill with its respective color 
    
    def drawApplianceScreen(self, canvas):
        appliance = self.currentAppliance 
        if appliance == 'mix':
            img = self.mixImg
        elif appliance == 'blend':
            img = self.blendImg
        elif appliance == 'bake':
            img = self.bakeImg
        elif appliance == 'saute':
            img = self.sauteImg
        elif appliance == 'stack':
            img = self.stackImg
        
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(img))
        #CookingMode.drawInventoryScreen(self, canvas)
        CookingMode.drawInventoryTable(self, canvas)
        CookingMode.drawInventoryIngredients(self, canvas)
        canvas.create_rectangle(80, 490, 400, 525, fill = 'lightgray', outline = '')
        canvas.create_rectangle(210, 490, 270, 525, fill = 'white', outline = '')
        width = 20
        height = 70
        canvas.create_rectangle(self.miniGameRectX0, 470, self.miniGameRectX1, 470+height, outline = '', fill = 'deepskyblue2')
        """
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
        """    
    def drawInventoryScreen(self, canvas):
        xStart = self.width - self.rightMargin + self.margin
        yStart = self.height/5
        canvas.create_rectangle(xStart, yStart, xStart + self.invWidth, yStart + self.invLength, fill = 'pink')
        canvas.create_text((2*xStart+self.invWidth)/2, yStart + self.invLength/35, text = 'INVENTORY')

    #this check is taken from example 10 of https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def pointInInvGrid(self, x, y):
        xStart = 468 
        invGridWidth = 541 - xStart
        yStart = 107
        invGridHeight = 513 - yStart
        xEnd = xStart + invGridWidth
        yEnd = yStart + invGridHeight

        # return True if (x, y) is inside the grid defined by app.
        inBounds = ((xStart <= x <= xEnd) and
                (yStart <= y <= yEnd))
        return inBounds
#CITATION: from CMU https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#ADJUSTED FOR ISOMETRIC DISPLAY
    def drawCell(self,canvas, row, col, color):
        x0, y0, x1, y1 = CookingMode.getIsoCellBounds(self, row, col)
        if (row, col) in self.applianceDict:
            print('ur getting here')
            canvas.create_image((x0+x1)/2, (y0+y1)/2, ImageTk.PhotoImage(self.blendImg)
        #canvas.create_rectangle(x0, y0, x1, y1, fill = color
                                 )
    def getIsoCellBounds(self, row, col):
        x0, y0, x1, y1 = CookingMode.getCellBounds(self, row, col)
        startX, startY = CookingMode.cartToIso(self, x0, y0, self.scalingFactor) 
        endX, endY = CookingMode.cartToIso(self, x1, y1, self.scalingFactor)
        return startX, startY, endX, endY
    def drawGameAI(self, canvas):
        (x0, y0, x1, y1) = CookingMode.getIsoCellBounds(self, self.oppRow, self.oppCol)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(self.gameAIDir))

    def drawPlayer(self, canvas):
        x0,y0,x1, y1 = CookingMode.getIsoCellBounds(self, self.charRow, self.charCol)
        canvas.create_image((x0+x1)/2, (y0+y1)/2, image = ImageTk.PhotoImage(self.img))
        #canvas.create_oval(x0, y0, x1, y1, fill='blue')
        
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
        canvas.create_text(7* self.width/8, self.height/10, text = f'Time Left: {minutes}:{seconds}', font = "Verdana 12 bold", fill = 'white')

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
                    try:
                        self.displayInventory[i][0] = loadedImg
                    except:
                        pass
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
    def drawCookbook(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.imgcookbookScreen))
        CookingMode.drawCookbookRecipes(self, canvas)
    def drawKitchen(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.imgKitchen))
    def drawCombinationScreen(self, canvas):
        if not self.combinationScreenLength==0:
            canvas.create_image(self.width/2, self.height/2, image= ImageTk.PhotoImage(self.imgCombinationScreen))
            if self.combinationScreenLength == self.width: #finished animating
                canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.imgYouMade))
                canvas.create_image(self.width/2, self.height/2.5, image = ImageTk.PhotoImage(self.combinationImg))
                canvas.create_text(self.width/2, self.height/1.7, text = f'{self.combination}'.upper(), font = 'Verdana 30 bold', fill = 'white')
                canvas.create_text(self.width/4, self.height/1.4, text = f'Cooking Skill: {int(self.skill)}', font = 'Vedana 15 bold', fill = 'white')
                canvas.create_text(3*self.width/4, self.height/1.4, text = f'Recipes Made: {self.recipeCounter}', font = 'Verdana 15 bold', fill = 'white')
                canvas.create_text(2*self.width/4, self.height/1.24, text = f'Complexity: {self.complexity}', font = 'Verdana 15 bold', fill = 'white')
    def drawTimeUp(self, canvas):
        r = self.height//3
        canvas.create_rectangle(self.width/2 - r, self.height/2 - r, self.width/2 +r, self.height/2 +r, fill = 'white', outline = '')
        canvas.create_text(self.width/2, self.height/2, text = 'TIME IS UP! PRESS "n" TO MOVE ON!', font = 'Verdana 15 bold')
    def drawInstructions(self, canvas):
        canvas.create_text(self.width/2, self.height-20, text = f'Go around and click different pink boxes and select ingreds to cook!')
    def drawSorry(self, canvas):
        r = self.height//3
        canvas.create_rectangle(self.width/2 - r, self.height/2 - r, self.width/2 +r, self.height/2 +r, fill = 'white', outline = '')
        canvas.create_text(self.width/2, self.height/2, text = 'SORRY! No hints in competition. Press X to exit.', font = 'Verdana 12 bold')

    def redrawAll(self, canvas):
    
        CookingMode.drawKitchen(self, canvas)
        CookingMode.drawBoard(self,canvas)
        if not self.isCasual:
            CookingMode.drawGameAI(self, canvas)
        CookingMode.drawPlayer(self, canvas)
        #CookingMode.setUpAppliances(self, canvas)
        #CookingMode.drawInventoryScreen(self, canvas)
        if not self.isCasual:
            CookingMode.drawTimer(self, canvas) #don't track time if casual mode
        if self.isApplianceScreen:
            CookingMode.drawApplianceScreen(self, canvas)
            if self.isCookbook:
                CookingMode.drawCookbook(self, canvas)
            elif self.isSorry:
                CookingMode.drawSorry(self, canvas)
            CookingMode.drawCombinationScreen(self, canvas)
        if self.isTimeUp:
            CookingMode.drawTimeUp(self, canvas)

        #CookingMode.drawButtons(self, canvas)
        #CookingMode.drawInventoryTable(self, canvas)
        #CookingMode.drawInventoryIngredients(self, canvas)
        #CookingMode.drawInstructions(self, canvas)
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
        self.cookbooks = self.app.cookingMode.cookbooks
        #self.gameAIRecipe = 'mashedPotato'
        self.playerWebScore = 0
        self.gameAIWebScore = 0
        self.complexity = self.app.cookingMode.complexity
        self.recipeCounter = self.app.cookingMode.recipeCounter
        self.gameCookBookIndex = 0 #the cookbook where it got the recipe
        for i in range(3):
            recipe = classes.returnRecipe(self.finalProductGameAI, self.cookbooks, i)
            if recipe != None:
                self.gameCookBookIndex = i
        #print(self.gameAIIngredients)
        self.numberCalculated = 0
        self.isWinnerCalculated=False
        self.idealCombos, self.grossCombos = classes.combos()
        self.judgingPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/judgingScreen.png'
        self.judgingImg = self.loadImage(self.judgingPath)
        self.losePath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingscreen (6)/lose.png'
        self.loseImg = self.loadImage(self.losePath)
        self.winPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingscreen (6)/win.png'
        self.winImg = self.loadImage(self.winPath)
        self.playerSkill = self.app.cookingMode.skill  
        self.playerComplexityScore = 0
        self.gameAIComplexityScore = 0
        #randomize gameAi skill based on difficult 
        if self.app.cookingMode.isHard:
            self.gameAISkill = random.randint(20, 50)
        else: self.gameAISkill = random.randint(0, 20)
        self.gameAITotalScore = 0
        self.playerTotalScore = 0
        self.isPlayerCalculated = False
        self.isGameAICalculated = False
        self.gameAIDishImg = self.app.cookingMode.getIngredientImg(self.finalProductGameAI)
        self.playerDishImg = self.app.cookingMode.getIngredientImg(self.finalProductPlayer)
    def keyPressed(self, event):
        #launch webScraping for players's dish
        if event.key == 'o':
            playerNum = web.recipeScraper(self.playerIngredients)
            self.playerWebScore = JudgingMode.calculateWebscraping(self, playerNum)
            self.playerComplexityScore = JudgingMode.calculateComplexity(self, self.complexity, self.recipeCounter)
            self.playerTotalScore = self.playerWebScore + self.playerComplexityScore + self.playerSkill
            self.isPlayerCalculated = True
            #rint(self.gameAINum)
        elif event.key == 'p':
            gameAINum = web.recipeScraper(self.gameAIIngredients)
            self.gameAIWebScore = JudgingMode.calculateWebscraping(self, gameAINum)
            self.gameAIComplexityScore = JudgingMode.calculateComplexity(self, self.gameCookBookIndex+1, self.gameCookBookIndex+1) #every cookbook is guaranteed to be a recipe
            self.gameAITotalScore = self.gameAIWebScore + self.gameAIComplexityScore + self.gameAISkill
            self.isGameAICalculated = True
        elif event.key == 'w':
            self.isWinnerCalculated = True
            print('ur getting here')
    def mousePressed(self, event):
        print(event.x, event.y)
        if 91<=event.x<=520 and 499<=event.y<=540:
            self.app.setActiveMode(self.app.leaderboardMode)
        elif 361<=event.x<=517 and 499<=event.y<=540:
            self.app.setActiveMode(self.app.titleMode)
    #function to calculate how many appliances were used, which level of cookbook its in 
    def calculateComplexity(self, complexity, recipeCounter):
        complexityScore = recipeCounter + complexity 
        complexityScore = complexityScore // 8 #number of appliances + levels of cooksbooks 
        complexityScore = complexityScore * 10 
        return complexityScore
    def calculateWebscraping(self, num):
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
        canvas.create_image(self.width/4, self.height/2.4, image = ImageTk.PhotoImage(self.playerDishImg)) 
        canvas.create_text(self.width/4, self.height/2, text = f'{self.finalProductPlayer}', font = 'Verdana 15 bold')
        canvas.create_text(self.width/4, self.height/1.9, text ='Press o to calculate Player', font = 'Verdana 12')
        if self.isPlayerCalculated:
            canvas.create_text(self.width/4, 3*self.height/5, text=f'Complexity Score: {self.playerComplexityScore}', font = 'Verdana 14 bold')
            canvas.create_text(self.width/4, 3.5*self.height/5, text=f'Skill Score: {self.playerSkill}', font = 'Verdana 14 bold')
            canvas.create_text(3*self.width/4, 4*self.height/5, text=f'Webscraping Score: {self.playerWebScore}', font = 'Verdana 14 bold')
            canvas.create_text(self.width/4, 4.5*self.height/5, text=f'TOTAL IS: {self.playerTotalScore}', font = 'Verdana 14 bold')
    def drawGameAIInfo(self, canvas):
        canvas.create_image(3*self.width/4, self.height/2.4, image = ImageTk.PhotoImage(self.gameAIDishImg)) 
        canvas.create_text(3*self.width/4, self.height/2, text = f'{self.finalProductGameAI}', font = 'Verdana 15 bold')
        canvas.create_text(3* self.width/4, self.height/1.9, text ='Press p to calculate Game AI', font = 'Verdana 12')
        if self.isGameAICalculated:
            canvas.create_text(3*self.width/4, 3*self.height/5, text=f'Complexity Score: {self.gameAIComplexityScore}', font = 'Verdana 14 bold')
            canvas.create_text(3*self.width/4, 3.5*self.height/5, text=f'Skill Score: {self.gameAISkill}', font = 'Verdana 14 bold')
            canvas.create_text(3*self.width/4, 4*self.height/5, text=f'Webscraping Score: {self.gameAIWebScore}', font = 'Verdana 14 bold')
            canvas.create_text(3*self.width/4, 4.5*self.height/5, text=f'TOTAL IS: {self.gameAITotalScore}', font = 'Verdana 14 bold')


    def drawScreen(self, canvas):
        #canvas.create_rectangle(0,0, self.width, self.height, fill = 'skyblue')
        #canvas.create_text(self.width/2, self.height/6, text='JUDGING BEGINS!', font='Arial 26 bold')
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.judgingImg))
        
    def drawWin(self,canvas):
        if self.playerTotalScore > self.gameAITotalScore:
            resultImg = self.winImg
        else:
            resultImg = self.loseImg
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(resultImg))
    def redrawAll(self, canvas):
        JudgingMode.drawScreen(self, canvas)
        JudgingMode.drawPlayerInfo(self, canvas)
        JudgingMode.drawGameAIInfo(self, canvas)
        if self.isGameAICalculated and self.isPlayerCalculated:
            r = self.height//3
            canvas.create_rectangle(self.width/2 - r, self.height/2 - r, self.width/2 +r, self.height/2 +r, fill = 'white', outline = '')
            canvas.create_text(self.width/2, self.height/2, text = 'SCORES TALLIED! PRESS "w" TO MOVE ON!', font = 'Verdana 15 bold')
        if self.isWinnerCalculated:
            JudgingMode.drawWin(self, canvas)

class LeaderboardMode(Mode):
    def appStarted(self):
        self.currentUser = self.app.logInMode.user
        self.currentScore = self.app.judgingMode.playerTotalScore
        #add your current session to leaderboard
        self.leaderboard = charInfo.updateLeaderboard('leaderboard.txt', self.currentUser, self.currentScore) #dictionary
        self.sortedLeaderboard = charInfo.sortLeaderboard('leaderboard.txt', self.leaderboard) #list 
        charInfo.addRecipe('savedRecipes.txt', self.currentUser, self.app.judgingMode.finalProductPlayer)
        self.combinationScreenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/combinationScreen.png'
        self.imgCombinationScreen = self.loadImage(self.combinationScreenPath)
    def keyPressed(self, event):
        if event.key == 'r':
            self.app.logInMode.user = ''
            self.app.logInMode.password = '' #reset user and password 
            self.app.setActiveMode(self.app.titleMode)
    def drawPlayerScore(self, canvas):
        i = self.height/15
        #go thru sorted leaderboard and display it on screen in order
        for descendingScore in self.sortedLeaderboard:
            matchingPerson = ''
            for key, value in self.leaderboard.items(): #find it in the dictionary
                if descendingScore == value:
                    matchingPerson = key 
                    canvas.create_text(self.width/2, self.height/5+i, text = (f'{matchingPerson}: {descendingScore}'.upper()), fill = 'white', font = "Verdana 15 bold")
                    i+= self.height/15
    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.imgCombinationScreen))
        canvas.create_text(self.width/2, self.height/9, text = ('LEADERBOARD'), font = 'Verdana 30 bold')
        canvas.create_text(self.width/2, self.height/1.4, text = ('PRESS R TO TRY AGAIN'), font = 'Verdana 15 bold')
        LeaderboardMode.drawPlayerScore(self, canvas)

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
        if 187<=event.x<=407 and 504<=event.y<=572:
            self.app.setActiveMode(self.app.cookingMode)
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
            outline = 'white'
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
        self.isHard = False
        
    def keyPressed(self, event):
        return
        #if event.key == 'Space':
         #   self.app.setActiveMode(self.app.instructionsMode)
    def mousePressed(self, event):
        if 60<=event.x<=255 and 175<=event.y<=497:
            #continue w status quo
            self.app.setActiveMode(self.app.logInMode)
        elif 327<=event.x<=522 and 175<=event.y<=497:
            self.isHard = True
            #now it's hardMode
            self.app.setActiveMode(self.app.logInMode)

    
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
        #call its basket function
        try: 
            self.dietaryList = self.app.customizeMode.dietaryList
        except:
            self.dietaryList = list()

        #call your ingedients!! EVERYTHING MUST REFEENCE HERE FO INITIAL BASKET CALL! 
        self.isHard = self.app.titleMode.isHard #get bool 
        self.cookbooks, self.basket, self.Person, self.Opponent, self.Appliances, self.Ingredients = classes.setUpObjects(self.dietaryList)
        self.basket = classes.randomizeBasket(self.cookbooks[0], self.dietaryList)
        self.isDisplayBasket = False
        #CITATION: self created on canva
        self.screenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/basketScreen.png'
        self.screenImg = self.loadImage(self.screenPath)
        self.basketLoadedIngredients = list()
        BasketMode.loadBasketIngreds(self)
    def mousePressed(self, event):
        print(event.x, event.y)
        if 187<=event.x<=407 and 504<=event.y<=572:
            self.app.setActiveMode(self.app.shoppingMode)

    def keyPressed(self, event):
        if event.key == 'Space':
            self.isDisplayBasket = True

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
            #self.scaledImg = self.scaleImage(self.ingredImg, self.width/6)
            self.basketLoadedIngredients.append(self.ingredImg)

    def drawScreen(self,canvas):
        canvas.create_rectangle(0,0, self.width, self.height, fill = 'pink')

        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.screenImg))
    #function to go thru basket loaded images and draw it 
    def drawBasket(self, canvas):
        #for item in self.basket:
        #img1 = self.scaleImage(self.basketLoadedIngredients[0], self.width/6)
        #img2 = self.scaleImage(self.basketLoadedIngredients[1], self.width/6)
        canvas.create_image(1.5*self.width/5, 3*self.height/5, image = ImageTk.PhotoImage(self.basketLoadedIngredients[0]))
        canvas.create_image(3.5*self.width/5, 3*self.height/5, image = ImageTk.PhotoImage(self.basketLoadedIngredients[1]))

    """
       i = 0 
        gap = self.width/3
        for item in self.basketLoadedIngredients:
            x  = gap + i*gap
    """
    def redrawAll(self, canvas):
        BasketMode.drawScreen(self, canvas)
        BasketMode.drawBasket(self, canvas)
class LogInMode(Mode):
    def appStarted(self):
        self.loginScreenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/loginPage.png'
        self.loginImg = self.loadImage(self.loginScreenPath)
        self.usersDict = charInfo.leaderboard('leaderboard.txt') #access current users
        self.isUser = False
        self.isPass = False
        self.user = ''
        self.password = ''
    def mousePressed(self, event):
        #check which box clicked
        print(event.x, event.y)
        if 72<=event.x<=537 and 198<=event.y<=250: #mid y ~220
            self.isUser = True
        elif 72<=event.x<=537 and 330<=event.y<=386: #mid y ~360 
            self.isPass = True

        if 91<=event.x<=278 and 499<=event.y<=540: 
            #check that this is a correct user pass
                board = charInfo.passUser('userpass.txt')
                for user, password in board.items():
                    if user==self.user and password == self.password:
                        self.app.setActiveMode(self.app.profileMode)
                        break

                    else:
                        board = charInfo.updateLeaderboard('userpass.txt', self.user, self.password)
                        self.app.setActiveMode(self.app.customizeMode)
                        break
        elif 361<=event.x<=517 and 499<=event.y<=540:
            #also add it to ur text file! says leaderboard but can be used for passwords as well
            if len(self.user)>0 and len(self.password)>0:
                board = charInfo.updateLeaderboard('userpass.txt', self.user, self.password)
                self.app.setActiveMode(self.app.customizeMode)

    def keyPressed(self, event):
        if event.key in 'abcdefghijklmnopqrstuvwxyz' or event.key in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if self.isUser:
                self.user = self.user + event.key
            elif self.isPass:
                self.password = self.password + event.key
        elif event.key =='Enter':
            self.isUser = False
            self.isPass = False
        elif event.key == 'Delete':
            if self.isUser and len(self.user)>0:
                self.user = self.user[0:-1]
                print(self.user)
            
            elif self.isPass and len(self.password)>0:
                self.password = self.password[0:-1]
    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.loginImg))
        canvas.create_text(259, 220, text=f'{self.user}', font = 'Verdana 15 bold', fill = 'white', anchor ='w')
        canvas.create_text(259, (330+386)/2, text=f'{self.password}', font = 'Verdana 15 bold', fill = 'white', anchor = 'w')

class CustomizeMode(Mode):
    def appStarted(self):
        print('getting here')
        self.combinationScreenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/cookingscreen (8)/customize.png'
        self.imgCombinationScreen = self.loadImage(self.combinationScreenPath)
        self.user = self.app.logInMode.user
        self.charPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/down.png'
        self.charImg = self.loadImage(self.charPath)
        self.scaleFactor = self.app.cookingMode.findScaleFactor(self.charImg, self.height//4)
        self.charImg = self.scaleImage(self.charImg, self.scaleFactor)
        self.originalCharImg = self.charImg
        self.isCasual = False
        self.hat = 'chef'
        self.hats = ['chef', 'santa', 'octopus', 'hat', 'stem']
        self.hatPaths = {'chef': '/Users/az/Documents/GitHub/Chopped_Simulation/images/chef.png', 
                    'santa': '/Users/az/Documents/GitHub/Chopped_Simulation/images/santa.png',   
                    'octopus': '/Users/az/Documents/GitHub/Chopped_Simulation/images/octopus.png',
                    'hat': '/Users/az/Documents/GitHub/Chopped_Simulation/images/hat.png' ,
                    'stem': '/Users/az/Documents/GitHub/Chopped_Simulation/images/stem.png'
                    }
        self.hatLoadedImgs = dict()
        for hat, path in self.hatPaths.items():
            self.hatPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/' + hat + '.png'
            self.loadedHatImg = self.loadImage(self.hatPath)
            scaleFactor = self.app.cookingMode.findScaleFactor(self.loadedHatImg, self.originalCharImg.size[0])
            self.loadedHatImg = self.scaleImage(self.loadedHatImg, scaleFactor)
            self.hatLoadedImgs[hat] = self.loadedHatImg
        #self.hair = 'brown'
        #self.hairs = ['brown', 'red', 'pink', 'blue']
        #self.outfit = 'brown'
        #self.outfits = ['brown', 'red', 'pink', 'blue']
        self.dietaryList = list()
        self.isVegetarian, self.isNutFree, self.isVegan = False, False, False
    #CITATION: https://www.google.com/search?q=image.paste+python&oq=image.paste+python&aqs=chrome.0.0i457j0i22i30l7.3209j0j4&sourceid=chrome&ie=UTF-8 
    #referenced for usage of pil 
    def combineCharImg(self, sprite, hat):
        updatedChar = Image.new('RGBA', (sprite.width, max(sprite.height, hat.height)))
        updatedChar.paste(sprite, (0,0))
        updatedChar.paste(hat, (0, 0), hat.convert('RGBA'))
        return updatedChar
    def keyPressed(self, event):
        if event.key == 'n':
            self.app.setActiveMode(self.app.instructionsMode)
    def mousePressed(self, event):
        print(event.x, event.y)
        #click hat
        if 61<=event.x<=182 and 146<=event.y<=158: 
            self.hats = self.hats[1:] + [self.hats[0]]
            self.hat = self.hats[0]
            #reset character image everything this is clicked with the new hat 
            print(self.hats)
            hatToLoad = self.hatLoadedImgs[self.hat]
            self.charImg = CustomizeMode.combineCharImg(self, self.originalCharImg, hatToLoad)
            
        elif 60<=event.x<=178 and 432<=event.y<=446: 
            self.dietaryList.append('vegetarian')
            self.isVegetarian = True
        elif 246<=event.x<=328 and 432<=event.y<=446: 
            self.dietaryList.append('nutfree')
            self.isNutFree = True
        elif 416<=event.x<=478 and 432<=event.y<=446: 
            self.dietaryList.append('vegan')
            self.isVegan = True
        """
        elif 61<=event.x<=182 and 213<=event.y<=226: 
            self.hairs = self.hairs[1:] + [self.hairs[0]]
            self.hair = self.hair[0]
        elif 61<=event.x<=300 and 290<=event.y<=303: 
            self.outfit = self.outfits[1:] + [self.outfits[0]]
            self.outfit = self.outfit[0]
        """
        #clickhair
        #click clothes
        #click purple buttons
        if 91<=event.x<=200 and 499<=event.y<=540: 
            self.app.setActiveMode(self.app.instructionsMode)
        elif 361<=event.x<=517 and 499<=event.y<=540:
            self.isCasual = True
            self.app.setActiveMode(self.app.instructionsMode)

    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.imgCombinationScreen))
        canvas.create_image(2*self.width/3, self.height/2.7, image = ImageTk.PhotoImage(self.charImg))
        canvas.create_text(2*self.width/3, self.height/1.73, font = 'Verdana 20 bold', text=f'{self.user}'.upper(), fill = 'white')
        
        if self.isVegetarian:
            canvas.create_line(60, 454, 178 ,454, fill = 'white')
        if self.isNutFree:
            canvas.create_line(246, 454, 328 ,454, fill = 'white')
        if self.isVegan:
            canvas.create_line(416, 454, 478 ,454, fill = 'white')

class ProfileMode(Mode):
    def appStarted(self):
        self.combinationScreenPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/characterprofile.png'
        self.imgCombinationScreen = self.loadImage(self.combinationScreenPath)
        self.recipesMade = charInfo.passUser('savedRecipes.txt') #should return dict
        self.recipes = ''
        for person, recipes in self.recipesMade.items():
            print(person)
            if person == self.app.logInMode.user:
                print('sucess!!')
                self.recipes = recipes
        self.isCasual = False
    def mousePressed(self, event):
        if 91<=event.x<=200 and 499<=event.y<=540: 
            self.app.setActiveMode(self.app.instructionsMode)
        elif 361<=event.x<=517 and 499<=event.y<=540:
            self.isCasual = True
            self.app.setActiveMode(self.app.instructionsMode)

    def keyPressed(self, event):
        if event.key == 'n':
            self.app.setActiveMode(self.app.instructionsMode)

    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.imgCombinationScreen))
        canvas.create_text(self.width/2, self.height/6, text = 'YOUR PROFILE', font = 'Verdana 30 bold', fill = 'white')
        canvas.create_text(self.width/2, self.height/3.5, text = f'{self.app.logInMode.user}', font = 'Verdana 20 bold', fill = 'white')
        canvas.create_text(self.width/10, self.height/2.5, text = f'{self.recipes}', font = 'Verdana 15 bold', fill = 'white', anchor = 'w')
class InstructionsMode(Mode):
    def appStarted(self):
        try:
            if (self.app.customizeMode.isCasual):
                self.instructionsPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/casualMode.png'
            else: 
                
                self.instructionsPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/instructions.png'
        except: #default catchall
            if self.app.profileMode.isCasual:

                self.instructionsPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/casualMode.png'
            else:
                self.instructionsPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/instructions.png'

        self.instructions = self.loadImage(self.instructionsPath)
    def mousePressed(self, event):
        print(event.x, event.y)
        if 187<=event.x<=407 and 504<=event.y<=572:
            self.app.setActiveMode(self.app.basketMode)

    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.instructions))
#leader board
#customize characer
#create a mii and add different parts to your sprite 
#mash the things the user put together and put into the sprite
class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleMode = TitleMode()
        app.shoppingMode = ShoppingMode()
        app.cookingMode = CookingMode()
        app.judgingMode = JudgingMode()
        app.basketMode = BasketMode()
        app.instructionsMode = InstructionsMode()
        app.leaderboardMode = LeaderboardMode()
        app.logInMode = LogInMode()
        app.customizeMode = CustomizeMode()
        app.profileMode = ProfileMode()
        app.setActiveMode(app.titleMode)

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