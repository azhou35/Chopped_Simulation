from cmu_112_graphics import *

def appStarted(self):
    print('getting here')
    self.charPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/down.png'
    self.charImg = self.loadImage(self.charPath)
    self.scaleFactor = findScaleFactor(self, self.charImg, self.height//4)
    self.charImg = self.scaleImage(self.charImg, self.scaleFactor)
    self.originalCharImg = self.charImg
    print(self.originalCharImg.size)
    self.hat = 'chef'
    self.hats = ['chef', 'santa', 'octopus', 'hat']
    self.hatPaths = {'chef': '/Users/az/Documents/GitHub/Chopped_Simulation/images/chef.png', 
                    'santa': '/Users/az/Documents/GitHub/Chopped_Simulation/images/santa.png',   
                    'octopus': '/Users/az/Documents/GitHub/Chopped_Simulation/images/octopus.png',
                    'hat': '/Users/az/Documents/GitHub/Chopped_Simulation/images/hat.png' 
                    }
    self.hatLoadedImgs = dict()
    self.mashedPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/basketScreen.png'
    self.mashedImg = self.loadImage(self.mashedPath)
    for hat, path in self.hatPaths.items():
        self.hatPath = '/Users/az/Documents/GitHub/Chopped_Simulation/images/' + hat + '.png'
        self.loadedHatImg = self.loadImage(self.hatPath)
        scaleFactor = findScaleFactor(self, self.loadedHatImg, self.originalCharImg.size[0])
        self.loadedHatImg = self.scaleImage(self.loadedHatImg, scaleFactor)
        self.hatLoadedImgs[hat] = self.loadedHatImg
    self.img = combineCharImg(self, self.charImg, self.hatLoadedImgs['chef'])

def keyPressed(self, event):
    if event.key == 'Space':
        #self.charImg = combineCharImg(self, self.originalCharImg, self.hatLoadedImgs['santa'])
        self.charImg = pilCombine(self, self.originalCharImg, self.hatLoadedImgs['chef'])
        print('getting here')
def pilCombine(self, sprite, hat):
    self.charImg = Image.alpha_composite(sprite, hat)
    print(self.charImg)
def combineCharImg(self, sprite, hat):
    updatedChar = Image.new('RGBA', (sprite.width, min(sprite.height, hat.height)))
    updatedChar.paste(sprite, (0,0))
    updatedChar.paste(hat, (0, 0), hat.convert('RGBA'))

    updatedChar.save("merged.jpg","png")
    return updatedChar
def findScaleFactor(self, image, goalWidth):
    width, height = image.size 
    scaleFactor = goalWidth / width 
    return scaleFactor  
def redrawAll(self, canvas):
    canvas.create_rectangle(0, 0, self.width, self.height, fill = 'blue')
    canvas.create_image(2*self.width/3, self.height/2.7, image = ImageTk.PhotoImage(self.img))


runApp(width=400, height=400)