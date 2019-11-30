import math, os, random

PATH = os.getcwd()

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
        
                    
    def display(self):
        
        self.movement()
        
        image(self.__img, self.__center_x - self.__radius, self.__center_y - self.__radius, self.__radius * 2, self.__radius * 2)

player_cannonball = Cannonball(500, 400, 50)

def setup():
    size(1000, 800)
    background(255)

def draw():

    background(255)
    player_cannonball.display()
