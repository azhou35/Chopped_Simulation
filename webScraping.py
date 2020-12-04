def recipeScraper(finalProduct):

    driver = webdriver.Chrome('//Users/az/Documents/GitHub/Chopped_Simulation/chromedriver')  # Optional argument, if not specified will search path.


    driver.get('https://myfridgefood.com/?detailed=true')
    time.sleep(5)

    for ingredient in finalProduct:
        name = ingredient.name 
        driver.find_element_by_xpath(‘//button[@type=f'{name}']’).click()
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
