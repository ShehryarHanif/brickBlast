add_library('minim') # We add the library we will be using for playing sounds and music.


import math, os, time, random # We import the various modules we will be using.


PATH = os.getcwd() # We save our current working directory in this global constant.

WIDTH, HEIGHT = 500, 700 # The ratio of "5:7" must be maintained for the width and height of the game window.

player = Minim(this) # This refers to the "music player"


class Cannon: # This is the cannon object which can be thought of as the "player".
    
    def __init__(self, base_x, base_y, cannon_width, cannon_height): # The ratio "cannon_width : cannon_height = 1 : 3" must be maintained. The image will consist of the cannon consists of two parts: the rotating cannon and the still base.
        
        self.__base_x = base_x # This is the x-coordinate for the base's center.
        self.__base_y = base_y # This is the y-coordinate for the base's center.
        self.__width = cannon_width # This is the width of the cannon image being used.
        self.__height = cannon_height # This is the height of the cannon image being used.
        self.__cannonBarrelImg =  loadImage(PATH + "/Resources/Cannon/Cannon.png") # We import the image of the cannon.
        self.__cannonBaseImg = loadImage(PATH + "/Resources/Cannon/CannonBase.png") # We import the image of the cannon's base.
    
    def __specialCannonBarrelDisplay(self): # This method will be later used to display the rotating cannon's image.
        
        image(self.__cannonBarrelImg, - self.__width / 2, -self.__height, self.__width, self.__height)
        
    def __specialCannonBaseImage(self): # This method will be later used to display the still cannon base's image.
        
        image(self.__cannonBaseImg, self.__base_x - self.__width / 2, int(self.__base_y - self.__height / 300.0 * 115.0), self.__width, int(self.__height / 300.0 * 115.0))

    def changePosition(self, newPosition): # This function will be used to change the position of the cannon after each position. Movement will be restricted to the x-plane and there are limits to the ends it can go to, so as to prevent it from going off-screen.
        
        self.__base_x = newPosition[0] # "newPosition" is supposed to hold the characteristics of the last cannonball that gets destroyed in a turn. We move the base of the cannon according to this cannonball's center's x-coordinate.
        
        if self.__base_x > 450:
            
            self.__base_x = 450
            
        elif self.__base_x < 50:
            
            self.__base_x = 50
        
    def rotation(self): # This is used to display the rotating cannon and its still base.
        
        angle = self.__angleCalculator() # Depending on where the player has the mouse at, the "plane" of the game will be rotated at a different angle.

        # The below lines are used to not only rotate the cannon but to also keep it on the screen.
        
        pushMatrix()
        translate(self.__base_x,self.__base_y - (self.__height / 300.0 * 64.0)) # To have the cannon pivot correctly, the end of the cannon is at a height of 364 relative to the original base_y.
        rotate(radians(90-angle))
        self.__specialCannonBarrelDisplay()
        popMatrix()
        
        self.__specialCannonBaseImage() # The cannon base is displayed after returning the game's "plane" to its normal state since its display should not change.
        
    def __angleCalculator(self): # This function will be used to calculate the angle at which the cannonball is to be launched as well as to orient the cannon's display. Importantly, we place bounds it so as to prevent a case where a "perpendicular" collision with the wall causes infinite bounces to occur.
        
        angle = math.degrees(math.atan2(abs(mouseY - (self.__base_y - (self.__height / 300.0 * 64.0))),(mouseX - self.__base_x))) # The angle is taken counterclockwise from the positive x-axis (where the center of the base is taken as the "origin").
        
        if angle < 30:
            
            angle = 30
            
        elif angle > 150:
            
            angle = 150
        
        return angle
    
    def requisiteForCannonBall(self): # This function will allow us to get the angle for the direction in which the cannonballs should move.
        
        angle = radians(self.__angleCalculator())
        
        return (angle, self.__base_x,self.__base_y - (self.__height / 300.0 * 64.0))
    
    def getCannonHeight(self): # This will allow us to get the height of the cannon for when we need to orient the direction of the cannonshot.
        
        return self.__height


class Demarcator: # This object is the line that marks the threshold below which a block should not reach. If a block comes underneath it, the game ends.
    
    def __init__(self):
        
        self.__height = 2 
        self.__color = "#25331F"
        self.__topCorner = (0, int(HEIGHT / 700.0 * 500.0 - self.__height / 2.0))
        self.__bottomCorner = (WIDTH, int(HEIGHT / 700.0 * 500.0 + self.__height / 2.0))
    
    def getBottomEnd(self):
        
        return self.__bottomCorner[1]
    
    def display(self):
        
        fill(self.__color)
        rectMode(CORNERS)
        rect(self.__topCorner[0], self.__topCorner[1], self.__bottomCorner[0], self.__bottomCorner[1])
      
          
class Score: # We treat the score as an object with specific attributes and methods, so as to modify game behaviour as the player progresses.
    
    def __init__(self): # This initial score is 0.
        
        self.__scoreAmount = 0
        
    def change(self, changeAmount): # The score will be later incremented according to the durability of the destroyed blocks.
        
        self.__scoreAmount += changeAmount
        
    def display(self): # The score will be displayed in a box near the bottom-right corner of the screen.
    
        rectMode(CORNER) 
        fill(87,65,47)
        rect(WIDTH * 60.0 / 80.0, HEIGHT * 151.0 / 160.0, 100.0, 30.0)
        
        fill(255)
        textSize(12)
        
        score_string = "SCORE:   " + str(self.__scoreAmount * 10) # We multiply the internally stored score by 10, so as to show bigger numbers on screen. This, in theory, should be more motivating for the player.
        
        text(score_string, WIDTH * 498.0 / 640.0, HEIGHT * 623.0 / 640.0)
        
    def getScore(self): # We will need to call the private attribute in various other objects' methods.
        
        return self.__scoreAmount


class CannonBall: # Each cannonball will be treated as an instance of this class with its own attributes.
        
    def __init__(self, userCannon, cannonBallCount):
        
        self.__separationDistance = 10.0 # This represents the distance between each of the cannonballs.
        
        self.__radius = 10.0 # This is the radius we will be using for collisions and motion in the game.
        self.__displayRadius = 8.0 # This will be utilized for the display. Processing "teleports" the cannonballs and so, we have added "padding" around the blocks, whereby collisions will occur without direct contact (but when the cannonball is close to the block). Appearance-wise, the game looks like it should and the player is none the wiser.
        
        self.__vectorDirection, self.__baseX, self.__baseY = userCannon.requisiteForCannonBall() # We need the angle in which the cannonballs should move. This depends on the positioning of the cannon.
        self.__cannonHeight = userCannon.getCannonHeight() # This will be utilized for the initial position of the cannonballs.
        self.__xCenter = float(self.__baseX) + float(self.__cannonHeight) * math.cos(self.__vectorDirection) - 2.0 * (float(self.__radius) + self.__separationDistance) * cannonBallCount * cos(self.__vectorDirection) # The first cannonball will be placed at the "head" of the cannon and the others will be "behind" it in a line.
        self.__yCenter = float(self.__baseY) - float(self.__cannonHeight) * math.sin(self.__vectorDirection) + 2.0 * (float(self.__radius) + self.__separationDistance)* cannonBallCount * sin(self.__vectorDirection) # The first cannonball will be placed at the "head" of the cannon and the others will be "behind" it in a line.
        
        self.__velocity = 4 # This is the total velocity, which should have two components (vertical and horizontal).
        self.__xVelocity = self.__velocity * math.cos(self.__vectorDirection) # This is the x-component of the velocity, which we will change in the case of horizontal collisions.
        self.__yVelocity = -self.__velocity * math.sin(self.__vectorDirection) # This is the y-component of the velocity, which we will change in the case of horizontal collisions.
        
        self.__isDead = False # We will delete the cannonball when this attribute turns true.
        self.__isAmmoCollision = False # We will increment the number of cannonballs when this attribute turns true.
        
    def isBallDead(self): # This is used to get the private attribute outside the class.
        
        return self.__isDead
        
    def checkCollisions(self, blockList, score): # This checks if a collision occurs and decrements block's durability accordingly. If the durability of the block becomes zero, the block is destroyed from the block_list and the score is added to the player's score.
        
        blockTempList = blockList[:] # We create this copy of the list, so as iterate through it while causing changes in the original list of blocks.
        
        for index, block in enumerate(blockTempList): # This allows us to save the index and item of each iteration.
            
            leftX, topY, rightX, bottomY = block.corners() # These are the four coordinates of the four corners of the respective block.
            
            closestPoint = [0, 0] # We create a list of two elements, so as to later save the x-coordinate and y-coordinate of the block that is closest to the cannonball this method has been called for.
            horizontal, vertical, corner = False, False, False # The cannonball can either collides with the block's vertical sides or the block's horizontal sides or the block's corners.
            
            if leftX - 20 <= self.__xCenter <= rightX + 20 and topY - 20 <= self.__yCenter <= bottomY + 20: # The below four checks will be only performed only if it is actually possible to collide with the horizontal or vertical walls of the block. The "corners" case will be handled separately.
            
                if self.__yCenter - self.__radius >= bottomY and leftX - math.floor(self.__velocity / self.__radius + 1) * self.__radius <= self.__xCenter <= rightX + math.floor(self.__velocity / self.__radius + 1) * self.__radius: # The is used to check for a collision with the bottom side of the block. 
                    
                    if self.__yCenter - self.__radius + self.__yVelocity <= bottomY:
                        
                        self.__xCenter += 2.0 * self.__xVelocity
                        
                    vertical = True
                    closestPoint = [self.__xCenter, bottomY]
                    
                elif self.__yCenter + self.__radius <= topY and leftX - math.floor(self.__velocity / self.__radius + 1) * self.__radius <= self.__xCenter <= rightX + math.floor(self.__velocity / self.__radius + 1) * self.__radius: # This is used to check for a collision with the top side of the block. 
                    
                    if self.__yCenter + self.__radius + self.__yVelocity >= topY:
                        
                        self.__xCenter += 2.0 * self.__xVelocity
                        
                    vertical = True
                    closestPoint = [self.__xCenter, topY]
                    
                if self.__xCenter - self.__radius >= rightX and topY - self.__radius <= self.__yCenter <= bottomY + self.__radius: # This is used to check for a collision with the right side of the block. 
                    
                    if self.__xCenter - self.__radius + self.__xVelocity <= rightX:
                        
                        self.__yCenter -= 2.0 * self.__yVelocity
                        
                    horizontal = True
                    closestPoint = [rightX, self.__yCenter]
                    
                elif self.__xCenter + self.__radius <= leftX and topY  - self.__radius <= self.__yCenter <= bottomY + self.__radius: # This is used to check for a collision with the left side of the block.
                    
                    if self.__xCenter + self.__radius + self.__xVelocity >= leftX:
                        
                        self.__yCenter -= 2.0 * self.__yVelocity
                        
                    horizontal = True
                    closestPoint = [leftX, self.__yCenter]
                    
            elif self.__xCenter <= leftX and self.__yCenter >= bottomY and self.__xCenter + self.__xVelocity >= leftX and self.__yCenter + self.__yVelocity <= bottomY: # This is used to check for a collision with the bottom-left corner of the block. 
                
                corner = True
            
            elif self.__xCenter >= rightX and self.__yCenter >= bottomY and self.__xCenter + self.__xVelocity <= rightX and self.__yCenter + self.__yVelocity <= bottomY: # This is used to check for a collision with the bottom-right corner of the block. 
            
                corner = True
                        
            elif self.__xCenter >= rightX and self.__yCenter <= topY and self.__xCenter + self.__xVelocity <= rightX and self.__yCenter + self.__yVelocity >= topY:  # This is used to check for a collision with the top-right corner of the block. 
                
                corner = True
                            
            elif self.__xCenter <= leftX and self.__yCenter <= topY and self.__xCenter + self.__xVelocity >= leftX and self.__yCenter + self.__yVelocity >= topY:  # This is used to check for a collision with the top-left corner of the block. 
                
                corner = True
                            
            if math.sqrt((self.__xCenter + self.__xVelocity - closestPoint[0]) ** 2 + (self.__yCenter + self.__yVelocity - closestPoint[1]) ** 2) <= self.__radius + 1 or corner: # If a collision occurs, this will decrement the block's durability and destroy it if need be.
                
                if isinstance(block, BrickBlock): # This block of code will be entered in case the block is not one of the side walls, but one that changes the score or increments ammo.
                    
                    block.decrementDurability() # The block's durability goes down with each collision.
                    
                    if block.isBlockDead(): # If the block is destroyed, this code will be executed, playing the "explosion" sound.
                        
                        self.__brickExplosion = player.loadFile(PATH + "/Resources/Sounds/brickExplosion.mp3")
                        self.__brickExplosion.rewind()
                        self.__brickExplosion.setGain(-20)
                        self.__brickExplosion.play()
                        
                        if isinstance(block, AmmoBlock): # This indicates to the game that it should increase the ammo of the player for the next turn.
                            
                            self.__isAmmoCollision = True
                            
                        else: # This indicates to the game that the score should be increased according to the original durability of the destroyed block.
                            
                            score.change(block.getOriginalDurability())
                            
                        self.__isDead = True # This status will be called later on through the "self.isBallDead" function.
                        del blockList[index] # The block is deleted from the original list of blocks.
                        
                    else: # This block of code is entered if the block was not destroyed, playing the below sound.
                        
                        self.__collisionSound = player.loadFile(PATH + "/Resources/Sounds/alternateBallCollision.mp3")
                        self.__collisionSound.rewind()
                        self.__collisionSound.setGain(-10)
                        self.__collisionSound.play()

                if horizontal or corner: # This produces a change in the x-component of the velocity.
                    
                    self.__xVelocity *= -1.0
                    
                if vertical or corner: # This produces a change in the y-component of the velocity.
                    
                    self.__yVelocity *= -1.0
                    
                break
                    
    def getCenterPosition(self): # This function will be called to move the cannon later on based on the location of the last destroyed cannonball.
        
            return self.__xCenter, self.__yCenter

    def isAmmoCollision(self): # This allows the game to check whether it has to increment the number of cannonballs.
        
        return self.__isAmmoCollision
    
    def updatePosition(self): # This will be used to move the cannonball across the screen.
        
        self.__xCenter += self.__xVelocity
        self.__yCenter += self.__yVelocity
        
    def lowerBoundaryCollision(self): # This will check if the cannonball has to be deleted after going out of play.
              
        return self.__yCenter - self.__radius > HEIGHT and self.__yVelocity >= 0 # The y-velocity has to be non-positive since at the beginning of the turn, the balls move from the bottom "into" the screen. We only delete them when they're coming from above the bottom of the screen.
        
    def display(self): # Each cannonball is displayed as a circle.
        
        circle(int(self.__xCenter), int(self.__yCenter), self.__displayRadius * 2)
      
          
class CannonShot(list): # This refers to the actual cannonshot, whereby different cannonballs are shot. The cannonballs move together initially, but are likely to diverge in different directions as collisions occur.
    
    def __init__(self, userCannon, cannonShootQuantity): # According to the initial number of cannonballs (e.g. 1), we will add them to the list (CannonShot).
        
        for ballCount in range(cannonShootQuantity):
            
            self.append(CannonBall(userCannon, ballCount))
            
        self.__increment = False # If this attribute turns true, the number of cannonballs will increase.
    
    def updateAndDisplay(self, blockList, cannon, score): # This will be used to move the cannonballs across the screen, updating the movement as collisions occur.
                
        index = -1 # This is the initial index. We will change it in the below "for" loop when we will be checking for collisions and deleting cannonballs in case they destroy a block or go out of play.
        
        for cBall in self: # We will iterate through each cannonball in the list.
            
            cBall.checkCollisions(blockList, score) # The game will check collisions for the next position that the cannonball will go to before causing a change in it. The velocity will change inside this function if a collision occurs.
            cBall.updatePosition() # This updates the position of the cannonball.
            
            index += 1 # This will allow us to check the cannonballs one-by-one, deleting the one that collides from the list (based on its index).
            
            if cBall.lowerBoundaryCollision() or cBall.isBallDead(): # This "if" block is entered if the ball goes out of play (goes out of the screen) or is destroyed due to a collision.
                
                if len(self) == 1: # Depending on the location of the last ball, the cannon will change its location on the screen.
                    
                    cannon.changePosition(self[index].getCenterPosition())
                    
                if cBall.isAmmoCollision(): # This will allow us to increase the number of cannonballs over the course of the game.
                    
                    self.setIncrementStatus(True)
                    
                del self[index] # This deletes the cannonball.
                
                index -= 1 # In case a cannonball is deleted, the list will become shorter and this will prevent us from having an invalid index (in the part where we delete cannonballs).
                
            cBall.display() # We will display each cannonball.    
    
    def getIncrementStatus(self): # This is used to get the private attribute, so as to allow the "Game" object to know whether it should increase the number of cannonballs (i.e. whether there has been a collision with an "Ammo Block").
        
        return self.__increment
    
    def setIncrementStatus(self, status): # This will be used to change the private attribute according to changes happening in the "Game" class.
        
        self.__increment = status    
    
    
class Block: # These are the blocks that appear on the screen. They also form the walls at the top, left and right of the screen.
    
    def __init__(self, leftX, topY, bW, bH): # These attributes represent the coordinates of the top-left corner of the block as well as its width and height.
        
        self.__originPoint = [leftX, topY] # These are the coordinates of the top-left corner of the block.
        self.__terminalPoint = [leftX + bW, topY + bH] # These are the coordinates of the bottom-right corner of the block.
    
    def getOriginPoint(self): # This returns the private attribute of the "Block" class.
        
        return self.__originPoint
    
    def getTerminalPoint(self): # This returns the private attribute of the "Block" class.
        
        return self.__terminalPoint
    
    def corners(self): # This function will allow us to get the position of the four corners/sides of the block.
        
        return self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1]
    
    def display(self): # This will be used to display the block.
        
        rectMode(CORNERS)
        stroke(0,0,0)
        fill(0)
        rect(self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1])
    
    def moveDownwards(self): # This will be used to move the blocks after each turn. Since the blocks are essentially shown in the form of a grid, their motion will be uniform and they will be moving "one row downwards".
        
        shiftHeight = self.__terminalPoint[1] - self.__originPoint[1] # This is the height of each block and also the distance it will have to move vertically.
        
        self.__originPoint[1] += shiftHeight
        self.__terminalPoint[1] += shiftHeight
        
    def demarcationCollision(self, demarcationLine): # This checks the bottom side of each block with the boundary line shown on screen. If even one block is below the boundary line, the game ends.
        
        return demarcationLine.getBottomEnd() <= self.__terminalPoint[1]
      
      
class BrickBlock(Block): # These are the blocks that are seen on screen. The player has to destory them. Attributes will be inherited from the "Block" superclass.
    
    def __init__(self, leftX, topY, bW, bH, durability): # These arguments, in addition to the arguments for the "Block" class, include the durability of the block.
        
        Block.__init__(self, leftX, topY, bW, bH) # We do inheritance.
        
        self.__durability = durability # This will be the changing durability of the block used to keep track of the block's "life".
        self.__originalDurability = durability # This durability will be used to increment the player's score and change the game state.
        
        self.__backgroundImage = loadImage(PATH + "/Resources/Block/latestBrickAltered.jpg") # This represents the appearance of the block.
        
        self.__diameter = 30 # This is the diameter of the circle used to display the durability.
        
    def getOriginalDurability(self): # This allows us to get the value of the private attribute.
        
        return self.__originalDurability
        
    def decrementDurability(self): # The block's durability will go down in the case of a collision.
        
        self.__durability -= 1
        
    def isBlockDead(self): # The block is to be destroyed if its durability becomes zero.
        
        return self.__durability == 0
    
    def getCircleDiameter(self): # This allows us to access the private attribute.
        
        return self.__diameter
    
    def display(self): # This will be used to display the brick and a circle upon which the durability is written. We also have a black rectangle in the background for aesthetic reasons since we have a "transparent" image for the brick.
        
        originPoint = self.getOriginPoint() # This represents the top-left corner of the block.
        terminalPoint = self.getTerminalPoint() # This represents the bottom-right corner of the block.
        
        rectMode(CORNERS)
        stroke(255)
        fill(0)
        rect(originPoint[0], originPoint[1], terminalPoint[0], terminalPoint[1])
        
        imageMode(CORNERS)
        image(self.__backgroundImage, originPoint[0], originPoint[1], terminalPoint[0], terminalPoint[1])
        imageMode(CORNER)
        
        fill(0)
        circle((originPoint[0] + terminalPoint[0]) / 2.0, (terminalPoint[1] + originPoint[1]) / 2.0, self.__diameter)
        
        fill(255)
        textSize(18)
        
        message = str(self.__durability)
        
        if len(message) == 1: # This will allow us to uniformly display durabilities with one or two digits. The game is unlikely to reach a stage where three digits will be necessary.
            
            message = "0" + message
            
        textMode(LEFT)    
        text(message, (originPoint[0] + terminalPoint[0]) / 2.0 - self.__diameter / 2.0 / math.sqrt(2), (originPoint[1] + terminalPoint[1]) / 2.0 + self.__diameter / 4.0)       
          
              
class AmmoBlock(BrickBlock): # This will inherit the BrickBlock class, being a special case with a durability of "1". Destroying this will cause the player to gain more ammo.
    
    def __init__(self, leftX, topY, bW, bH): # These object is initialized with the coorinates of the top-left corner, the width and the height.
        
        BrickBlock.__init__(self, leftX, topY, bW, bH, 1) # This allows inheritance. The durability is always one.
        
        self.__backgroundImage = loadImage(PATH + "/Resources/Block/latestBrickAltered.jpg") # The background image is the same as any other brick.
        self.__foregroundImage = loadImage(PATH + "/Resources/CannonBall/Cannonball.png") # Instead of displaying the durability, we will be showing a cannonball at the center of the block.
        
    def display(self): # This will be used to display the brick as well as the cannonball (which indicates that destruction of this block will cause an increase in ammo for the player).
        
        originPoint = self.getOriginPoint()
        terminalPoint = self.getTerminalPoint()
        
        rectMode(CORNERS)
        stroke(255)
        fill(0)
        rect(originPoint[0], originPoint[1], terminalPoint[0], terminalPoint[1])
        
        imageMode(CORNERS)
        image(self.__backgroundImage, originPoint[0], originPoint[1], terminalPoint[0], terminalPoint[1])
        imageMode(CORNER)
        
        image(self.__foregroundImage, (originPoint[0] + terminalPoint[0]) / 2 - self.getCircleDiameter() / 2, (originPoint[1] + terminalPoint[1]) / 2 - self.getCircleDiameter() / 2, self.getCircleDiameter(), self.getCircleDiameter())


class BlockList(list): # This stores all the types of blocks.
    
    def __init__(self):
        
        self.append(Block(-100, 0, 101, HEIGHT - WIDTH / 10.0 * 3 / 300.0 * 115)) # This represents the left boundary of the screen.
        self.append(Block(WIDTH - 1, 0, 100, HEIGHT - WIDTH / 10.0 * 3 / 300.0 * 115)) # This represents the right boundary of the screen.
        self.append(Block(0, -100, WIDTH, 101)) # This represents the bottom boundary of the screen.
        
        # Below, we add three blocks of our choosing as part of the initial game state.
        
        self.append(BrickBlock(1 * 100, 2 * 50, 100, 50, 1))
        self.append(BrickBlock(3 * 100, 4 * 50, 100, 50, 1))
        self.append(BrickBlock(4 * 100, 8 * 50, 100, 50, 1))
                                                        
        self.__demarcationLineCollided = False # The game continues as long as this is "False".

    def display(self): # We iterate through the list to display each block.
        
        for block in self:
            
            block.display()
            
    def moveAllDownwardsAndFlagGameEnd(self, demarcationLine): # This will be used to move the blocks down after each turn and to check if the game should end.
        
        for block in self[3:]: # We won't be moving the first three elements since they are the boundary walls.
            
            block.moveDownwards()
            
            if block.demarcationCollision(demarcationLine): # After the blocks are moved, the game checks if the game should end.
                
                self.__demarcationLineCollided = True
            
    def demarcationLineCollision(self): # This allows us to access the private attribute.
        
        return self.__demarcationLineCollided        
            
    def createNewRow(self, playerScore, shotQuantity): # This will allow us to add more blocks at the top of the screen as the game proceeds.
        
        score = playerScore.getScore() # The game has to adapt according to the score.
        
        newBlockQuantity = 1 # At the beginning of the game, only one block will be added after each turn.
        availableColPositions = [0, 1, 2, 3, 4] # We are treating the screen as five columns in which blocks can move.
        
        # The number of blocks added after each turn depends on the score, with the game becoming proceedingly harder.
                                
        if score <= 25:
            
            newBlockQuantity = 2
                                
        elif score <= 150:
            
            newBlockQuantity = 3
                
        elif score <= 275:
            
            newBlockQuantity = 4
            
        else:
            
            newBlockQuantity = 5
        
        for newBlock in range(newBlockQuantity): # Depending on the number of blocks to be added, we will append alements to the list of blocks.
            
            newColPosition = availableColPositions.pop(random.randint(0, (len(availableColPositions) - 1))) # This allows us to avoid repeating a position for two or more blocks.
            
            ammoBlockChance = random.randint(1, 10) # This allows us to randomly determine whether there should or should not be an "Ammo Block".
            
            if ammoBlockChance == 1 or ammoBlockChance == 2 or ammoBlockChance == 3: # The probability of getting an "Ammo Block" is 3/10.
                
                self.append(AmmoBlock(100 * newColPosition, 0, 100, 50)) # This appends an "Ammo Block" to the list of blocks.
                                                        
            else: # If not an "Ammo Block", a brick block of random durability is added to the screen.
                
                self.append(BrickBlock(100 * newColPosition, 0, 100, 50, shotQuantity + random.randint(1, newBlockQuantity))) # Depending on the amount of ammo the player has, the game will add blocks of increasing durability (which will be somewhat random).                                           
            
            
class Background: # This represents the background display.
    
    def __init__(self): # We initialize the object with the image we will be using.
        
        self.__backgroundImage = loadImage(PATH + "/Resources/Background/alteredConcrete.jpg")

    def display(self): # This will be used to display the background.
        
        image(self.__backgroundImage, 0, 0, WIDTH, HEIGHT, 0, frameCount % 700, WIDTH, (frameCount % 700) + 700) # The game will have a scrolling background.
            
            
class CannonWall: # This will be a rectangular image at the bottom of the screen. It will help hide the cannonballs coming from below at the start of each turn and will also provide great aesthetic appeal.
    
    def __init__(self, x1, y1, x2, y2): # We have the corner coordinates for where the image is to be displayed.
        
        self.__originPoint = [x1, y1]
        self.__terminalPoint = [x2, y2]
        
        self.__backgroundImage = loadImage(PATH + "/Resources/Background/tiledNight.png") # This is the image that will be used.

    def display(self): # This will be used to display the object.
        
        imageMode(CORNERS)
        image(self.__backgroundImage, self.__originPoint[0], self.__originPoint[1], self.__terminalPoint[0], self.__terminalPoint[1], 0,  (frameCount % 180), WIDTH, (frameCount % 180) + 100) # The image will be a "scrolling" image.
        imageMode(CORNER)


class Game: # This combines all the different elements of the game together.
    
    def __init__(self):
        
        self.__playerCannonShotQuantity = 1 # The original number of cannonballs is 1.
        
        self.__playerCannon = Cannon(x, y, WIDTH  / 10.0, WIDTH / 10.0 * 3) # The cannon is initally placed at the bottom-center of the screen.
        self.__playerShot = CannonShot(self.__playerCannon, 0) # The object "CannonShot" initially starts with zero cannonballs until the first move is taken by the player.
        self.__gameEndLine = Demarcator() # This is the line below which no block should come.
        self.__blockList = BlockList() # This is the list of blocks through which we will iterate.
        self.__playerScore = Score() # This is the score used for adaptive game behavior.
        self.__background = Background() # This represents the background display of the screen.
        self.__cannonWall = CannonWall(0, HEIGHT - WIDTH / 10.0 * 3 / 300.0 * 115, WIDTH, HEIGHT) # This will allow us to show a wall behind the cannon.
        
        # We are using background music from the original game and it will keep on looping until the game ends. It will play both when the title screen is being shown and the game is being played, but not when the player loses.

        self.__background_sound = player.loadFile(PATH + "/Resources/Sounds/backgroundMusic.mp3")
        self.__background_sound.rewind()
        self.__background_sound.setGain(-40)
        self.__background_sound.loop()
        
        self.__turnInPlay = False # This will be used to check whether a move is going on, so as to halt the changes produced by mouse-clicks when needed.
        self.__gameContinue = True # This will be used to check whether the game should continue or end.
        
    def __updateAndDisplayCannon(self): # This will be used for the rotation of the cannon when the player is aiming.
        
        self.__playerCannon.rotation()
    
    def shootCannon(self): # This is used to fire the cannonballs.
        
        self.__playerShot = CannonShot(self.__playerCannon, self.__playerCannonShotQuantity) # The cannon's shot will depend on the amount of ammo.
        
        # We will get the below sound when the player fires a shot.
        
        if self.__gameContinue: # We add this check to prevent the sound of cannonfire when the player resets the game.
        
            self.__cannonLaunch = player.loadFile(PATH + "/Resources/Sounds/cannonAlternateExplosion.mp3")
            self.__cannonLaunch.rewind()
            self.__cannonLaunch.setGain(-30)
            self.__cannonLaunch.play()
        
        self.__turnInPlay = True # This will allow the player to make a new move.
    
    def ammoDisplay(self): # The ammo will be displayed in a box near the bottom-left corner of the screen.
    
        rectMode(CORNER) 
        fill(87,65,47)
        rect(WIDTH * 4.0 / 80.0, HEIGHT * 151.0 / 160.0, 100.0, 30.0)
        
        fill(255)
        textSize(12)
        
        score_string = "Ammo:   " + str(self.__playerCannonShotQuantity)
        
        text(score_string, WIDTH * 58.0 / 640.0, HEIGHT * 623.0 / 640.0)
    
    def updateAndDisplay(self): # This is used to update the game's state and to display the game's various elements.
        
        self.__background.display()
        self.__gameEndLine.display()
        self.__playerShot.updateAndDisplay(self.__blockList, self.__playerCannon, self.__playerScore)
        self.__cannonWall.display()
        self.__updateAndDisplayCannon()
        self.__blockList.display()
        self.__playerScore.display()
        self.ammoDisplay()
        
        if len(self.__playerShot) == 0: # Whenever all the cannonballs have gone out of play, the game will update the game state before the next turn.
            
            if self.__turnInPlay: # If the player is allowed to take a new turn, this block of code will be executed.
                
                self.__blockList.moveAllDownwardsAndFlagGameEnd(self.__gameEndLine) # The game updates the blocks already on screen, moving them downwards.
                self.__blockList.createNewRow(self.__playerScore, self.__playerCannonShotQuantity) # The game adds new blocks at the top of the screen.
                self.__gameContinue = not(self.__blockList.demarcationLineCollision()) # The game checks whether any block is below the demarcation line.
                
            self.__turnInPlay = False # This allows the player to take anothe shot.
            
        if self.__playerShot.getIncrementStatus(): # If the player hit an "Ammo Block", we will increase the number of cannonballs.
            
            self.__incrementCannonShot()
            self.__playerShot.setIncrementStatus(False)
            
    def __incrementCannonShot(self): # This is used to increase the number of cannonballs.
        
        self.__playerCannonShotQuantity += 1
        
    def inputStatus(self): # This will tell the game whether it should accept an input or not.
        
        return not (self.__turnInPlay)

    def getGameContinueStatus(self): # This will tell the game whether it should continue or end.
        
        return self.__gameContinue
    
    def gameOverDisplay(self): # This method will be executed when the game ends, displaying the score.

        self.__background_sound.close() # The music ends when the player loses.

        background(139,0,0)
        
        noStroke()
        
        fill(0)
        rect(0, HEIGHT * 5 / 14, WIDTH, 240) 
             
        fill(255, 255, 255)
        textSize(44)
                
        gameOverString = "GAME OVER\n SCORE: " + str(self.__playerScore.getScore() * 10)
        
        text(gameOverString, WIDTH / 4, HEIGHT * 30 / 64)
        self.__background_sound.close()
        
        fill(255)
        rect(0, HEIGHT * 34 / 56, WIDTH, 35) 
             
        fill(0)
        textSize(20)
                
        length_string = "CLICK HERE TO RESTART GAME"
        
        text(length_string, WIDTH * 13 / 64, HEIGHT * 290 / 450)
    
def setup(): # We initialize the conditions of the display.
    
    size(WIDTH, HEIGHT)
    frameRate(60)
    background(255)
    
    
x, y = WIDTH / 2, HEIGHT # This will be used to place the cannon at the bottom-center of the screen


brickBlast = Game() # This creates an instance of the "Game" class, wihch in turn has all the other elements.


gameAllowed = False # The game will not be played until the player chooses to start playing.


titleScreen =  loadImage(PATH + "/Resources/TitleScreen/startScreen1.png") # We have two "Start Screens", of which one is used at the beginning.


def draw(): # This function is called sixty times a second.
    
    if not gameAllowed: # The title screen is displayed until the player chooses to start playing.

        image(titleScreen, 0, 0, WIDTH, HEIGHT, 0,  0, 500, 700)
            
    elif brickBlast.getGameContinueStatus(): # The game keeps on going until the player loses.
        
        background(255) # We create a white background after each frame-update, so as to prevent old "displays" from showing.
        brickBlast.updateAndDisplay()
        
    else: # If the player loses, the "Game Over" screen is shown.
        
        background(255) # We create a white background after each frame-update, so as to prevent old "displays" from showing.
        brickBlast.gameOverDisplay()
    
def mouseClicked() :# The player fires cannonballs by clicking the mouse's button.
        
    global brickBlast, gameAllowed, titleScreen # This allows us to reset the game.
        
    if (not gameAllowed) and  (WIDTH / 500 * 210 <= mouseX <= WIDTH / 500 * (210  + 100)) and (HEIGHT / 700 * 510 <= mouseY <= HEIGHT / 700 * (510 + 200)): # The player has to click the "Cannon" "button" to start the game.
    
        gameAllowed = True # The player can now play the game.

    elif gameAllowed and brickBlast.inputStatus() == True: # This condition helps prevent more than one click per turn.
        
        brickBlast.shootCannon() # Cannonballs are fired and the turn takes place.
        
    elif not brickBlast.getGameContinueStatus() and HEIGHT * 34 / 56 <= mouseY <= HEIGHT * 34 / 56 + 35: # If the player clicks the mouse at the indicated location after losing, the game restarts. Since the player might wish to see the instructions again, we purposedly chose to show the title screen again. If we wanted to not show it, we just need to remove the line saying "gameAllowed = False" in the below block of code,
        
        brickBlast = Game() # We create a fresh instance of the "Game" class.
        gameAllowed = False # This allows us to see the instructions again.
        titleScreen =  loadImage(PATH + "/Resources/TitleScreen/startScreen" + str(random.randint(1,2)) + ".png") # We randomize the background display as an added bonus for players who try to play the game multiple times and see the screen more than once. This will help maintain interest.
