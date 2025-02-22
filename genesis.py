"""
Create the main game for "Genesis"

Author: Bradley Lamitie
Date: 12/11/2017
Version Number: 3.0 (Final)

What the Code Does:
The code so far creates the world using the tiles provided by rendering
one room at a time and zooming in on it to make it more visible.
Then, the player is put into the world and can use the directional
keys( UpArrow, RightArrow, LeftArrow, and DownArrow ) to move around the world
The player can also now use potions and spells using the E and Q key
The player can switch between potions using A and D
and switch between spells with W and S
The Right Shift key can be used to attack
The H key shows the controls for 5 seconds
The code runs through the events and moves the sprite.
The enemies can drop items and the player can pick them up by walking over them
NPCs can give quests for rewards.
You can win the game by progressing through the grassland to the clocktower
and defeating the boss.

How to Play:
The player can use the directional keys to move around the world.
Use spells to fight and destroy obstacles.
Use attacking to fight enemys.
Use potions to heal and restore mana.

GitHub Repository: https://github.com/BradleyLamitie/Genesis

Credits:
Silk Wonderland font by jelloween Found on:
 https://jelloween.deviantart.com/art/Font-SILKY-WONDERLAND-free-45103645
"Factory Time" By visager
"The Black Box" By roleMusic
"The White" By RoleMusic found on http://freemusicarchive.org/genre/Chiptune/
All Sprites are made by me using Pixilart.com


Changes in this version:
- Passed the style checker without errors
- Game balancing

Known Glitches:
- Sometimes enemies disappear into walls
- Occasionally enemies move unnaturally fast
- Player Sprite warps when attacking
- Enemies sometimes move away from player, rather than towards
- When the player gets a spell/potion, the display doesn't update dynamically
- Collision detection for Patience's attacks are inaccurate
- When a player grabs an item, they pick up all the items in the room

Features I didn't have time to implement:
- Make it so that the WORLD_DATA is imported from a .tmx file.
- If possible import a tileset from a Tiled file.
- Use a sprite Sheet to load in sprites.
- Add Save states or a pause function.
- Add a menu.
- Animate the characters as they move throughout the world.
- Add a better plot
- Modularization
"""

# Import the necessary packages
import pygame
from pygame.sprite import spritecollide, groupcollide
import random
import math

# --- Global constants ---
# Colors:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTBLUE = (0, 191, 255)
GRAY = (205, 201, 201)

# Set the color key to hot pink to make the background translucent
COLORKEY = (255, 0, 255)

# The width and height of the room (16 tiles * 11 tiles)
ROOM_WIDTH = 400
ROOM_HEIGHT = 275

# The width and height of the world
WORLD_WIDTH = 4000
WORLD_HEIGHT = 1650

# The rate at which we magnify the pixels
WINDOW_MAGNIFICATION = 2

# For every frame the player sprite will be moved by the WALKRATE variable
WALKRATE = 7

# How many seconds an animation frame should last.
ANIMRATE = 0.15

# The width and height of the magnified window
WINDOW_WIDTH = ROOM_WIDTH * WINDOW_MAGNIFICATION
WINDOW_HEIGHT = ROOM_HEIGHT * WINDOW_MAGNIFICATION

# The Camera starts at the second room from the right, second room down.
CAMERA_LEFT = ROOM_WIDTH * 2
CAMERA_TOP = ROOM_HEIGHT * 5

# Set the need for a new game to false
NEWGAME = False

# Set the screen as a global variable
# (This is necessary in order to load in the sprites)
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)

# Load in each of the sprite images
Cliff_bottom_bottom = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_bottom.png").convert()
Cliff_bottom_corner_bottomleft = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_bottomleft.png").convert()
Cliff_bottom_corner_bottomright = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_bottomright.png").convert()
Cliff_bottom_corner_inset_bottomleft = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_inset_bottomleft.png").convert()
Cliff_bottom_corner_inset_bottomright = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_inset_bottomright.png").convert()
Cliff_bottom_topleft = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_inset_topleft.png").convert()
Cliff_bottom_corner_inset_topright = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_inset_topright.png").convert()
Cliff_bottom_corner_inset_topleft = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_inset_topleft.png").convert()
Cliff_bottom_corner_topleft = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_topleft.png").convert()
Cliff_bottom_corner_topright = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_corner_topright.png").convert()
Cliff_bottom_left = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_left.png").convert()
Cliff_bottom_right = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_right.png").convert()
Cliff_bottom_top = pygame.image.load(
    "Genesis_Sprites/Cliff_bottom_top.png").convert()
Cliff_corner_bottomleft = pygame.image.load(
    "Genesis_Sprites/Cliff_corner_bottomleft.png").convert()
Cliff_corner_bottomright = pygame.image.load(
    "Genesis_Sprites/Cliff_corner_bottomright.png").convert()
Cliff_corner_topleft = pygame.image.load(
    "Genesis_Sprites/Cliff_corner_topleft.png").convert()
Cliff_corner_topright = pygame.image.load(
    "Genesis_Sprites/Cliff_corner_topright.png").convert()
Cliff_top = pygame.image.load(
    "Genesis_Sprites/Cliff_top.png").convert()
Cliff_top_corner_bottomleft = pygame.image.load(
    "Genesis_Sprites/Cliff_top_corner_bottomleft.png").convert()
Cliff_top_corner_bottomright = pygame.image.load(
    "Genesis_Sprites/Cliff_top_corner_bottomright.png").convert()
Cliff_top_corner_topleft = pygame.image.load(
    "Genesis_Sprites/Cliff_top_corner_topleft.png").convert()
Cliff_top_corner_topright = pygame.image.load(
    "Genesis_Sprites/Cliff_top_corner_topright.png").convert()
Cliff_top_edge_bottom = pygame.image.load(
    "Genesis_Sprites/Cliff_top_edge_bottom.png").convert()
Cliff_top_edge_left = pygame.image.load(
    "Genesis_Sprites/Cliff_top_edge_left.png").convert()
Cliff_top_edge_right = pygame.image.load(
    "Genesis_Sprites/Cliff_top_edge_right.png").convert()
Cliff_top_edge_top = pygame.image.load(
    "Genesis_Sprites/Cliff_top_edge_top.png").convert()
Cliff_wall = pygame.image.load(
    "Genesis_Sprites/Cliff_wall.png").convert()
Clocktower_door = pygame.image.load(
    "Genesis_Sprites/Clocktower_door.png").convert()
Clocktower_door_open = pygame.image.load(
    "Genesis_Sprites/Clocktower_door_open.png").convert()
Clocktower_door_open_right = pygame.image.load(
    "Genesis_Sprites/Clocktower_door_open_right.png").convert()
Grass_cut = pygame.image.load(
    "Genesis_Sprites/Grass_cut.png").convert()
Grass_uncut = pygame.image.load(
    "Genesis_Sprites/Grass_uncut.png").convert()
gray_ground_path = pygame.image.load(
    "Genesis_Sprites/gray_ground_path.png").convert()
Ground_grass = pygame.image.load(
    "Genesis_Sprites/Ground_grass.png").convert()
Rock_exploded = pygame.image.load(
    "Genesis_Sprites/Rock_exploded.png").convert()
Rock_exploded_path = pygame.image.load(
    "Genesis_Sprites/Rock_exploded_path.png").convert()
Rock_turtle = pygame.image.load(
    "Genesis_Sprites/Rock_turtle.png").convert()
Rock_unexploded = pygame.image.load(
    "Genesis_Sprites/Rock_unexploded.png").convert()
Rock_unexploded_path = pygame.image.load(
    "Genesis_Sprites/Rock_unexploded_path.png").convert()
Signpost = pygame.image.load(
    "Genesis_Sprites/Signpost.png").convert()
Signpost_path = pygame.image.load(
    "Genesis_Sprites/Signpost_path.png").convert()
Chest_Closed = pygame.image.load(
    "Genesis_Sprites/Chest_closed.png").convert()
Chest_Open = pygame.image.load(
    "Genesis_Sprites/Chest_open.png").convert()
ClockTowerFace1 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face1.png").convert()
ClockTowerFace2 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face2.png").convert()
ClockTowerFace3 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face3.png").convert()
ClockTowerFace4 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face4.png").convert()
ClockTowerFace5 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face5.png").convert()
ClockTowerFace6 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face6.png").convert()
ClockTowerFace7 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face7.png").convert()
ClockTowerFace8 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face8.png").convert()
ClockTowerFace9 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face9.png").convert()
ClockTowerFace10 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face10.png").convert()
ClockTowerFace11 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face11.png").convert()
ClockTowerFace12 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face12.png").convert()
ClockTowerFace13 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face13.png").convert()
ClockTowerFace14 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face14.png").convert()
ClockTowerFace15 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face15.png").convert()
ClockTowerFace16 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face16.png").convert()
ClockTowerFace17 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face17.png").convert()
ClockTowerFace18 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face18.png").convert()
ClockTowerFace19 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face19.png").convert()
ClockTowerFace20 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face20.png").convert()
ClockTowerFace21 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face21.png").convert()
ClockTowerFace22 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face22.png").convert()
ClockTowerFace23 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face23.png").convert()
ClockTowerFace24 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face24.png").convert()
ClockTowerFace25 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face25.png").convert()
ClockTowerFace26 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face26.png").convert()
ClockTowerFace27 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face27.png").convert()
ClockTowerFace28 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face28.png").convert()
ClockTowerFace29 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face29.png").convert()
ClockTowerFace30 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face30.png").convert()
ClockTowerFace31 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face31.png").convert()
ClockTowerFace32 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face32.png").convert()
ClockTowerFace33 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face33.png").convert()
ClockTowerFace34 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face34.png").convert()
ClockTowerFace35 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face35.png").convert()
ClockTowerFace36 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face36.png").convert()
ClockTowerFace37 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face37.png").convert()
ClockTowerFace38 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face38.png").convert()
ClockTowerFace39 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face39.png").convert()
ClockTowerFace40 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face40.png").convert()
ClockTowerFace41 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face41.png").convert()
ClockTowerFace42 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face42.png").convert()
ClockTowerFace43 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face43.png").convert()
ClockTowerFace44 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face44.png").convert()
ClockTowerFace45 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face45.png").convert()
ClockTowerFace46 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face46.png").convert()
ClockTowerFace47 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face47.png").convert()
ClockTowerFace48 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face48.png").convert()
ClockTowerFace49 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face49.png").convert()
ClockTowerFace50 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face50.png").convert()
ClockTowerFace51 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face51.png").convert()
ClockTowerFace52 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face52.png").convert()
ClockTowerFace53 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face53.png").convert()
ClockTowerFace54 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face54.png").convert()
ClockTowerFace55 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face55.png").convert()
ClockTowerFace56 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face56.png").convert()
ClockTowerFace57 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face57.png").convert()
ClockTowerFace58 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face58.png").convert()
ClockTowerFace59 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face59.png").convert()
ClockTowerFace60 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face60.png").convert()
ClockTowerFace61 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face61.png").convert()
ClockTowerFace62 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face62.png").convert()
ClockTowerFace63 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face63.png").convert()
ClockTowerFace64 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face64.png").convert()
ClockTowerFace65 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face65.png").convert()
ClockTowerFace66 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face66.png").convert()
ClockTowerFace67 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face67.png").convert()
ClockTowerFace68 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face68.png").convert()
ClockTowerFace69 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face69.png").convert()
ClockTowerFace70 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face70.png").convert()
ClockTowerFace71 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face71.png").convert()
ClockTowerFace72 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face72.png").convert()
ClockTowerFace73 = pygame.image.load(
    "Genesis_Sprites/Clocktower_face73.png").convert()

# 2nd level sprites
GrayFloorTile = pygame.image.load(
    "Genesis_Sprites/GrayFloorTile.png").convert()
BlackFloorTile = pygame.image.load(
    "Genesis_Sprites/BlackFloorTile.png").convert()
WhiteFloorTile = pygame.image.load(
    "Genesis_Sprites/WhiteFloorTile.png").convert()
Obstacle = pygame.image.load(
    "Genesis_Sprites/Obstacle.png").convert()
FloorTile = pygame.image.load(
    "Genesis_Sprites/FloorTile.png").convert()
LeftBrick = pygame.image.load(
    "Genesis_Sprites/LeftBrick.png").convert()
BottomBrick = pygame.image.load(
    "Genesis_Sprites/BottomBrick.png").convert()
TopBrick = pygame.image.load(
    "Genesis_Sprites/TopBrick.png").convert()
RightBrick = pygame.image.load(
    "Genesis_Sprites/RightBrick.png").convert()
LeftBrick = pygame.image.load(
    "Genesis_Sprites/LeftBrick.png").convert()
BottomRightBrick = pygame.image.load(
    "Genesis_Sprites/BottomRightBrick.png").convert()
TopLeftBrick = pygame.image.load(
    "Genesis_Sprites/TopLeftBrick.png").convert()
TopRightBrick = pygame.image.load(
    "Genesis_Sprites/TopRightBrick.png").convert()
BottomLeftBrick = pygame.image.load(
    "Genesis_Sprites/BottomLeftBrick.png").convert()
BottomLeftCornerBrick = pygame.image.load(
    "Genesis_Sprites/BottomLeftCornerBrick.png").convert()
BottomRightCornerBrick = pygame.image.load(
    "Genesis_Sprites/BottomRightCornerBrick.png").convert()
TopLeftCornerBrick = pygame.image.load(
    "Genesis_Sprites/TopLeftCornerBrick.png").convert()
TopRightCornerBrick = pygame.image.load(
    "Genesis_Sprites/TopRightCornerBrick.png").convert()
BreakableBrickWall = pygame.image.load(
    "Genesis_Sprites/BreakableBrickWall.png").convert()
BreakableBrickWallDown = pygame.image.load(
    "Genesis_Sprites/BreakableBrickWallDown.png").convert()
BrokenBrickWall = pygame.image.load(
    "Genesis_Sprites/BrokenBrickWall.png").convert()
Chest_Closed_tile = pygame.image.load(
    "Genesis_Sprites/Chest_Closed_tile.png").convert()
Chest_Open_tile = pygame.image.load(
    "Genesis_Sprites/Chest_Open_tile.png").convert()
Signpost_Tile = pygame.image.load(
    "Genesis_Sprites/Signpost_Tile.png").convert()
HourglassDoor = pygame.image.load(
    "Genesis_Sprites/BossDoor.png").convert()
SkullDoor = pygame.image.load(
    "Genesis_Sprites/BossDoor2.png").convert()
Gear = pygame.image.load(
    "Genesis_Sprites/Gear.png")
Map_Image = pygame.image.load(
    "Genesis_Sprites/Genesis_Map.png").convert()

# Add the NPCs
Merchant = pygame.image.load(
    "Genesis_Sprites/Merchant.png").convert()
OldMan = pygame.image.load(
    "Genesis_Sprites/OldMan.png").convert()
ManaMerchant = pygame.image.load(
    "Genesis_Sprites/ManaMerchant.png")
Rock_Turtle_Quest = pygame.image.load(
    "Genesis_Sprites/Rock_Turtle_quest.png").convert()
RobotNPC = pygame.image.load(
    "Genesis_Sprites/RobotNPC.png").convert()

# Add the images for the snake enemy
Snake_Forward_1 = pygame.image.load(
    "Genesis_Sprites/Snake_Forward_1.png").convert()
Snake_Forward_2 = pygame.image.load(
    "Genesis_Sprites/Snake_Forward_2.png").convert()
Snake_Back_1 = pygame.image.load("Genesis_Sprites/Snake_Back_1.png").convert()
Snake_Back_2 = pygame.image.load("Genesis_Sprites/Snake_Back_2.png").convert()
Snake_Right_1 = pygame.image.load(
    "Genesis_Sprites/Snake_Right_1.png").convert()
Snake_Right_2 = pygame.image.load(
    "Genesis_Sprites/Snake_Right_2.png").convert()
Snake_Left_1 = pygame.transform.flip(Snake_Right_1, True, False)
Snake_Left_2 = pygame.transform.flip(Snake_Right_2, True, False)
Snake_Red_Right = pygame.image.load(
    "Genesis_Sprites/Snake_Red_Right.png").convert()
Snake_Red_Front = pygame.image.load(
    "Genesis_Sprites/Snake_Red_Front.png").convert()
Snake_Red_Back = pygame.image.load(
    "Genesis_Sprites/Snake_Red_Back.png").convert()
Snake_Red_Left = pygame.transform.flip(Snake_Red_Right, True, False)

# Add images for the boss
Spider_Legless = pygame.image.load(
    "Genesis_Sprites/Spider_Legless.png").convert()
LeftSpiderArmScytheBase = pygame.image.load(
    "Genesis_Sprites/SpiderArmScytheBase.png").convert()
LeftSpiderArmScytheBlade = pygame.image.load(
    "Genesis_Sprites/SpiderArmScytheBlade.png").convert()
LeftSpiderArmBlade = pygame.image.load(
    "Genesis_Sprites/SpiderArmBlade.png").convert()
LeftSpiderArmBase = pygame.image.load(
    "Genesis_Sprites/SpiderArmBase.png").convert()
RightSpiderArmScytheBase = pygame.transform.flip(
    LeftSpiderArmScytheBase, True, False)
RightSpiderArmScytheBlade = pygame.transform.flip(
    LeftSpiderArmScytheBlade, True, False)
RightSpiderArmBlade = pygame.transform.flip(
    LeftSpiderArmBlade, True, False)
RightSpiderArmBase = pygame.transform.flip(
    LeftSpiderArmBase, True, False)
LeftSpiderScythe = pygame.image.load(
    "Genesis_Sprites/SpiderArmScytheLeft.png").convert()
RightSpiderScythe = pygame.transform.flip(LeftSpiderScythe, True, False)

# Add the icons that will be used in the feedback system
Fireball_Regular = pygame.image.load(
    "Genesis_Sprites/Fireball_Regular.png").convert()
Fireball_Swirl = pygame.image.load(
    "Genesis_Sprites/Fireball_Swirl.png").convert()
Explosion_Bomb = pygame.image.load(
    "Genesis_Sprites/Explosion_Bomb.png").convert()
Explosion_Blast = pygame.image.load(
    "Genesis_Sprites/Explosion_Blast.png").convert()
Lesser_Mana_Potion = pygame.image.load(
    "Genesis_Sprites/Lesser_Mana_Potion.png").convert()
Lesser_Health_Potion = pygame.image.load(
    "Genesis_Sprites/Lesser_Health_Potion.png").convert()
Mana_Potion = pygame.image.load(
    "Genesis_Sprites/Mana_Potion.png").convert()
Health_Potion = pygame.image.load(
    "Genesis_Sprites/Health_Potion.png").convert()
Spell_Frame = pygame.image.load(
    "Genesis_Sprites/Spell_Frame_Filled.png").convert()
Potion_Frame = pygame.image.load(
    "Genesis_Sprites/Potion_Frame_Filled.png").convert()
Coin = pygame.image.load(
    "Genesis_Sprites/Coin.png").convert()
Blank = pygame.image.load(
    "Genesis_Sprites/Blank.png").convert()
DarkRoom = pygame.image.load(
    "Genesis_Sprites/DarkRoom.png").convert()

# Add the images for Angel sprites in each armor
# Add the images for Angel with wooden Armor and Sword
Angel_wood_Back_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_wood_back_idle.png").convert()
Angel_wood_Back_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_back_walking1.png").convert()
Angel_wood_Back_Walking2 = Angel_wood_Back_Idle
Angel_wood_Back_Walking3 = pygame.transform.flip(
    Angel_wood_Back_Walking1, True, False)
Angel_wood_Back_Walking4 = Angel_wood_Back_Idle
Angel_wood_Back_Attacking1 = Angel_wood_Back_Idle
Angel_wood_Back_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_back_Attacking2.png").convert()
Angel_wood_Back_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_back_Attacking3.png").convert()
Angel_wood_Back_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_back_Attacking4.png").convert()
Angel_wood_Back_Attacking5 = Angel_wood_Back_Idle
Angel_wood_Back_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_back_Attacking2_swordtip.png").convert()
Angel_wood_Back_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_back_Attacking3_swordtip.png").convert()
Angel_wood_Back_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_back_Attacking4_swordtip.png").convert()

Angel_wood_Front_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_idle.png").convert()
Angel_wood_Front_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_walking1.png").convert()
Angel_wood_Front_Walking2 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_walking2.png").convert()
Angel_wood_Front_Walking3 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_walking3.png").convert()
Angel_wood_Front_Walking4 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_walking4.png").convert()
Angel_wood_Front_Attacking1 = Angel_wood_Front_Idle
Angel_wood_Front_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_Attacking2.png").convert()
Angel_wood_Front_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_Attacking3.png").convert()
Angel_wood_Front_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_Attacking4.png").convert()
Angel_wood_Front_Attacking5 = Angel_wood_Front_Idle
Angel_wood_Front_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_Attacking2_swordtip.png").convert()
Angel_wood_Front_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_Attacking3_swordtip.png").convert()
Angel_wood_Front_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_front_Attacking4_swordtip.png").convert()

Angel_wood_Left_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_idle.png").convert()
Angel_wood_Left_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_walking1.png").convert()
Angel_wood_Left_Walking2 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_walking2.png").convert()
Angel_wood_Left_Walking3 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_walking3.png").convert()
Angel_wood_Left_Walking4 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_walking4.png").convert()
Angel_wood_Left_Attacking1 = Angel_wood_Left_Idle
Angel_wood_Left_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_Attacking2.png").convert()
Angel_wood_Left_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_Attacking3.png").convert()
Angel_wood_Left_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_Attacking4.png").convert()
Angel_wood_Left_Attacking5 = Angel_wood_Left_Idle
Angel_wood_Left_Attacking1_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_Attacking1_Swordtip.png").convert()
Angel_wood_Left_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_Attacking2_Swordtip.png").convert()
Angel_wood_Left_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_Attacking3_Swordtip.png").convert()
Angel_wood_Left_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_Attacking4_Swordtip.png").convert()
Angel_wood_Left_Attacking5_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_wood_left_Attacking5_Swordtip.png").convert()

Angel_wood_Right_Idle = pygame.transform.flip(
    Angel_wood_Left_Idle, True, False)
Angel_wood_Right_Walking1 = pygame.transform.flip(
    Angel_wood_Left_Walking1, True, False)
Angel_wood_Right_Walking2 = pygame.transform.flip(
    Angel_wood_Left_Walking2, True, False)
Angel_wood_Right_Walking3 = pygame.transform.flip(
    Angel_wood_Left_Walking3, True, False)
Angel_wood_Right_Walking4 = pygame.transform.flip(
    Angel_wood_Left_Walking4, True, False)
Angel_wood_Right_Attacking1 = pygame.transform.flip(
    Angel_wood_Left_Attacking1, True, False)
Angel_wood_Right_Attacking2 = pygame.transform.flip(
    Angel_wood_Left_Attacking2, True, False)
Angel_wood_Right_Attacking3 = pygame.transform.flip(
    Angel_wood_Left_Attacking3, True, False)
Angel_wood_Right_Attacking4 = pygame.transform.flip(
    Angel_wood_Left_Attacking4, True, False)
Angel_wood_Right_Attacking5 = pygame.transform.flip(
    Angel_wood_Left_Attacking5, True, False)
Angel_wood_Right_Attacking1_Swordtip = pygame.transform.flip(
    Angel_wood_Left_Attacking1_Swordtip, True, False)
Angel_wood_Right_Attacking2_Swordtip = pygame.transform.flip(
    Angel_wood_Left_Attacking2_Swordtip, True, False)
Angel_wood_Right_Attacking3_Swordtip = pygame.transform.flip(
    Angel_wood_Left_Attacking3_Swordtip, True, False)
Angel_wood_Right_Attacking4_Swordtip = pygame.transform.flip(
    Angel_wood_Left_Attacking4_Swordtip, True, False)
Angel_wood_Right_Attacking5_Swordtip = pygame.transform.flip(
    Angel_wood_Left_Attacking5_Swordtip, True, False)

Angel_wood_Get_Item = pygame.image.load(
    "Genesis_Sprites/Angel_wood_get_item.png").convert()


# Steel Armor and sword
Angel_Steel_Back_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_steel_back_idle.png").convert()
Angel_Steel_Back_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_back_walking1.png").convert()
Angel_Steel_Back_Walking2 = Angel_Steel_Back_Idle
Angel_Steel_Back_Walking3 = pygame.transform.flip(
    Angel_Steel_Back_Walking1, True, False)
Angel_Steel_Back_Walking4 = Angel_Steel_Back_Idle
Angel_Steel_Back_Attacking1 = Angel_Steel_Back_Idle
Angel_Steel_Back_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_back_Attacking2.png").convert()
Angel_Steel_Back_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_back_Attacking3.png").convert()
Angel_Steel_Back_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_back_Attacking4.png").convert()
Angel_Steel_Back_Attacking5 = Angel_Steel_Back_Idle
Angel_Steel_Back_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_back_Attacking2_swordtip.png").convert()
Angel_Steel_Back_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_back_Attacking3_swordtip.png").convert()
Angel_Steel_Back_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_back_Attacking4_swordtip.png").convert()

Angel_Steel_Front_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_idle.png").convert()
Angel_Steel_Front_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_walking1.png").convert()
Angel_Steel_Front_Walking2 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_walking2.png").convert()
Angel_Steel_Front_Walking3 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_walking3.png").convert()
Angel_Steel_Front_Walking4 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_walking4.png").convert()
Angel_Steel_Front_Attacking1 = Angel_Steel_Front_Idle
Angel_Steel_Front_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_Attacking2.png").convert()
Angel_Steel_Front_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_Attacking3.png").convert()
Angel_Steel_Front_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_Attacking4.png").convert()
Angel_Steel_Front_Attacking5 = Angel_Steel_Front_Idle
Angel_Steel_Front_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_Attacking2_swordtip.png").convert()
Angel_Steel_Front_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_Attacking3_swordtip.png").convert()
Angel_Steel_Front_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_front_Attacking4_swordtip.png").convert()

Angel_Steel_Left_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_idle.png").convert()
Angel_Steel_Left_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_walking1.png").convert()
Angel_Steel_Left_Walking2 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_walking2.png").convert()
Angel_Steel_Left_Walking3 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_walking3.png").convert()
Angel_Steel_Left_Walking4 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_walking4.png").convert()
Angel_Steel_Left_Attacking1 = Angel_Steel_Left_Idle
Angel_Steel_Left_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_Attacking2.png").convert()
Angel_Steel_Left_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_Attacking3.png").convert()
Angel_Steel_Left_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_Attacking4.png").convert()
Angel_Steel_Left_Attacking5 = Angel_Steel_Left_Idle
Angel_Steel_Left_Attacking1_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_Attacking1_Swordtip.png").convert()
Angel_Steel_Left_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_Attacking2_Swordtip.png").convert()
Angel_Steel_Left_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_Attacking2_Swordtip.png").convert()
Angel_Steel_Left_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_Attacking4_Swordtip.png").convert()
Angel_Steel_Left_Attacking5_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_steel_left_Attacking5_Swordtip.png").convert()

Angel_Steel_Right_Idle = pygame.transform.flip(
    Angel_Steel_Left_Idle, True, False)
Angel_Steel_Right_Walking1 = pygame.transform.flip(
    Angel_Steel_Left_Walking1, True, False)
Angel_Steel_Right_Walking2 = pygame.transform.flip(
    Angel_Steel_Left_Walking2, True, False)
Angel_Steel_Right_Walking3 = pygame.transform.flip(
    Angel_Steel_Left_Walking3, True, False)
Angel_Steel_Right_Walking4 = pygame.transform.flip(
    Angel_Steel_Left_Walking4, True, False)
Angel_Steel_Right_Attacking1 = pygame.transform.flip(
    Angel_Steel_Left_Attacking1, True, False)
Angel_Steel_Right_Attacking2 = pygame.transform.flip(
    Angel_Steel_Left_Attacking2, True, False)
Angel_Steel_Right_Attacking3 = pygame.transform.flip(
    Angel_Steel_Left_Attacking3, True, False)
Angel_Steel_Right_Attacking4 = pygame.transform.flip(
    Angel_Steel_Left_Attacking4, True, False)
Angel_Steel_Right_Attacking5 = pygame.transform.flip(
    Angel_Steel_Left_Attacking5, True, False)
Angel_Steel_Right_Attacking1_Swordtip = pygame.transform.flip(
    Angel_Steel_Left_Attacking1_Swordtip, True, False)
Angel_Steel_Right_Attacking2_Swordtip = pygame.transform.flip(
    Angel_Steel_Left_Attacking2_Swordtip, True, False)
Angel_Steel_Right_Attacking3_Swordtip = pygame.transform.flip(
    Angel_Steel_Left_Attacking3_Swordtip, True, False)
Angel_Steel_Right_Attacking4_Swordtip = pygame.transform.flip(
    Angel_Steel_Left_Attacking4_Swordtip, True, False)
Angel_Steel_Right_Attacking5_Swordtip = pygame.transform.flip(
    Angel_Steel_Left_Attacking5_Swordtip, True, False)

Angel_Steel_Get_Item = pygame.image.load(
    "Genesis_Sprites/Angel_Steel_get_item.png").convert()

# Golden Armor and sword
Angel_Gold_Back_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_back_idle.png").convert()
Angel_Gold_Back_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_back_walking1.png").convert()
Angel_Gold_Back_Walking2 = Angel_Gold_Back_Idle
Angel_Gold_Back_Walking3 = pygame.transform.flip(
    Angel_Gold_Back_Walking1, True, False)
Angel_Gold_Back_Walking4 = Angel_Gold_Back_Idle
Angel_Gold_Back_Attacking1 = Angel_Gold_Back_Idle
Angel_Gold_Back_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_back_Attacking2.png").convert()
Angel_Gold_Back_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_back_Attacking3.png").convert()
Angel_Gold_Back_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_back_Attacking4.png").convert()
Angel_Gold_Back_Attacking5 = Angel_Gold_Back_Idle
Angel_Gold_Back_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_back_Attacking2_swordtip.png").convert()
Angel_Gold_Back_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_back_Attacking3_swordtip.png").convert()
Angel_Gold_Back_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_back_Attacking4_swordtip.png").convert()

Angel_Gold_Front_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_idle.png").convert()
Angel_Gold_Front_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_walking1.png").convert()
Angel_Gold_Front_Walking2 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_walking2.png").convert()
Angel_Gold_Front_Walking3 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_walking3.png").convert()
Angel_Gold_Front_Walking4 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_walking4.png").convert()
Angel_Gold_Front_Attacking1 = Angel_Gold_Front_Idle
Angel_Gold_Front_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_Attacking2.png").convert()
Angel_Gold_Front_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_Attacking3.png").convert()
Angel_Gold_Front_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_Attacking4.png").convert()
Angel_Gold_Front_Attacking5 = Angel_Gold_Front_Idle
Angel_Gold_Front_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_Attacking2_swordtip.png").convert()
Angel_Gold_Front_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_Attacking3_swordtip.png").convert()
Angel_Gold_Front_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_front_Attacking4_swordtip.png").convert()

Angel_Gold_Left_Idle = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_idle.png").convert()
Angel_Gold_Left_Walking1 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_walking1.png").convert()
Angel_Gold_Left_Walking2 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_walking2.png").convert()
Angel_Gold_Left_Walking3 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_walking3.png").convert()
Angel_Gold_Left_Walking4 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_walking4.png").convert()
Angel_Gold_Left_Attacking1 = Angel_Gold_Left_Idle
Angel_Gold_Left_Attacking2 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_Attacking2.png").convert()
Angel_Gold_Left_Attacking3 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_Attacking3.png").convert()
Angel_Gold_Left_Attacking4 = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_Attacking4.png").convert()
Angel_Gold_Left_Attacking5 = Angel_Gold_Left_Idle
Angel_Gold_Left_Attacking1_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_Attacking1_Swordtip.png").convert()
Angel_Gold_Left_Attacking2_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_Attacking2_Swordtip.png").convert()
Angel_Gold_Left_Attacking3_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_Attacking3_Swordtip.png").convert()
Angel_Gold_Left_Attacking4_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_Attacking4_Swordtip.png").convert()
Angel_Gold_Left_Attacking5_Swordtip = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_left_Attacking5_Swordtip.png").convert()

Angel_Gold_Right_Idle = pygame.transform.flip(
    Angel_Gold_Left_Idle, True, False)
Angel_Gold_Right_Walking1 = pygame.transform.flip(
    Angel_Gold_Left_Walking1, True, False)
Angel_Gold_Right_Walking2 = pygame.transform.flip(
    Angel_Gold_Left_Walking2, True, False)
Angel_Gold_Right_Walking3 = pygame.transform.flip(
    Angel_Gold_Left_Walking3, True, False)
Angel_Gold_Right_Walking4 = pygame.transform.flip(
    Angel_Gold_Left_Walking4, True, False)
Angel_Gold_Right_Attacking1 = pygame.transform.flip(
    Angel_Gold_Left_Attacking1, True, False)
Angel_Gold_Right_Attacking2 = pygame.transform.flip(
    Angel_Gold_Left_Attacking2, True, False)
Angel_Gold_Right_Attacking3 = pygame.transform.flip(
    Angel_Gold_Left_Attacking3, True, False)
Angel_Gold_Right_Attacking4 = pygame.transform.flip(
    Angel_Gold_Left_Attacking4, True, False)
Angel_Gold_Right_Attacking5 = pygame.transform.flip(
    Angel_Gold_Left_Attacking5, True, False)
Angel_Gold_Right_Attacking1_Swordtip = pygame.transform.flip(
    Angel_Gold_Left_Attacking1_Swordtip, True, False)
Angel_Gold_Right_Attacking2_Swordtip = pygame.transform.flip(
    Angel_Gold_Left_Attacking2_Swordtip, True, False)
Angel_Gold_Right_Attacking3_Swordtip = pygame.transform.flip(
    Angel_Gold_Left_Attacking3_Swordtip, True, False)
Angel_Gold_Right_Attacking4_Swordtip = pygame.transform.flip(
    Angel_Gold_Left_Attacking4_Swordtip, True, False)
Angel_Gold_Right_Attacking5_Swordtip = pygame.transform.flip(
    Angel_Gold_Left_Attacking5_Swordtip, True, False)
Angel_Gold_Get_Item = pygame.image.load(
    "Genesis_Sprites/Angel_Gold_get_item.png").convert()

# Add red versions of player sprites to show
# the player is hurt and invincible
Angel_Left_Hurt = pygame.image.load(
    "Genesis_Sprites/Angel_Left_Hurt.png").convert()
Angel_Right_Hurt = pygame.transform.flip(Angel_Left_Hurt, True, False)
Angel_Front_Hurt = pygame.image.load(
    "Genesis_Sprites/Angel_Front_Hurt.png").convert()
Angel_Back_Hurt = pygame.image.load(
    "Genesis_Sprites/Angel_Back_Hurt.png").convert()

# Add global variables to hold String constants used
# in event processing and player direction
RIGHT = "RIGHT"
DOWN = "DOWN"
LEFT = "LEFT"
UP = "UP"

# WORLD_DATA is a large string that includes
# all the tile data copied from Tiled file.
with open("tileData.txt", "r") as myfile:
    WORLD_DATA = myfile.read()

# Split the WORLD_DATA string and sort it into a 2D array
global tile_Data
tile_Data = WORLD_DATA
tile_Data = tile_Data.split('\n')
tile_Data = [line.split(',') for line in tile_Data]

# This list represents the tile numbers of tiles the player and
# enemies shouldn't be able to walk through.
boundary_tiles = [4, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29,
                  30, 31, 32, 33, 34, 35, 36, 37, 40, 41, 46, 47, 48, 49, 50,
                  51, 52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
                  68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 82, 83, 84,
                  85, 86, 87, 88, 89, 90, 91, 92, 93, 96, 97, 98, 99, 100,
                  101, 102, 103, 104, 105, 106, 107, 108, 110, 111, 112, 113,
                  114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                  126, 127, 128, 129, 130, 137, 138, 140, 141, 142, 143, 144,
                  145, 146, 147, 148, 149, 150, 151, 152, 154, 155, 156, 157,
                  158, 159, 160, 161, 162]

# These lists represent tiles that are able to be interacted with
explodable_tiles = [44, 47, 48, 55, 152, 160]
burnable_tiles = [44]
interactive_tiles = [41, 53, 56, 57, 58, 59, 151, 154, 156, 157, 158, 159]
cuttable_tiles = [44]

# --- Classes ---


class Tile(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    global tile_Data

    def __init__(self, x, y, leftmostTile, topmostTile):
        """ Constructor, create the image of the block. """
        super().__init__()

        # Initialize the tiles size and locations
        self.image = pygame.Surface(
            [25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION])
        self.rect = self.image.get_rect()
        self.y = y
        self.x = x
        self.tilex = (x - leftmostTile) * 25 * WINDOW_MAGNIFICATION
        self.tiley = (y - topmostTile) * 25 * WINDOW_MAGNIFICATION
        self.rect.x = self.tilex
        self.rect.y = self.tiley

    def getTileNumber(self, x, y):
        """ This function is used to fetch a tileNumber from the tile_Data """
        tileNumber = tile_Data[y][x]
        return tileNumber

    def getTile(self, tileNumber):
        """ This function is used to retrieve the sprite
        surfaces using the tile Number provided. """

        # Just in case, ensure tileNumber is an integer.
        tileNumber = int(tileNumber)

        # Run through each of the cases.
        if(tileNumber == 1):
            return Grass_cut
        elif(tileNumber == 2):
            return Rock_exploded
        elif(tileNumber == 3):
            return Rock_exploded_path
        elif(tileNumber == 4):
            return Chest_Open
        elif(tileNumber == 5):
            return Clocktower_door_open
        elif(tileNumber == 16):
            return Cliff_bottom_bottom
        elif(tileNumber == 17):
            return Cliff_bottom_corner_bottomleft
        elif(tileNumber == 18):
            return Cliff_bottom_corner_bottomright
        elif(tileNumber == 19):
            return Cliff_bottom_corner_topleft
        elif(tileNumber == 20):
            return Cliff_bottom_corner_topright
        elif(tileNumber == 21):
            return Cliff_bottom_left
        elif(tileNumber == 22):
            return Cliff_bottom_right
        elif(tileNumber == 23):
            return Cliff_bottom_top
        elif(tileNumber == 24):
            return Cliff_corner_bottomleft
        elif(tileNumber == 25):
            return Cliff_corner_bottomright
        elif(tileNumber == 26):
            return Cliff_corner_topleft
        elif(tileNumber == 27):
            return Cliff_corner_topright
        elif(tileNumber == 28):
            return Cliff_top
        elif(tileNumber == 29):
            return Cliff_top_corner_bottomleft
        elif(tileNumber == 30):
            return Cliff_top_corner_bottomright
        elif(tileNumber == 31):
            return Cliff_top_corner_topleft
        elif(tileNumber == 32):
            return Cliff_top_corner_topright
        elif(tileNumber == 33):
            return Cliff_top_edge_bottom
        elif(tileNumber == 34):
            return Cliff_top_edge_left
        elif(tileNumber == 35):
            return Cliff_top_edge_right
        elif(tileNumber == 36):
            return Cliff_top_edge_top
        elif(tileNumber == 37):
            return Cliff_wall
        elif(tileNumber == 41):
            return Clocktower_door
        elif(tileNumber == 42):
            return Clocktower_door_open_right
        elif(tileNumber == 43):
            return Grass_cut
        elif(tileNumber == 44):
            return Grass_uncut
        elif(tileNumber == 45):
            return Ground_grass
        elif(tileNumber == 46):
            return Rock_exploded
        elif(tileNumber == 47):
            return Rock_turtle
        elif(tileNumber == 48):
            return Rock_unexploded
        elif(tileNumber == 49):
            return Cliff_bottom_corner_inset_bottomleft
        elif(tileNumber == 50):
            return Cliff_bottom_corner_inset_bottomright
        elif(tileNumber == 51):
            return Cliff_bottom_corner_inset_topleft
        elif(tileNumber == 52):
            return Cliff_bottom_corner_inset_topright
        elif(tileNumber == 53):
            return Signpost
        elif(tileNumber == 54):
            return gray_ground_path
        elif(tileNumber == 55):
            return Rock_unexploded_path
        elif(tileNumber == 56):
            return Signpost_path
        elif(tileNumber == 57):
            return Chest_Closed
        elif(tileNumber == 58):
            return Merchant
        elif(tileNumber == 59):
            return OldMan
        elif(tileNumber == 60):
            return ClockTowerFace1
        elif(tileNumber == 61):
            return ClockTowerFace2
        elif(tileNumber == 62):
            return ClockTowerFace3
        elif(tileNumber == 63):
            return ClockTowerFace4
        elif(tileNumber == 64):
            return ClockTowerFace5
        elif(tileNumber == 65):
            return ClockTowerFace6
        elif(tileNumber == 66):
            return ClockTowerFace7
        elif(tileNumber == 67):
            return ClockTowerFace8
        elif(tileNumber == 68):
            return ClockTowerFace9
        elif(tileNumber == 69):
            return ClockTowerFace10
        elif(tileNumber == 70):
            return ClockTowerFace11
        elif(tileNumber == 71):
            return ClockTowerFace12
        elif(tileNumber == 72):
            return ClockTowerFace13
        elif(tileNumber == 73):
            return ClockTowerFace14
        elif(tileNumber == 74):
            return ClockTowerFace15
        elif(tileNumber == 75):
            return ClockTowerFace16
        elif(tileNumber == 76):
            return ClockTowerFace17
        elif(tileNumber == 77):
            return ClockTowerFace18
        elif(tileNumber == 78):
            return ClockTowerFace19
        elif(tileNumber == 79):
            return ClockTowerFace20
        elif(tileNumber == 80):
            return ClockTowerFace21
        elif(tileNumber == 81):
            return ClockTowerFace22
        elif(tileNumber == 82):
            return ClockTowerFace23
        elif(tileNumber == 83):
            return ClockTowerFace24
        elif(tileNumber == 84):
            return ClockTowerFace25
        elif(tileNumber == 85):
            return ClockTowerFace26
        elif(tileNumber == 86):
            return ClockTowerFace27
        elif(tileNumber == 87):
            return ClockTowerFace28
        elif(tileNumber == 88):
            return ClockTowerFace29
        elif(tileNumber == 89):
            return ClockTowerFace30
        elif(tileNumber == 90):
            return ClockTowerFace31
        elif(tileNumber == 91):
            return ClockTowerFace32
        elif(tileNumber == 92):
            return ClockTowerFace33
        elif(tileNumber == 93):
            return ClockTowerFace34
        elif(tileNumber == 94):
            return ClockTowerFace35
        elif(tileNumber == 95):
            return ClockTowerFace36
        elif(tileNumber == 96):
            return ClockTowerFace37
        elif(tileNumber == 97):
            return ClockTowerFace38
        elif(tileNumber == 98):
            return ClockTowerFace39
        elif(tileNumber == 99):
            return ClockTowerFace40
        elif(tileNumber == 100):
            return ClockTowerFace41
        elif(tileNumber == 101):
            return ClockTowerFace42
        elif(tileNumber == 102):
            return ClockTowerFace43
        elif(tileNumber == 103):
            return ClockTowerFace44
        elif(tileNumber == 104):
            return ClockTowerFace45
        elif(tileNumber == 105):
            return ClockTowerFace46
        elif(tileNumber == 106):
            return ClockTowerFace47
        elif(tileNumber == 107):
            return ClockTowerFace48
        elif(tileNumber == 108):
            return ClockTowerFace49
        elif(tileNumber == 109):
            return ClockTowerFace50
        elif(tileNumber == 110):
            return ClockTowerFace51
        elif(tileNumber == 111):
            return ClockTowerFace52
        elif(tileNumber == 112):
            return ClockTowerFace53
        elif(tileNumber == 113):
            return ClockTowerFace54
        elif(tileNumber == 114):
            return ClockTowerFace55
        elif(tileNumber == 115):
            return ClockTowerFace56
        elif(tileNumber == 116):
            return ClockTowerFace57
        elif(tileNumber == 117):
            return ClockTowerFace58
        elif(tileNumber == 118):
            return ClockTowerFace59
        elif(tileNumber == 119):
            return ClockTowerFace60
        elif(tileNumber == 120):
            return ClockTowerFace61
        elif(tileNumber == 121):
            return ClockTowerFace62
        elif(tileNumber == 122):
            return ClockTowerFace63
        elif(tileNumber == 123):
            return ClockTowerFace65
        elif(tileNumber == 124):
            return ClockTowerFace66
        elif(tileNumber == 125):
            return ClockTowerFace67
        elif(tileNumber == 126):
            return ClockTowerFace68
        elif(tileNumber == 127):
            return ClockTowerFace69
        elif(tileNumber == 128):
            return ClockTowerFace70
        elif(tileNumber == 129):
            return ClockTowerFace71
        elif(tileNumber == 130):
            return ClockTowerFace72
        elif(tileNumber == 131):
            return ClockTowerFace73
        elif(tileNumber == 132):
            return FloorTile
        elif(tileNumber == 134):
            return BlackFloorTile
        elif(tileNumber == 135):
            return WhiteFloorTile
        elif(tileNumber == 136):
            return GrayFloorTile
        elif(tileNumber == 137):
            return Obstacle
        elif(tileNumber == 138):
            return LeftBrick
        elif(tileNumber == 140):
            return BottomBrick
        elif(tileNumber == 141):
            return TopBrick
        elif(tileNumber == 142):
            return BottomRightBrick
        elif(tileNumber == 143):
            return RightBrick
        elif(tileNumber == 144):
            return TopLeftBrick
        elif(tileNumber == 145):
            return TopRightBrick
        elif(tileNumber == 146):
            return BottomLeftBrick
        elif(tileNumber == 147):
            return BottomLeftCornerBrick
        elif(tileNumber == 148):
            return BottomRightCornerBrick
        elif(tileNumber == 149):
            return TopLeftCornerBrick
        elif(tileNumber == 150):
            return TopRightCornerBrick
        elif(tileNumber == 151):
            return ManaMerchant
        elif(tileNumber == 152):
            return BreakableBrickWall
        elif(tileNumber == 153):
            return BrokenBrickWall
        elif(tileNumber == 154):
            return Chest_Closed_tile
        elif(tileNumber == 155):
            return Chest_Open_tile
        elif(tileNumber == 156):
            return Signpost_Tile
        elif(tileNumber == 157):
            return HourglassDoor
        elif(tileNumber == 158):
            return SkullDoor
        elif(tileNumber == 159):
            return RobotNPC
        elif(tileNumber == 160):
            return BreakableBrickWallDown
        elif(tileNumber == 161):
            return GrayFloorTile
        else:
            return Blank


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
            [11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION])
        self.currentSpellSprite.image = Blank
        self.currentSpellSprite.image.set_colorkey(COLORKEY)
        self.currentSpellSpritex = WINDOW_WIDTH - 23 * WINDOW_MAGNIFICATION
        self.currentSpellSpritey = 10 * WINDOW_MAGNIFICATION
        self.currentSpellSprite = pygame.transform.scale(
            self.currentSpellSprite.image,
            (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentSpellSprite,
                    (self.currentSpellSpritex, self.currentSpellSpritey))

        # Initialize the SwordTip Sprites Location
        self.swordx = 5000
        self.swordy = 5000

        # Initialize the sword sprite for attacking
        self.currentSwordSprite = pygame.sprite.Sprite()
        self.currentSwordSprite.image = pygame.Surface(
            [16 * WINDOW_MAGNIFICATION, 9 * WINDOW_MAGNIFICATION])
        self.currentSwordSprite.image = Blank
        self.currentSwordSprite.image.set_colorkey(COLORKEY)
        self.currentSwordSpritex = 0
        self.currentSwordSpritey = 0
        self.currentSwordSprite = pygame.transform.scale(
            self.currentSwordSprite.image,
            (16 * WINDOW_MAGNIFICATION, 9 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentSwordSprite,
                    (self.currentSwordSpritex, self.currentSwordSpritey))

        # Initialize the Interact Sprites Location
        self.interactx = 5000
        self.interacty = 5000

        # Initialize the interact sprite for interacting
        self.currentInteractSprite = pygame.sprite.Sprite()
        self.currentInteractSprite.image = pygame.Surface(
            [16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION])
        self.currentInteractSprite.image = Blank
        self.currentInteractSprite.image.set_colorkey(COLORKEY)
        self.currentInteractSpritex = 0
        self.currentInteractSpritey = 0
        self.currentInteractSprite = pygame.transform.scale(
            self.currentInteractSprite.image,
            (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentInteractSprite,
                    (self.currentInteractSpritex, self.currentInteractSpritey))

        # This sets the image to be the Angel surface defined above.
        self.image = pygame.Surface(
            [16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION])
        self.rect = self.image.get_rect()
        self.image = Angel_wood_Front_Idle
        self.image.set_colorkey(COLORKEY)

        # Set the players starting position to center screen
        # NOTE: The player's x position is not centered at WINDOW_HEIGHT//2
        self.x = WINDOW_WIDTH // 2 - 36
        self.y = WINDOW_HEIGHT // 2
        self.rect.x = self.x
        self.rect.y = self.y - 10 * WINDOW_MAGNIFICATION

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
        self.worldx = WORLD_WIDTH // 2
        self.worldy = (WORLD_HEIGHT * 5) // 6

        # Scale the image by the window magnification
        self.image = pygame.transform.scale(
            self.image, (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))

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
        self.dialogCoords = [120, WINDOW_HEIGHT - 50]
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
            self.image, (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
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
                (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
            screen.blit(self.currentSpellSprite, (self.spellx, self.spelly))
        else:
            # Once time is up, move the sprite far
            # away where it can't collide anymore
            self.spellx = 5000
            self.spelly = 5000

        # Change the dimensions of the swordtip
        # sprite depending on the attack directions.
        if self.direction == "RIGHT" or self.direction == "LEFT":
            magx = 9 * WINDOW_MAGNIFICATION
            magy = 16 * WINDOW_MAGNIFICATION
        else:
            magx = 16 * WINDOW_MAGNIFICATION
            magy = 9 * WINDOW_MAGNIFICATION

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
            self.image, (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
        self.image.set_colorkey(COLORKEY)

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
                self.swordx = self.x + (16 * WINDOW_MAGNIFICATION)
                self.swordy = self.y + 8
        elif self.direction == "LEFT":
            self.swordx = self.x - (9 * WINDOW_MAGNIFICATION)
            self.swordy = self.y + 8
        elif self.direction == "UP":
            self.swordx = self.x
            self.swordy = self.y - (9 * WINDOW_MAGNIFICATION)
        elif self.direction == "DOWN":
            self.swordx = self.x + 2
            self.swordy = self.y + (21 * WINDOW_MAGNIFICATION)

        # Rescale the image and set the background to be translucent
        self.image = pygame.transform.scale(
            self.image, (9 * WINDOW_MAGNIFICATION, 16 * WINDOW_MAGNIFICATION))
        self.image.set_colorkey(COLORKEY)
        self.currentSwordSprite.set_colorkey(COLORKEY)

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
            (11 * WINDOW_MAGNIFICATION + 1, 15 * WINDOW_MAGNIFICATION + 1))
        self.currentSpellSprite.set_colorkey(COLORKEY)

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
            [16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION])
        self.rect = self.image.get_rect()
        self.image = Blank
        self.image.set_colorkey(COLORKEY)

        # Initialize x and y based on direction player is facing.
        if(self.direction == "UP"):
            self.interactx = self.x
            self.interacty = self.y - 21 * WINDOW_MAGNIFICATION
        elif(self.direction == "DOWN"):
            self.interactx = self.x
            self.interacty = self.y + 21 * WINDOW_MAGNIFICATION
        elif(self.direction == "RIGHT"):
            self.interactx = self.x + 16 * WINDOW_MAGNIFICATION
            self.interacty = self.y
        elif(self.direction == "LEFT"):
            self.interactx = self.x - 16 * WINDOW_MAGNIFICATION
            self.interacty = self.y

        # Reset the timer
        self.interactTimer = 0


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
            [121 * (WINDOW_MAGNIFICATION + 1),
             84 * (WINDOW_MAGNIFICATION + 1)])
        self.rect = self.image.get_rect()
        self.image = Spider_Legless
        self.image.set_colorkey(COLORKEY)

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
            [88 * WINDOW_MAGNIFICATION, 44 * WINDOW_MAGNIFICATION])
        self.leftArm.image = LeftSpiderScythe
        self.leftArm.rect = self.leftArm.image.get_rect()
        self.leftArm.rect.center = self.leftArm.rect.bottomleft
        self.leftArm.image.set_colorkey(COLORKEY)
        self.leftArmx = self.x + 15
        self.leftArmy = self.y + 145
        self.leftArmRect = self.leftArm.rect
        self.leftArmRectx = 0
        self.leftArmRecty = 0

        # Instantiate all variables related to Patience's left Arm
        self.rightArm = pygame.sprite.Sprite()
        self.rightArm.image = pygame.Surface(
            [88 * WINDOW_MAGNIFICATION, 44 * WINDOW_MAGNIFICATION])
        self.rightArm.image = RightSpiderScythe
        self.rightArm.rect = self.rightArm.image.get_rect()
        self.rightArm.rect.center = self.rightArm.rect.bottomleft
        self.rightArm.image.set_colorkey(COLORKEY)
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
                    121 * (WINDOW_MAGNIFICATION + 1), 84 * (
                        WINDOW_MAGNIFICATION + 1)))
        screen.blit(patience, [self.x, self.y])

        # If the boss is attacking update the right Arm,
        # otherwise draw it in place
        if(self.attacking != "right"):
            rightArm = pygame.transform.scale(
                self.rightArm.image, (88 * (
                    WINDOW_MAGNIFICATION + 1), 44 * (
                        WINDOW_MAGNIFICATION + 1)))
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
                    88 * (WINDOW_MAGNIFICATION + 1), 44 * (
                        WINDOW_MAGNIFICATION + 1)))
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
                    88 * (WINDOW_MAGNIFICATION + 1), 44 * (
                        WINDOW_MAGNIFICATION + 1)))
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
                self.leftArm.image, (88 * (WINDOW_MAGNIFICATION + 1), 44 * (
                    WINDOW_MAGNIFICATION + 1)))
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
                    88 * (WINDOW_MAGNIFICATION + 1), 44 * (
                        WINDOW_MAGNIFICATION + 1)))
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
                self.leftArm.image, (88 * (WINDOW_MAGNIFICATION + 1), 44 * (
                    WINDOW_MAGNIFICATION + 1)))
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
            [13 * WINDOW_MAGNIFICATION * self.size,
             20 * WINDOW_MAGNIFICATION * self.size])
        self.rect = self.image.get_rect()
        self.image = Snake_Forward_1
        self.image.set_colorkey(COLORKEY)

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
        self.playerx2 = player.x + (16 * WINDOW_MAGNIFICATION * self.size)
        self.playery2 = player.y + (21 * WINDOW_MAGNIFICATION * self.size)

    def draw(self, screen):
        """ Draw the sprites in their new positions """
        Enemy = pygame.transform.scale(
            self.image, (25 * WINDOW_MAGNIFICATION * self.size,
                         25 * WINDOW_MAGNIFICATION * self.size))
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
                self.image, (23 * WINDOW_MAGNIFICATION * self.size,
                             19 * WINDOW_MAGNIFICATION * self.size))
        elif(self.direction == "UP"):
            self.image = pygame.transform.scale(
                self.image, (9 * WINDOW_MAGNIFICATION * self.size,
                             24 * WINDOW_MAGNIFICATION * self.size))
        else:
            self.image = pygame.transform.scale(
                self.image, (13 * WINDOW_MAGNIFICATION * self.size,
                             20 * WINDOW_MAGNIFICATION * self.size))
        self.image.set_colorkey(COLORKEY)

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
                self.image, (23 * WINDOW_MAGNIFICATION * self.size,
                             19 * WINDOW_MAGNIFICATION * self.size))
        elif(self.sector == "UP" or self.sector == "UP RIGHT" or
             self.sector == "UP LEFT"):
            self.image = pygame.transform.scale(
                self.image, (9 * WINDOW_MAGNIFICATION * self.size,
                             24 * WINDOW_MAGNIFICATION * self.size))
        else:
            self.image = pygame.transform.scale(
                self.image, (13 * WINDOW_MAGNIFICATION * self.size,
                             20 * WINDOW_MAGNIFICATION * self.size))
        self.image.set_colorkey(COLORKEY)

        # Reset the clock
        self.elapsed = 0


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
            [15 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION])
        self.coin_Image.image = Coin
        self.coin_Image.image.set_colorkey(COLORKEY)
        self.coin_Imagex = 10
        self.coin_Imagey = WINDOW_HEIGHT - 40
        self.coin_Image = pygame.transform.scale(
            self.coin_Image.image,
            (15 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.coin_Image, (self.coin_Imagex, self.coin_Imagey))

        # Initialize the amount of money the player has
        money = str(self.money)
        money = "X " + money
        self.moneyText = self.font.render(money, True, WHITE)
        screen.blit(self.moneyText,
                    (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 150))

        # Initialize and draw the frame used for displaying the current potion
        self.potion_Frame = pygame.sprite.Sprite()
        self.potion_Frame.image = pygame.Surface(
            [15 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION])
        self.potion_Frame.image = Potion_Frame
        self.potion_Frame.image.set_colorkey(COLORKEY)
        self.potion_Framex = WINDOW_WIDTH - 100
        self.potion_Framey = 10
        self.potion_Frame = pygame.transform.scale(
            self.potion_Frame.image,
            (15 * (WINDOW_MAGNIFICATION + 1), 15 * (WINDOW_MAGNIFICATION + 1)))
        screen.blit(self.potion_Frame,
                    (self.potion_Framex, self.potion_Framey))

        # Initialize and draw the frame used for displaying the current spell
        self.spell_Frame = pygame.sprite.Sprite()
        self.spell_Frame.image = pygame.Surface(
            [11 * WINDOW_MAGNIFICATION, 19 * WINDOW_MAGNIFICATION])
        self.spell_Frame.image = Spell_Frame
        self.spell_Frame.image.set_colorkey(COLORKEY)
        self.spell_Framex = WINDOW_WIDTH - 25 * WINDOW_MAGNIFICATION
        self.spell_Framey = 2 * WINDOW_MAGNIFICATION
        self.spell_Frame = pygame.transform.scale(
            self.spell_Frame.image,
            (11 * (WINDOW_MAGNIFICATION + 1), 19 * (WINDOW_MAGNIFICATION + 1)))
        screen.blit(self.spell_Frame, (self.spell_Framex, self.spell_Framey))

        # Initialize and draw the spell Sprite
        # used for displaying the current spell
        self.currentSpellSprite = pygame.sprite.Sprite()
        self.currentSpellSprite.image = pygame.Surface(
            [11 * WINDOW_MAGNIFICATION, 19 * WINDOW_MAGNIFICATION])
        self.currentSpellSprite.image = Blank
        self.currentSpellSprite.image.set_colorkey(COLORKEY)
        self.currentSpellSpritex = WINDOW_WIDTH - 23 * WINDOW_MAGNIFICATION
        self.currentSpellSpritey = 10 * WINDOW_MAGNIFICATION
        self.currentSpellSprite = pygame.transform.scale(
            self.currentSpellSprite.image,
            (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentSpellSprite,
                    (self.currentSpellSpritex, self.currentSpellSpritey))

        # Initialize and draw the potion Sprite
        # used for displaying the current potion
        self.currentPotionSprite = pygame.sprite.Sprite()
        self.currentPotionSprite.image = pygame.Surface(
            [11 * WINDOW_MAGNIFICATION, 19 * WINDOW_MAGNIFICATION])
        self.currentPotionSprite.image = Blank
        self.currentPotionSprite.image.set_colorkey(COLORKEY)
        self.currentPotionSpritex = WINDOW_WIDTH - 90
        self.currentPotionSpritey = 20
        self.currentPotionSprite = pygame.transform.scale(
            self.currentPotionSprite.image,
            (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentPotionSprite,
                    (self.currentPotionSpritex, self.currentPotionSpritey))

        # These 2 lines update the display frames for spells and potions.
        self.switchPotionRight(player)
        self.switchSpellLeft(player)

        # Initialize the quest feedback for displaying quest progress
        self.currentQuestSprite = pygame.sprite.Sprite()
        self.currentQuestSprite.image = pygame.Surface(
            [25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION])
        self.currentQuestSprite.image = Blank
        self.currentQuestSprite.image.set_colorkey(COLORKEY)
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
        self.moneyText = self.font.render(money, True, WHITE)

        # Initialize the text used to display how many potions the player has.
        potionAmount = str(self.potion_Number)
        potionText = self.font2.render(potionAmount, True, WHITE)

        # Initialize the text used to display how much health the player has.
        healthText = str(self.health) + "/" + str(self.max_Health)
        self.healthText = self.font2.render(healthText, True, BLACK)

        # Initialize the text used to display how much health the boss has.
        bosshealthText = str(self.boss_health) + "/" + str(
            self.boss_max_Health)
        self.bosshealthText = self.font.render(bosshealthText, True, BLACK)
        bossNameText = "Patience"
        self.bossNameText = self.font.render(bossNameText, True, WHITE)

        # Initialize the text used to display how much mana the player has.
        manaText = str(self.mana) + "/" + str(self.max_Mana)
        self.manaText = self.font2.render(manaText, True, BLACK)

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
        self.questText = self.font.render(questText, True, WHITE)

        # Rescale and set the image's background to clear
        self.currentQuestSprite = pygame.transform.scale(
            self.currentQuestSprite,
            (25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION))
        self.currentQuestSprite.set_colorkey(COLORKEY)

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
        pygame.draw.rect(screen, GRAY,
                         [10, 10, self.max_Health * WINDOW_MAGNIFICATION,
                          5 * WINDOW_MAGNIFICATION])
        pygame.draw.rect(screen, RED,
                         [10, 10, self.health * WINDOW_MAGNIFICATION,
                          5 * WINDOW_MAGNIFICATION])
        screen.blit(self.healthText, (self.max_Health - 10, 8))
        pygame.draw.rect(screen, GRAY,
                         [10, 20, self.max_Mana * WINDOW_MAGNIFICATION,
                          5 * WINDOW_MAGNIFICATION])
        pygame.draw.rect(screen, LIGHTBLUE,
                         [10, 20, self.mana * WINDOW_MAGNIFICATION,
                          5 * WINDOW_MAGNIFICATION])
        screen.blit(self.manaText, (self.max_Mana - 10, 18))

        # If the player is in the boss room, display the boss' health bar
        if(self.playerRoom == 28):
            pygame.draw.rect(screen, GRAY,
                             [70, 500, self.boss_max_Health / 3,
                              10 * WINDOW_MAGNIFICATION])
            pygame.draw.rect(screen, RED,
                             [70, 500, self.boss_health / 3,
                              10 * WINDOW_MAGNIFICATION])
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
            (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentPotionSprite.set_colorkey(COLORKEY)

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
            (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentPotionSprite.set_colorkey(COLORKEY)

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
            (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentSpellSprite.set_colorkey(COLORKEY)

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
            (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentSpellSprite.set_colorkey(COLORKEY)


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
                CAMERA_LEFT = ROOM_WIDTH * 2
                CAMERA_TOP = ROOM_HEIGHT * 5

            # If the game is over and the mouse is clicked start a new game
            elif (self.game_won and event.type == pygame.MOUSEBUTTONDOWN):
                NEWGAME = True
                CAMERA_LEFT = ROOM_WIDTH * 2
                CAMERA_TOP = ROOM_HEIGHT * 5

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
                    text1 = font.render("Controls:", True, WHITE)
                    text2 = font.render(
                        "W - Cycle Spell Forward", True, (WHITE))
                    text3 = font.render(
                        "A - Cycle Potion Backward", True, (WHITE))
                    text4 = font.render(
                        "S - Cycle Spell Backward", True, (WHITE))
                    text5 = font.render(
                        "D - Cycle Potion Forward", True, (WHITE))
                    text6 = font.render("Q - Use Spell", True, (WHITE))
                    text7 = font.render("E - Use Potion", True, (WHITE))
                    text8 = font.render("SPACE BAR - Interact", True, (WHITE))
                    text9 = font.render("Arrow Keys - Move", True, (WHITE))
                    text10 = font.render("Right Shift - Attack", True, (WHITE))
                    text11 = font.render("H - View Controls", True, (WHITE))

                    screen.fill(BLACK)
                    screen.blit(text1, (WINDOW_WIDTH//2 - 75, 25))
                    screen.blit(text2, (75, WINDOW_HEIGHT//2 - 150))
                    screen.blit(
                        text3, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150))
                    screen.blit(text4, (75, WINDOW_HEIGHT//2 - 100))
                    screen.blit(
                        text5, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
                    screen.blit(text6, (75, WINDOW_HEIGHT//2 - 50))
                    screen.blit(
                        text7, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
                    screen.blit(text8, (75, WINDOW_HEIGHT//2))
                    screen.blit(text9, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                    screen.blit(text10, (75, WINDOW_HEIGHT//2 + 50))
                    screen.blit(
                        text11, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
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
                self.player.y -= WALKRATE
                self.player.worldy -= WALKRATE
                self.player.swordx = 5000
                self.player.swordy = 5000
                if self.player.worldy < 0:
                    self.player.worldy = 0
                    self.player.worldy += WALKRATE
                elif self.player.y < 0:
                    self.player.y = WINDOW_WIDTH - 300
                    CAMERA_TOP -= ROOM_HEIGHT
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
                self.player.y += WALKRATE
                self.player.worldy += WALKRATE
                self.player.swordx = 5000
                self.player.swordy = 5000
                if self.player.worldy > WORLD_HEIGHT:
                    self.player.worldy = (WORLD_HEIGHT -
                                          25 * WINDOW_MAGNIFICATION)
                elif self.player.y > WINDOW_HEIGHT:
                    self.player.y = 0
                    CAMERA_TOP += ROOM_HEIGHT
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
                self.player.x -= WALKRATE
                self.player.worldx -= WALKRATE
                self.player.swordx = 5000
                self.player.swordy = 5000
                if self.player.x < 0:
                    self.player.x = WINDOW_WIDTH - 25 * WINDOW_MAGNIFICATION
                    CAMERA_LEFT -= ROOM_WIDTH
                    self.player.room += 1
                if self.player.worldx < 0:
                    self.player.worldx = 0
                    self.player.worldx -= WALKRATE

            if self.DIRECTION == "RIGHT":
                self.player.x += WALKRATE
                self.player.worldx += WALKRATE
                self.player.swordx = 5000
                self.player.swordy = 5000
                if self.player.x > WINDOW_WIDTH:
                    self.player.x = 0
                    CAMERA_LEFT += ROOM_WIDTH
                    self.player.room -= 1
                if self.player.worldx + 25 > WORLD_WIDTH:
                    self.player.worldx = WORLD_WIDTH - 25
                    self.player.worldx -= WALKRATE

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
        roomSurf = pygame.Surface((ROOM_WIDTH, ROOM_HEIGHT))

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
                                          (ROOM_WIDTH * WINDOW_MAGNIFICATION,
                                           ROOM_HEIGHT * WINDOW_MAGNIFICATION))
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
                    self.player.y += WALKRATE
                    self.player.worldy += WALKRATE
                elif (self.DIRECTION == "DOWN"):
                    self.player.y -= WALKRATE
                    self.player.worldy -= WALKRATE
                elif (self.DIRECTION == "RIGHT"):
                    self.player.x -= WALKRATE
                    self.player.worldx -= WALKRATE
                elif (self.DIRECTION == "LEFT"):
                    self.player.x += WALKRATE
                    self.player.worldx += WALKRATE
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
                    [9 * WINDOW_MAGNIFICATION, 16 * WINDOW_MAGNIFICATION])
            else:
                swordTipRect.image = pygame.Surface(
                    [16 * WINDOW_MAGNIFICATION, 9 * WINDOW_MAGNIFICATION])
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
                [16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION])
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
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                elif(room == 4):
                    if(coords == (30, 64)):
                        self.player.dialog = ("You found 5 Health Potions " +
                                              "and the Clocktower Key!")
                        self.player.dialogCoords[0] = 175
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
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
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                elif(room == 8):
                    if(coords == (38, 51)):
                        self.player.dialog = (
                            "North - Clocktower, South - Glade")
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                    if(coords == (34, 51)):
                        if(self.talk):
                            if self.merchant_dialog == 0:
                                self.player.dialog = ("Hey there! I'll sell" +
                                                      " you a health potion" +
                                                      " for 10 coins. Just" +
                                                      " talk to me again.")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
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
                                        WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.talk = False
                                else:
                                    self.player.dialog = ("Sorry you dont " +
                                                          "have enough coins!")
                                    self.player.dialogCoords[0] = 250
                                    self.player.dialogCoords[1] = (
                                        WINDOW_HEIGHT - 50)
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
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
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
                                        WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.talk = False
                                else:
                                    self.player.dialog = ("Sorry you dont " +
                                                          "have enough coins!")
                                    self.player.dialogCoords[0] = 250
                                    self.player.dialogCoords[1] = (
                                        WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.talk = False
                elif(room == 9):
                    if(coords == (17, 47)):
                        self.player.dialog = ("Please do not go any" +
                                              " further, danger ahead")
                        self.player.dialogCoords[0] = 200
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                elif(room == 10):
                    if(coords == (7, 47)):
                        self.player.dialog = "PLEASE DONT GO ANY FURTHER"
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                    elif(coords == (6, 50)):
                        self.player.dialog = "I MEAN IT"
                        self.player.dialogCoords[0] = 350
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                    elif(coords == (6, 53)):
                        self.player.dialog = "DONT SAY I DIDNT WARN YOU"
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25

                elif(room == 11):
                    if(coords == (70, 35)):
                        if(self.talk):
                            if self.old_man_dialog == 0:
                                self.player.dialog = (
                                    "Hey! I bet youre here for" +
                                    " the clocktower key right?")
                                self.player.dialogCoords[0] = 150
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 25
                            elif self.old_man_dialog == 1:
                                self.player.dialog = (
                                    "Well, first youll have to" +
                                    " do a couple of favors for me.")
                                self.player.dialogCoords[0] = 175
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                            elif self.old_man_dialog == 2:
                                self.player.dialog = (
                                    "You may have noticed there" +
                                    " are a lot of snakes around here.")
                                self.player.dialogCoords[0] = 150
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                            elif self.old_man_dialog == 3:
                                self.player.dialog = (
                                    "I need you to get rid" +
                                    " of 20 of them for me.")
                                self.player.dialogCoords[0] = 200
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 25
                                self.player.quest = "snake"
                            elif self.old_man_dialog == 4:
                                if(self.player.snakes < 20):
                                    self.player.dialog = (
                                        "Go out there and kill those snakes!")
                                    self.player.dialogCoords[0] = 200
                                    self.player.dialogCoords[1] = (
                                        WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                                    self.old_man_dialog -= 1
                                elif(self.player.snakes >= 20):
                                    self.player.dialog = "Nice Job!"
                                    self.player.quest = ""
                                    self.player.dialogCoords[0] = 350
                                    self.player.dialogCoords[1] = (
                                        WINDOW_HEIGHT - 50)
                                    self.player.fontSize = 25
                            elif self.old_man_dialog == 5:
                                self.player.dialog = (
                                    "Here's the explosion spell, the key" +
                                    " is to the west of the merchant.")
                                self.player.dialogCoords[0] = 150
                                self.player.dialogCoords[1] = (
                                    WINDOW_HEIGHT - 50)
                                self.player.fontSize = 20
                                self.player.inventory[4][1] = 1
                            elif self.old_man_dialog == 6:
                                self.player.dialog = (
                                    "But I have another offer for you!")
                                self.player.dialogCoords[0] = 250
                                self.player.dialogCoords[1] = (
                                    WINDOW_HEIGHT - 50)
                                self.player.fontSize = 25
                            elif self.old_man_dialog == 7:
                                self.player.dialog = (
                                    "You may have noticed some strange" +
                                    " rocks here or there.")
                                self.player.dialogCoords[0] = 175
                                self.player.dialogCoords[1] = (
                                    WINDOW_HEIGHT - 50)
                                self.player.fontSize = 20
                            elif self.old_man_dialog == 8:
                                self.player.dialog = (
                                    "I need you to get rid of all 13 of" +
                                    " them for me using the spell I gave you.")
                                self.player.dialogCoords[0] = 150
                                self.player.dialogCoords[1] = (
                                    WINDOW_HEIGHT - 50)
                                self.player.fontSize = 16
                                self.player.quest = "rock"
                            elif self.old_man_dialog == 9:
                                self.player.dialog = (
                                    "There's some shiny new armor" +
                                    " in it for you!")
                                self.player.dialogCoords[0] = 175
                                self.player.dialogCoords[1] = (
                                    WINDOW_HEIGHT - 50)
                                self.player.fontSize = 25
                            elif self.old_man_dialog == 10:
                                if(self.player.rockMimics < 13):
                                    self.player.dialog = (
                                        "Go out there and kill those mimics!")
                                    self.player.dialogCoords[0] = 200
                                    self.player.dialogCoords[1] = (
                                        WINDOW_HEIGHT - 50)
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
                                        WINDOW_HEIGHT - 50)
                                    self.player.quest = ""
                            elif self.old_man_dialog == 11:
                                self.player.dialog = (
                                    "Now i can sleep " +
                                    "soundly with my eyes open!")
                                self.player.dialogCoords[0] = 200
                                self.player.dialogCoords[1] = (
                                    WINDOW_HEIGHT - 50)
                                self.player.fontSize = 25
                            else:
                                self.player.dialog = "Zzz"
                                self.player.dialogCoords[0] = 400
                                self.player.dialogCoords[1] = (
                                    WINDOW_HEIGHT - 50)
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
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                    elif(coords == (40, 37) or coords == (39, 37)):
                        if(self.player.inventory[5][1] >= 1):
                            tile_Data[37][40] = "42"
                            tile_Data[37][39] = "5"
                            self.player.dialog = "Door Opened"
                            self.player.dialogCoords[0] = 250
                            self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                            self.player.fontSize = 25
                        else:
                            self.player.dialog = "Door is locked"
                            self.player.dialogCoords[0] = 250
                            self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                            self.player.fontSize = 25
                elif(room == 15):
                    if(coords == (6, 34)):
                        self.player.dialog = (
                            "REMINDER: Use A and D to switch between" +
                            " potions and E to use them")
                        self.player.dialogCoords[0] = 150
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                    elif(coords == (7, 34)):
                        self.player.dialog = (
                            "You found Health and Mana Potions!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[9][1] += 5
                        self.player.inventory[8][1] += 3
                        self.player.inventory[7][1] += 5
                        tile_Data[34][7] = 4
                    elif(coords == (8, 34)):
                        self.player.dialog = "You found the Fireball Spell!"
                        self.player.dialogCoords[0] = 250
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[3][1] += 1
                        tile_Data[34][8] = 4
                    elif(coords == (9, 34)):
                        self.player.dialog = (
                            "REMINDER: Use W and S to switch between" +
                            " spells and Q to use them")
                        self.player.dialogCoords[0] = 150
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                elif(room == 18):
                    if(self.talk):
                            if self.robot_dialog == 0:
                                self.player.dialog = ("zzrt HELLO ANGEL")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                                self.talk = False
                                self.robot_dialog += 1
                            elif self.robot_dialog == 1:
                                self.player.dialog = ("I COULD USE YOUR HELP" +
                                                      " FINDING MY GEAR")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
                                                               50)
                                self.player.fontSize = 20
                                self.talk = False
                                self.robot_dialog += 1
                            elif self.robot_dialog == 2:
                                self.player.dialog = ("IF YOU FIND IT ILL " +
                                                      "GIVE YOU ARMOR")
                                self.player.dialogCoords[0] = 100
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
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
                                        WINDOW_HEIGHT - 50)
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
                                self.player.dialogCoords[1] = (WINDOW_HEIGHT -
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
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 20
                    elif(coords == (39, 11) or coords == (40, 11)):
                        if(self.player.inventory[10][1] == 1):
                            tile_Data[11][40] = 132
                            tile_Data[11][39] = 132
                            self.player.dialog = "Door Opened"
                            self.player.dialogCoords[0] = 250
                            self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                            self.player.fontSize = 25
                        else:
                            self.player.dialog = "Door is locked"
                            self.player.dialogCoords[0] = 250
                            self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                            self.player.fontSize = 25
                elif(room == 26):
                    if(coords == (71, 1)):
                        self.player.dialog = ("You found the Boss Key!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[10][1] += 1
                        tile_Data[1][71] = 155
                elif(room == 27):
                    if(coords == (54, 1)):
                        self.player.dialog = (
                            "You found 50 coins!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.money += 50
                        tile_Data[1][54] = 155
                    elif(coords == (57, 1)):
                        self.player.dialog = (
                            "You found Health and Mana Potions!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
                        self.player.fontSize = 25
                        self.player.inventory[8][1] += 3
                        self.player.inventory[6][1] += 3
                        tile_Data[1][57] = 155
                elif(room == 29):
                    if(coords == (23, 1)):
                        self.player.dialog = (
                            "You found a gear!")
                        self.player.dialogCoords[0] = 225
                        self.player.dialogCoords[1] = WINDOW_HEIGHT - 50
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
                    itemDrop.image.set_colorkey(COLORKEY)
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
                [11 * WINDOW_MAGNIFICATION, 16 * WINDOW_MAGNIFICATION])
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
               (self.player.y < (225 * WINDOW_MAGNIFICATION))):
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

        # Clear the screen to White
        screen.fill(WHITE)

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
                    [350 * WINDOW_MAGNIFICATION, 225 * WINDOW_MAGNIFICATION])
                darkness.image = DarkRoom
                darkness.image.set_colorkey(COLORKEY)
                darknessx = 25 * WINDOW_MAGNIFICATION
                darknessy = 25 * WINDOW_MAGNIFICATION
                darkness = pygame.transform.scale(
                    darkness.image,
                    (350 * WINDOW_MAGNIFICATION, 225 * WINDOW_MAGNIFICATION))
                screen.blit(darkness,
                            (darknessx, darknessy))
            elif(self.player.room == 20 and self.room20Darkness):
                darkness = pygame.sprite.Sprite()
                darkness.image = pygame.Surface(
                    [350 * WINDOW_MAGNIFICATION, 225 * WINDOW_MAGNIFICATION])
                darkness.image = DarkRoom
                darkness.image.set_colorkey(COLORKEY)
                darknessx = 25 * WINDOW_MAGNIFICATION
                darknessy = 25 * WINDOW_MAGNIFICATION
                darkness = pygame.transform.scale(
                    darkness.image,
                    (350 * WINDOW_MAGNIFICATION, 225 * WINDOW_MAGNIFICATION))
                screen.blit(darkness,
                            (darknessx, darknessy))
            elif(self.player.room == 25 and self.room25Darkness):
                darkness = pygame.sprite.Sprite()
                darkness.image = pygame.Surface(
                    [350 * WINDOW_MAGNIFICATION, 225 * WINDOW_MAGNIFICATION])
                darkness.image = DarkRoom
                darkness.image.set_colorkey(COLORKEY)
                darknessx = 25 * WINDOW_MAGNIFICATION
                darknessy = 25 * WINDOW_MAGNIFICATION
                darkness = pygame.transform.scale(
                    darkness.image,
                    (350 * WINDOW_MAGNIFICATION, 225 * WINDOW_MAGNIFICATION))
                screen.blit(darkness,
                            (darknessx, darknessy))
            elif(self.player.room == 30 and self.room30Darkness):
                darkness = pygame.sprite.Sprite()
                darkness.image = pygame.Surface(
                    [350 * WINDOW_MAGNIFICATION, 225 * WINDOW_MAGNIFICATION])
                darkness.image = DarkRoom
                darkness.image.set_colorkey(COLORKEY)
                darknessx = 25 * WINDOW_MAGNIFICATION
                darknessy = 25 * WINDOW_MAGNIFICATION
                darkness = pygame.transform.scale(
                    darkness.image,
                    (350 * WINDOW_MAGNIFICATION, 225 * WINDOW_MAGNIFICATION))
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
                    itemDrop.image.set_colorkey(COLORKEY)
                    itemDropx = item[2]
                    itemDropy = item[3]
                    itemDrop = pygame.transform.scale(itemDrop.image, (25, 25))
                    screen.blit(itemDrop, (itemDropx, itemDropy))
                    if(item[0] == "nothing"):
                        self.dropped_Items.remove(item)

            # If the player is at the clockTower entrance we render the
            # tunnel leading to the next area.
            if(self.player.room == 13):
                scale = 25 * WINDOW_MAGNIFICATION
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
                        [25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION])
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
            dialog_text = font.render(self.player.dialog, True, WHITE)
            screen.blit(
                dialog_text,
                (self.player.dialogCoords[0], self.player.dialogCoords[1]))

            # Copy back buffer onto the front buffer
            pygame.display.flip()

        # If the game is over display game over screen
        elif(self.game_won):
            font = pygame.font.Font("SILKWONDER.ttf", 50)
            text1 = font.render("YOU WON!", True, WHITE)
            playAgain = font.render("Click to play again", True, WHITE)
            screen.fill(BLACK)
            screen.blit(text1, (WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 150))
            screen.blit(
                playAgain, (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT - 150))
            pygame.display.flip()

        # If the game is over display game over screen
        elif(self.game_over):
            font = pygame.font.Font("SILKWONDER.ttf", 50)
            text1 = font.render("GAME OVER", True, WHITE)
            playAgain = font.render("Click to play again", True, WHITE)
            screen.fill(BLACK)
            screen.blit(text1, (WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 150))
            screen.blit(playAgain,
                        (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT - 150))
            pygame.display.flip()

        # If the game hasn't started yet, display the splash screen
        elif(not self.game_start):

            # Display the Splash screen
            if(self.splashNumber == 1):
                font = pygame.font.Font("SILKWONDER.ttf", 50)
                font2 = pygame.font.Font("SILKWONDER.ttf", 20)
                text1 = font.render("Genesis", True, WHITE)
                text2 = font.render("By Bradley Lamitie", True, (WHITE))
                text3 = font.render("Final Version (12/8/17)", True, (WHITE))
                continueText = font2.render("Click to continue", True, WHITE)

                screen.fill(BLACK)
                screen.blit(text1,
                            (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 150))
                screen.blit(text2,
                            (WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2 - 50))
                screen.blit(text3,
                            (WINDOW_WIDTH//2 - 280, WINDOW_HEIGHT//2 + 50))
                screen.blit(continueText,
                            (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 75))
                pygame.display.flip()

            # Display the Story screen
            elif(self.splashNumber == 2):
                font = pygame.font.Font("SILKWONDER.ttf", 25)
                font2 = pygame.font.Font("SILKWONDER.ttf", 20)
                text1 = font.render(
                    "You play as an angel cast onto Earth", True, WHITE)
                text2 = font.render(
                    "after having your wings stripped from you.",
                    True, (WHITE))
                text3 = font.render(
                    "Your goal is to defeat all 7 virtues on Earth to ",
                    True, (WHITE))
                text4 = font.render(
                    "redeem yourself and earn your place in heaven.",
                    True, (WHITE))
                text5 = font.render("Story:", True, WHITE)
                continueText = font2.render("Click to continue", True, WHITE)

                screen.fill(BLACK)
                screen.blit(text1,
                            (WINDOW_WIDTH//2 - 220, WINDOW_HEIGHT//2 - 170))
                screen.blit(text2,
                            (WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2 - 70))
                screen.blit(text3,
                            (WINDOW_WIDTH//2 - 260, WINDOW_HEIGHT//2 + 30))
                screen.blit(text4,
                            (WINDOW_WIDTH//2 - 275, WINDOW_HEIGHT//2 + 120))
                screen.blit(text5, (WINDOW_WIDTH//2 - 75, 25))
                screen.blit(continueText,
                            (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 75))

                pygame.display.flip()

            # Display the Controls screen
            elif(self.splashNumber == 3):
                font = pygame.font.Font("SILKWONDER.ttf", 25)
                font2 = pygame.font.Font("SILKWONDER.ttf", 20)
                text1 = font.render("Controls:", True, WHITE)
                text2 = font.render("W - Cycle Spell Forward", True, (WHITE))
                text3 = font.render("A - Cycle Potion Backward", True, (WHITE))
                text4 = font.render("S - Cycle Spell Backward", True, (WHITE))
                text5 = font.render("D - Cycle Potion Forward", True, (WHITE))
                text6 = font.render("Q - Use Spell", True, (WHITE))
                text7 = font.render("E - Use Potion", True, (WHITE))
                text8 = font.render("SPACE BAR - Interact", True, (WHITE))
                text9 = font.render("Arrow Keys - Move", True, (WHITE))
                text10 = font.render("Right Shift - Attack", True, (WHITE))
                text11 = font.render("H - View Controls", True, (WHITE))
                continueText = font2.render("Click to continue", True, WHITE)

                screen.fill(BLACK)
                screen.blit(text1, (WINDOW_WIDTH//2 - 75, 25))
                screen.blit(text2, (75, WINDOW_HEIGHT//2 - 150))
                screen.blit(text3, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 150))
                screen.blit(text4, (75, WINDOW_HEIGHT//2 - 100))
                screen.blit(text5, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
                screen.blit(text6, (75, WINDOW_HEIGHT//2 - 50))
                screen.blit(text7, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
                screen.blit(text8, (75, WINDOW_HEIGHT//2))
                screen.blit(text9, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                screen.blit(text10, (75, WINDOW_HEIGHT//2 + 50))
                screen.blit(text11, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
                screen.blit(continueText,
                            (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 75))
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
        elif(chance < 0.85):
            item = "Coin1"
        elif(chance < 0.95):
            item = "Coin3"
        elif(chance < 1.00):
            item = "Coin5"

        return([item, room, x, y])


def rotatePoint(pointX, pointY, originX, originY, angle):
    """ This function finds the coordinates of a
    point rotated around a defined point"""
    angle = angle * (math.pi / 180)
    rotatedX = (math.cos(angle) * (pointX - originX)) - (
        math.sin(angle) * (pointY-originY)) + originX
    rotatedY = (math.sin(angle) * (pointX - originX)) + (
        math.cos(angle) * (pointY-originY)) + originY
    rotatedCoords = [rotatedX, rotatedY]
    return rotatedCoords


def rot_center(image, rect, angle):
    """Rotate the image while keeping its center."""
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect


def main():
    """ Main program function. """
    global NEWGAME

    # Initialize Pygame and set up the window
    pygame.init()

    # Set the window title.
    pygame.display.set_caption("Genesis")

    # Make the mouse invisible
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:

        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

        # If the game starts over, stop the music and start up a new game.
        if(NEWGAME):
            pygame.mixer.music.stop()
            NEWGAME = False
            game = Game()

    # Close window and exit
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
