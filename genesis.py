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
"The Constants.BLACK Box" By roleMusic
"The Constants.WHITE" By RoleMusic found on http://freemusicarchive.org/genre/Chiptune/
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
from Enemy import Enemy
import Constants
import Player
import Game
import FeedbackSystem

# Set the screen as a global variable
# (This is necessary in order to load in the sprites)
size = (Constants.Constants.WINDOW_WIDTH, Constants.Constants.WINDOW_HEIGHT)
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
Constants.BLACKFloorTile = pygame.image.load(
    "Genesis_Sprites/Constants.BLACKFloorTile.png").convert()
Constants.WHITEFloorTile = pygame.image.load(
    "Genesis_Sprites/Constants.WHITEFloorTile.png").convert()
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
