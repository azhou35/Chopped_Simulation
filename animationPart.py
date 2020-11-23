#animation
import selenium
import math, copy, random
from selenium.common.exceptions import NoSuchElementException 
import time
from selenium import webdriver
#input path name to where driver is
driver = webdriver.Chrome('/Users/az/Documents/GitHub/Zhou_Annie_112_TP/chromedriver')  # Optional argument, if not specified will search path.

from cmu_112_graphics import *


def randomIngredients(app):
    app.basket = random.choice(app.possibleIngredients, k = 3)    

def appStarted(app):

    app.possibleIngredients = ['potato', 'ice cream', 'banana', 'cheese stick',
                                'bun', 'grapes']
def timerFired(app,canvas):
    doStep(app)
    return  
def doStep(app):
    return
def keyPressed(app, event):
    if event.key == 'x':
        webScraping(app)
def drawText(app, canvas):
    canvas.create_text(text = "Press x to launch web scraping for form")
def redrawAll(app, canvas):
   drawText(app, canvas)     

def webScraping(app):

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


runApp(width = 1000, height = 1000)