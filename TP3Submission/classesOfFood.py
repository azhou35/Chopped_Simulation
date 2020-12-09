
#CITATION: how to set up classes taken from https://www.cs.cmu.edu/~112/notes/notes-oop-part2.html
#CITATION: RANDOM MODULE FROM https://docs.python.org/3/library/random.html
import random

#callable function to set up objects given a dietary list of which ingreds to avoid, randomizes basket accordingly, returns objects
def setUpObjects(dietaryList):

    cookbooks = setUpCookbooks()
    basket = randomizeBasket(cookbooks[0], dietaryList)
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
    Egg = Staples('egg', 'protein')
    Butter = Staples('butter', 'dairy')
    Milk = Staples('milk', 'dairy')
    Onion = Staples('onion', 'vegetable')
    Flour = Staples('flour', 'grain')
    Strawberry = Staples('strawberry', 'fruit')
    Lettuce = Staples('lettuce', 'vegetable')
    Fish = Staples('fish', 'protein')
    Cheese = Staples('cheese', 'dairy')
    Chicken = Staples('chicken', 'protein')
    Tomato = Staples('tomato', 'vegetable')
    Kale = Staples('kale', 'vegetable')
    Rice = Staples('rice', 'grain')
    Sugar = Staples('sugar', 'fruit')
    Bread = Staples('bread', 'grain')
    Naan = Staples('naan', 'grain')




    ingredients = (Potato, Butter, Milk, Onion, Flour, Strawberry, Lettuce, Fish, Cheese, Chicken, Tomato, Kale, Rice, Sugar, Bread, Naan, Egg)

    
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
    if method in recipe[1]:
        return True        
    else:
        return False 
#"wrapper" function that goes through every recipe in the three cookbooks and checks if the ingredients fit in any of the 
#recipes 
#returns the new dish item that it creates 
def validCombination(basket, methods, firstLevelCookbook, secondLevelCookbook, thirdLevelCookbook):
    for cookbook in [firstLevelCookbook, secondLevelCookbook, thirdLevelCookbook]:
        for dish, recipe in cookbook.items():
            #if dish == 'mashedPotato':
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
                        'mashedPotato': [['potato', 'milk', 'butter'], ['mix', 'saute', 'blend']],                    
                        'cookedFish': [['fish'], ['saute', 'bake']],
                        'salad': [['lettuce', 'onion', 'kale'], ['mix', 'stack']],
                        'toastedNaan': [['naan'], ['saute', 'bake']]

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
def combos():
    idealCombos = [['cheese', 'tomato', 'bread'], ['milk', 'sugar']]
    grossCombos = [['fish', 'strawberry'], ['chicken', 'sugar'], ['tomato', 'milk'], ['potato', 'sugar']]
    return idealCombos, grossCombos
#list of all the base ingredients 
def ingredientList(firstLevelCookbook):
    ingredients = set()
    for dish, recipe in firstLevelCookbook.items():
        #look at every ingredient in recipe, add it to set, since it's a set, it won't add duplicates
        for ingred in recipe[0]:
            ingredients.add(ingred)
    return ingredients


#randomize basket given cookbook and which ingreds to avoid
#adjusted to not include allergens
def randomizeBasket(cookbook, dietaryList):
    #call helper function to get all possible ingredients from firstCookbook level
    ingredients = ingredientList(cookbook)
    #convert to list to make subscriptable for random.choices
    ingredients = list(ingredients)
    #remove any bad in gredients
    if 'vegetarian' in dietaryList:
        ingredients.remove('chicken')
        ingredients.remove('fish')
    if 'vegan' in dietaryList:
        ingredients.remove('milk')
        ingredients.remove('butter')
        ingredients.remove('egg')
    basket = random.choices(ingredients, k=2)
    return basket

#create any possible iterations of firstLevelCookbook from basket ingredients, which will be used
#to build up game AI recipe
#combinations starts off as an empty list (2D)
#since each combination can be an ingredient in another level's recipe, keep calling recursively
#until you've looked thru all possible cookbooks 
def accessRecipes(basket, cookbooks):
    recipeDict = dict()
    for i in range(3):
        dishList = list() 
        possibleRecipes = list()
        for dish, recipe in cookbooks[i].items():
            #loop thru every ingredient
            for ingred in basket:
                if ingred in recipe[0]:
                    #check that recipe wasn't added already
                    if not dish in recipeDict:
                        recipeDict[dish] = recipe
    return recipeDict
#RECURSIVE function to return list of all the possible combinations you can make IF the ingredient within basket is within the recipe
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
#search for the final dish in cookbook dictionary and returns the recipe (ingredients + appliance)
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

#set up ingredient object with possible fucntions to combine with other ingredients given other ingredients and method
class Staples(object):
    cookbooks = setUpCookbooks()
    def __init__(self, name, foodGroup):
        self.name = name
        #set up object's path given str
        self.path = './images' + f'/{self.name}' + '.png'
        self.foodGroup = foodGroup 

    #function to combine two ingredients using a method
    def combine(self, listOfOtherIngredients, method):
        self.totalIngredients = [self.name]
        for ingred in listOfOtherIngredients:
            self.totalIngredients.append(ingred.name) #access their name attribute, should be a list of strings
        #call helper function to see if this combination of ingredients can create anything
        #self.totalIngredients = [self.name]
        #self.totalIngredients += listOfOtherIngredients 
        combination = validCombination(self.totalIngredients, method, Staples.cookbooks[0], Staples.cookbooks[1], Staples.cookbooks[2])
        #combination is either none or the dish that it creates
        if combination != None:
            return combination #return the dish created
        else: #in the case it is none
            uniqueCombo = ''
            for ingred in self.totalIngredients: 
                if self.totalIngredients.index(ingred)==0: #if the ingredient is the first in list 
                    uniqueCombo = uniqueCombo + ingred
                else: 
                    uniqueCombo = f'{uniqueCombo} + {ingred}'
            return uniqueCombo
    
    #code taken from https://www.cs.cmu.edu/~112/notes/notes-oop-part3.html
    def __repr__(self):
        return f'{self.name}'
            

#class to set up appliance object and its path
class Appliance(object):
    def __init__(self, name, method): #location is a tuple 
        self.name = name
        self.method = method 
        self.path = './images' + f'/{self.name}'
        self.cellsInLength = 5
        self.cellsInWidth = 1 
#GAME AI CODE 
#class to set up game AI that inherit from player class, randomizes final product, generates the appliances and groceries it needs to make the final product
class gameAI(Player):
    def __init__(self, row, col, basket, cookbooks):
        super().__init__(row, col, basket, cookbooks) #super method to inherit methods and properties from parents
        self.finalProduct = ''
        self.applianceList = list()
        self.groceries = set() 
 
    #function for gameAI to choose which final Product to make based on basket
    def randomizeFinalProduct(self):
        randomCookbook = random.randint(0, 2)
        #call recursive helper function to get all possible recipes from cookbooks
        possibilities = itemInRecipe(self.basket, self.cookbooks, combinations=[])
        tot = possibilities[randomCookbook]
        if len(tot) == 0:
            self.finalDish = 'mashedPotatoes'
        else:
            self.finalDish = random.choice(tot)

    #function to create list of appliances and ingredients game Ai needs to use in order to create final dish
    def generateApplianceAndGroceriesList(self):
        #find recipe
        total = len(self.cookbooks)
        #loop thru list backwards
        for index in range(total-1, -1, -1):
            recipe = returnRecipe(self.finalDish, self.cookbooks, index)
            if recipe != None:
                #add a random appliance from this list of appliances
                self.applianceList.append(random.choice(recipe[1]))
                for item in recipe[0]: #add grocery ingredients
                    self.groceries.add(item)
                while index != 0: #if ur not at the 1st cookbook, u have more levels to check 
                    for dish in recipe[0]:
                            #look at cookbooks lower than this index
                        for i in range(index-1, -1, -1):
                            innerRecipe = returnRecipe(dish, self.cookbooks, i)
                            if innerRecipe != None: 
                                self.applianceList.append(random.choice(innerRecipe[1]))
                                for item in innerRecipe[0]:
                                    self.groceries.add(item)
                    index -=1 
                if index == 0: 
                    for baseIngred in recipe[0]:
                        self.groceries.add(baseIngred)
    #def generateGroceries(self):


                    #find base level ingredients
                            #search cookbook 
    #create any possible iterations of firstLevelCookbook from basket ingredients, which will be used
    #to build up game AI recipe
    #i think this cna be recurive too
    #combinations starts off as an empty list (2D)
    #since each combination can be an ingredient in another level's recipe, keep calling recursively
    #until you've looked thru all possible cookbooks 

    #recursively find item combinations
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

