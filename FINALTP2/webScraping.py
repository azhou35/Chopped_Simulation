#webScraping code
#import modules
#CITATION: SELENIUM USED FROM HERE https://pypi.org/project/selenium/ FOR WEBSCRAPING
#CITATION: SELENIUM DOCUMENTATION AND FUNCTIONS FROM https://www.selenium.dev/documentation/en/
#CITATION: WEBDRIVER DOWNLOADED FROM https://chromedriver.chromium.org/downloads 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
#CITATION: time module https://docs.python.org/3/library/time.html
import time
#function to go thru every ingred in final Product 
def recipeScraper(finalProduct):
    #your own path for wherever webdriver is downloaded
    driver = webdriver.Chrome('//Users/az/Documents/GitHub/Chopped_Simulation/chromedriver')  # Optional argument, if not specified will search path.
    #CITATION: RECIPE RESULTS TAKEN FROM 'https://www.yummly.com/pantry-search/'

    driver.get('https://www.yummly.com/pantry-search/')
    time.sleep(5)

    #click out of automatic pop up
    startSearchBox = '//*[@id="mainApp"]/div[2]/div/div/div/div/a[1]'
    findSearchBox = driver.find_element_by_xpath(startSearchBox)
    clickStartSearchBox = findSearchBox.click()
    
    #click input box
    time.sleep(5) # Let the user actually see something!
    inputBox = '//*[@id="mainApp"]/div[1]/div[5]/div/div/div/div[1]/form/div/input'
    findInputBox = driver.find_element_by_xpath(inputBox)
    clickInputBox = findInputBox.click()

    #input each ingredient into box
    for ingred in finalProduct:
        findInputBox.send_keys(ingred)
        time.sleep(5) # Let the user actually see something!
        findInputBox.send_keys(Keys.RETURN)
    
    time.sleep(5)
    #click outside to reveal search button    
    outside = '//*[@id="mainApp"]/div[1]/div[5]/div/p'
    findOutside = driver.find_element_by_xpath(outside)
    clickFindOutside = findOutside.click()
    #print('click successful')
    #click search button to search
    time.sleep(5)
    searchButton = '//html//body//div[3]//div[1]//div[5]//div//div[1]//div//div[3]//button[1]'
    #findSearchButton = driver.find_element_by_class_name("button search-submit-button btn-primary")
    #driver.switch_to.frame(frame)
    
    #searchClass = driver.find_element_by_class_name("button search-submit-button btn-primary")
    findSearchButton = driver.find_element_by_xpath(searchButton)
    #try without xPath 
    #find all the search buttons 
    #find the right index 
    #find all elements of "search Button"

    clickSearchButton = findSearchButton.click()

    time.sleep(15)

    h4Results = driver.find_elements_by_tag_name('h4')
    recipeResult = h4Results[1]

    #search_box.submit()
    recipeText = recipeResult.text
    num = ''
    for x in recipeText:
        if x in '0123456789':
            num = num + x
        if x== " ":
            break
    #convert back into a number 
    num = int(num)
    #driver.quit()
    return num
