#Term Project Try 2
#My code all deleted i AM SO SAD

from urllib.request import urlopen
#Step 0.5: Learn Basic Url opening
url = "http://olympus.realpython.org/profiles/aphrodite"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
title_index = html.find("<title>")
start_index = title_index + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]
#print(title)

url = "http://olympus.realpython.org/profiles/poseidon"
url = "http://olympus.realpython.org/profiles/poseidon"
page = urlopen(url)
start_index = html.find("<title>") + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]

#Step 1: Use BeautifulSoup
import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen


url = "https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
#print(soup.get_text())
print(f"This is title string {soup.title.string}")
listOfNames = list()
for link in soup.find_all("a"):
    try:
        link_url = url + link["href"]
        listOfNames.append(link_url)
    except:
        pass
print(f"This is list of names {listOfNames}")

url2 = "http://olympus.realpython.org/profiles/dionysus"
page2 = urlopen(url2)
html2 = page2.read().decode("utf-8")
soup2 = BeautifulSoup(html2, "html.parser")
#print(soup2.get_text())
noLines = soup2.get_text().replace("\n", " ")
#print(noLines)
image1, image2 = soup2.find_all("img")
print(f"This is title {soup2.title}")

#STEP 1.5 LOLMAO
import re
test_string = "sad bc term project is making me sad" 
filter = re.findall("sad", test_string) 
filter2 = re.findall("[a-c]", test_string)
print(filter)
print(filter2)

#Step 2 Use Selenium
import time
from selenium import webdriver
#input path name to where driver is
driver = webdriver.Chrome('/Users/az/Documents/GitHub/Zhou_Annie_112_TP/chromedriver')  # Optional argument, if not specified will search path.
"""
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
"""

#ok this works!!! 
#try to run on headless browder without graphics 
"""
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver.get("https://www.nintendo.com/")
print(driver.page_source)
driver.quit()
"""

#EXAMPLE: logging into a simple log in page Y Combinator
"""
driver.get("https://news.ycombinator.com/login")

login = driver.find_element_by_xpath("//input").send_keys('anniepotato')
password = driver.find_element_by_xpath("//input[@type='password']").send_keys('mashedpotatoes')
submit = driver.find_element_by_xpath("//input[@value='login']").click()

# dont forget from selenium.common.exceptions import NoSuchElementException  
try:
    logout_button = driver.find_element_by_id("logout")
    print('Successfully logged in')
except NoSuchElementException:
    print('Incorrect login/password')
"""
#https://towardsdatascience.com/using-python-and-selenium-to-automate-filling-forms-and-mouse-clicks-f87c74ed5c0f


#Example: Using Selenium to Fill out arbitrary google form
from selenium.common.exceptions import NoSuchElementException 

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
