import pygame
import random
import math
import Constants

class Patience(pygame.sprite.Sprite):
    """ This class represents the boss, Patience.
    The enemy can attack in 2 ways."""

    def __init__(self, x, y):
        """ Constructs the Patience object and Initializes variables. """

        # This calls the superconstructor
        super().__init__()

        # This sets the image to be the Patience surface defined above.
        # This is the main body for Patience
        self.image = pygame.Surface(
            [121 * (Constants.WINDOW_MAGNIFICATION + 1),
             84 * (Constants.WINDOW_MAGNIFICATION + 1)])
        self.rect = self.image.get_rect()
        self.image = Spider_Legless
        self.image.set_colorkey(Constants.Constants.COLORKEY)

        # Initialize the many variables used in making enemies
        # Initialize location
        self.x = x
        self.y = y

        # Initialize variables used to calculate and update time
        self.elapsed = 0
        self.dt = 0
        self.clock = pygame.time.Clock()

        # Initialize health, defense and attack
        self.health = 2000
        self.maxHealth = 2000
        self.defense = 7
        self.attackDamage = 30
        self.spellDefense = 25

        # Instantiate all variables related to Patience's left Arm
        self.leftArm = pygame.sprite.Sprite()
        self.leftArm.image = pygame.Surface(
            [88 * Constants.WINDOW_MAGNIFICATION, 44 * Constants.WINDOW_MAGNIFICATION])
        self.leftArm.image = LeftSpiderScythe
        self.leftArm.rect = self.leftArm.image.get_rect()
        self.leftArm.rect.center = self.leftArm.rect.bottomleft
        self.leftArm.image.set_colorkey(Constants.Constants.COLORKEY)
        self.leftArmx = self.x + 15
        self.leftArmy = self.y + 145
        self.leftArmRect = self.leftArm.rect
        self.leftArmRectx = 0
        self.leftArmRecty = 0

        # Instantiate all variables related to Patience's left Arm
        self.rightArm = pygame.sprite.Sprite()
        self.rightArm.image = pygame.Surface(
            [88 * Constants.WINDOW_MAGNIFICATION, 44 * Constants.WINDOW_MAGNIFICATION])
        self.rightArm.image = RightSpiderScythe
        self.rightArm.rect = self.rightArm.image.get_rect()
        self.rightArm.rect.center = self.rightArm.rect.bottomleft
        self.rightArm.image.set_colorkey(Constants.Constants.COLORKEY)
        self.rightArmx = self.x + 75
        self.rightArmy = self.y + 145
        self.rightArmRect = self.rightArm.rect
        self.rightArmRectx = 0
        self.rightArmRecty = 0

        # Instantiate variables used in rotating the arms
        self.rotateSpeed = 2
        self.rotateAngle = 0

        # Instantiate variables used for timers
        self.attackTimer = 0
        self.elapsed = 0

        # Instentiate variables used in collision detection
        self.leftRect = pygame.Rect(0, 0, 0, 0)
        self.rightRect = pygame.Rect(0, 0, 0, 0)

        # Instantiate a variable to keep track of what kind of attack is being
        # done
        self.attacking = "none"

    def update(self):
        """ Updates the bosses variables. """
        # Update where to set the image.
        self.rect.x = self.x
        self.rect.y = self.y

        # Update the time variables
        previousElapsed = self.elapsed
        self.elapsed = pygame.time.get_ticks()
        self.attackTimer += ((self.elapsed - previousElapsed)/100)

        # When the Arm is fully extend reverse the rotation
        if(self.attacking == "left" or self.attacking == "right" or
           self.attacking == "both"):
            self.rotateAngle += self.rotateSpeed
            if(self.rotateAngle > 90):
                self.rotateSpeed *= -1
            elif(self.rotateAngle < 0):
                self.rotateSpeed *= -1
        else:
            self.rotateAngle = 0

    def draw(self, screen):
        """ Draw the sprites in their new positions """
        # Attack every few seconds
        if(self.attackTimer > 30):
            self.attack()
            self.rotateAngle = 0

        # Draw the body of Patience's body onto the screen.
        patience = pygame.transform.scale(
                self.image, (
                    121 * (Constants.WINDOW_MAGNIFICATION + 1), 84 * (
                        Constants.WINDOW_MAGNIFICATION + 1)))
        screen.blit(patience, [self.x, self.y])

        # If the boss is attacking update the right Arm,
        # otherwise draw it in place
        if(self.attacking != "right"):
            rightArm = pygame.transform.scale(
                self.rightArm.image, (88 * (
                    Constants.WINDOW_MAGNIFICATION + 1), 44 * (
                        Constants.WINDOW_MAGNIFICATION + 1)))
            rightArm2, rectR = rot_center(
                rightArm, self.rightArm.image.get_rect(), 0)
            self.rightRect = pygame.Rect(
                rectR.x + 550, rectR.y + 275,
                (rectR.width // 2) - 50, rectR.height - 30)
            self.rightArmRectx = rectR.x + self.rightArmx + 95
            self.rightArmRecty = rectR.y + self.rightArmy + 50
            screen.blit(rightArm2, (
                rectR.x + self.rightArmx + 95, rectR.y + self.rightArmy + 50))
        else:
            rightArm = pygame.transform.scale(
                self.rightArm.image, (
                    88 * (Constants.WINDOW_MAGNIFICATION + 1), 44 * (
                        Constants.WINDOW_MAGNIFICATION + 1)))
            rightArm2, rectR = rot_center(
                rightArm, self.rightArm.image.get_rect(),
                0 - self.rotateAngle)
            moveLeft = self.rotateAngle * 1.2
            self.rightRect = pygame.Rect(
                rectR.x + 550 - moveLeft, rectR.y + 275,
                rectR.width // 2 - 50, rectR.height - 30)
            screen.blit(rightArm2, (rectR.x + self.rightArmx + 95,
                                    rectR.y + self.rightArmy + 50))
            if(self.rotateAngle < 0):
                self.attacking = ""

        # If the boss is attacking update the left Arm,
        # otherwise draw it in place
        if(self.attacking != "left"):
            leftArm = pygame.transform.scale(
                self.leftArm.image, (
                    88 * (Constants.WINDOW_MAGNIFICATION + 1), 44 * (
                        Constants.WINDOW_MAGNIFICATION + 1)))
            leftArm2, rectL = rot_center(
                leftArm, self.leftArm.image.get_rect(), 0)
            self.leftArmRect = rectL
            self.leftRect = pygame.Rect(
                rectL.x + 350, rectL.y + 275,
                (rectL.width // 2) - 50, rectL.height - 30)
            self.leftArmRectx = rectL.x + self.leftArmx + 95
            self.leftArmRecty = rectL.y + self.leftArmy + 50
            screen.blit(leftArm2, (rectL.x + self.leftArmx + 95,
                                   rectL.y + self.leftArmy + 50))
        else:
            leftArm = pygame.transform.scale(
                self.leftArm.image, (88 * (Constants.WINDOW_MAGNIFICATION + 1), 44 * (
                    Constants.WINDOW_MAGNIFICATION + 1)))
            leftArm2, rectL = rot_center(
                leftArm, self.leftArm.image.get_rect(), self.rotateAngle)
            moveRight = self.rotateAngle * 0.8
            self.leftRect = pygame.Rect(
                rectL.x + 350 + moveRight, rectL.y + 275,
                rectL.width // 2 - 50, rectL.height - 30)
            screen.blit(leftArm2, (
                rectL.x + self.leftArmx + 95, rectL.y + self.leftArmy + 50))
            if(self.rotateAngle < 0):
                self.attacking = ""

        # If the boss is attacking update the left Arm and the right Arm
        # otherwise draw it in place
        if(self.attacking == "both"):

            print("both")
            rightArm = pygame.transform.scale(
                self.rightArm.image, (
                    88 * (Constants.WINDOW_MAGNIFICATION + 1), 44 * (
                        Constants.WINDOW_MAGNIFICATION + 1)))
            rightArm2, rectR = rot_center(
                rightArm, self.rightArm.image.get_rect(),
                0 - self.rotateAngle)
            moveLeft = self.rotateAngle * 1.2
            self.rightRect = pygame.Rect(
                rectR.x + 550 - moveLeft, rectR.y + 275,
                rectR.width // 2 - 50, rectR.height - 30)
            screen.blit(rightArm2, (rectR.x + self.rightArmx + 95,
                                    rectR.y + self.rightArmy + 50))
            if(self.rotateAngle < 0):
                self.attacking = ""

            leftArm = pygame.transform.scale(
                self.leftArm.image, (88 * (Constants.WINDOW_MAGNIFICATION + 1), 44 * (
                    Constants.WINDOW_MAGNIFICATION + 1)))
            leftArm2, rectL = rot_center(
                leftArm, self.leftArm.image.get_rect(), self.rotateAngle)
            moveRight = self.rotateAngle * 0.8
            self.leftRect = pygame.Rect(
                rectL.x + 350 + moveRight, rectL.y + 275,
                rectL.width // 2 - 50, rectL.height - 30)
            screen.blit(leftArm2, (
                rectL.x + self.leftArmx + 95, rectL.y + self.leftArmy + 50))
            if(self.rotateAngle < 0):
                self.attacking = ""

    def attack(self):
        """ Causes the player to attack. """
        self.attackTimer = 0
        chance = random.random()

        # If the boss' health is less than half, start attacking with both
        if(self.health > self.maxHealth // 2):
            if(chance <= 0.5):
                self.attacking = "right"
            else:
                self.attacking = "left"
        else:
            if(chance <= 0.33):
                self.attacking = "right"
            elif(chance <= 0.5):
                self.attacking = "both"
            else:
                self.attacking = "left"

