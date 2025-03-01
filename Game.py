import pygame
import random
import math
import Constants
import Player
import FeedbackSystem
import Enemy
import Patience

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """
        global tile_Data
        tile_Data = WORLD_DATA
        tile_Data = tile_Data.split('\n')
        tile_Data = [line.split(',') for line in tile_Data]

        # Initialize the current splash screen number
        self.splashNumber = 1

        # Initialize that the game hasn't ended or started yet
        self.game_over = False
        self.game_start = False
        self.game_won = False

        # Initialize dropped items array
        self.dropped_Items = []

        # Create sprite groups
        self.all_boundaries_Group = pygame.sprite.Group()
        self.all_explodables_Group = pygame.sprite.Group()
        self.all_burnables_Group = pygame.sprite.Group()
        self.all_sprites_Group = pygame.sprite.Group()
        self.all_cuttables_Group = pygame.sprite.Group()
        self.all_interactive_Group = pygame.sprite.Group()
        self.room1_enemies_Group = pygame.sprite.Group()
        self.room2_enemies_Group = pygame.sprite.Group()
        self.room4_enemies_Group = pygame.sprite.Group()
        self.room5_enemies_Group = pygame.sprite.Group()
        self.room6_enemies_Group = pygame.sprite.Group()
        self.room7_enemies_Group = pygame.sprite.Group()
        self.room9_enemies_Group = pygame.sprite.Group()
        self.room12_enemies_Group = pygame.sprite.Group()
        self.room14_enemies_Group = pygame.sprite.Group()
        self.room16_enemies_Group = pygame.sprite.Group()
        self.room17_enemies_Group = pygame.sprite.Group()
        self.room22_enemies_Group = pygame.sprite.Group()
        self.room21_enemies_Group = pygame.sprite.Group()
        self.room28_enemies_Group = pygame.sprite.Group()
        self.boss = Patience(225, 60)

        # Show the darkness in each room
        self.room20Darkness = True
        self.room19Darkness = True
        self.room25Darkness = True
        self.room30Darkness = True

        # Create the player
        self.player = Player()

        # Add a super Enemy with 2 times the
        # attack damage and defensive damage.
        superEnemy = Enemy(450, 300, size=2)
        superEnemy.defense = 2
        superEnemy.attackDamage = superEnemy.attackDamage * 2
        superEnemy.aggroRange = superEnemy.aggroRange * 2

        # Add a ultra Enemy with 3 times the
        # attack damage and defensive damage.
        ultraEnemy = Enemy(450, 300, size=3)
        ultraEnemy.defense = 3
        ultraEnemy.attackDamage = ultraEnemy.attackDamage * 3
        ultraEnemy.aggroRange = ultraEnemy.aggroRange * 3

        # Add all the enemys for each room.
        room1 = [Enemy(150, 400), Enemy(150, 400), Enemy(300, 400)]
        room2 = [Enemy(100, 200), Enemy(500, 100), Enemy(150, 300),
                 Enemy(200, 400), Enemy(500, 350)]
        room4 = [Enemy(150, 100), Enemy(300, 100)]
        room5 = [superEnemy]
        room6 = [Enemy(150, 100), Enemy(400, 450), Enemy(600, 350)]
        room7 = [Enemy(150, 100), Enemy(400, 450), Enemy(600, 350)]
        room9 = [Enemy(100, 200), Enemy(500, 100), Enemy(150, 300),
                 Enemy(200, 400), Enemy(500, 350)]
        room12 = [Enemy(600, 200), Enemy(600, 100), Enemy(600, 400),
                  Enemy(400, 200), Enemy(400, 100), Enemy(400, 400),
                  Enemy(200, 200), Enemy(200, 100), Enemy(200, 400),
                  Enemy(200, 200)]
        room14 = [Enemy(100, 200), Enemy(500, 100), Enemy(150, 300),
                  Enemy(200, 400), Enemy(500, 350)]
        room16 = [Enemy(100, 200), Enemy(500, 100), Enemy(150, 300),
                  Enemy(200, 400), Enemy(500, 350)]
        room17 = [Enemy(50, 200), Enemy(500, 300), Enemy(150, 300),
                  Enemy(200, 300), Enemy(500, 350)]
        room21 = [ultraEnemy]
        room22 = [Enemy(100, 200), Enemy(500, 100), Enemy(150, 200),
                  Enemy(200, 400), Enemy(500, 350)]

        # Add each enemy into proper groups to be rendered and drawn
        for enemy in room1:
            self.room1_enemies_Group.add(enemy)
        for enemy in room2:
            self.room2_enemies_Group.add(enemy)
        for enemy in room4:
            self.room4_enemies_Group.add(enemy)
        for enemy in room5:
            self.room5_enemies_Group.add(enemy)
        for enemy in room6:
            self.room6_enemies_Group.add(enemy)
        for enemy in room7:
            self.room7_enemies_Group.add(enemy)
        for enemy in room9:
            self.room9_enemies_Group.add(enemy)
        for enemy in room12:
            self.room12_enemies_Group.add(enemy)
        for enemy in room14:
            self.room14_enemies_Group.add(enemy)
        for enemy in room16:
            enemy.color = "red"
            enemy.attackDamage = enemy.attackDamage * 2
            self.room16_enemies_Group.add(enemy)
        for enemy in room17:
            enemy.color = "red"
            enemy.attackDamage = enemy.attackDamage * 2
            self.room17_enemies_Group.add(enemy)
        for enemy in room21:
            enemy.color = "red"
            enemy.attackDamage = enemy.attackDamage * 2
            self.room21_enemies_Group.add(enemy)
        for enemy in room22:
            enemy.color = "red"
            enemy.attackDamage = enemy.attackDamage * 2
            self.room22_enemies_Group.add(enemy)
        self.room28_enemies_Group.add(self.boss)

        # Create a new feedback System
        self.feedback = FeedbackSystem(self.player, self.boss)

        # Instantiate  starting variables for event handling
        self.upKeyPressed = False
        self.downKeyPressed = False
        self.rightKeyPressed = False
        self.leftKeyPressed = False
        self.DIRECTION = "UP"

        # Instantiate variables for managing how long dialog is displayed.
        # Allow the spell sprite to exist for a few seconds
        self.dt = 0
        self.elapsed = 0

        # Load in the music files
        pygame.mixer.music.load("Genesis_Sprites/Overworld.mp3")

        # Allow the music to play indefinitely
        pygame.mixer.music.play(-1)

        # Instantiate progress for NPC interactions
        self.mana_merchant_dialog = 0
        self.merchant_dialog = 0
        self.old_man_dialog = 0
        self.robot_dialog = 0
        # Instantiate whether or not the NPC can talk
        self.talk = False

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        # Access global variables
        global CAMERA_LEFT, CAMERA_TOP, NEWGAME

        # Run through each event processed
        for event in pygame.event.get():

            # If the window is closed Stop the game
            if event.type == pygame.QUIT:
                return True

            # If the game is over and the mouse is clicked start a new game
            elif (self.game_over and event.type == pygame.MOUSEBUTTONDOWN):
                NEWGAME = True
                CAMERA_LEFT = Constants.ROOM_WIDTH * 2
                CAMERA_TOP = Constants.ROOM_HEIGHT * 5

            # If the game is over and the mouse is clicked start a new game
            elif (self.game_won and event.type == pygame.MOUSEBUTTONDOWN):
                NEWGAME = True
                CAMERA_LEFT = Constants.ROOM_WIDTH * 2
                CAMERA_TOP = Constants.ROOM_HEIGHT * 5

            # If the game hasn't started yet and the player clicks,
            # advance to the next splash screen
            elif (not self.game_start and
                  event.type == pygame.MOUSEBUTTONDOWN):
                self.splashNumber += 1

            # Detect when a key is pressed or held
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.upKeyPressed = True
                    self.downKeyPressed = False
                    # DIRECTION is used later to determine movement direction
                    self.DIRECTION = "UP"
                    self.player.dialog = ""
                elif event.key == pygame.K_DOWN:
                    self.downKeyPressed = True
                    self.upKeyPressed = False
                    self.DIRECTION = "DOWN"
                    self.player.dialog = ""
                elif event.key == pygame.K_RIGHT:
                    self.rightKeyPressed = True
                    self.leftKeyPressed = False
                    self.DIRECTION = "RIGHT"
                    self.player.dialog = ""
                elif event.key == pygame.K_LEFT:
                    self.rightKeyPressed = False
                    self.leftKeyPressed = True
                    self.DIRECTION = "LEFT"
                    self.player.dialog = ""
                elif event.key == pygame.K_q:
                    if(self.player.currentSpell == 0):
                        if self.player.mana >= 10:
                            self.player.useSpell()

                            # If the player uses fireball in a dark room,
                            # erase the darkness
                            if(self.player.room == 19):
                                self.room19Darkness = False
                            elif(self.player.room == 20):
                                self.room20Darkness = False
                            elif(self.player.room == 25):
                                self.room25Darkness = False
                            elif(self.player.room == 30):
                                self.room30Darkness = False

                    if(self.player.currentSpell == 1):
                        if self.player.mana >= 25:
                            self.player.useSpell()
                elif event.key == pygame.K_e:
                    self.player.usePotion()
                elif event.key == pygame.K_h:

                    # Pause the game for a couple seconds and show help screen
                    font = pygame.font.Font("SILKWONDER.ttf", 25)
                    text1 = font.render("Controls:", True, Constants.WHITE)
                    text2 = font.render(
                        "W - Cycle Spell Forward", True, (Constants.WHITE))
                    text3 = font.render(
                        "A - Cycle Potion Backward", True, (Constants.WHITE))
                    text4 = font.render(
                        "S - Cycle Spell Backward", True, (Constants.WHITE))
                    text5 = font.render(
                        "D - Cycle Potion Forward", True, (Constants.WHITE))
                    text6 = font.render("Q - Use Spell", True, (Constants.WHITE))
                    text7 = font.render("E - Use Potion", True, (Constants.WHITE))
                    text8 = font.render("SPACE BAR - Interact", True, (Constants.WHITE))
                    text9 = font.render("Arrow Keys - Move", True, (Constants.WHITE))
                    text10 = font.render("Right Shift - Attack", True, (Constants.WHITE))
                    text11 = font.render("H - View Controls", True, (Constants.WHITE))

                    screen.fill(Constants.BLACK)
                    screen.blit(text1, (Constants.WINDOW_WIDTH//2 - 75, 25))
                    screen.blit(text2, (75, Constants.WINDOW_HEIGHT//2 - 150))
                    screen.blit(
                        text3, (Constants.WINDOW_WIDTH // 2, Constants.WINDOW_HEIGHT // 2 - 150))
                    screen.blit(text4, (75, Constants.WINDOW_HEIGHT//2 - 100))
                    screen.blit(
                        text5, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2 - 100))
                    screen.blit(text6, (75, Constants.WINDOW_HEIGHT//2 - 50))
                    screen.blit(
                        text7, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2 - 50))
                    screen.blit(text8, (75, Constants.WINDOW_HEIGHT//2))
                    screen.blit(text9, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2))
                    screen.blit(text10, (75, Constants.WINDOW_HEIGHT//2 + 50))
                    screen.blit(
                        text11, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2 + 50))
                    pygame.display.flip()
                    pygame.time.wait(5000)
                elif event.key == pygame.K_w:
                    self.feedback.switchSpellLeft(self.player)
                elif event.key == pygame.K_s:
                    self.feedback.switchSpellRight(self.player)
                elif event.key == pygame.K_a:
                    self.feedback.switchPotionLeft(self.player)
                elif event.key == pygame.K_d:
                    self.feedback.switchPotionRight(self.player)
                elif event.key == pygame.K_RSHIFT:
                    self.player.attackEnemy()
                elif event.key == pygame.K_SPACE:
                    self.talk = True
                    self.player.interact()

            # Detect when a key is released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.upKeyPressed = False
                    if self.rightKeyPressed:
                        self.DIRECTION = "RIGHT"
                    elif self.leftKeyPressed:
                        self.DIRECTION = "LEFT"
                elif event.key == pygame.K_DOWN:
                    self.downKeyPressed = False
                    if self.rightKeyPressed:
                        self.DIRECTION = "RIGHT"
                    elif self.leftKeyPressed:
                        self.DIRECTION = "LEFT"
                elif event.key == pygame.K_LEFT:
                    self.leftKeyPressed = False
                    if self.upKeyPressed:
                        self.DIRECTION = "UP"
                    elif self.downKeyPressed:
                        self.DIRECTION = "DOWN"
                elif event.key == pygame.K_RIGHT:
                    self.rightKeyPressed = False
                    if self.upKeyPressed:
                        self.DIRECTION = "UP"
                    elif self.downKeyPressed:
                        self.DIRECTION = "DOWN"

        # If any directional key was pressed we now
        # calculate the player's new coordinates
        if ((self.upKeyPressed or self.downKeyPressed or
             self.leftKeyPressed or self.rightKeyPressed)):

            # Change the player sprite to match player direction
            self.player.changePlayerDirection(self.DIRECTION)

            # Actually move the position of the player
            # If the player exits the room we move to the next one.
            if self.DIRECTION == "UP":
                self.player.y -= Constants.WALKRATE
                self.player.worldy -= Constants.WALKRATE
                self.player.swordx = 5000
                self.player.swordy = 5000
                if self.player.worldy < 0:
                    self.player.worldy = 0
                    self.player.worldy += Constants.WALKRATE
                elif self.player.y < 0:
                    self.player.y = Constants.WINDOW_WIDTH - 300
                    CAMERA_TOP -= Constants.ROOM_HEIGHT
                    self.player.room += 5

                    # If the player enters a new level,
                    # change the background music
                    if(self.player.room == 18):
                        pygame.mixer.music.load(
                            "Genesis_Sprites/ClockTower.mp3")
                        pygame.mixer.music.play(-1)
                    elif(self.player.room == 28):
                        pygame.mixer.music.load("Genesis_Sprites/Boss1.mp3")
                        pygame.mixer.music.play(-1)

            if self.DIRECTION == "DOWN":
                self.player.y += Constants.WALKRATE
                self.player.worldy += Constants.WALKRATE
                self.player.swordx = 5000
                self.player.swordy = 5000
                if self.player.worldy > Constants.WORLD_HEIGHT:
                    self.player.worldy = (Constants.WORLD_HEIGHT -
                                          25 * Constants.WINDOW_MAGNIFICATION)
                elif self.player.y > Constants.WINDOW_HEIGHT:
                    self.player.y = 0
                    CAMERA_TOP += Constants.ROOM_HEIGHT
                    self.player.room -= 5

                    # If the player enters a new level,
                    # change the background music
                    if(self.player.room == 23):
                        pygame.mixer.music.load(
                            "Genesis_Sprites/ClockTower.mp3")
                        pygame.mixer.music.play(-1)
                    elif(self.player.room == 13):
                        pygame.mixer.music.load(
                            "Genesis_Sprites/Overworld.mp3")
                        pygame.mixer.music.play(-1)

            if self.DIRECTION == "LEFT":
                self.player.x -= Constants.WALKRATE
                self.player.worldx -= Constants.WALKRATE
                self.player.swordx = 5000
                self.player.swordy = 5000
                if self.player.x < 0:
                    self.player.x = Constants.WINDOW_WIDTH - 25 * Constants.WINDOW_MAGNIFICATION
                    CAMERA_LEFT -= Constants.ROOM_WIDTH
                    self.player.room += 1
                if self.player.worldx < 0:
                    self.player.worldx = 0
                    self.player.worldx -= Constants.WALKRATE

            if self.DIRECTION == "RIGHT":
                self.player.x += Constants.WALKRATE
                self.player.worldx += Constants.WALKRATE
                self.player.swordx = 5000
                self.player.swordy = 5000
                if self.player.x > Constants.WINDOW_WIDTH:
                    self.player.x = 0
                    CAMERA_LEFT += Constants.ROOM_WIDTH
                    self.player.room -= 1
                if self.player.worldx + 25 > Constants.WORLD_WIDTH:
                    self.player.worldx = Constants.WORLD_WIDTH - 25
                    self.player.worldx -= Constants.WALKRATE

        return False

    def getRoomSurface(self, leftPixel, topPixel):
        """
        This method is used to fetch all tiles in a single room and
        expand them for easier viewing. It is a great space optimization.
        """

        # Get the leftmost and topmost tile numbers
        leftmostTile = leftPixel // 25
        topmostTile = topPixel // 25

        # Empty all the tile groups
        self.all_boundaries_Group.empty()
        self.all_burnables_Group.empty()
        self.all_explodables_Group.empty()
        self.all_cuttables_Group.empty()
        self.all_interactive_Group.empty()

        # Get the initial room surface
        roomSurf = pygame.Surface((Constants.ROOM_WIDTH, Constants.ROOM_HEIGHT))

        # For each tile in the tile_Data we draw it at the room's coordinates.
        for tiley in range(topmostTile, topmostTile + 11):
            for tilex in range(leftmostTile, leftmostTile + 16):
                tile = Tile(tilex, tiley, leftmostTile, topmostTile)
                tile_number = tile.getTileNumber(tilex, tiley)

                # Just in case, ensure tile_number is an integer.
                tile_number = int(tile_number)

                roomSurf.blit(tile.getTile(tile_number),
                              ((tilex - leftmostTile) * 25,
                               (tiley - topmostTile) * 25))

                # Check if the tile at tilex and tiley is
                # a boundary, burnable, or explodable
                if tile_number in boundary_tiles:
                    self.all_boundaries_Group.add(tile)
                if tile_number in explodable_tiles:
                    self.all_explodables_Group.add(tile)
                if tile_number in burnable_tiles:
                    self.all_burnables_Group.add(tile)
                if tile_number in cuttable_tiles:
                    self.all_cuttables_Group.add(tile)
                if tile_number in interactive_tiles:
                    self.all_interactive_Group.add(tile)

        # Zoom in on the room to make it more viewable and return the room
        roomSurf = pygame.transform.scale(roomSurf,
                                          (Constants.ROOM_WIDTH * Constants.WINDOW_MAGNIFICATION,
                                           Constants.ROOM_HEIGHT * Constants.WINDOW_MAGNIFICATION))
        return roomSurf

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        # If the player has no health start over
        if(self.player.health <= 0):
            self.game_over = True

        # Updates the feedback system's information
        self.feedback.update(self.player, self.boss)
        group = self.room1_enemies_Group

        # If the game isnt over continue to update sprites
        if not self.game_over:
            player = self.player

            # Move all the sprites and update positions
            self.all_sprites_Group.update()
            self.all_boundaries_Group.update()
            self.all_explodables_Group.update()
            self.all_burnables_Group.update()
            self.all_cuttables_Group.update()

            # Update the enemies in the room the player is in.
            if self.player.room == 1:
                self.room1_enemies_Group.update(self.player)
                group = self.room1_enemies_Group
            elif self.player.room == 2:
                self.room2_enemies_Group.update(self.player)
                group = self.room2_enemies_Group
            elif self.player.room == 4:
                self.room4_enemies_Group.update(self.player)
                group = self.room4_enemies_Group
            elif self.player.room == 5:
                self.room5_enemies_Group.update(self.player)
                group = self.room5_enemies_Group
            elif self.player.room == 6:
                self.room6_enemies_Group.update(self.player)
                group = self.room6_enemies_Group
            elif self.player.room == 7:
                self.room7_enemies_Group.update(self.player)
                group = self.room7_enemies_Group
            elif self.player.room == 9:
                self.room9_enemies_Group.update(self.player)
                group = self.room9_enemies_Group
            elif self.player.room == 12:
                self.room12_enemies_Group.update(self.player)
                group = self.room12_enemies_Group
            elif self.player.room == 14:
                self.room14_enemies_Group.update(self.player)
                group = self.room14_enemies_Group
            elif self.player.room == 16:
                self.room16_enemies_Group.update(self.player)
                group = self.room16_enemies_Group
            elif self.player.room == 17:
                self.room17_enemies_Group.update(self.player)
                group = self.room17_enemies_Group
            elif self.player.room == 21:
                self.room21_enemies_Group.update(self.player)
                group = self.room21_enemies_Group
            elif self.player.room == 22:
                self.room22_enemies_Group.update(self.player)
                group = self.room22_enemies_Group
            elif self.player.room == 28:
                self.boss.update()
                group = self.room28_enemies_Group

            # Update the player sprite
            self.player.update()

            # Check if there are any collisions
            # between the player and a boundary tile.
            bump_list = spritecollide(self.player,
                                      self.all_boundaries_Group, False)

            # If there is than we have to move
            # the player back to where they were
            if(len(bump_list) >= 1):

                # Based on the direction we last moved
                # the sprite in, move the sprite back.
                if(self.DIRECTION == "UP"):
                    self.player.y += Constants.WALKRATE
                    self.player.worldy += Constants.WALKRATE
                elif (self.DIRECTION == "DOWN"):
                    self.player.y -= Constants.WALKRATE
                    self.player.worldy -= Constants.WALKRATE
                elif (self.DIRECTION == "RIGHT"):
                    self.player.x -= Constants.WALKRATE
                    self.player.worldx -= Constants.WALKRATE
                elif (self.DIRECTION == "LEFT"):
                    self.player.x += Constants.WALKRATE
                    self.player.worldx += Constants.WALKRATE
            else:

                # Set the new position of the player.
                self.player = player

            # Get a list of all the enemies that collide with boundaries
            enemy_collision_list = groupcollide(
                group, self.all_boundaries_Group, False, False)
            if(self.player.room == 28):
                enemy_collision_list = []
            # If there is than we have to move
            # the enemy back to where they were
            if(len(enemy_collision_list) >= 1):
                for enemy in enemy_collision_list:
                    # Based on the direction we last moved
                    # the sprite in, move the sprite back.
                    if(enemy.direction == "UP"):
                        enemy.y += enemy.walkRate
                    elif (enemy.direction == "DOWN"):
                        enemy.y -= enemy.walkRate
                    elif (enemy.direction == "RIGHT"):
                        enemy.x -= enemy.walkRate
                    elif (enemy.direction == "LEFT"):
                        enemy.x += enemy.walkRate
                    elif (enemy.sector == "UP LEFT"):
                        enemy.y += enemy.walkRate
                        enemy.x += enemy.walkRate
                    elif (enemy.sector == "UP RIGHT"):
                        enemy.x -= enemy.walkRate
                        enemy.y += enemy.walkRate
                    elif (enemy.sector == "DOWN LEFT"):
                        enemy.y -= enemy.walkRate
                        enemy.x += enemy.walkRate
                    elif (enemy.sector == "DOWN RIGHT"):
                        enemy.x -= enemy.walkRate
                        enemy.y -= enemy.walkRate

            if not self.player.invincible:
                # Check to see collisions between the
                # player and enemies in the current room
                player_collision_list = spritecollide(
                    self.player, group, False)

                for enemy in player_collision_list:
                    # Take away health from the player
                    if(self.player.room != 28):
                        self.player.health -= (
                            enemy.attackDamage // self.player.defense)
                        self.player.invincible = True
                        self.player.invincibleTimer = 0

            # Create a Rect to be used in attack collision detection
            swordTipRect = pygame.sprite.Sprite()
            if ((self.player.direction == "RIGHT" or
                 self.player.direction == "LEFT")):
                swordTipRect.image = pygame.Surface(
                    [9 * Constants.WINDOW_MAGNIFICATION, 16 * Constants.WINDOW_MAGNIFICATION])
            else:
                swordTipRect.image = pygame.Surface(
                    [16 * Constants.WINDOW_MAGNIFICATION, 9 * Constants.WINDOW_MAGNIFICATION])
            swordTipRect.rect = swordTipRect.image.get_rect()

            # Move the swordtip's frame
            swordTipRect.rect.x = self.player.swordx
            swordTipRect.rect.y = self.player.swordy

            # Check collisions between the enemies and the tip of the sword.
            attack_enemy_list = spritecollide(swordTipRect, group, False)
            for enemy in attack_enemy_list:

                # Decrement the enemy's health
                enemy.health -= self.player.attack // enemy.defense
                if enemy.health <= 0:
                    if(self.player.room == 28):
                        self.game_won = True
                    group.remove(enemy)
                    self.player.snakes += 1
                    sampleItem = self.dropItem(
                        self.player.room, enemy.x, enemy.y)
                    self.dropped_Items.append(sampleItem)

            # Check collisions between cuttable tiles and the player's sword.
            cuttable_list = spritecollide(
                swordTipRect, self.all_cuttables_Group, False)

            # Change the tiles to a changed form.
            for i in range(len(cuttable_list)):
                tile = cuttable_list[i]
                tilex = tile.x
                tiley = tile.y
                tileNumber = tile_Data[tiley][tilex]

                # If it does, replace the cut tiles with the new tile
                if(tileNumber == "44"):
                    tile_Data[tiley][tilex] = "1"

            # Create a rect to be used for
            # checking collisions with interactive tiles
            interactRect = pygame.sprite.Sprite()
            interactRect.image = pygame.Surface(
                [16 * Constants.WINDOW_MAGNIFICATION, 21 * Constants.WINDOW_MAGNIFICATION])
            interactRect.rect = interactRect.image.get_rect()
            interactRect.rect.x = self.player.interactx
            interactRect.rect.y = self.player.interacty

            # Check to see if the interaction
            # sprite collides with interactive tiles.
            interacted_list = spritecollide(
                interactRect, self.all_interactive_Group, False)

            # Change the tiles to a changed form after interacting with it
            # This will also set dialog depending on the coordinates and room.
            for i in range(len(interacted_list)):
                tile = interacted_list[i]
                tilex = tile.x
                tiley = tile.y
                tileNumber = tile_Data[tiley][tilex]
                coords = (tile.x, tile.y)
                room = self.player.room
                # Depending on the room and tile that
                # is interacted with, change the dialog.
                if(room == 3):
                    if(coords == (38, 56)):
                        self.player.dialog = "Press Right Shift to attack"
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                elif(room == 4):
                    if(coords == (30, 64)):
                        self.player.dialog = ("You found 5 Health Potions " +
                                              "and the Clocktower Key!")
                        self.player.dialogCoords[0] = 175
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[6][1] += 5
                        self.player.inventory[5][1] = 1
                        tile_Data[64][30] = 4
                elif(room == 7):
                    if(coords == (61, 47)):
                        self.player.dialog = ("A rockslide has blocked this" +
                                              " path! Sorry for the" +
                                              " inconvenience!")
                        self.player.dialogCoords[0] = 150
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                elif(room == 8):
                    if(coords == (38, 51)):
                        self.player.dialog = (
                            "North - Clocktower, South - Glade")
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                    if(coords == (34, 51)):
                        if(self.talk):
                            if self.merchant_dialog == 0:
                                self.player.dialog = ("Hey there! I'll sell" +
                                                      " you a health potion" +
                                                      " for 10 coins. Just" +
                                                      " talk to me again.")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                                self.talk = False
                                self.merchant_dialog += 1
                            else:
                                if(self.player.money >= 10):
                                    self.player.money -= 10
                                    self.player.inventory[6][1] += 1
                                    self.player.dialog = ("Thanks for " +
                                                          "the business!")
                                    self.player.dialogCoords[0] = 300
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.talk = False
                                else:
                                    self.player.dialog = ("Sorry you dont " +
                                                          "have enough coins!")
                                    self.player.dialogCoords[0] = 250
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.talk = False
                    if(coords == (45, 51)):
                        if(self.talk):
                            if self.mana_merchant_dialog == 0:
                                self.player.dialog = ("Hey there! I'll sell" +
                                                      " you a mana potion" +
                                                      " for 10 coins. Just" +
                                                      " talk to me again.")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                                self.talk = False
                                self.mana_merchant_dialog += 1
                            else:
                                if(self.player.money >= 10):
                                    self.player.money -= 10
                                    self.player.inventory[8][1] += 1
                                    self.player.dialog = ("Thanks for " +
                                                          "the business!")
                                    self.player.dialogCoords[0] = 300
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.talk = False
                                else:
                                    self.player.dialog = ("Sorry you dont " +
                                                          "have enough coins!")
                                    self.player.dialogCoords[0] = 250
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.talk = False
                elif(room == 9):
                    if(coords == (17, 47)):
                        self.player.dialog = ("Please do not go any" +
                                              " further, danger ahead")
                        self.player.dialogCoords[0] = 200
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                elif(room == 10):
                    if(coords == (7, 47)):
                        self.player.dialog = "PLEASE DONT GO ANY FURTHER"
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                    elif(coords == (6, 50)):
                        self.player.dialog = "I MEAN IT"
                        self.player.dialogCoords[0] = 350
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                    elif(coords == (6, 53)):
                        self.player.dialog = "DONT SAY I DIDNT WARN YOU"
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25

                elif(room == 11):
                    if(coords == (70, 35)):
                        if(self.talk):
                            if self.old_man_dialog == 0:
                                self.player.dialog = (
                                    "Hey! I bet youre here for" +
                                    " the clocktower key right?")
                                self.player.dialogCoords[0] = 150
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 25
                            elif self.old_man_dialog == 1:
                                self.player.dialog = (
                                    "Well, first youll have to" +
                                    " do a couple of favors for me.")
                                self.player.dialogCoords[0] = 175
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                            elif self.old_man_dialog == 2:
                                self.player.dialog = (
                                    "You may have noticed there" +
                                    " are a lot of snakes around here.")
                                self.player.dialogCoords[0] = 150
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                            elif self.old_man_dialog == 3:
                                self.player.dialog = (
                                    "I need you to get rid" +
                                    " of 20 of them for me.")
                                self.player.dialogCoords[0] = 200
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 25
                                self.player.quest = "snake"
                            elif self.old_man_dialog == 4:
                                if(self.player.snakes < 20):
                                    self.player.dialog = (
                                        "Go out there and kill those snakes!")
                                    self.player.dialogCoords[0] = 200
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.old_man_dialog -= 1
                                elif(self.player.snakes >= 20):
                                    self.player.dialog = "Nice Job!"
                                    self.player.quest = ""
                                    self.player.dialogCoords[0] = 350
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                            elif self.old_man_dialog == 5:
                                self.player.dialog = (
                                    "Here's the explosion spell, the key" +
                                    " is to the west of the merchant.")
                                self.player.dialogCoords[0] = 150
                                self.player.dialogCoords[1] = (
                                    Constants.WINDOW_HEIGHT - 50)
                                self.player.fontSize = 20
                                self.player.inventory[4][1] = 1
                            elif self.old_man_dialog == 6:
                                self.player.dialog = (
                                    "But I have another offer for you!")
                                self.player.dialogCoords[0] = 250
                                self.player.dialogCoords[1] = (
                                    Constants.WINDOW_HEIGHT - 50)
                                self.player.fontSize = 25
                            elif self.old_man_dialog == 7:
                                self.player.dialog = (
                                    "You may have noticed some strange" +
                                    " rocks here or there.")
                                self.player.dialogCoords[0] = 175
                                self.player.dialogCoords[1] = (
                                    Constants.WINDOW_HEIGHT - 50)
                                self.player.fontSize = 20
                            elif self.old_man_dialog == 8:
                                self.player.dialog = (
                                    "I need you to get rid of all 13 of" +
                                    " them for me using the spell I gave you.")
                                self.player.dialogCoords[0] = 150
                                self.player.dialogCoords[1] = (
                                    Constants.WINDOW_HEIGHT - 50)
                                self.player.fontSize = 16
                                self.player.quest = "rock"
                            elif self.old_man_dialog == 9:
                                self.player.dialog = (
                                    "There's some shiny new armor" +
                                    " in it for you!")
                                self.player.dialogCoords[0] = 175
                                self.player.dialogCoords[1] = (
                                    Constants.WINDOW_HEIGHT - 50)
                                self.player.fontSize = 25
                            elif self.old_man_dialog == 10:
                                if(self.player.rockMimics < 13):
                                    self.player.dialog = (
                                        "Go out there and kill those mimics!")
                                    self.player.dialogCoords[0] = 200
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.old_man_dialog -= 1
                                elif(self.player.rockMimics >= 13):
                                    if(self.armor != "gold"):
                                        self.player.dialog = (
                                            "Nice Job, take this steel Armor" +
                                            " and sword." +
                                            " (Your defense and" +
                                            " offense rose!)")
                                        self.player.fontSize = 16
                                        self.player.defense += 1
                                        self.player.attack += 10
                                        self.player.inventory[1][1] = 1
                                        self.player.armor = "Steel"
                                    else:
                                        self.player.dialog = (
                                            "You already have better Armor")
                                    self.player.dialogCoords[0] = 150
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.quest = ""
                            elif self.old_man_dialog == 11:
                                self.player.dialog = (
                                    "Now i can sleep " +
                                    "soundly with my eyes open!")
                                self.player.dialogCoords[0] = 200
                                self.player.dialogCoords[1] = (
                                    Constants.WINDOW_HEIGHT - 50)
                                self.player.fontSize = 25
                            else:
                                self.player.dialog = "Zzz"
                                self.player.dialogCoords[0] = 400
                                self.player.dialogCoords[1] = (
                                    Constants.WINDOW_HEIGHT - 50)
                                self.player.fontSize = 25
                            self.talk = False
                            self.old_man_dialog += 1

                elif(room == 13):
                    print(coords)
                    if(coords == (38, 40)):
                        self.player.dialog = (
                            "Clocktower is closed for maintenance." +
                            " See Old Man for the key")
                        self.player.dialogCoords[0] = 100
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                    elif(coords == (40, 37) or coords == (39, 37)):
                        if(self.player.inventory[5][1] >= 1):
                            tile_Data[37][40] = "42"
                            tile_Data[37][39] = "5"
                            self.player.dialog = "Door Opened"
                            self.player.dialogCoords[0] = 250
                            self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                            self.player.fontSize = 25
                        else:
                            self.player.dialog = "Door is locked"
                            self.player.dialogCoords[0] = 250
                            self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                            self.player.fontSize = 25
                elif(room == 15):
                    if(coords == (6, 34)):
                        self.player.dialog = (
                            "REMINDER: Use A and D to switch between" +
                            " potions and E to use them")
                        self.player.dialogCoords[0] = 150
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                    elif(coords == (7, 34)):
                        self.player.dialog = (
                            "You found Health and Mana Potions!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[9][1] += 5
                        self.player.inventory[8][1] += 3
                        self.player.inventory[7][1] += 5
                        tile_Data[34][7] = 4
                    elif(coords == (8, 34)):
                        self.player.dialog = "You found the Fireball Spell!"
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[3][1] += 1
                        tile_Data[34][8] = 4
                    elif(coords == (9, 34)):
                        self.player.dialog = (
                            "REMINDER: Use W and S to switch between" +
                            " spells and Q to use them")
                        self.player.dialogCoords[0] = 150
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                elif(room == 18):
                    if(self.talk):
                            if self.robot_dialog == 0:
                                self.player.dialog = ("zzrt HELLO ANGEL")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                                self.talk = False
                                self.robot_dialog += 1
                            elif self.robot_dialog == 1:
                                self.player.dialog = ("I COULD USE YOUR HELP" +
                                                      " FINDING MY GEAR")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                                self.talk = False
                                self.robot_dialog += 1
                            elif self.robot_dialog == 2:
                                self.player.dialog = ("IF YOU FIND IT ILL " +
                                                      "GIVE YOU ARMOR")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                                self.talk = False
                                self.robot_dialog += 1
                                self.player.quest = "gear"
                            elif self.robot_dialog == 3:
                                if(self.player.inventory[11][1] >= 1):
                                    self.player.dialog = (
                                        "THANK YOU, TAKE THIS. (You got a " +
                                        "golden sword and armor!)")
                                    self.player.dialogCoords[0] = 150
                                    self.player.dialogCoords[1] = (
                                        Constants.WINDOW_HEIGHT - 50)
                                    self.player.quest = ""
                                    self.player.fontSize = 16
                                    self.player.defense += 1
                                    self.player.attack += 10
                                    self.player.inventory[1][1] = 1
                                    self.player.armor = "Gold"
                                    self.robot_dialog += 1
                                elif(self.player.inventory[11][1] <= 0):
                                    self.player.dialog = (
                                        "GO FIND THE GEAR PLEASE zzrrt")
                            else:
                                self.player.dialog = ("POWERING DOWN...")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (Constants.WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                                self.talk = False
                                self.robot_dialog += 1
                elif(room == 23):
                    if(coords == (37, 13)):
                        self.player.dialog = (
                            "BEWARE: Boss Room is to the north. " +
                            "Once you enter you cant ever leave again.")
                        self.player.dialogCoords[0] = 100
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                    elif(coords == (39, 11) or coords == (40, 11)):
                        if(self.player.inventory[10][1] == 1):
                            tile_Data[11][40] = 132
                            tile_Data[11][39] = 132
                            self.player.dialog = "Door Opened"
                            self.player.dialogCoords[0] = 250
                            self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                            self.player.fontSize = 25
                        else:
                            self.player.dialog = "Door is locked"
                            self.player.dialogCoords[0] = 250
                            self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                            self.player.fontSize = 25
                elif(room == 26):
                    if(coords == (71, 1)):
                        self.player.dialog = ("You found the Boss Key!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[10][1] += 1
                        tile_Data[1][71] = 155
                elif(room == 27):
                    if(coords == (54, 1)):
                        self.player.dialog = (
                            "You found 50 coins!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.money += 50
                        tile_Data[1][54] = 155
                    elif(coords == (57, 1)):
                        self.player.dialog = (
                            "You found Health and Mana Potions!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[8][1] += 3
                        self.player.inventory[6][1] += 3
                        tile_Data[1][57] = 155
                elif(room == 29):
                    if(coords == (23, 1)):
                        self.player.dialog = (
                            "You found a gear!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = Constants.WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[11][1] += 1
                        tile_Data[1][23] = 155

            # Create rects to be used in item collision detection
            dropped_Items_Group = pygame.sprite.Group()
            for item in self.dropped_Items:

                # Render sprites depending on what items are dropped in a room
                if(item[1] == self.player.room):
                    if(item[0] != "nothing"):
                        if(item[0] == "smallHealthPotion"):
                            sprite = Lesser_Health_Potion
                        elif(item[0] == "smallManaPotion"):
                            sprite = Lesser_Mana_Potion
                        elif(item[0] == "Coin1"):
                            sprite = Coin
                        elif(item[0] == "Coin3"):
                            sprite = Coin
                        elif(item[0] == "Coin5"):
                            sprite = Coin
                    else:
                        sprite = Blank
                    itemDrop = pygame.sprite.Sprite()
                    itemDrop.image = pygame.Surface([25, 25])
                    itemDrop.rect = itemDrop.image.get_rect()
                    itemDrop.rect.x = item[2]
                    itemDrop.rect.y = item[3]
                    itemDrop.image = sprite
                    itemDrop.image.set_colorkey(Constants.COLORKEY)
                    dropped_Items_Group.add(itemDrop)

            # If the player picks up an item, add them to their inventory
            items_picked_up = spritecollide(
                self.player, dropped_Items_Group, True)
            for i in range(len(items_picked_up)):
                print(i)
                pickup = self.dropped_Items[i]
                if(pickup[0] == "Coin1"):
                    self.player.money += 1
                elif(pickup[0] == "Coin3"):
                    self.player.money += 3
                elif(pickup[0] == "Coin5"):
                    self.player.money += 5
                elif(pickup[0] == "smallManaPotion"):
                    self.player.inventory[9][1] += 1
                elif(pickup[0] == "smallHealthPotion"):
                    self.player.inventory[7][1] += 1
                self.dropped_Items.remove(pickup)
            items_picked_up.clear()

            # Create a rect to be used in spell collision detection
            spellRect = pygame.sprite.Sprite()
            spellRect.image = pygame.Surface(
                [11 * Constants.WINDOW_MAGNIFICATION, 16 * Constants.WINDOW_MAGNIFICATION])
            spellRect.rect = spellRect.image.get_rect()
            spellRect.rect.x = self.player.spellx
            spellRect.rect.y = self.player.spelly

            # Check to see if the fire spell collides with burnable objects
            if(self.player.currentSpell == 0):
                spell_burn_collision_list = spritecollide(
                    spellRect, self.all_burnables_Group, False)
                for i in range(len(spell_burn_collision_list)):
                    tile = spell_burn_collision_list[i]
                    tilex = tile.x
                    tiley = tile.y
                    tileNumber = tile_Data[tiley][tilex]

                    # If it does, replace the burned tiles with the new tile.
                    if(tileNumber == "44"):
                        tile_Data[tiley][tilex] = "1"

            # Check to see if the explosion spell
            # collides with explodable objects
            if(self.player.currentSpell == 1):
                spell_explode_collision_list = spritecollide(
                    spellRect, self.all_explodables_Group, False)
                for i in range(len(spell_explode_collision_list)):
                    tile = spell_explode_collision_list[i]
                    tilex = tile.x
                    tiley = tile.y
                    tileNumber = tile_Data[tiley][tilex]

                    # If it does, replace the exploded tiles with the new tile
                    if(tileNumber == "44"):
                        tile_Data[tiley][tilex] = "1"
                    elif(tileNumber == "47"):
                        tile_Data[tiley][tilex] = "2"
                        self.player.rockMimics += 1
                    elif(tileNumber == "48"):
                        tile_Data[tiley][tilex] = "2"
                    elif(tileNumber == "55"):
                        tile_Data[tiley][tilex] = "3"
                    elif(tileNumber == "152"):
                        tile_Data[tiley][tilex] = "153"
                    elif(tileNumber == "160"):
                        tile_Data[tiley][tilex] = "153"
                        tile_Data[tiley + 1][tilex] = "153"

            # Check to see if the fire spell collides with burnable objects
            if(self.player.currentSpell == 0):
                spell_burn_collision_list = spritecollide(
                    spellRect, self.all_burnables_Group, False)
                for i in range(len(spell_burn_collision_list)):
                    tile = spell_burn_collision_list[i]
                    tilex = tile.x
                    tiley = tile.y
                    tileNumber = tile_Data[tiley][tilex]

                    # If it does, replace the burned tiles with the new tile.
                    if(tileNumber == "44"):
                        tile_Data[tiley][tilex] = "1"

            # Check collisions between spells and enemies
            enemy_spell_collisions = spritecollide(spellRect, group, False)
            for enemy in enemy_spell_collisions:

                # Depending on the spell equipped deal damage
                spellDamage = 0
                if(self.player.currentSpell == 0):
                    spellDamage = 50
                elif(self.player.currentSpell == 1):
                    spellDamage = 100

                # Decrement enemy's health
                damageTaken = spellDamage // enemy.spellDefense
                enemy.health -= damageTaken

                # If an enemy's health dies we increment
                # the counter to be used in quests.
                if enemy.health <= 0:
                    if(self.player.room == 28):
                        self.game_won = True
                    group.remove(enemy)
                    self.player.snakes -= 1
                    sampleItem = self.dropItem(
                        self.player.room, enemy.x, enemy.y)
                    self.dropped_Items.append(sampleItem)

            # Close off the Boss Level once the player enters
            if(self.player.room == 28 and
               (self.player.y < (225 * Constants.WINDOW_MAGNIFICATION))):
                tile_Data[10][39] = 158
                tile_Data[10][40] = 158
                self.player.quest = ""

            # If the player is in the boss room, check for collisions
            # between the player and Patience's arms
            if self.player.room == 28:
                # Set up the sprites to use in colission detection
                leftArmRect = pygame.sprite.Sprite()
                leftArmRect.image = self.boss.leftArm.image
                leftArmRect.rect = self.boss.leftRect

                rightArmRect = pygame.sprite.Sprite()
                rightArmRect.image = self.boss.rightArm.image
                rightArmRect.rect = self.boss.rightRect

                armGroup = pygame.sprite.Group()
                armGroup.add(rightArmRect)
                armGroup.add(leftArmRect)

                # If the player isnt invincible, check collisions
                # and handle them
                if not self.player.invincible:
                    spiderHitList = spritecollide(self.player, armGroup, False)
                    for _ in range(len(spiderHitList)):

                        # If there are collisons deduct from the player's
                        # health and make them invincible for a bit
                        self.player.health -= (
                            self.boss.attackDamage // self.player.defense)
                        self.player.invincible = True
                        self.player.invincibleTimer = 0

            # Update each of the room groups based on the current room.
            if self.player.room == 1:
                self.room1_enemies_Group = group
            elif self.player.room == 2:
                self.room2_enemies_Group = group
            elif self.player.room == 4:
                self.room4_enemies_Group = group
            elif self.player.room == 5:
                self.room5_enemies_Group = group
            elif self.player.room == 6:
                self.room6_enemies_Group = group
            elif self.player.room == 7:
                self.room7_enemies_Group = group
            elif self.player.room == 9:
                self.room9_enemies_Group = group
            elif self.player.room == 12:
                self.room12_enemies_Group = group
            elif self.player.room == 14:
                self.room14_enemies_Group = group
            elif self.player.room == 16:
                self.room16_enemies_Group = group
            elif self.player.room == 17:
                self.room17_enemies_Group = group
            elif self.player.room == 21:
                self.room21_enemies_Group = group
            elif self.player.room == 22:
                self.room22_enemies_Group = group
            elif self.player.room == 28:
                self.room28_enemies_Group = group

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """

        # Clear the screen to Constants.WHITE
        screen.fill(Constants.WHITE)

        # If the game hasnt ended and the game has started draw he sprites
        if(not self.game_over and self.game_start and not self.game_won):

            # Instantiate the font needed
            font = pygame.font.Font("SILKWONDER.ttf", self.player.fontSize)

            # Create a new surface for the current room
            roomSurface = self.getRoomSurface(CAMERA_LEFT, CAMERA_TOP)

            # Copy the background image to the viewport.
            screen.blit(roomSurface, (0, 0))

            # Draw each of the sprites in the all_sprites_Group
            self.all_sprites_Group.draw(screen)

            # Draw the Darkness in each level
            if(self.player.room == 19 and self.room19Darkness):
                darkness = pygame.sprite.Sprite()
                darkness.image = pygame.Surface(
                    [350 * Constants.WINDOW_MAGNIFICATION, 225 * Constants.WINDOW_MAGNIFICATION])
                darkness.image = DarkRoom
                darkness.image.set_colorkey(Constants.COLORKEY)
                darknessx = 25 * Constants.WINDOW_MAGNIFICATION
                darknessy = 25 * Constants.WINDOW_MAGNIFICATION
                darkness = pygame.transform.scale(
                    darkness.image,
                    (350 * Constants.WINDOW_MAGNIFICATION, 225 * Constants.WINDOW_MAGNIFICATION))
                screen.blit(darkness,
                            (darknessx, darknessy))
            elif(self.player.room == 20 and self.room20Darkness):
                darkness = pygame.sprite.Sprite()
                darkness.image = pygame.Surface(
                    [350 * Constants.WINDOW_MAGNIFICATION, 225 * Constants.WINDOW_MAGNIFICATION])
                darkness.image = DarkRoom
                darkness.image.set_colorkey(Constants.COLORKEY)
                darknessx = 25 * Constants.WINDOW_MAGNIFICATION
                darknessy = 25 * Constants.WINDOW_MAGNIFICATION
                darkness = pygame.transform.scale(
                    darkness.image,
                    (350 * Constants.WINDOW_MAGNIFICATION, 225 * Constants.WINDOW_MAGNIFICATION))
                screen.blit(darkness,
                            (darknessx, darknessy))
            elif(self.player.room == 25 and self.room25Darkness):
                darkness = pygame.sprite.Sprite()
                darkness.image = pygame.Surface(
                    [350 * Constants.WINDOW_MAGNIFICATION, 225 * Constants.WINDOW_MAGNIFICATION])
                darkness.image = DarkRoom
                darkness.image.set_colorkey(Constants.COLORKEY)
                darknessx = 25 * Constants.WINDOW_MAGNIFICATION
                darknessy = 25 * Constants.WINDOW_MAGNIFICATION
                darkness = pygame.transform.scale(
                    darkness.image,
                    (350 * Constants.WINDOW_MAGNIFICATION, 225 * Constants.WINDOW_MAGNIFICATION))
                screen.blit(darkness,
                            (darknessx, darknessy))
            elif(self.player.room == 30 and self.room30Darkness):
                darkness = pygame.sprite.Sprite()
                darkness.image = pygame.Surface(
                    [350 * Constants.WINDOW_MAGNIFICATION, 225 * Constants.WINDOW_MAGNIFICATION])
                darkness.image = DarkRoom
                darkness.image.set_colorkey(Constants.COLORKEY)
                darknessx = 25 * Constants.WINDOW_MAGNIFICATION
                darknessy = 25 * Constants.WINDOW_MAGNIFICATION
                darkness = pygame.transform.scale(
                    darkness.image,
                    (350 * Constants.WINDOW_MAGNIFICATION, 225 * Constants.WINDOW_MAGNIFICATION))
                screen.blit(darkness,
                            (darknessx, darknessy))
            # Draw the player
            self.player.draw()

            # Actually draw each item that has been dropped in a room
            sprite = Blank
            for item in self.dropped_Items:
                if(item[1] == self.player.room):
                    if(item[0] != "nothing"):
                        if(item[0] == "smallHealthPotion"):
                            sprite = Lesser_Health_Potion
                        elif(item[0] == "smallManaPotion"):
                            sprite = Lesser_Mana_Potion
                        elif(item[0] == "Coin1"):
                            sprite = Coin
                        elif(item[0] == "Coin3"):
                            sprite = Coin
                        elif(item[0] == "Coin5"):
                            sprite = Coin
                    else:
                        sprite = Blank
                    itemDrop = pygame.sprite.Sprite()
                    itemDrop.image = pygame.Surface([25, 25])
                    itemDrop.rect = itemDrop.image.get_rect()
                    itemDrop.image = sprite
                    itemDrop.image.set_colorkey(Constants.COLORKEY)
                    itemDropx = item[2]
                    itemDropy = item[3]
                    itemDrop = pygame.transform.scale(itemDrop.image, (25, 25))
                    screen.blit(itemDrop, (itemDropx, itemDropy))
                    if(item[0] == "nothing"):
                        self.dropped_Items.remove(item)

            # If the player is at the clockTower entrance we render the
            # tunnel leading to the next area.
            if(self.player.room == 13):
                scale = 25 * Constants.WINDOW_MAGNIFICATION
                tunnelTiles = [[ClockTowerFace7, 39, 33],
                               [ClockTowerFace8, 40, 33],
                               [ClockTowerFace21, 39, 34],
                               [ClockTowerFace22, 40, 34],
                               [ClockTowerFace35, 39, 35],
                               [ClockTowerFace36, 40, 35],
                               [ClockTowerFace50, 40, 36],
                               [ClockTowerFace73, 39, 36]]
                for Tunnelset in tunnelTiles:
                    tunnelSprite = pygame.sprite.Sprite()
                    tunnelSprite.image = pygame.Surface(
                        [25 * Constants.WINDOW_MAGNIFICATION, 25 * Constants.WINDOW_MAGNIFICATION])
                    tunnelSprite.image = Tunnelset[0]
                    tunnelSpritex = Tunnelset[1]
                    tunnelSpritey = Tunnelset[2]
                    tunnelSprite = pygame.transform.scale(tunnelSprite.image,
                                                          (scale, scale))
                    screen.blit(tunnelSprite, ((tunnelSpritex - 32) * scale,
                                               (tunnelSpritey - 33) * scale))

            # Draw each of the feedback sprites and information
            self.feedback.draw()

            # Draw the current enemies for the room the player is in.
            if self.player.room == 1:
                self.room1_enemies_Group.draw(screen)
            elif self.player.room == 2:
                self.room2_enemies_Group.draw(screen)
            elif self.player.room == 4:
                self.room4_enemies_Group.draw(screen)
            elif self.player.room == 5:
                self.room5_enemies_Group.draw(screen)
            elif self.player.room == 6:
                self.room6_enemies_Group.draw(screen)
            elif self.player.room == 7:
                self.room7_enemies_Group.draw(screen)
            elif self.player.room == 9:
                self.room9_enemies_Group.draw(screen)
            elif self.player.room == 12:
                self.room12_enemies_Group.draw(screen)
            elif self.player.room == 14:
                self.room14_enemies_Group.draw(screen)
            elif self.player.room == 16:
                self.room16_enemies_Group.draw(screen)
            elif self.player.room == 17:
                self.room17_enemies_Group.draw(screen)
            elif self.player.room == 21:
                self.room21_enemies_Group.draw(screen)
            elif self.player.room == 22:
                self.room22_enemies_Group.draw(screen)
            elif self.player.room == 28:
                self.boss.draw(screen)

            # Draw the dialog onto the screen.
            dialog_text = font.render(self.player.dialog, True, Constants.WHITE)
            screen.blit(
                dialog_text,
                (self.player.dialogCoords[0], self.player.dialogCoords[1]))

            # Copy back buffer onto the front buffer
            pygame.display.flip()

        # If the game is over display game over screen
        elif(self.game_won):
            font = pygame.font.Font("SILKWONDER.ttf", 50)
            text1 = font.render("YOU WON!", True, Constants.WHITE)
            playAgain = font.render("Click to play again", True, Constants.WHITE)
            screen.fill(Constants.BLACK)
            screen.blit(text1, (Constants.WINDOW_WIDTH//2 - 120, Constants.WINDOW_HEIGHT//2 - 150))
            screen.blit(
                playAgain, (Constants.WINDOW_WIDTH//2 - 200, Constants.WINDOW_HEIGHT - 150))
            pygame.display.flip()

        # If the game is over display game over screen
        elif(self.game_over):
            font = pygame.font.Font("SILKWONDER.ttf", 50)
            text1 = font.render("GAME OVER", True, Constants.WHITE)
            playAgain = font.render("Click to play again", True, Constants.WHITE)
            screen.fill(Constants.BLACK)
            screen.blit(text1, (Constants.WINDOW_WIDTH//2 - 120, Constants.WINDOW_HEIGHT//2 - 150))
            screen.blit(playAgain,
                        (Constants.WINDOW_WIDTH//2 - 200, Constants.WINDOW_HEIGHT - 150))
            pygame.display.flip()

        # If the game hasn't started yet, display the splash screen
        elif(not self.game_start):

            # Display the Splash screen
            if(self.splashNumber == 1):
                font = pygame.font.Font("SILKWONDER.ttf", 50)
                font2 = pygame.font.Font("SILKWONDER.ttf", 20)
                text1 = font.render("Genesis", True, Constants.WHITE)
                text2 = font.render("By Bradley Lamitie", True, (Constants.WHITE))
                text3 = font.render("Final Version (12/8/17)", True, (Constants.WHITE))
                continueText = font2.render("Click to continue", True, Constants.WHITE)

                screen.fill(Constants.BLACK)
                screen.blit(text1,
                            (Constants.WINDOW_WIDTH//2 - 100, Constants.WINDOW_HEIGHT//2 - 150))
                screen.blit(text2,
                            (Constants.WINDOW_WIDTH//2 - 180, Constants.WINDOW_HEIGHT//2 - 50))
                screen.blit(text3,
                            (Constants.WINDOW_WIDTH//2 - 280, Constants.WINDOW_HEIGHT//2 + 50))
                screen.blit(continueText,
                            (Constants.WINDOW_WIDTH//2 - 100, Constants.WINDOW_HEIGHT - 75))
                pygame.display.flip()

            # Display the Story screen
            elif(self.splashNumber == 2):
                font = pygame.font.Font("SILKWONDER.ttf", 25)
                font2 = pygame.font.Font("SILKWONDER.ttf", 20)
                text1 = font.render(
                    "You play as an angel cast onto Earth", True, Constants.WHITE)
                text2 = font.render(
                    "after having your wings stripped from you.",
                    True, (Constants.WHITE))
                text3 = font.render(
                    "Your goal is to defeat all 7 virtues on Earth to ",
                    True, (Constants.WHITE))
                text4 = font.render(
                    "redeem yourself and earn your place in heaven.",
                    True, (Constants.WHITE))
                text5 = font.render("Story:", True, Constants.WHITE)
                continueText = font2.render("Click to continue", True, Constants.WHITE)

                screen.fill(Constants.BLACK)
                screen.blit(text1,
                            (Constants.WINDOW_WIDTH//2 - 220, Constants.WINDOW_HEIGHT//2 - 170))
                screen.blit(text2,
                            (Constants.WINDOW_WIDTH//2 - 250, Constants.WINDOW_HEIGHT//2 - 70))
                screen.blit(text3,
                            (Constants.WINDOW_WIDTH//2 - 260, Constants.WINDOW_HEIGHT//2 + 30))
                screen.blit(text4,
                            (Constants.WINDOW_WIDTH//2 - 275, Constants.WINDOW_HEIGHT//2 + 120))
                screen.blit(text5, (Constants.WINDOW_WIDTH//2 - 75, 25))
                screen.blit(continueText,
                            (Constants.WINDOW_WIDTH//2 - 100, Constants.WINDOW_HEIGHT - 75))

                pygame.display.flip()

            # Display the Controls screen
            elif(self.splashNumber == 3):
                font = pygame.font.Font("SILKWONDER.ttf", 25)
                font2 = pygame.font.Font("SILKWONDER.ttf", 20)
                text1 = font.render("Controls:", True, Constants.WHITE)
                text2 = font.render("W - Cycle Spell Forward", True, (Constants.WHITE))
                text3 = font.render("A - Cycle Potion Backward", True, (Constants.WHITE))
                text4 = font.render("S - Cycle Spell Backward", True, (Constants.WHITE))
                text5 = font.render("D - Cycle Potion Forward", True, (Constants.WHITE))
                text6 = font.render("Q - Use Spell", True, (Constants.WHITE))
                text7 = font.render("E - Use Potion", True, (Constants.WHITE))
                text8 = font.render("SPACE BAR - Interact", True, (Constants.WHITE))
                text9 = font.render("Arrow Keys - Move", True, (Constants.WHITE))
                text10 = font.render("Right Shift - Attack", True, (Constants.WHITE))
                text11 = font.render("H - View Controls", True, (Constants.WHITE))
                continueText = font2.render("Click to continue", True, Constants.WHITE)

                screen.fill(Constants.BLACK)
                screen.blit(text1, (Constants.WINDOW_WIDTH//2 - 75, 25))
                screen.blit(text2, (75, Constants.WINDOW_HEIGHT//2 - 150))
                screen.blit(text3, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2 - 150))
                screen.blit(text4, (75, Constants.WINDOW_HEIGHT//2 - 100))
                screen.blit(text5, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2 - 100))
                screen.blit(text6, (75, Constants.WINDOW_HEIGHT//2 - 50))
                screen.blit(text7, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2 - 50))
                screen.blit(text8, (75, Constants.WINDOW_HEIGHT//2))
                screen.blit(text9, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2))
                screen.blit(text10, (75, Constants.WINDOW_HEIGHT//2 + 50))
                screen.blit(text11, (Constants.WINDOW_WIDTH//2, Constants.WINDOW_HEIGHT//2 + 50))
                screen.blit(continueText,
                            (Constants.WINDOW_WIDTH//2 - 100, Constants.WINDOW_HEIGHT - 75))
                pygame.display.flip()
            else:

                # Start the game once we finish
                self.game_start = True

    def dropItem(self, room, x, y):
        chance = random.random()
        item = "nothing"
        if(chance < 0.50):
            item = "nothing"
        elif(chance < 0.60):
            item = "smallHealthPotion"
        elif(chance < 0.70):
            item = "smallManaPotion"
        elif chance < 0.85:
            item = "Coin1"
        elif(chance < 0.95):
            item = "Coin3"
        elif(chance < 1.00):
            item = "Coin5"

        return([item, room, x, y])
