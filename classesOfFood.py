import random


def setUpObjects():

    cookbooks = setUpCookbooks()
    basket = randomizeBasket(cookbooks[0])
    row, col = 0, 0
    Person = Player(row, col, basket, cookbooks)
    Opponent = gameAI(row, col, basket, cookbooks)

    Oven = Appliance('oven', 'bake')
    Stovetop = Appliance('stove', 'saute')
    Blender = Appliance('blender', 'blend')
    Whisk = Appliance('whisk', 'mix')
    Plating = Appliance('plating', 'stack')
    
    appliances = (Oven, Stovetop, Blender, Whisk, Plating)

    Potato = Staples('potato', 'vegetable')
    Butter = Staples('butter', 'dairy')
    Milk = Staples('milk', 'dairy')

    ingredients = (Potato, Butter, Milk)

    print(Potato.combine([Milk, Butter], ['saute']))
    
    return cookbooks, basket, Person, Opponent, appliances, ingredients

#helper function that takes in list of ingredients, list of cooking methods, and a specific recipe
#returns if the list of ingredients can combine into the recipe 
def isRecipe(inventory, method, recipe):
    #recipe is a 2D list
    neededIngredients = recipe[0]
    #check to see if every necessary ingredient is in your current inventory of ingredients
    for food in neededIngredients:
        if food not in inventory:
            return False
    #you exit for loop only if you have every necessary ingredient

    #now check if the appliance you're at is in the recommended appliance
    
    if method[0] in recipe[1]:
            return True        
    return False 
#"wrapper" function that goes through every recipe in the three cookbooks and checks if the ingredients fit in any of the 
#recipes 
#returns the new dish item that it creates 
def validCombination(basket, methods, firstLevelCookbook, secondLevelCookbook, thirdLevelCookbook):
    for cookbook in [firstLevelCookbook, secondLevelCookbook, thirdLevelCookbook]:
        for dish, recipe in cookbook.items():
            if isRecipe(basket, methods, recipe):
                return dish #return the dish that it successfully creates 
    return None 
    
def setUpCookbooks():
    #12/2 setting up recipes for food, simplified representations
    #first listindex of recipe is all the REQUIRED ingredients
    #second list index of recipe is all the POSSIBLE appliances
    firstLevelCookbook = {'toast': [['bread'], ['saute', 'bake']],
                        'batter': [['egg', 'milk', 'flour', 'sugar'], ['mix']],
                        'cheeseSandwich': [['bread', 'cheese'], ['stack', 'saute', 'bake']],
                        'tomatoSauce': [['tomato'], ['mix', 'saute', 'blend']],
                        'strawberrySauce': [['strawberry', 'sugar'], ['mix', 'saute', 'blend']],
                        'cookedChicken': [['chicken'], ['saute', 'bake']],
                        'friedEgg': [['egg'], ['saute', 'bake']], 
                        'cookedRice': [['rice'], ['saute']],
                        'mashedPotato': [['potato', 'milk', 'butter'], ['mix', 'saute', 'blend']]                    

    }     

    secondLevelCookbook = {'tomatoPasta': [['tomatoSauce', 'pasta'], ['saute', 'mix', 'bake']], 
                        'cake': [['batter'], ['bake']],
                        'pancake': [['batter'], ['saute']],
                        'eggToast': [['toast', 'friedEgg'], ['stack']],
                        'flavoredChicken': [['chicken', 'tomatoSauce'], ['saute', 'mix', 'bake']],
                        'strawberryMilk': [['strawberrySauce', 'milk'], ['saute', 'blend', 'mix']],
                        'friedEggRice': [['friedEgg', 'cookedRice'], ['saute']]
    }

    thirdLevelCookbook = {
                        'avoEggToast': [['eggToast', 'avocado'], ['stack']],
                        'strawberryCake': [['strawberrySauce', 'cake'], ['stack']],
                        'strawberryPancake': [['strawberrySauce', 'pancake'], ['stack']],
                        'chickenParm': [['flavoredChicken', 'cheese'], ['stack', 'bake', 'saute']],    
                        'potatoChicken': [['mashedPotato', 'flavoredChicken'], ['stack']]

    }

    #looks at attribues only
    generalCookbook = {'sandwich': [['grain', 'protein'], ['stack']],
                        'puree': [['fruit'], ['blend', 'saute']],
                        'sauce': [['vegetable'], ['saute', 'blend']],
                        'proteinPasta': [['pasta', 'protein'], ['mix', 'saute', 'bake']],
                        'dairyPasta': [['pasta', 'dairy'], ['mix', 'saute', 'bake']],
                        'veggiePasta': [['pasta', 'vegetable'], ['mix', 'saute', 'bake']],
                        'salad': [['vegetable'], ['mix', 'saute', 'bake']],
                        'stirFry': [['vegetable', 'protein'], ['saute']]
    }
    cookbooks = [firstLevelCookbook, secondLevelCookbook, thirdLevelCookbook]
    return cookbooks 
#list of all the base ingredients 
def ingredientList(firstLevelCookbook):
    ingredients = set()
    for dish, recipe in firstLevelCookbook.items():
        #look at every ingredient in recipe, add it to set, since it's a set, it won't add duplicates
        for ingred in recipe[0]:
            ingredients.add(ingred)
    return ingredients



#should I use recursion? 
#result from this should be a list of all the appliances I need to visit 
def randomizeBasket(cookbook):
    #call helper function to get all possible ingredients from firstCookbook level
    ingredients = ingredientList(cookbook)
    #convert to list to make subscriptable for random.choices
    ingredients = list(ingredients)
    basket = random.choices(ingredients, k=4)
    return basket

#create any possible iterations of firstLevelCookbook from basket ingredients, which will be used
#to build up game AI recipe
#i think this cna be recurive too
#combinations starts off as an empty list (2D)
#since each combination can be an ingredient in another level's recipe, keep calling recursively
#until you've looked thru all possible cookbooks 
def itemInRecipe(basket, cookbooks, combinations):
    if len(cookbooks)==0:
        return combinations 
    else:
        dishList = list() 
        possibleRecipes = list()
        for dish, recipe in cookbooks[0].items():
            #loop thru every ingredient
            for ingred in basket:
                if ingred in recipe[0]:
                    #check that recipe wasn't added already
                    if not recipe in possibleRecipes:
                        if not dish in dishList:
                            possibleRecipes.append(dish)
                            dishList.append(dish)
        combinations.append(possibleRecipes)
        return itemInRecipe(basket+dishList, cookbooks[1:], combinations)

#function that creates a random path for game ai to follow based on which appliances
#it needs, given a recipe 
def returnRecipe(finalDish, cookbooks, index):
    for dish, recipe in cookbooks[index].items(): 
        if dish == finalDish: 
            return recipe 
    else:
        return None 

class Player(object):
    def __init__(self, row, col, basket, cookbooks):
        self.row = row
        self.col = col 
        self.basket = basket 
        self.cookbooks = cookbooks
        self.inventory = basket #will hold basket ingreds + all the stuff u shop for
    #taken from https://www.cs.cmu.edu/~112/notes/notes-oop-part3.html#convertingToStrings
    #def __repr__(self):
    #    return f'{self}'

class Staples(object):
    cookbooks = setUpCookbooks()
    def __init__(self, name, foodGroup):
        self.name = name
        self.path = '/Users/az/Documents/GitHub/Chopped_Simulation/images' + f'/{self.name}' + '.png'
        self.foodGroup = foodGroup 

    #function to combine two ingredients using a method
    def combine(self, listOfOtherIngredients, method):
        self.totalIngredients = [self.name]
        for ingred in listOfOtherIngredients:
            self.totalIngredients.append(ingred.name) #access their name attribute, should be a list of strings
        #call helper function to see if this combination of ingredients can create anything
        combination = validCombination(self.totalIngredients, method, Staples.cookbooks[0], Staples.cookbooks[1], Staples.cookbooks[2])
        #combination is either none or the dish that it creates
        if combination != None:
            return combination #return the dish created
        else: #in the case it is none
            uniqueCombo = ''
            for ingred in self.totalIngredients: 
                if self.totalIngredients.index(ingred)==0: #if the ingredient is the first in list 
                    uniqueCombo += ingred
                else: 
                    uniqueCombo += f' + {ingred}'
    #code taken from https://www.cs.cmu.edu/~112/notes/notes-oop-part3.html
    def __repr__(self):
        return f'{self.x}'
            


class Appliance(object):
    def __init__(self, name, method): #location is a tuple 
        self.name = name
        self.method = method 
        self.path = '/Users/az/Documents/GitHub/Chopped_Simulation/images' + f'/{self.name}'
        self.cellsInLength = 5
        self.cellsInWidth = 1 

class gameAI(Player):
    def __init__(self, row, col, basket, cookbooks):
        super().__init__(row, col, basket, cookbooks) #super method to inherit methods and properties from parents
        self.finalProduct = ''
        self.applianceList = list()
        self.groceries = set() 
 
    #function for gameAI to choose which final Product to make based on basket
    def randomizeFinalProduct(self):
        randomCookbook = random.randint(0, 3)
        #call recursive helper function to get all possible recipes from cookbooks
        possibilities = itemInRecipe(self.basket, self.cookbooks, combinations=[])
        self.finalDish = random.randchoice(possibilities[randomCookbook])

    #function to create list of appliances and ingredients game Ai needs to use in order to create final dish
    def generateApplianceAndGroceriesList():
        #find recipe
        total = len(self.cookbooks)
        #loop thru list backwards
        for index in range(total-1, -1, -1):
            recipe = returnRecipe(self.finalDish, self.cookbooks, index)
            if recipe != None:
                #add a random appliance from this list of appliances
                self.applianceList.append(random.choice(recipe[1]))

                while index != 0: #if ur not at the 1st cookbook, u have more levels to check 
                    for dish in recipe[0]:
                            #look at cookbooks lower than this index
                        for i in range(index-1, -1, -1):
                            innerRecipe = returnRecipe(dish, self.cookbooks, i)
                            if innerRecipe != None: 
                                self.applianceList.append(random.choice(innerRecipe[1]))
                    index -=1 
                if index == 0: 
                    for baseIngred in recipe[0]:
                        self.groceries.add(baseIngred)
                    #find base level ingredients
                            #search cookbook 
    #create any possible iterations of firstLevelCookbook from basket ingredients, which will be used
    #to build up game AI recipe
    #i think this cna be recurive too
    #combinations starts off as an empty list (2D)
    #since each combination can be an ingredient in another level's recipe, keep calling recursively
    #until you've looked thru all possible cookbooks 
    def itemInRecipe(basket, cookbooks, combinations):
        if len(cookbooks)==0:
            return combinations 
        else:
            dishList = list() 
            possibleRecipes = list()
            for dish, recipe in cookbooks[0].items():
                #loop thru every ingredient
                for ingred in basket:
                    if ingred in recipe[0]:
                        #check that recipe wasn't added already
                        if not recipe in possibleRecipes:
                            if not dish in dishList:
                                possibleRecipes.append(dish)
                                dishList.append(dish)
            combinations.append(possibleRecipes)
            return itemInRecipe(basket+dishList, cookbooks[1:], combinations)

    #function that creates a random path for game ai to follow based on which appliances
    #it needs, given a recipe 
    def returnRecipe(finalDish, cookbooks, index):
        for dish, recipe in cookbooks[index].items(): 
            if dish == finalDish: 
                return recipe 
        else:
            return None 
   


"""
combinations = []
combinations = itemInRecipe(['potato', 'chicken', 'strawberry', 'egg'], cookbooks, combinations)
print(f'this is combinations: {combinations}')
"""
#not getting to third cookbook
#for some reason 

    #get list of every possible firstLevel component that contains basket ingredients



"""
class Sauces(Staples):
    def __init__(self):
        super().__init__(self, name, foodGroup)
        #self.cookingMethods = ['mix', 'bake', 'blend'] #how do i initlalize this w objects

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
"""

"""    
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


class gameAI(Player):
    basket = list() #list of ingredient object
    def __init__(self, cx, cy, difficulty):
        super().__init__(self, cx, cy)
    def moveDir(self, dx, dy):
        self.cx += dx
        self.cy += dy 
    def addToBasket(self, ingredient):
        gameAI.basket.append(ingredient)
    def randomizeFinalProduct(self):
        r1 = random.randint(0, 1000)
        if (r1<300): #bad dish
            #randomly choose from base
            #randomly choose from either fruit or vegetable
                #randomly choose item from there
            #randomly choose a purree
            return
        elif (r1>300 and r1<700): #meh dish
            #randomly choose a second-degree ingredient
            #see what items you need need, what appliances 
            return
        else:
            #randomly choose a third-degree ingredient
            #see what second-degree ingredients you need, what appliances 
                #what first degrees, what items from pantry
            #choose from an optimal combination listed
            #follow a preset recipe? 
            #call webscraping for a recipe that u know is good 
            return

"""
def optimalIngredientCombos(ingredients):
    return 

def isLegal(direction):
    return True 


    #similar to word search

    #does this need to be recurisve?


    #choose a random direction (up, down, right, left)
    #check if next cell of grid is a wall or an appliance
    #randomly interact with wall for a bit
    #if cell is wall go back to step 1
    #else move avatar to that cell 
    #depthfirst algorithm 
    #or pathfinding algorithm
    return 

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
def kitchenNightmare(avatar):
    #chance events happening to your food like food randomly burning
    #ice cream machine not working
    #food is dropp
    #maybe triggers a mini game where you have to save your food or else deduction

    return 
def kitchenDreams(basket):
    #did they have flavor combos like sofrito? like mirepoix? 
    return 

def nameInput(input):
    #get user to name their final dish 
    return
def gameMode(basket):
    #hell's ktichen -- random bad chance events higher probability 
    #college mode -- inspired by what you get in college and rlly ratchet supplies
    return 
