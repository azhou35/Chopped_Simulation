#started Nov/30
#trying to set structure better
from cmu_112_graphics import *
from classesOfFood import * 
#Main class that calls different modes based on timer and such 
class MyApp(App):
    def appStarted(self):
    #instantiate objects
        self.cx = self.width/4
        self.cy = 3*self.height/4
        self.r = 20

        self.player = classesOfFood.Player(self, self.cx, self.cy)


    
        