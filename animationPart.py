#Animation Framework Creds to CMU: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

#image sources:
# https://stock.adobe.com/images/tin-can-market-shelf-icon-isometric-of-tin-can-market-shelf-vector-icon-for-web-design-isolated-on-white-background/238231291
#http://clipart-library.com/free/egg-clipart-png.html
#https://previews.123rf.com/images/chubarov/chubarov1506/chubarov150600023/41161413-gray-shut-down-gas-stove.jpg

import selenium
import math, copy, random
from selenium.common.exceptions import NoSuchElementException 
import time
from selenium import webdriver
#input path name to where driver is
#driver = webdriver.Chrome('//Users/az/Documents/GitHub/Chopped_Simulation/chromedriver')  # Optional argument, if not specified will search path.

from cmu_112_graphics import *
from classesOfFood import * 
#create classes of objects and ppl in sep file, import module here
#import classesOfFood as Food
class MyApp(App):
    def appStarted(self):
        #setting up the center of the avatar
        self.cx = self.width/4
        self.cy = 3*self.height/4
        self.messages = ['appStarted']
        self.r = 20

        #setting up center of game AI
        self.oppCX = 3 * self.width / 4
        self.oppCY = 3 * self.height / 4 
        self.possibleIngredients = ['potato', 'avocado', 'ricecake', 'pastrami', 'salami', 'bread', 
                                    'cheese', 'pasta', 'oatmeal']
        self.basket = MyApp.randomIngredients(self)
        #list of all the objects you need 
        self.finalProduct = list()
        self.pantryTimer = 20000 #start with 1 minute = 180000
        #different screens of game
        self.isTitleScreen = True
        self.isIngredientScreen = False
        self.isPantryMode = False
        self.isCookingMode = False
        self.isTimeUp = False
        self.isApplianceScreen = False 
        #load images
        shelfPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/isoshelf.jpg'
        self.imageShelf = self.loadImage(shelfPath)
        self.imageShelf = self.scaleImage(self.imageShelf, 1/2)
        eggPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/egg.png'
        self.imageEgg = self.scaleImage(self.loadImage(eggPath), 1/10)
        choppedPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/chopped.png'
        self.imageChopped = self.scaleImage(self.loadImage(choppedPath), 1/2)
        self.imageOven = self.loadImage('/Users/az/Documents/GitHub/Chopped_Simulation/images/oven.jpg')
        self.imageOven = self.scaleImage(self.imageOven, 1/10)

    def randomIngredients(self):
        self.basket = random.choices(self.possibleIngredients, k = 3)    
        return self.basket 
    def timerFired(self):
        if not self.isTitleScreen:
            if self.pantryTimer>=0:
                self.pantryTimer -=100
                MyApp.moveGameAI(self)
            else:
                self.isTimeUp = True

            
    def drawIngredientScreen(self, canvas):
        canvas.create_rectangle(self.width/8, 6*self.height/8, 7* self.width/8, self.height, fill = 'gray')
        displayWidth = 7*self.width/8 - self.width/8
        """
        for x in range(int(displayWidth)):
            y = 6.5 * self.height / 8 
            canvas.create_oval(x-self.r, y-self.r, x+self.r, y+self.r, fill = "red")
            x += 20
            """
        #some list of objects and their attributes 
        #canvas.create_oval(self.width//2 - self.r, 7* self.height/8-self.r, self.width//2 + self.r, 7* self.height/8+self.r, fill = 'red')
        canvas.create_image(self.width/2, 7*self.height/8, image = ImageTk.PhotoImage(self.imageEgg)) 
        canvas.create_text(6* self.width/8, 7*self.height/8, text = 'Press x to Exit', font = 'Verdana')

    def drawBasket(self, canvas):
        canvas.create_rectangle(6*self.width/8, 2*self.height/8, self.width, 5*self.height/8, fill = 'gray')
        canvas.create_text(7*self.width/8, 2.5 * self.height/8, text = 'BASKET', font = 'Verdana 20', fill = 'blue')
        counter = self.height/20
        for item in self.basket:
            canvas.create_text(7*self.width/8, 2.5*self.height/8 + counter, text = f'{item}')
            counter += self.height/25
    def mousePressed(self, event):
        mouseX, mouseY = event.x, event.y 
        #if mouseX in image and mouseY in image:
        #    trigger your pop up menu 
        self.messages.append((mouseX, mouseY))
        if mouseX <= self.width/2 and mouseY <= self.height/2:
            self.isIngredientScreen = True 
        if self.isCookingMode==True and mouseX<= self.width/2 and mouseY <= self.height/2:
            self.isApplianceScreen = True
        
    def keyPressed(self, event):
        if event.key =='Up': self.cy -= 20
        elif event.key == 'Down': self.cy += 20 
        elif event.key == 'Left': self.cx -= 20 
        elif event.key == 'Right': self.cx += 20

        elif self.isIngredientScreen: 
            if event.key == 'p':
            #add it to your basket!
                self.basket.append('Egg')
                print('egg added')

            elif event.key == 'x':
                self.isIngredientScreen = False

        #for ingredient page
        if event.key == 'Space':
            self.isTitleScreen = False
            self.isPantryMode = True 

        if self.isTimeUp:
            if event.key == 'n':
                self.isTimeUp = False
                self.isCookingMode = True 
                self.pantryTimer = 300000 
        
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
    def drawPerson(self, canvas): 
        canvas.create_oval(self.cx-self.r, self.cy-self.r, self.cx+ self.r, self.cy+self.r, fill = 'cyan')
    
    def drawPantry(self, canvas):
        canvas.create_image(self.width/2, self.height/6, image = ImageTk.PhotoImage(self.imageShelf))
        
    def drawTitleScreen(self, canvas):
        canvas.create_image(self.width/2, self.height/8, image = ImageTk.PhotoImage(self.imageChopped)) 
        canvas.create_rectangle(0, 0, self.width, self.height, fill = 'gray')
        canvas.create_text(self.width/2, self.height/2, text = "Welcome to Chopped Simulation!", font = 'Verdana 30')
        canvas.create_text(self.width/2, 6* self.height/8, text = 'Press Space To Play')

    def drawPantryMode(self, canvas):
        MyApp.drawPantry(self, canvas)
        MyApp.drawPerson(self, canvas)
        MyApp.drawGameAI(self, canvas)
        MyApp.drawStartingBasket(self, canvas)
        if self.isIngredientScreen:
            MyApp.drawIngredientScreen(self, canvas)
        MyApp.drawTimer(self, canvas)

    def drawCookingScreen(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = 'white')
        canvas.create_text(self.width/2, self.height/8, text = 'Next Round!')
        MyApp.drawCookingMap(self, canvas)
        if self.isApplianceScreen:
            MyApp.drawApplianceScreen(self, canvas)

    def drawApplianceScreen(self, canvas):
        canvas.create_rectangle(self.width/8, 5*self.height/7, 7*self.width/8, 6.5*self.height/7,fill='blue')
    def drawCookingMap(self, canvas):
        canvas.create_rectangle(0,self.height/5, self.width, self.height/3, fill = 'gray')
        canvas.create_rectangle(0,self.height/3, self.width/5, self.height/1.5, fill = 'pink')
        canvas.create_rectangle(4*self.width/5, self.height/3, self.width, self.height/1.5, fill = 'red')
        canvas.create_image(self.width/2, self.height/4, image = ImageTk.PhotoImage(self.imageOven)) 

    def drawStartingBasket(self, canvas):
        canvas.create_text(self.width/2, self.height/2.5, text = f'Your starting basket:', font = 'Verdana 11', fill = 'white')
        canvas.create_text(self.width/2, self.height/2, text = f'{self.basket}', font = 'Verdana 15', fill = 'red')

    def drawTimeUp(self, canvas):
        canvas.create_rectangle(self.width/6, self.height/3, 5* self.width/6, self.height/1.5, fill = 'deep sky blue', width = 0)
        canvas.create_text(self.width/2, self.height/2, text = 'TIMES UP! DROP YOUR HANDS!', font = 'Verdana 25', fill = 'maroon')
        canvas.create_text(self.width/2, self.height/1.8, text = 'Press n for next round')
    """
    def drawTimer(self, canvas):
        canvas.create_text(7* self.width/8, self.height/8, text = f'{self.countdown}')
        """
    def distance(self, x0, y0, x1, y1):
        return (( (x0-x1)** 2 + (y0-y1) **2 ) ** 1/2)

    def drawCookingMode(self, canvas):
        MyApp.drawCookingScreen(self, canvas)
        MyApp.drawTimer(self, canvas)
        MyApp.drawPerson(self, canvas)
        MyApp.drawGameAI(self, canvas)

#draw gameAI avatar

    def moveGameAI(self):
        possibleDirs = [(0,+1), (0,-1), (1,0), (-1,0)]
        direction = 500000* random.choice(possibleDirs)
        if MyApp.isLegal(self, direction):
            self.oppCX += direction[0]
            self.oppCY -= direction[1]
        else:
            direction = random.choice(possibleDirs)
            self.oppCX += direction[0]
            self.oppCY -= direction[1]
    #heuristic to move towards an appliance 
    #try to move towards the next thing you need 
    #once you finish each step, move onto assembling part 

    #for tp2:
    #finishing game ai 
    #using appliances in cooking mode
    #connect with web scraping
    #work on shared kitchen
    #no two ppl can share appliance at once
    #replace dots with characters
    #add ingredients 
    #collisoin detection 
#search psuedo code:
#initialize "frontier" w initial state 
#initialized explored set to be empty
#while frontier is not empty do:
    #remove node from frontier
    #if node is goal state then we are done
    #add node to explored set
    #expand node, add children to the frontier

#draw final product
    def drawFinalProduct(self): #for plating mode 
        """
        if item is base: add to bottom
        if item is midde: add to middle
        if item is topping: add to top 
        """
        return 
    def drawCombined(self):
        #mix the colors of items 
        #randomize pixel colors to generate new one
        return

    def isLegal(self, direction):
        return True 
    
    def drawGameAI(self, canvas):
        canvas.create_oval(self.oppCX-self.r, self.oppCY-self.r, self.oppCX+ self.r, self.oppCY+self.r, fill = 'red')


    def redrawAll(self, canvas):
        if self.isTitleScreen: MyApp.drawTitleScreen(self, canvas)
        elif self.isPantryMode: MyApp.drawPantryMode(self, canvas)
        if self.isTimeUp: MyApp.drawTimeUp(self, canvas)
        if self.isCookingMode: MyApp.drawCookingMode(self, canvas)
        
    """
    def webScraping(self):

        driver.get('https://forms.gle/7hmyNe5eYrDKuYub7')
        time.sleep(5)

        question1 = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div/span/div/div[1]/label'

        question2turkey = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/label/div/div[2]/div/span'
        question2mashed = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/label/div/div[2]/div/span'
        question3brussels = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[4]/label/div/div[2]/div/span'

        submitbutton = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div/div/span'
        #steps the automation needs to take
        clickmpc = driver.find_element_by_xpath(question1).click()

        clickturkey = driver.find_element_by_xpath(question2turkey).click()
        clickmashed = driver.find_element_by_xpath(question2mashed).click()
        clickbrussel = driver.find_element_by_xpath(question3brussels).click()
        clicksubmit = driver.find_element_by_xpath(submitbutton).click()
"""

MyApp(width = 600, height = 600)

#image.size 
#image.width
#image.height