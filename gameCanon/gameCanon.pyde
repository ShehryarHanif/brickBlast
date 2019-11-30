import math, os, random

PATH = os.getcwd()

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
        image(self.__cannonBaselImg, - self.__width / 2, -self.__height, self.__width, self.__height / 300 * 115)
        
    def __specialDisplay(self):
        image(self.__cannonBarrelImg, - self.__width / 2, -self.__height, self.__width, self.__height)
        image(self.__cannonBaselImg, - self.__width / 2, -self.__height, self.__width, self.__height / 300 * 115)
        
    def rotation(self):
        angle = math.degrees(math.atan2(abs(mouseY - self.__base_y),(mouseX - self.__base_x)))
        print(angle)
        pushMatrix()
        translate(x,y)
        rotate(radians(90-angle))
        circle(0,0,10)
        stroke(255,00,00)
        line(0,0,100,0)
        stroke(0,255,0)
        line(0,0,0,100)
        self.__specialDisplay()
        popMatrix()
x, y = 500, 400
player_cannon = Cannon(x, y, 100, 246)

def setup():
    size(1000, 800)
    background(255)

def draw():
    background(255)
    rect(width / 2, height / 2, 100, 246)
    stroke(0)
    strokeWeight(5)
    line(x, y, mouseX, mouseY)
    player_cannon.rotation()


def mouseClicked():
    
    player_cannon.rotation()
    
    
