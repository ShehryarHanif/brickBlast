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

class Cannonball:
    
    def __init__(self, center_x, center_y, radius):
        
        self.__img = loadImage(PATH  + "/Images/Cannonball.png")
        
        self.__center_x = center_x
        self.__center_y = center_y
        
        self.__radius = radius
        
        self.__left_x = self.__center_x - self.__radius
        self.__right_x = self.__center_x + self.__radius
        
        self.__up_y = self.__center_y - self.__radius
        self.__down_y = self.__center_y + self.__radius
        
        self.__vy = -3
        self.__vx = 05
        
        self.__block_list = []
        
        block_1 = Block(255, 0, 0, 750, 600, 150, 100)
        block_2 = Block(0, 0, 255, 250, 200, 150, 100)
        
        self.__block_list.append(block_1)
        self.__block_list.append(block_2)
    
    def movement(self):
            
        if self.__down_y >= 800 or self.__up_y <= 0:
            
            self.__vy = -1 * self.__vy
            
        if self.__left_x <= 0 or self.__right_x >= 1000:
            
            self.__vx = -1 * self.__vx
            
        self.__center_x = self.__center_x + self.__vx
        self.__center_y = self.__center_y + self.__vy
        
        self.__left_x = self.__center_x - self.__radius
        self.__right_x = self.__center_x + self.__radius
        
        self.__up_y = self.__center_y - self.__radius
        self.__down_y = self.__center_y + self.__radius

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
  
