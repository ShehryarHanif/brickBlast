import math, os, random

PATH = os.getcwd()
WIDTH, HEIGHT = 500, 700 #5:7 must be maintained
print PATH

class Cannon:
    
    def __init__(self, base_x, base_y, cannon_width, cannon_height): #cannon_width:cannon_height = 1:3 
        self.__base_x = base_x
        self.__base_y = base_y
        self.__width = cannon_width
        self.__height = cannon_height
        self.__cannonBarrelImg =  loadImage(PATH + "/Resources/Cannon/Cannon.png")
        self.__cannonBaseImg = loadImage(PATH + "/Resources/Cannon/CannonBase.png")
    
    def __specialCannonBarrelDisplay(self):
        image(self.__cannonBarrelImg, - self.__width / 2, -self.__height, self.__width, self.__height)
        
    def __specialCannonBaseImage(self):
        image(self.__cannonBaseImg, self.__base_x - self.__width / 2, int(self.__base_y - self.__height / 300.0 * 115.0), self.__width, int(self.__height / 300.0 * 115.0))
        
        
    def rotation(self):
        angle = math.degrees(math.atan2(abs(mouseY - (self.__base_y - (self.__height / 300.0 * 64.0))),(mouseX - self.__base_x)))
        line(self.__base_x, self.__base_y - (self.__height / 300.0 * 64.0), mouseX, mouseY)
        #print(angle)
        pushMatrix()
        translate(self.__base_x,self.__base_y - (self.__height / 300.0 * 64.0)) #to have the cannon pivot correctly, the end of the cannon is at 364 relative to base_y
        rotate(radians(90-angle))
        self.__specialCannonBarrelDisplay()
        popMatrix()
        self.__specialCannonBaseImage()

class Demarcator:
    def __init__(self):
        self.__height = 10 
        self.__color = "#25331F"
        self.__topCorner = (0, int(HEIGHT / 700.0 * 500.0 - self.__height / 2.0))
        print self.__topCorner
        self.__bottomCorner = (WIDTH, int(HEIGHT / 700.0 * 500.0 + self.__height / 2.0))
        print self.__bottomCorner
        
    def display(self):
        fill(self.__color)
        rectMode(CORNERS)
        rect(self.__topCorner[0], self.__topCorner[1], self.__bottomCorner[0], self.__bottomCorner[1])
        
    
        

class Game:
    def __init__(self):
        self.__playerCannon = Cannon(x, y, WIDTH / 10.0, WIDTH / 10.0 * 3)
        self.__gameEndLine = Demarcator()
        
    def __updateAndDisplayCannon(self):
        self.__playerCannon.rotation()
        
    def display(self):
        self.__gameEndLine.display()
        self.__updateAndDisplayCannon()
    


def setup():
    size(WIDTH, HEIGHT)
    background(255)
    
x, y = WIDTH / 2, HEIGHT
brickBlast = Game()

def draw():
    background(255)
    brickBlast.display()
  
