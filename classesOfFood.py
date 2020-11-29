class Staples(object):
    def __init__(self, name, flavor):
        self.name = name
        self. flavor = flavor
        self.quant = 0 
        self.path = '/Users/az/Documents/GitHub/Chopped_Simulation/images' + f'/{self.name}'

    def addItem(self):
        self.quant+= 1
    def useItem(self):
        self.quant -= 1 
    def cookItem(self, appliance):
        self.appliance = appliance 
    
class Sauces(Staples):
    def __init__(self):
        super().__init__(self, name, flavor)
        self.appliances = [Mix, Oven, Blender] #how do i initlalize this w objects

class Grains(Staples):
    def __init__(self):
        super().__init__(self, name, flavor)
        self.placement: 'base'
class Produce(Staples):
    def __init__(self):
        self.appliances = [Knife, Saute, Blender] #how do i initlalize this w objects
class Protein(Staples):
    def __init__(self):
        self.appliances = [Knife, Saute, Oven] #how do i initlalize this w objects
class Dairy(Staples):
    def __init__(self):
        self.appliances = [Knife, Saute, Oven] #how do i initlalize this w objects


#these are the basket ingredients
class Wildcards(Staples):
    def __init__(self):
        return


class Appliance(object):
    def __init__(self, name, timer):
        self.name = name
        self.timer = timer
        self.isActive = True 
class Oven(Appliance):
    def __init__(self, name, timer):
        return
class Stove(Appliance):
    def __init__(self, name, timer):
        return

class Blender(Appliance):
    def __init__(self, name, timer):
        return

class Knife(Appliance):
    def __init__(self, name, timer):
        return


class Whisk(Appliance):
    def __init__(self, name, timer):
        return
class IceCreamMachine(Appliance):
    def __init__(self, name, timer):
        return
class Microwave(Appliance):
    def __init__(self, name, timer):
        return


#game ai code:
def setUpIngredients(finalProduct):
        
    egg = Staples('egg', 'neutral')
    icecream = Wildcards('icecream', 'sweet')
    #Produce
    fruitList = ['banana', 'strawberry', 'blueberry', 'persimmon', 'orange']
    for fruit in fruitList:
        fruit = Produce(f'{fruit}', 'sweet')
    veggieList = ['potato', 'mushroom', 'tomato', 'bok choy', 'brussel sprout', 'celery', 'carrot', 'onion']
    for veggie in veggieList:
        veggie = Produce(f'{veggie}', 'umami')
    grainList = ['tortilla', 'bread', 'bagel', 'pita', 'crackers']
    for grain in grainList:
        grain = Grains(f'{grain}', 'neutral')
    bakeryList = ['pancake', 'waffle']
    for sweet in bakeryList: 
        sweet = Grains(f'{sweet}', 'sweet')
    proteinList = ['beef', 'pork', 'chicken', 'tofu', 'egg']
    for protein in proteinList: 
        protein = Protein(f'{protein}', 'umami')
    dairyList = ['milk', 'yogurt', 'cheese']
    for dairy in dairyList: 
        dairy = Dairy(f'{dairy}', 'sweet')

#helper function to load image given image path property
def loadImage(ingredient, cx, cy):
    self.ingredientImage = self.scaleImage(self.loadImage(ingredient.path), 1/2)
    canvas.create_image(cx, cy, image = ImageTk.PhotoImage(self.ingredientImage)) 

def pantryMode(basket):
    return 
def cookBook(items, appliance):
    return
def scoreCalculator(basket):
    #uniqueness = 0 
    #for item in finalProduct:

    #look at how flavorful everything is for "uniqueness"
    #score deductions for burnt food
    return
def flavorCalculator(basket):
    return
def presentationCalculator(basket):
    #value color ful presentation
    colorsOfDish = list()
    for item in basket:
        colorsOfDish.append(colorPicker(item))
    #get average somehow 
    return pixelList
def colorPicker(item):
    pixelList = list()
    path = item.path
    for x in path.width:
        for y in path.height:
            pixelList.append(path.getpixel(x, y))
    #some how get average, then color from here
    #check out image.getdata()
    return pixelList 
def recipeScraper(finalProduct):

    driver = webdriver.Chrome('//Users/az/Documents/GitHub/Chopped_Simulation/chromedriver')  # Optional argument, if not specified will search path.


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
    #convert basket ingredients and stuff into key words for scraping
    return
def kitchenNightmare(avatar):
    #chance events happening to your food like food randomly burning
    #ice cream machine not working
    #food is dropp
    #maybe triggers a mini game where you have to save your food or else deduction

    return 
def kitchenDreams(basket):
    #did they have flavor combos like sofrito? like mirepoix? 
    return 
def gameAi(basket):
    #need a base, a fill, and a topping, and a sauce
    opponentFP = random.choices(basket, k = 3)

    #approximate Q learning representation
    #https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=5b844f22-9c1a-4247-9f97-ac6b0126162d
    #feature based representation
    #randomly automates something to create food as well
    #split screen? or same kitchen
    return 
def nameInput(input):
    #get user to name their final dish 
    return
def gameMode(basket):
    #hell's ktichen -- random bad chance events higher probability 
    #college mode -- inspired by what you get in college and rlly ratchet supplies
    return 
