import pygame
import random
import math
import Constants

class Enemy(pygame.sprite.Sprite):
    """ This class represents the enemy.
    The enemy can attack and move around the world. """

    def __init__(self, x, y, size=1, color="green"):
        """ Constructs the enemy object and Initializes variables. """

        # This calls the superconstructor
        super().__init__()

        # Instantiate a constant to increase size.
        self.size = size

        # This sets the image to be the Snake surface defined above.
        self.image = pygame.Surface(
            [13 * Constants.WINDOW_MAGNIFICATION * self.size,
             20 * Constants.WINDOW_MAGNIFICATION * self.size])
        self.rect = self.image.get_rect()
        self.image = Snake_Forward_1
        self.image.set_colorkey(Constants.COLORKEY)

        # Initialize the many variables used in making enemies
        # Initialize location
        self.x = x
        self.y = y

        # Initialize direction enemy is facing
        self.direction = "DOWN"

        # Initialize how many pixels an enemy walks at a time.
        self.walkRate = 10

        # Initialize how close the player must
        # be before the enemy starts to chase.
        self.aggroRange = 100

        # Initialize variables used to calculate distance from player.
        self.distancePlayerx = 0
        self.distancePlayery = 0
        self.distancePlayerTheta = 0
        self.distancePlayer = 0

        # Initialize variables used to calculate and update time
        self.elapsed = 0
        self.dt = 0
        self.clock = pygame.time.Clock()

        # Initialize the coordinates of the x and ys
        self.playerx2 = 0
        self.playery2 = 0
        self.playerx1 = 0
        self.playery1 = 0

        # Initialize what direction the enemy
        # is from the player's point of view.
        self.sector = "UP LEFT"

        # Initialize health, defense and attack
        self.health = 100
        self.defense = 1
        self.attackDamage = 5
        self.spellDefense = 1

        # Instantiate a constant to change color of enemies
        if(color == "green"):
            self.color = "green"
        else:
            self.color = "red"
            self.attackDamage = 10
            self.defense = 2

    def update(self, player):
        """ Updates the Enemy's variables """

        # Calculate the distance from the player.
        self.distancePlayerx = self.rect.x - player.rect.x
        self.distancePlayery = self.rect.y - player.rect.y
        self.distancePlayer = math.hypot(
            self.distancePlayerx, self.distancePlayery)

        # Move every few seconds
        self.dt = self.clock.tick()
        self.elapsed += self.dt
        if(self.elapsed > 200):
            self.distancePlayerx = self.rect.x - player.rect.x
            self.distancePlayery = self.rect.y - player.rect.y
            self.distancePlayer = math.hypot(
                self.distancePlayerx, self.distancePlayery)

            # If the enemy is within aggroRange we chase after them,
            # otherwise, the enemy wanders randomly.
            if(self.distancePlayer > self.aggroRange):
                self.wander()
            else:
                self.attack()

        # Update where to set the image.
        self.rect.x = self.x
        self.rect.y = self.y

        # Update the coordinates for the player's sprites
        self.playerx1 = player.x
        self.playery1 = player.y
        self.playerx2 = player.x + (16 * Constants.WINDOW_MAGNIFICATION * self.size)
        self.playery2 = player.y + (21 * Constants.WINDOW_MAGNIFICATION * self.size)

    def draw(self, screen):
        """ Draw the sprites in their new positions """
        Enemy = pygame.transform.scale(
            self.image, (25 * Constants.WINDOW_MAGNIFICATION * self.size,
                         25 * Constants.WINDOW_MAGNIFICATION * self.size))
        screen.blit(Enemy, [self.x, self.y])

    def wander(self):
        """ Moves  the enemy object. """

        # Randomly assign a direction to move the enemy in
        chance = random.random()
        if(chance < 0.25):
            self.direction = "DOWN"
        elif(chance < 0.50):
            self.direction = "UP"
        elif(chance < 0.75):
            self.direction = "LEFT"
        elif(chance < 1.0):
            self.direction = "RIGHT"

        # Change the sprite image and move the sprite in a direction
        if self.direction == "DOWN":
            self.image = Snake_Forward_1
            if(self.color == "red"):
                self.image = Snake_Red_Front
            self.y += self.walkRate
        elif self.direction == "UP":
            self.image = Snake_Back_1
            if(self.color == "red"):
                self.image = Snake_Red_Back
            self.y -= self.walkRate
        elif self.direction == "RIGHT":
            self.image = Snake_Right_1
            if(self.color == "red"):
                self.image = Snake_Red_Right
            self.x += self.walkRate
        elif self.direction == "LEFT":
            self.image = Snake_Left_1
            if(self.color == "red"):
                self.image = Snake_Red_Left
            self.x -= self.walkRate

        # Rescale and set the background to be translucent
        if(self.direction == "LEFT" or self.direction == "RIGHT"):
            self.image = pygame.transform.scale(
                self.image, (23 * Constants.WINDOW_MAGNIFICATION * self.size,
                             19 * Constants.WINDOW_MAGNIFICATION * self.size))
        elif(self.direction == "UP"):
            self.image = pygame.transform.scale(
                self.image, (9 * Constants.WINDOW_MAGNIFICATION * self.size,
                             24 * Constants.WINDOW_MAGNIFICATION * self.size))
        else:
            self.image = pygame.transform.scale(
                self.image, (13 * Constants.WINDOW_MAGNIFICATION * self.size,
                             20 * Constants.WINDOW_MAGNIFICATION * self.size))
        self.image.set_colorkey(Constants.COLORKEY)

        # Reset the clock
        self.elapsed = 0

    def attack(self):
        """ Allows the enemy to attack. """

        # Change the sector, image,
        # and update the coordinates to reach the player.
        if(self.x < self.playerx2 and self.x > self.playerx1 and
           self.y > self.playery2):
            self.sector = "UP"
            self.y -= self.walkRate
            self.image = Snake_Back_1
            if(self.color == "red"):
                self.image = Snake_Red_Back
        elif(self.y < self.playery2 and self.y > self.playery1 and
             self.x < self.playerx1):
            self.sector = "RIGHT"
            self.x += self.walkRate
            self.image = Snake_Right_1
            if(self.color == "red"):
                self.image = Snake_Red_Right
        elif(self.y < self.playery2 and self.y > self.playery1 and
             self.x > self.playerx2):
            self.sector = "LEFT"
            self.x -= self.walkRate
            self.image = Snake_Left_1
            if(self.color == "red"):
                self.image = Snake_Red_Left
        elif((self.x > self.playerx1 and self.x < self.playerx2 and
              self.y < self.playery1)):
            self.sector = "DOWN"
            self.y += self.walkRate
            self.image = Snake_Forward_1
            if(self.color == "red"):
                self.image = Snake_Red_Front
        elif(self.x > self.playerx1 and self.y > self.playery2):
            self.sector = "UP LEFT"
            self.x -= self. walkRate
            self.y -= self.walkRate
            self.image = Snake_Back_1
            if(self.color == "red"):
                self.image = Snake_Red_Back
        elif(self.x > self.playerx1 and self.y < self.playery2):
            self.sector = "DOWN LEFT"
            self.x -= self.walkRate
            self.y += self.walkRate
            self.image = Snake_Forward_1
            if(self.color == "red"):
                self.image = Snake_Red_Front
        elif(self.x < self.playerx2 and self.y < self.playery2):
            self.sector = "DOWN RIGHT"
            self.x += self.walkRate
            self.y += self.walkRate
            self.image = Snake_Forward_1
            if(self.color == "red"):
                self.image = Snake_Red_Front
        elif(self.x < self.playerx2 and self.y > self.playery1):
            self.sector = "UP RIGHT"
            self.x += self.walkRate
            self.y -= self.walkRate
            self.image = Snake_Back_1
            if(self.color == "red"):
                self.image = Snake_Red_Back

        # Rescale and set the background to be translucent
        if(self.sector == "LEFT" or self.sector == "RIGHT"):
            self.image = pygame.transform.scale(
                self.image, (23 * Constants.WINDOW_MAGNIFICATION * self.size,
                             19 * Constants.WINDOW_MAGNIFICATION * self.size))
        elif(self.sector == "UP" or self.sector == "UP RIGHT" or
             self.sector == "UP LEFT"):
            self.image = pygame.transform.scale(
                self.image, (9 * Constants.WINDOW_MAGNIFICATION * self.size,
                             24 * Constants.WINDOW_MAGNIFICATION * self.size))
        else:
            self.image = pygame.transform.scale(
                self.image, (13 * Constants.WINDOW_MAGNIFICATION * self.size,
                             20 * Constants.WINDOW_MAGNIFICATION * self.size))
        self.image.set_colorkey(Constants.COLORKEY)

        # Reset the clock
        self.elapsed = 0
