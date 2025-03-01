import pygame
import random
import math
import Constants

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    def __init__(self):

        # Call the superclass' constructor
        super().__init__()

        # This sets the player's current spell and potion
        # to be used when using a potion
        self.currentPotion = -1
        self.currentSpell = -1

        # Initialize the Spell Sprites location
        self.spellx = 5000
        self.spelly = 5000

        # Initialize the spell sprite
        self.currentSpellSprite = pygame.sprite.Sprite()
        self.currentSpellSprite.image = pygame.Surface(
            [11 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION])
        self.currentSpellSprite.image = Blank
        self.currentSpellSprite.image.set_colorkey(Constants.COLORKEY)
        self.currentSpellSpritex = Constants.WINDOW_WIDTH - 23 * Constants.WINDOW_MAGNIFICATION
        self.currentSpellSpritey = 10 * Constants.WINDOW_MAGNIFICATION
        self.currentSpellSprite = pygame.transform.scale(
            self.currentSpellSprite.image,
            (11 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION))
        screen.blit(self.currentSpellSprite,
                    (self.currentSpellSpritex, self.currentSpellSpritey))

        # Initialize the SwordTip Sprites Location
        self.swordx = 5000
        self.swordy = 5000

        # Initialize the sword sprite for attacking
        self.currentSwordSprite = pygame.sprite.Sprite()
        self.currentSwordSprite.image = pygame.Surface(
            [16 * Constants.WINDOW_MAGNIFICATION, 9 * Constants.WINDOW_MAGNIFICATION])
        self.currentSwordSprite.image = Blank
        self.currentSwordSprite.image.set_colorkey(Constants.COLORKEY)
        self.currentSwordSpritex = 0
        self.currentSwordSpritey = 0
        self.currentSwordSprite = pygame.transform.scale(
            self.currentSwordSprite.image,
            (16 * Constants.WINDOW_MAGNIFICATION, 9 * Constants.WINDOW_MAGNIFICATION))
        screen.blit(self.currentSwordSprite,
                    (self.currentSwordSpritex, self.currentSwordSpritey))

        # Initialize the Interact Sprites Location
        self.interactx = 5000
        self.interacty = 5000

        # Initialize the interact sprite for interacting
        self.currentInteractSprite = pygame.sprite.Sprite()
        self.currentInteractSprite.image = pygame.Surface(
            [16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION])
        self.currentInteractSprite.image = Blank
        self.currentInteractSprite.image.set_colorkey(Constants.COLORKEY)
        self.currentInteractSpritex = 0
        self.currentInteractSpritey = 0
        self.currentInteractSprite = pygame.transform.scale(
            self.currentInteractSprite.image,
            (16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION))
        screen.blit(self.currentInteractSprite,
                    (self.currentInteractSpritex, self.currentInteractSpritey))

        # This sets the image to be the Angel surface defined above.
        self.image = pygame.Surface(
            [16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION])
        self.rect = self.image.get_rect()
        self.image = Angel_wood_Front_Idle
        self.image.set_colorkey(Constants.COLORKEY)

        # Set the players starting position to center screen
        # NOTE: The player's x position is not centered at WINDOW_HEIGHT//2
        self.x = Constants.WINDOW_WIDTH // 2 - 36
        self.y = Constants.WINDOW_HEIGHT // 2
        self.rect.x = self.x
        self.rect.y = self.y - 10 * Constants.WINDOW_MAGNIFICATION

        # Set the direction the player is facing
        self.direction = "DOWN"

        # Set the player's max Health and Mana
        self.max_Health = 100
        self.max_Mana = 50

        # Set the player's health and mana
        self.health = 75
        self.mana = 50

        # Set the player's current money
        self.money = 10

        # Set the player's current quest
        self.quest = ""

        # Set the player's current Armor
        self.armor = "Wood"

        # Set the player's inventory
        self.inventory = [["Wood Armor", 0], ["Steel Armor", 0],
                          ["Gold Armor", 0], ["Fireball Spell", 0],
                          ["Explosion Spell", 0], ["Clocktower Key", 0],
                          ["Health Potion", 0], ["Lesser Health Potion", 0],
                          ["Mana Potion", 0], ["Lesser Mana Potion", 0],
                          ["Boss Key", 0], ["Gear", 0]]

        # Set the players position in the world
        self.worldx = Constants.WORLD_WIDTH // 2
        self.worldy = (Constants.WORLD_HEIGHT * 5) // 6

        # Scale the image by the window magnification
        self.image = pygame.transform.scale(
            self.image, (16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION))

        # Create a timer to keep track of sprite longevity
        self.timer = 0
        self.interactTimer = 0

        # Initialize the elapsed variable
        self.elapsed = 0

        # Initialize what room the player is in currently
        self.room = 3

        # Initialize the defense and attack for the player
        self.defense = 1
        self.attack = 10

        # Initialize the counters for enemy kills
        self.rockMimics = 0
        self.snakes = 0

        # Instantiate dialog
        self.dialog = ""
        self.dialogCoords = [120, Constants.WINDOW_HEIGHT - 50]
        self.fontSize = 25

        # Instantiate variables used to check invincibility
        self.invincible = False
        self.invincibleTimer = 0

    def update(self):
        """ Update the player location. """
        # Update a rect to be used in spell collision detection

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        """ Draw the Player sprite onto the back buffer. """

        # Scale the player's sprite and copy it to back buffer
        Angel = pygame.transform.scale(
            self.image, (16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION))
        screen.blit(Angel, [self.x, self.y])

        # Instantiate variables used in calculating timers
        previousElapsed = self.elapsed
        self.elapsed = pygame.time.get_ticks()
        self.timer += ((self.elapsed - previousElapsed)/100)
        self.interactTimer += ((self.elapsed - previousElapsed)/100)
        self.invincibleTimer += ((self.elapsed - previousElapsed)/100)

        # Allow the spell sprite to exist for a few seconds
        if(self.timer < 3):
            self.currentSpellSprite = pygame.transform.scale(
                self.currentSpellSprite,
                (16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION))
            screen.blit(self.currentSpellSprite, (self.spellx, self.spelly))
        else:
            # Once time is up, move the sprite far
            # away where it can't collide anymore
            self.spellx = 5000
            self.spelly = 5000

        # Change the dimensions of the swordtip
        # sprite depending on the attack directions.
        if self.direction == "RIGHT" or self.direction == "LEFT":
            magx = 9 * Constants.WINDOW_MAGNIFICATION
            magy = 16 * Constants.WINDOW_MAGNIFICATION
        else:
            magx = 16 * Constants.WINDOW_MAGNIFICATION
            magy = 9 * Constants.WINDOW_MAGNIFICATION

        # Limit the time the player attacks.
        if(self.timer < 1):
            self.currentSwordSprite = pygame.transform.scale(
                self.currentSwordSprite, (magx, magy))
            screen.blit(self.currentSwordSprite, (self.swordx, self.swordy))
        else:

            # Once time is up, move the sword sprite far away
            self.changePlayerDirection(self.direction)
            self.swordx = 5000
            self.swordy = 5000

        # Limit the time the player interacts and reset dialog
        if(self.interactTimer > 25):
            self.interactx = 5000
            self.interacty = 5000
            self.dialog = ""

        # Limit the time the player is invincible
        if(self.invincibleTimer < 10):
            self.invincible = True
            if(self.elapsed % 5):
                if(self.direction == "UP"):
                    self.image = Angel_Back_Hurt
                elif(self.direction == "DOWN"):
                    self.image = Angel_Front_Hurt
                elif(self.direction == "RIGHT"):
                    self.image = Angel_Right_Hurt
                elif(self.direction == "LEFT"):
                    self.image = Angel_Left_Hurt
                self.image.set_colorkey(COLORKEY)
            else:
                self.changePlayerDirection(self.direction)
        else:
            self.invincible = False

    def changePlayerDirection(self, direction):
        """ Change the player's sprite based on what direction
        the player moved and what armor they have. """

        # Set the player's direction to the direction passed in.
        self.direction = direction

        # Change the sprite based on whatever direction the player is in.
        if direction == "UP":
            if self.armor == "Wood":
                self.image = Angel_wood_Back_Idle
            elif self.armor == "Steel":
                self.image = Angel_Steel_Back_Idle
            elif self.armor == "Gold":
                self.image = Angel_Gold_Back_Idle
        elif direction == "DOWN":
            if self.armor == "Wood":
                self.image = Angel_wood_Front_Idle
            elif self.armor == "Steel":
                self.image = Angel_Steel_Front_Idle
            elif self.armor == "Gold":
                self.image = Angel_Gold_Front_Idle
        elif direction == "LEFT":
            if self.armor == "Wood":
                self.image = Angel_wood_Left_Idle
            elif self.armor == "Steel":
                self.image = Angel_Steel_Left_Idle
            elif self.armor == "Gold":
                self.image = Angel_Gold_Left_Idle
        elif direction == "RIGHT":
            if self.armor == "Wood":
                self.image = Angel_wood_Right_Idle
            elif self.armor == "Steel":
                self.image = Angel_Steel_Right_Idle
            elif self.armor == "Gold":
                self.image = Angel_Gold_Right_Idle

        # Rescale the image and set the background to be translucent
        self.image = pygame.transform.scale(
            self.image, (16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION))
        self.image.set_colorkey(Constants.COLORKEY)

    def attackEnemy(self):
        """ Allow the player to attack. """
        # Depending on what direction and armor the player is in,
        # change the sprites needed to attack.
        if self.direction == "UP":
            if self.armor == "Wood":
                self.image = Angel_wood_Back_Attacking3
                self.currentSwordSprite = Angel_wood_Back_Attacking3_Swordtip
            elif self.armor == "Steel":
                self.image = Angel_Steel_Back_Attacking3
                self.currentSwordSprite = Angel_Steel_Back_Attacking3_Swordtip
            elif self.armor == "Gold":
                self.image = Angel_Gold_Back_Attacking3
                self.currentSwordSprite = Angel_Gold_Back_Attacking3_Swordtip
        elif self.direction == "DOWN":
            if self.armor == "Wood":
                self.image = Angel_wood_Front_Attacking3
                self.currentSwordSprite = Angel_wood_Front_Attacking3_Swordtip
            elif self.armor == "Steel":
                self.image = Angel_Steel_Front_Attacking3
                self.currentSwordSprite = Angel_Steel_Front_Attacking3_Swordtip
            elif self.armor == "Gold":
                self.image = Angel_Gold_Front_Attacking3
                self.currentSwordSprite = Angel_Gold_Front_Attacking3_Swordtip
        elif self.direction == "LEFT":
            if self.armor == "Wood":
                self.image = Angel_wood_Left_Attacking3
                self.currentSwordSprite = Angel_wood_Left_Attacking3_Swordtip
            elif self.armor == "Steel":
                self.image = Angel_Steel_Left_Attacking3
                self.currentSwordSprite = Angel_Steel_Left_Attacking3_Swordtip
            elif self.armor == "Gold":
                self.image = Angel_Gold_Left_Attacking3
                self.currentSwordSprite = Angel_Gold_Left_Attacking3_Swordtip
        elif self.direction == "RIGHT":
            if self.armor == "Wood":
                self.image = Angel_wood_Right_Attacking3
                self.currentSwordSprite = Angel_wood_Right_Attacking3_Swordtip
            elif self.armor == "Steel":
                self.image = Angel_Steel_Right_Attacking3
                self.currentSwordSprite = Angel_Steel_Right_Attacking3_Swordtip
            elif self.armor == "Gold":
                self.image = Angel_Gold_Right_Attacking3
                self.currentSwordSprite = Angel_Gold_Right_Attacking3_Swordtip

        # Depending on the user's direction change the location of
        # the swordtip used in collision detection
        if self.direction == "RIGHT":
                self.swordx = self.x + (16 * Constants.WINDOW_MAGNIFICATION)
                self.swordy = self.y + 8
        elif self.direction == "LEFT":
            self.swordx = self.x - (9 * Constants.WINDOW_MAGNIFICATION)
            self.swordy = self.y + 8
        elif self.direction == "UP":
            self.swordx = self.x
            self.swordy = self.y - (9 * Constants.WINDOW_MAGNIFICATION)
        elif self.direction == "DOWN":
            self.swordx = self.x + 2
            self.swordy = self.y + (21 * Constants.WINDOW_MAGNIFICATION)

        # Rescale the image and set the background to be translucent
        self.image = pygame.transform.scale(
            self.image, (9 * Constants.WINDOW_MAGNIFICATION, 16 * Constants.WINDOW_MAGNIFICATION))
        self.image.set_colorkey(Constants.COLORKEY)
        self.currentSwordSprite.set_colorkey(Constants.COLORKEY)

        # Reset the timer
        self.timer = 0

    def useSpell(self):
        """ Function used to allow player to use spells"""

        # Assume the player has no spells
        hasSpells = False

        # Grab the spell inventory
        spellInventory = [self.inventory[3][1], self.inventory[4][1]]
        for i in range(len(spellInventory)):

            # Check to see if the player has any spells
            if(spellInventory[i] >= 1):
                hasSpells = True

        # Initialize the spellSprite's location to be far off screen
        spell = self.currentSpell
        self.spellx = 5000
        self.spelly = 5000
        playerx = self.x
        playery = self.y
        if(hasSpells):

            # Set the x and y coordinates of the spell sprite
            if(self.direction == "LEFT"):
                self.spellx = playerx - 30
                self.spelly = playery + 5
            elif(self.direction == "RIGHT"):
                self.spellx = playerx + 30
                self.spelly = playery + 5
            elif(self.direction == "DOWN"):
                self.spellx = playerx - 5
                self.spelly = playery + 45
            elif(self.direction == "UP"):
                self.spellx = playerx - 5
                self.spelly = playery - 45

        # Set the sprite image and consume Mana
        if self.inventory[spell + 3][0] == "Fireball Spell":
                self.currentSpellSprite = Fireball_Regular
                self.mana -= 10
        elif self.inventory[spell + 3][0] == "Explosion Spell":
                self.currentSpellSprite = Explosion_Blast
                self.mana -= 25

        # Rescale and set the image's background to clear
        self.currentSpellSprite = pygame.transform.scale(
            self.currentSpellSprite,
            (11 * Constants.WINDOW_MAGNIFICATION + 1, 15 * Constants.WINDOW_MAGNIFICATION + 1))
        self.currentSpellSprite.set_colorkey(Constants.COLORKEY)

        # Reset the timer
        self.timer = 0

    def usePotion(self):
        """ This function allows the player to consume a potion and
        have it heal them or restore mana. """

        # Assume the player has no potions
        hasPotions = False

        # Grab the inventory slots of each potion
        potionInventory = [self.inventory[6][1], self.inventory[7][1],
                           self.inventory[8][1], self.inventory[9][1]]

        # Check if the player has any potions at all.
        for i in range(len(potionInventory)):
            if(potionInventory[i] >= 1):
                hasPotions = True

        # If they have potions check which one is selected ad use it.
        if hasPotions:
            if(potionInventory[self.currentPotion] > 0):

                # Decrement the number of potions the player has.
                self.inventory[self.currentPotion + 6][1] -= 1

                # Find the name of the potion we used
                # and restore mana or health.
                potionType = self.inventory[self.currentPotion + 6][0]
                if potionType == "Health Potion":
                    self.health += 50
                    if(self.health > self.max_Health):
                        self.health = self.max_Health
                elif potionType == "Lesser Health Potion":
                    self.health += 25
                    if(self.health > self.max_Health):
                        self.health = self.max_Health
                elif potionType == "Mana Potion":
                    self.mana += 50
                    if(self.mana > self.max_Mana):
                        self.mana = self.max_Mana
                elif potionType == "Lesser Mana Potion":
                    self.mana += 25
                    if(self.mana > self.max_Mana):
                        self.mana = self.max_Mana

    def interact(self):
        """ This function will allow the player
        to interact with certain tiles."""

        # This sets the image to be a Blank surface defined above.
        self.image = pygame.Surface(
            [16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION])
        self.rect = self.image.get_rect()
        self.image = Blank
        self.image.set_colorkey(Constants.COLORKEY)

        # Initialize x and y based on direction player is facing.
        if(self.direction == "UP"):
            self.interactx = self.x
            self.interacty = self.y - 21 * Constants.WINDOW_MAGNIFICATION
        elif(self.direction == "DOWN"):
            self.interactx = self.x
            self.interacty = self.y + 21 * Constants.WINDOW_MAGNIFICATION
        elif(self.direction == "RIGHT"):
            self.interactx = self.x + 16 * Constants.WINDOW_MAGNIFICATION
            self.interacty = self.y
        elif(self.direction == "LEFT"):
            self.interactx = self.x - 16 * Constants.WINDOW_MAGNIFICATION
            self.interacty = self.y

        # Reset the timer
        self.interactTimer = 0
