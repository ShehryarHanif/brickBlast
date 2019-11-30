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
        
        self.__block_list = []
        
        block_1 = Block(255, 0, 0, 750, 600, 150, 100)
        block_2 = Block(0, 0, 255, 250, 200, 150, 100)
        
        self.__block_list.append(block_1)
        self.__block_list.append(block_2)
    
    def movement(self):
        
        for block in self.__block_list:
            
            # if (block.y1 <= self.__down_y <= block.y1 + self.__vy and block.x1 <= self.__center_x <= block.x2) or (block.y2 - self.__vy <= self.__up_y <= block.y2 and block.x1 <= self.__center_x <= block.x2):
                
            #     self.__vy = -1 * self.__vy
                
            #     break
            
            # if (block.x2 - self.__vx <= self.__left_x <= block.x2 and block.y1 <= self.__center_y <= block.y2) or (block.x1 <= self.__right_x <= block.x1 + self.__vx and block.y1 <= self.__center_y <= block.y2):
            
            #     self.__vx = -1 * self.__vx
                
            #     break
            
            if (((block.y1) ** 2 - (self.__center_y) ** 2) ** 0.5 < self.__radius and block.x1 <= self.__center_x <= block.x2) or (((block.y2) ** 2 - (self.__center_y) ** 2) ** 0.5 < self.__radius and block.x1 <= self.__center_x <= block.x2):
                  
                  self.__vy = -1 * self.__vy
                  break
              
            if (((block.x1) ** 2 - (self.__center_x) ** 2) ** 0.5 < self.__radius and block.y1 <= self.__center_y <= block.y2) or (((block.x2) ** 2 - (self.__center_x) ** 2) ** 0.5 < self.__radius and block.y1 <= self.__center_y <= block.y2):
                  
                  self.__vx = -1 * self.__vx
                  break
            
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
        
        for block in self.__block_list:
            
            block.display()

class Block():
    
    def __init__(self, r, g, b, x, y, w, h):
        
        self.r = r
        self.g = g
        self.b = b
        
        self.x = x
        self.y = y
                
        self.w = w
        self.h = h
        
        self.x1 = self.x
        self.x2 = self.x + self.w
        
        self.y1 = self.y
        self.y2 = self.y + self.h
    
    def display(self):
        
        fill(self.r, self.g, self.b)
        stroke(self.r, self.g, self.b)
        rect(self.x, self.y, self.w, self.h)

player_cannonball = Cannonball(500, 400, 50)

def setup():
    size(1000, 800)
    background(255)

def draw():

    background(255)
    player_cannonball.display()
