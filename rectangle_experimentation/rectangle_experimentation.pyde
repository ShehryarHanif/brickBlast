import math, os, random

class Cannon:
    
    def __init__(self, base_x, base_y, cannon_width, cannon_height):
        
        self.__base_x = base_x
        self.__base_y = base_y
        self.__width = cannon_width
        self.__height = cannon_height
    
    def __specialDisplay(self):
        fill(0)
        rect(- self.__width / 2, -self.__height, self.__width, self.__height)
        
    def rotation(self):
        print("JELLO")
        print("y", abs(mouseY - self.__base_y))
        print("x", (mouseX - self.__base_x))
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
    
    
