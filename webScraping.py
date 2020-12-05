#webScraping code
#import modules
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import time
#function to go thru every ingred in final Product 
def recipeScraper(finalProduct):

    driver = webdriver.Chrome('//Users/az/Documents/GitHub/Chopped_Simulation/chromedriver')  # Optional argument, if not specified will search path.
    driver.get('https://www.yummly.com/pantry-search/')
    time.sleep(5) # Let the user actually see something!

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
    #frame = driver.find_element_by_xpath('//frame[@name="main"]')
    #driver.switch_to.frame(frame)
    #findSearchButton = driver.find_element_by_class_name("button search-submit-button btn-primary")s

#    clickSearchButton = findSearchButton.click()

    time.sleep(15)

    
    #recipesResult = '//html//body//div[3]//div[1]//div[3]//div//div[2]//section[1]//h4'
    #findRecipesResult = driver.find_element_by_xpath(recipesResult)
    #findRecipesResult = driver.find_element_by_class_name("grid-title h4-text primary-dark font-bold")
    h4Results = driver.find_elements_by_tag_name('h4')
    recipeResult = h4Results[1]
    #recipeText = recipeResult.getAttribute("outerHTML")
    
    #print(recipeText)
    
    #search_box = driver.find_element_by_name('q')
    #search_box.send_keys('ChromeDriver')
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

    #https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
    #PARSING THE HTML PAGE

#gameAINumRecipes = recipeScraper(finalProduct)
#print(gameAINumRecipes)
"""
driver.get('https://myfridgefood.com/?detailed=true')
    time.sleep(5)

    for ingredient in finalProduct:
        name = ingredient.name 
        driver.find_element_by_xpath('//button[@type=f"{name}"]').click()
    driver.find_element_by_xpath(‘//button[@type="Find Recipes"]’).click()
    #count the number of resulting recipes 

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
    #convert basket ingredients and stuff into key words for scraping
    return
"""