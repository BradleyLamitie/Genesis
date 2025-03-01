import pygame
import random
import math
import Constants

class FeedbackSystem():
    """ This class represents the Feedback system that
    displays health, mana, potions, spells, current quest, and currency"""

    def __init__(self, player, boss):
        """ Initialize all the variables used in the feedback system. """

        # Initialize the fonts used in the feedback system.
        self.font = pygame.font.Font("SILKWONDER.ttf", 20)
        self.font2 = pygame.font.Font("SILKWONDER.ttf", 10)

        # Initialize the current Potion, Spell, and Quest selected
        self.currentPotion = player.currentPotion
        self.currentQuest = player.quest
        self.currentSpell = player.currentSpell

        # Find the quantity of the selected potions
        self.potion_Number = player.inventory[self.currentPotion + 6][1]

        # Set the player's current health, mana, max_Health, and max_Mana
        self.max_Health = player.max_Health
        self.max_Mana = player.max_Mana
        self.health = player.health
        self.mana = player.mana

        # Copy boss info
        self.boss_max_Health = boss.maxHealth
        self.boss_health = boss.health

        # Set the player's ammount of money
        self.money = player.money

        # Initialize a copy of the player's inventory
        self.inventory = player.inventory

        # Initialize the coin Image
        self.coin_Image = pygame.sprite.Sprite()
        self.coin_Image.image = pygame.Surface(
            [15 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION])
        self.coin_Image.image = Coin
        self.coin_Image.image.set_colorkey(Constants.COLORKEY)
        self.coin_Imagex = 10
        self.coin_Imagey = Constants.WINDOW_HEIGHT - 40
        self.coin_Image = pygame.transform.scale(
            self.coin_Image.image,
            (15 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION))
        screen.blit(self.coin_Image, (self.coin_Imagex, self.coin_Imagey))

        # Initialize the amount of money the player has
        money = str(self.money)
        money = "X " + money
        self.moneyText = self.font.render(money, True, Constants.WHITE)
        screen.blit(self.moneyText,
                    (Constants.WINDOW_WIDTH//2 - 100, Constants.WINDOW_HEIGHT//2 - 150))

        # Initialize and draw the frame used for displaying the current potion
        self.potion_Frame = pygame.sprite.Sprite()
        self.potion_Frame.image = pygame.Surface(
            [15 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION])
        self.potion_Frame.image = Potion_Frame
        self.potion_Frame.image.set_colorkey(Constants.COLORKEY)
        self.potion_Framex = Constants.WINDOW_WIDTH - 100
        self.potion_Framey = 10
        self.potion_Frame = pygame.transform.scale(
            self.potion_Frame.image,
            (15 * (Constants.WINDOW_MAGNIFICATION + 1), 15 * (Constants.WINDOW_MAGNIFICATION + 1)))
        screen.blit(self.potion_Frame,
                    (self.potion_Framex, self.potion_Framey))

        # Initialize and draw the frame used for displaying the current spell
        self.spell_Frame = pygame.sprite.Sprite()
        self.spell_Frame.image = pygame.Surface(
            [11 * Constants.WINDOW_MAGNIFICATION, 19 * Constants.WINDOW_MAGNIFICATION])
        self.spell_Frame.image = Spell_Frame
        self.spell_Frame.image.set_colorkey(Constants.COLORKEY)
        self.spell_Framex = Constants.WINDOW_WIDTH - 25 * Constants.WINDOW_MAGNIFICATION
        self.spell_Framey = 2 * Constants.WINDOW_MAGNIFICATION
        self.spell_Frame = pygame.transform.scale(
            self.spell_Frame.image,
            (11 * (Constants.WINDOW_MAGNIFICATION + 1), 19 * (Constants.WINDOW_MAGNIFICATION + 1)))
        screen.blit(self.spell_Frame, (self.spell_Framex, self.spell_Framey))

        # Initialize and draw the spell Sprite
        # used for displaying the current spell
        self.currentSpellSprite = pygame.sprite.Sprite()
        self.currentSpellSprite.image = pygame.Surface(
            [11 * Constants.WINDOW_MAGNIFICATION, 19 * Constants.WINDOW_MAGNIFICATION])
        self.currentSpellSprite.image = Blank
        self.currentSpellSprite.image.set_colorkey(Constants.COLORKEY)
        self.currentSpellSpritex = Constants.WINDOW_WIDTH - 23 * Constants.WINDOW_MAGNIFICATION
        self.currentSpellSpritey = 10 * Constants.WINDOW_MAGNIFICATION
        self.currentSpellSprite = pygame.transform.scale(
            self.currentSpellSprite.image,
            (11 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION))
        screen.blit(self.currentSpellSprite,
                    (self.currentSpellSpritex, self.currentSpellSpritey))

        # Initialize and draw the potion Sprite
        # used for displaying the current potion
        self.currentPotionSprite = pygame.sprite.Sprite()
        self.currentPotionSprite.image = pygame.Surface(
            [11 * Constants.WINDOW_MAGNIFICATION, 19 * Constants.WINDOW_MAGNIFICATION])
        self.currentPotionSprite.image = Blank
        self.currentPotionSprite.image.set_colorkey(Constants.COLORKEY)
        self.currentPotionSpritex = Constants.WINDOW_WIDTH - 90
        self.currentPotionSpritey = 20
        self.currentPotionSprite = pygame.transform.scale(
            self.currentPotionSprite.image,
            (11 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION))
        screen.blit(self.currentPotionSprite,
                    (self.currentPotionSpritex, self.currentPotionSpritey))

        # These 2 lines update the display frames for spells and potions.
        self.switchPotionRight(player)
        self.switchSpellLeft(player)

        # Initialize the quest feedback for displaying quest progress
        self.currentQuestSprite = pygame.sprite.Sprite()
        self.currentQuestSprite.image = pygame.Surface(
            [25 * Constants.WINDOW_MAGNIFICATION, 25 * Constants.WINDOW_MAGNIFICATION])
        self.currentQuestSprite.image = Blank
        self.currentQuestSprite.image.set_colorkey(Constants.Constants.COLORKEY)
        self.questText = ""
        self.currentQuestSpritex = 500
        self.currentQuestSpritey = 500

        # Instantiate variables to be used in quest feedback
        self.snakes = 0
        self.rockMimics = 0
        self.healthText = ""
        self.bossNameText = "Patience"

        # This variable keeps track of what room the player is in
        self.playerRoom = 0

    def update(self, player, boss):
        """ Updates the information needed to run the feedbacksystem. """
        if self.currentPotion == -1:
            self.currentPotion = 0
        self.currentQuest = player.quest
        self.max_Health = player.max_Health
        self.max_Mana = player.max_Mana
        self.health = player.health
        self.mana = player.mana
        self.money = player.money
        self.currentQuest = player.quest
        self.inventory = player.inventory
        self.potion_Number = player.inventory[self.currentPotion + 6][1]
        self.snakes = player.snakes
        self.rockMimics = player.rockMimics
        self.boss_max_Health = boss.maxHealth
        self.boss_health = boss.health
        self.playerRoom = player.room

    def draw(self):
        """ Draws the updated feedback system. """

        # Initialize the text used to display how much money the player has.
        money = str(self.money)
        money = "X " + money
        self.moneyText = self.font.render(money, True, Constants.WHITE)

        # Initialize the text used to display how many potions the player has.
        potionAmount = str(self.potion_Number)
        potionText = self.font2.render(potionAmount, True, Constants.WHITE)

        # Initialize the text used to display how much health the player has.
        healthText = str(self.health) + "/" + str(self.max_Health)
        self.healthText = self.font2.render(healthText, True, Constants.BLACK)

        # Initialize the text used to display how much health the boss has.
        bosshealthText = str(self.boss_health) + "/" + str(
            self.boss_max_Health)
        self.bosshealthText = self.font.render(bosshealthText, True, Constants.BLACK)
        bossNameText = "Patience"
        self.bossNameText = self.font.render(bossNameText, True, Constants.WHITE)

        # Initialize the text used to display how much mana the player has.
        manaText = str(self.mana) + "/" + str(self.max_Mana)
        self.manaText = self.font2.render(manaText, True, Constants.BLACK)

        # Initialize the sprites and texts
        # used to display the current quest feedback.
        if(self.currentQuest == ""):
            questText = ""
            self.currentQuestSprite = Blank
        elif(self.currentQuest == "snake"):
            if(self.snakes < 20):
                questText = str(self.snakes) + " / 20"
                self.currentQuestSprite = Snake_Right_1
            else:
                questText = "Turn in to Old Man"
                self.currentQuestSprite = Blank
        elif(self.currentQuest == "rock"):
            if(self.rockMimics < 13):
                questText = str(self.rockMimics) + " / 13"
                self.currentQuestSprite = Rock_Turtle_Quest
            else:
                questText = "Turn in to Old Man"
                self.currentQuestSprite = Blank
        elif(self.currentQuest == "gear"):
            if(self.inventory[11][1] <= 0):
                questText = "Find the gear"
                self.currentQuestSprite = Gear
            else:
                questText = "Turn into Robot"
        self.questText = self.font.render(questText, True, Constants.WHITE)

        # Rescale and set the image's background to clear
        self.currentQuestSprite = pygame.transform.scale(
            self.currentQuestSprite,
            (25 * Constants.WINDOW_MAGNIFICATION, 25 * Constants.WINDOW_MAGNIFICATION))
        self.currentQuestSprite.set_colorkey(Constants.Constants.COLORKEY)

        # Draw all the sprites needed to the screen
        screen.blit(self.currentQuestSprite,
                    (self.currentQuestSpritex, self.currentQuestSpritey))
        screen.blit(self.questText,
                    (self.currentQuestSpritex + 50, self.coin_Imagey + 5))
        screen.blit(self.coin_Image,
                    (self.coin_Imagex, self.coin_Imagey))
        screen.blit(self.moneyText,
                    (self.coin_Imagex + 40, self.coin_Imagey + 5))
        screen.blit(self.potion_Frame,
                    (self.potion_Framex, self.potion_Framey))
        screen.blit(self.spell_Frame,
                    (self.spell_Framex, self.spell_Framey))
        screen.blit(self.currentSpellSprite,
                    (self.currentSpellSpritex, self.currentSpellSpritey))
        screen.blit(self.currentPotionSprite,
                    (self.currentPotionSpritex, self.currentPotionSpritey))
        screen.blit(potionText,
                    (self.potion_Framex + 30, self.potion_Framey + 30))
        pygame.draw.rect(screen, Constants.GRAY,
                         [10, 10, self.max_Health * Constants.WINDOW_MAGNIFICATION,
                          5 * Constants.WINDOW_MAGNIFICATION])
        pygame.draw.rect(screen, Constants.RED,
                         [10, 10, self.health * Constants.WINDOW_MAGNIFICATION,
                          5 * Constants.WINDOW_MAGNIFICATION])
        screen.blit(self.healthText, (self.max_Health - 10, 8))
        pygame.draw.rect(screen, Constants.GRAY,
                         [10, 20, self.max_Mana * Constants.WINDOW_MAGNIFICATION,
                          5 * Constants.WINDOW_MAGNIFICATION])
        pygame.draw.rect(screen, Constants.LIGHTBLUE,
                         [10, 20, self.mana * Constants.WINDOW_MAGNIFICATION,
                          5 * Constants.WINDOW_MAGNIFICATION])
        screen.blit(self.manaText, (self.max_Mana - 10, 18))

        # If the player is in the boss room, display the boss' health bar
        if(self.playerRoom == 28):
            pygame.draw.rect(screen, Constants.GRAY,
                             [70, 500, self.boss_max_Health / 3,
                              10 * Constants.WINDOW_MAGNIFICATION])
            pygame.draw.rect(screen, Constants.RED,
                             [70, 500, self.boss_health / 3,
                              10 * Constants.WINDOW_MAGNIFICATION])
            screen.blit(self.bosshealthText, (self.boss_max_Health // 6 + 20,
                                              500))
            screen.blit(self.bossNameText, (70, 475))

    def switchPotionRight(self, player):
        """ Switches the potion selection forward. """

        # Assume the player has no potions
        hasPotions = False

        # Initialize the inventory
        inventory = player.inventory

        # Retrieve all the information about the potions
        potionInventory = [inventory[6][1], inventory[7][1],
                           inventory[8][1], inventory[9][1]]

        # Check if the player has any potions
        for i in range(len(potionInventory)):
            if(potionInventory[i] >= 1):
                hasPotions = True

        # If the player has potions we will
        # check to see if we have any other ones.
        if hasPotions:

            # Start the while loop
            startPoint = self.currentPotion + 1
            started = False
            while self.currentPotion != startPoint:
                if(not started):
                    startPoint = self.currentPotion
                started = True
                # Cycle through each potion until we find one the player
                # has or we wind up where we started.
                self.currentPotion += 1
                if self.currentPotion > 3:
                    self.currentPotion = 0
                if potionInventory[self.currentPotion] > 0:
                    player.currentPotion = self.currentPotion
                    self.potion_Number = player.inventory[
                        self.currentPotion + 6][1]
                    break

            # Check what potion is selected
            if inventory[self.currentPotion + 6][0] == "Health Potion":
                self.currentPotionSprite = Health_Potion
            elif inventory[self.currentPotion + 6][0] == ("Lesser" +
                                                          " Health Potion"):
                self.currentPotionSprite = Lesser_Health_Potion
            elif inventory[self.currentPotion + 6][0] == "Mana Potion":
                self.currentPotionSprite = Mana_Potion
            elif inventory[self.currentPotion + 6][0] == "Lesser Mana Potion":
                self.currentPotionSprite = Lesser_Mana_Potion
            else:
                # If we dont have any potions we dont display anything.
                self.currentPotionSprite = Blank

        # If we dont have any potions we dont display anything.
        else:
            self.currentPotionSprite = Blank

        # Rescale and set the image's background to clear
        self.currentPotionSprite = pygame.transform.scale(
            self.currentPotionSprite,
            (11 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION))
        self.currentPotionSprite.set_colorkey(Constants.COLORKEY)

    def switchPotionLeft(self, player):
        """ Switches the potion selection backward. """

        # Assume the player has no potions
        hasPotions = False

        # Initialize the inventory
        inventory = player.inventory

        # Retrieve all the information about the potions
        potionInventory = [inventory[6][1], inventory[7][1],
                           inventory[8][1], inventory[9][1]]

        # Check if the player has any potions
        for i in range(len(potionInventory)):
            if(potionInventory[i] >= 1):
                hasPotions = True

        # If the player has potions we will
        # check to see if we have any other ones.
        if hasPotions:

            # Start the while loop
            startPoint = self.currentPotion + 1
            started = False
            while self.currentPotion != startPoint:
                if(not started):
                    startPoint = self.currentPotion
                started = True

                # Cycle through each potion until we find one the player
                # has or we wind up where we started.
                self.currentPotion -= 1
                if self.currentPotion < 0:
                    self.currentPotion = 3
                if potionInventory[self.currentPotion] > 0:
                    player.currentPotion = self.currentPotion
                    self.potion_Number = player.inventory[
                        self.currentPotion + 6][1]
                    break

            # Check what potion is selected
            if inventory[self.currentPotion + 6][0] == "Health Potion":
                self.currentPotionSprite = Health_Potion
            elif inventory[self.currentPotion + 6][0] == ("Lesser " +
                                                          "Health Potion"):
                self.currentPotionSprite = Lesser_Health_Potion
            elif inventory[self.currentPotion + 6][0] == "Mana Potion":
                self.currentPotionSprite = Mana_Potion
            elif inventory[self.currentPotion + 6][0] == "Lesser Mana Potion":
                self.currentPotionSprite = Lesser_Mana_Potion
            else:

                # If we dont have any potions we dont display anything.
                self.currentPotionSprite = Blank

        # If we dont have any potions we dont display anything.
        else:
            self.currentPotionSprite = Blank

        # Rescale and set the image's background to clear
        self.currentPotionSprite = pygame.transform.scale(
            self.currentPotionSprite,
            (11 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION))
        self.currentPotionSprite.set_colorkey(Constants.COLORKEY)

    def switchSpellLeft(self, player):
        """ Switches the spell selection backward. """

        # Set the spellSprite far off screen
        player.spellx = 5000
        player.spelly = 5000

        # Assume the player has no spells
        hasSpells = False

        # initialize a copy of the player's inventory
        inventory = player.inventory

        # Retrieve all the information about the spells
        spellInventory = [inventory[3][1], inventory[4][1]]

        # Check if the player has any spells
        for i in range(len(spellInventory)):
            if(spellInventory[i] >= 1):
                hasSpells = True

        # If the player has spells we will check
        # to see if we have any other ones.
        if hasSpells:

            # Start the while loop
            startPoint = self.currentSpell + 1
            started = False
            while self.currentSpell != startPoint:
                if(not started):
                    startPoint = self.currentSpell
                started = True

                # Cycle through each spell until we find one the player
                # has or we wind up where we started.
                self.currentSpell -= 1
                if self.currentSpell < 0:
                    self.currentSpell = 1
                if spellInventory[self.currentSpell] > 0:
                    player.currentSpell = self.currentSpell
                    self.spell_Number = player.inventory[
                        self.currentSpell + 3][1]
                    break

            # Check what spell iis selected
            if inventory[self.currentSpell + 3][0] == "Fireball Spell":
                self.currentSpellSprite = Fireball_Regular
            elif inventory[self.currentSpell + 3][0] == "Explosion Spell":
                self.currentSpellSprite = Explosion_Blast
            else:

                # If we dont have any spells we dont display anything
                self.currentSpellSprite = Blank

        # If we dont have any spells we dont display anything
        else:
            self.currentSpellSprite = Blank

        # Rescale and set the image's background to clear
        self.currentSpellSprite = pygame.transform.scale(
            self.currentSpellSprite,
            (11 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION))
        self.currentSpellSprite.set_colorkey(Constants.COLORKEY)

    def switchSpellRight(self, player):
        """ Switches the spell selection backward. """
        # Set the spellSprite far off screen
        player.spellx = 5000
        player.spelly = 5000

        # Assume the player has no spells
        hasSpells = False

        # initialize a copy of the player's inventory
        inventory = player.inventory

        # Retrieve all the information about the spells
        spellInventory = [inventory[3][1], inventory[4][1]]

        # Check if the player has any spells
        for i in range(len(spellInventory)):
            if(spellInventory[i] >= 1):
                hasSpells = True

        # If the player has spells we will
        # check to see if we have any other ones.
        if hasSpells:

            # Start the while loop
            startPoint = self.currentSpell + 1
            started = False
            while self.currentSpell != startPoint:
                if(not started):
                    startPoint = self.currentSpell
                started = True

                # Cycle through each spell until we find one
                # the player has or we wind up where we started.
                self.currentSpell += 1
                if self.currentSpell > 1:
                    self.currentSpell = 0
                if spellInventory[self.currentSpell] > 0:
                    player.currentSpell = self.currentSpell
                    self.spell_Number = player.inventory[
                        self.currentSpell + 3][1]
                    break

            # Check what spell is selected
            if inventory[self.currentSpell + 3][0] == "Fireball Spell":
                self.currentSpellSprite = Fireball_Regular
            elif inventory[self.currentSpell + 3][0] == "Explosion Spell":
                self.currentSpellSprite = Explosion_Blast
            else:

                # If we dont have any spells we dont display anything
                self.currentSpellSprite = Blank

        # If we dont have any spells we dont display anything
        else:
            self.currentSpellSprite = Blank

        # Rescale and set the image's background to clear
        self.currentSpellSprite = pygame.transform.scale(
            self.currentSpellSprite,
            (11 * Constants.WINDOW_MAGNIFICATION, 15 * Constants.WINDOW_MAGNIFICATION))
        self.currentSpellSprite.set_colorkey(Constants.COLORKEY)
