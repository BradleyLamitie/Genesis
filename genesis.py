"""
Create the main game for "Genesis"
 
Author: Bradley Lamitie
Date: 11/14/2017
Version Number: 2.0 (Demo)
 
What the Code Does: 
The code so far creates the world using the tiles provided by rendering one room at a time
and zooming in on it to make it more visible. 
Then, the player is put into the world and can use the directional 
keys( UpArrow, RightArrow, LeftArrow, and DownArrow ) to move around the world
The player can also now use potions and spells using the E and Q key respectively
The player can switch between potions using A and D and switch between spells with W and S
The Right Shift key can be used to attack
The code runs through the events and moves the sprite. 
So far, the game doesnt have any real way to lose or win. 

How to Play: 
The player can use the directional keys( UpArrow, RightArrow, LeftArrow, and DownArrow )
 to move around the world. 
 Use spells to fight and destroy obstacles. 
 Use attacking to fight enemys. 
 Use potions to heal and restore mana. 

GitHub Repository: https://github.com/BradleyLamitie/Genesis

Credits: 
Silk Wonderland font by jelloween Found on https://jelloween.deviantart.com/art/Font-SILKY-WONDERLAND-free-45103645
"The White" By RoleMusic found on http://freemusicarchive.org/genre/Chiptune/
All Sprites are made by me using Pixilart.com

Changes in this version: 
- Added Quests
- Added ability to interact with things like chests, NPCs, and signposts. 

Known Glitches: 
- Dialog runs through too quickly
- Player attack sprite is too short
- Sometimes enemies disappear into walls or move unnaturally fast
- 

TODOs for Final Project: 
- Finish building the world's second level. 
- Make it so that the WORLD_DATA is imported from a .tmx file. 
- If possible import a tileset from a Tiled file. 
- Learn to Use a sprite Sheet to load in sprites. 
- Animate the characters as they move throughout the world. 
- Replace all clocktower_door sprites with new sprites. 
- Add Save states or a pause function.
- Add a menu.
- Add Sounds.
- Add cheat codes for quick demonstrations.
- Add Screen animations
- Add Item Drops
- Add quest feedback
- Add enemy knockback when player attacks
- Add better enemy AI
- Game Balancing

"""
import pygame
from pygame.sprite import spritecollide, groupcollide
import random
from math import hypot
 
# --- Global constants ---
# Colors: 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTBLUE = (0,191,255)
GRAY = (205, 201, 201)

# Set the color key to hot pink to make the background translucent
COLORKEY = (255,0,255)

# The width and height of the room (16 tiles * 11 tiles)
ROOM_WIDTH = 400
ROOM_HEIGHT = 275

# The width and height of the world
WORLD_WIDTH = 2000
WORLD_HEIGHT = 825

# The rate at which we magnify the pixels
WINDOW_MAGNIFICATION = 2

# For every frame the player sprite will be moved by the WALKRATE variable
WALKRATE = 5

# How many seconds an animation frame should last. 
ANIMRATE = 0.15

# The width and height of the magnified window
WINDOW_WIDTH = ROOM_WIDTH * WINDOW_MAGNIFICATION
WINDOW_HEIGHT = ROOM_HEIGHT * WINDOW_MAGNIFICATION

# The Camera starts at the second room from the right, second room down.
CAMERA_LEFT = ROOM_WIDTH * 2
CAMERA_TOP = ROOM_HEIGHT * 2

# Set the need for a new game to false
NEWGAME = False

# Set the screen as a global variable
# (This is necessary in order to load in the sprites)
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)

# Load in each of the sprite images  
Cliff_bottom_bottom = pygame.image.load("Genesis_Sprites/Cliff_bottom_bottom.png").convert()
Cliff_bottom_corner_bottomleft = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_bottomleft.png").convert()
Cliff_bottom_corner_bottomright = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_bottomright.png").convert()
Cliff_bottom_corner_inset_bottomleft = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_inset_bottomleft.png").convert()
Cliff_bottom_corner_inset_bottomright = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_inset_bottomright.png").convert()
Cliff_bottom_topleft = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_inset_topleft.png").convert()
Cliff_bottom_corner_inset_topright = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_inset_topright.png").convert()
Cliff_bottom_corner_inset_topleft = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_inset_topleft.png").convert()
Cliff_bottom_corner_topleft = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_topleft.png").convert()
Cliff_bottom_corner_topright = pygame.image.load("Genesis_Sprites/Cliff_bottom_corner_topright.png").convert()
Cliff_bottom_left = pygame.image.load("Genesis_Sprites/Cliff_bottom_left.png").convert()
Cliff_bottom_right = pygame.image.load("Genesis_Sprites/Cliff_bottom_right.png").convert()
Cliff_bottom_top = pygame.image.load("Genesis_Sprites/Cliff_bottom_top.png").convert()
Cliff_corner_bottomleft = pygame.image.load("Genesis_Sprites/Cliff_corner_bottomleft.png").convert()
Cliff_corner_bottomright = pygame.image.load("Genesis_Sprites/Cliff_corner_bottomright.png").convert()
Cliff_corner_topleft = pygame.image.load("Genesis_Sprites/Cliff_corner_topleft.png").convert()
Cliff_corner_topright = pygame.image.load("Genesis_Sprites/Cliff_corner_topright.png").convert()
Cliff_top = pygame.image.load("Genesis_Sprites/Cliff_top.png").convert()
Cliff_top_corner_bottomleft = pygame.image.load("Genesis_Sprites/Cliff_top_corner_bottomleft.png").convert()
Cliff_top_corner_bottomright = pygame.image.load("Genesis_Sprites/Cliff_top_corner_bottomright.png").convert()
Cliff_top_corner_topleft = pygame.image.load("Genesis_Sprites/Cliff_top_corner_topleft.png").convert()
Cliff_top_corner_topright = pygame.image.load("Genesis_Sprites/Cliff_top_corner_topright.png").convert()
Cliff_top_edge_bottom = pygame.image.load("Genesis_Sprites/Cliff_top_edge_bottom.png").convert()
Cliff_top_edge_left = pygame.image.load("Genesis_Sprites/Cliff_top_edge_left.png").convert()
Cliff_top_edge_right = pygame.image.load("Genesis_Sprites/Cliff_top_edge_right.png").convert()
Cliff_top_edge_top = pygame.image.load("Genesis_Sprites/Cliff_top_edge_top.png").convert()
Cliff_wall = pygame.image.load("Genesis_Sprites/Cliff_wall.png").convert()
Clocktower_door = pygame.image.load("Genesis_Sprites/Clocktower_door.png").convert()
Clocktower_door_open = pygame.image.load("Genesis_Sprites/Clocktower_door_open.png").convert()
Grass_cut = pygame.image.load("Genesis_Sprites/Grass_cut.png").convert()
Grass_uncut = pygame.image.load("Genesis_Sprites/Grass_uncut.png").convert()
gray_ground_path = pygame.image.load("Genesis_Sprites/gray_ground_path.png").convert()
Ground_grass = pygame.image.load("Genesis_Sprites/Ground_grass.png").convert()
Rock_exploded = pygame.image.load("Genesis_Sprites/Rock_exploded.png").convert()
Rock_exploded_path = pygame.image.load("Genesis_Sprites/Rock_exploded_path.png").convert()
Rock_turtle = pygame.image.load("Genesis_Sprites/Rock_turtle.png").convert()
Rock_unexploded = pygame.image.load("Genesis_Sprites/Rock_unexploded.png").convert()
Rock_unexploded_path = pygame.image.load("Genesis_Sprites/Rock_unexploded_path.png").convert()
Signpost = pygame.image.load("Genesis_Sprites/Signpost.png").convert()
Signpost_path = pygame.image.load("Genesis_Sprites/Signpost_path.png").convert()
Chest_Closed = pygame.image.load("Genesis_Sprites/Chest_closed.png").convert()
Chest_Open = pygame.image.load("Genesis_Sprites/Chest_open.png").convert()
Map_Image = pygame.image.load("Genesis_Sprites/Genesis_Map.png").convert()
 
# Add the NPCs
Merchant = pygame.image.load("Genesis_Sprites/Merchant.png").convert()
OldMan = pygame.image.load("Genesis_Sprites/OldMan.png").convert()

# Add the images for the snake enemy
Snake_Forward_1 = pygame.image.load("Genesis_Sprites/Snake_Forward_1.png").convert()
Snake_Forward_2 = pygame.image.load("Genesis_Sprites/Snake_Forward_2.png").convert()
Snake_Back_1 = pygame.image.load("Genesis_Sprites/Snake_Back_1.png").convert()
Snake_Back_2 = pygame.image.load("Genesis_Sprites/Snake_Back_2.png").convert()
Snake_Right_1 = pygame.image.load("Genesis_Sprites/Snake_Right_1.png").convert()
Snake_Right_2 = pygame.image.load("Genesis_Sprites/Snake_Right_2.png").convert()
Snake_Left_1 = pygame.transform.flip(Snake_Right_1, True, False)
Snake_Left_2 = pygame.transform.flip(Snake_Right_2, True, False)

# Add the icons that will be used in the feedback system
Fireball_Regular = pygame.image.load("Genesis_Sprites/Fireball_Regular.png").convert()
Fireball_Swirl = pygame.image.load("Genesis_Sprites/Fireball_Swirl.png").convert()
Explosion_Bomb = pygame.image.load("Genesis_Sprites/Explosion_Bomb.png").convert()
Explosion_Blast = pygame.image.load("Genesis_Sprites/Explosion_Blast.png").convert()
Lesser_Mana_Potion = pygame.image.load("Genesis_Sprites/Lesser_Mana_Potion.png").convert()
Lesser_Health_Potion = pygame.image.load("Genesis_Sprites/Lesser_Health_Potion.png").convert()
Mana_Potion = pygame.image.load("Genesis_Sprites/Mana_Potion.png").convert()
Health_Potion = pygame.image.load("Genesis_Sprites/Health_Potion.png").convert()
Spell_Frame = pygame.image.load("Genesis_Sprites/Spell_Frame_Filled.png").convert()
Potion_Frame = pygame.image.load("Genesis_Sprites/Potion_Frame_Filled.png").convert()
Coin = pygame.image.load("Genesis_Sprites/Coin.png").convert()
Blank = pygame.image.load("Genesis_Sprites/Blank.png").convert()

# Add the images for Angel sprites in each armor
# Add the images for Angel with wooden Armor and Sword
Angel_wood_Back_Idle = pygame.image.load("Genesis_Sprites/Angel_wood_back_idle.png").convert()
Angel_wood_Back_Walking1 = pygame.image.load("Genesis_Sprites/Angel_wood_back_walking1.png").convert()
Angel_wood_Back_Walking2 = Angel_wood_Back_Idle
Angel_wood_Back_Walking3 = pygame.transform.flip(Angel_wood_Back_Walking1, True, False)
Angel_wood_Back_Walking4 = Angel_wood_Back_Idle 
Angel_wood_Back_Attacking1 = Angel_wood_Back_Idle
Angel_wood_Back_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_wood_back_Attacking2.png").convert()
Angel_wood_Back_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_wood_back_Attacking3.png").convert()
Angel_wood_Back_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_wood_back_Attacking4.png").convert()
Angel_wood_Back_Attacking5 = Angel_wood_Back_Idle
Angel_wood_Back_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_back_Attacking2_swordtip.png").convert()
Angel_wood_Back_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_back_Attacking3_swordtip.png").convert()
Angel_wood_Back_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_back_Attacking4_swordtip.png").convert()

Angel_wood_Front_Idle = pygame.image.load("Genesis_Sprites/Angel_wood_front_idle.png").convert()
Angel_wood_Front_Walking1 = pygame.image.load("Genesis_Sprites/Angel_wood_front_walking1.png").convert()
Angel_wood_Front_Walking2 = pygame.image.load("Genesis_Sprites/Angel_wood_front_walking2.png").convert()
Angel_wood_Front_Walking3 = pygame.image.load("Genesis_Sprites/Angel_wood_front_walking3.png").convert()
Angel_wood_Front_Walking4 = pygame.image.load("Genesis_Sprites/Angel_wood_front_walking4.png").convert()
Angel_wood_Front_Attacking1 = Angel_wood_Front_Idle
Angel_wood_Front_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_wood_front_Attacking2.png").convert()
Angel_wood_Front_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_wood_front_Attacking3.png").convert()
Angel_wood_Front_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_wood_front_Attacking4.png").convert()
Angel_wood_Front_Attacking5 = Angel_wood_Front_Idle
Angel_wood_Front_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_front_Attacking2_swordtip.png").convert()
Angel_wood_Front_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_front_Attacking3_swordtip.png").convert()
Angel_wood_Front_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_front_Attacking4_swordtip.png").convert()

Angel_wood_Left_Idle = pygame.image.load("Genesis_Sprites/Angel_wood_left_idle.png").convert()
Angel_wood_Left_Walking1 = pygame.image.load("Genesis_Sprites/Angel_wood_left_walking1.png").convert()
Angel_wood_Left_Walking2 = pygame.image.load("Genesis_Sprites/Angel_wood_left_walking2.png").convert()
Angel_wood_Left_Walking3 = pygame.image.load("Genesis_Sprites/Angel_wood_left_walking3.png").convert()
Angel_wood_Left_Walking4 = pygame.image.load("Genesis_Sprites/Angel_wood_left_walking4.png").convert()
Angel_wood_Left_Attacking1 = Angel_wood_Left_Idle
Angel_wood_Left_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_wood_left_Attacking2.png").convert()
Angel_wood_Left_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_wood_left_Attacking3.png").convert()
Angel_wood_Left_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_wood_left_Attacking4.png").convert()
Angel_wood_Left_Attacking5 = Angel_wood_Left_Idle
Angel_wood_Left_Attacking1_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_left_Attacking1_Swordtip.png").convert()
Angel_wood_Left_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_left_Attacking2_Swordtip.png").convert()
Angel_wood_Left_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_left_Attacking3_Swordtip.png").convert()
Angel_wood_Left_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_left_Attacking4_Swordtip.png").convert()
Angel_wood_Left_Attacking5_Swordtip = pygame.image.load("Genesis_Sprites/Angel_wood_left_Attacking5_Swordtip.png").convert()

Angel_wood_Right_Idle = pygame.transform.flip(Angel_wood_Left_Idle, True, False)
Angel_wood_Right_Walking1 = pygame.transform.flip(Angel_wood_Left_Walking1, True, False)
Angel_wood_Right_Walking2 = pygame.transform.flip(Angel_wood_Left_Walking2, True, False)
Angel_wood_Right_Walking3 = pygame.transform.flip(Angel_wood_Left_Walking3, True, False)
Angel_wood_Right_Walking4 = pygame.transform.flip(Angel_wood_Left_Walking4, True, False)
Angel_wood_Right_Attacking1 = pygame.transform.flip(Angel_wood_Left_Attacking1, True, False)
Angel_wood_Right_Attacking2 = pygame.transform.flip(Angel_wood_Left_Attacking2, True, False)
Angel_wood_Right_Attacking3 = pygame.transform.flip(Angel_wood_Left_Attacking3, True, False)
Angel_wood_Right_Attacking4 = pygame.transform.flip(Angel_wood_Left_Attacking4, True, False)
Angel_wood_Right_Attacking5 = pygame.transform.flip(Angel_wood_Left_Attacking5, True, False)
Angel_wood_Right_Attacking1_Swordtip = pygame.transform.flip(Angel_wood_Left_Attacking1_Swordtip, True, False)
Angel_wood_Right_Attacking2_Swordtip = pygame.transform.flip(Angel_wood_Left_Attacking2_Swordtip, True, False)
Angel_wood_Right_Attacking3_Swordtip = pygame.transform.flip(Angel_wood_Left_Attacking3_Swordtip, True, False)
Angel_wood_Right_Attacking4_Swordtip = pygame.transform.flip(Angel_wood_Left_Attacking4_Swordtip, True, False)
Angel_wood_Right_Attacking5_Swordtip = pygame.transform.flip(Angel_wood_Left_Attacking5_Swordtip, True, False)

Angel_wood_Get_Item = pygame.image.load("Genesis_Sprites/Angel_wood_get_item.png").convert()


# Steel Armor and sword
Angel_Steel_Back_Idle = pygame.image.load("Genesis_Sprites/Angel_steel_back_idle.png").convert()
Angel_Steel_Back_Walking1 = pygame.image.load("Genesis_Sprites/Angel_steel_back_walking1.png").convert()
Angel_Steel_Back_Walking2 = Angel_Steel_Back_Idle
Angel_Steel_Back_Walking3 = pygame.transform.flip(Angel_Steel_Back_Walking1, True, False)
Angel_Steel_Back_Walking4 = Angel_Steel_Back_Idle 
Angel_Steel_Back_Attacking1 = Angel_Steel_Back_Idle
Angel_Steel_Back_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_steel_back_Attacking2.png").convert()
Angel_Steel_Back_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_steel_back_Attacking3.png").convert()
Angel_Steel_Back_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_steel_back_Attacking4.png").convert()
Angel_Steel_Back_Attacking5 = Angel_Steel_Back_Idle
Angel_Steel_Back_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_back_Attacking2_swordtip.png").convert()
Angel_Steel_Back_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_back_Attacking3_swordtip.png").convert()
Angel_Steel_Back_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_back_Attacking4_swordtip.png").convert()

Angel_Steel_Front_Idle = pygame.image.load("Genesis_Sprites/Angel_steel_front_idle.png").convert()
Angel_Steel_Front_Walking1 = pygame.image.load("Genesis_Sprites/Angel_steel_front_walking1.png").convert()
Angel_Steel_Front_Walking2 = pygame.image.load("Genesis_Sprites/Angel_steel_front_walking2.png").convert()
Angel_Steel_Front_Walking3 = pygame.image.load("Genesis_Sprites/Angel_steel_front_walking3.png").convert()
Angel_Steel_Front_Walking4 = pygame.image.load("Genesis_Sprites/Angel_steel_front_walking4.png").convert()
Angel_Steel_Front_Attacking1 = Angel_Steel_Front_Idle
Angel_Steel_Front_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_steel_front_Attacking2.png").convert()
Angel_Steel_Front_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_steel_front_Attacking3.png").convert()
Angel_Steel_Front_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_steel_front_Attacking4.png").convert()
Angel_Steel_Front_Attacking5 = Angel_Steel_Front_Idle
Angel_Steel_Front_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_front_Attacking2_swordtip.png").convert()
Angel_Steel_Front_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_front_Attacking3_swordtip.png").convert()
Angel_Steel_Front_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_front_Attacking4_swordtip.png").convert()

Angel_Steel_Left_Idle = pygame.image.load("Genesis_Sprites/Angel_steel_left_idle.png").convert()
Angel_Steel_Left_Walking1 = pygame.image.load("Genesis_Sprites/Angel_steel_left_walking1.png").convert()
Angel_Steel_Left_Walking2 = pygame.image.load("Genesis_Sprites/Angel_steel_left_walking2.png").convert()
Angel_Steel_Left_Walking3 = pygame.image.load("Genesis_Sprites/Angel_steel_left_walking3.png").convert()
Angel_Steel_Left_Walking4 = pygame.image.load("Genesis_Sprites/Angel_steel_left_walking4.png").convert()
Angel_Steel_Left_Attacking1 = Angel_Steel_Left_Idle
Angel_Steel_Left_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_steel_left_Attacking2.png").convert()
Angel_Steel_Left_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_steel_left_Attacking3.png").convert()
Angel_Steel_Left_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_steel_left_Attacking4.png").convert()
Angel_Steel_Left_Attacking5 = Angel_Steel_Left_Idle
Angel_Steel_Left_Attacking1_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_left_Attacking1_Swordtip.png").convert()
Angel_Steel_Left_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_left_Attacking2_Swordtip.png").convert()
Angel_Steel_Left_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_left_Attacking3_Swordtip.png").convert()
Angel_Steel_Left_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_left_Attacking4_Swordtip.png").convert()
Angel_Steel_Left_Attacking5_Swordtip = pygame.image.load("Genesis_Sprites/Angel_steel_left_Attacking5_Swordtip.png").convert()

Angel_Steel_Right_Idle = pygame.transform.flip(Angel_Steel_Left_Idle, True, False)
Angel_Steel_Right_Walking1 = pygame.transform.flip(Angel_Steel_Left_Walking1, True, False)
Angel_Steel_Right_Walking2 = pygame.transform.flip(Angel_Steel_Left_Walking2, True, False)
Angel_Steel_Right_Walking3 = pygame.transform.flip(Angel_Steel_Left_Walking3, True, False)
Angel_Steel_Right_Walking4 = pygame.transform.flip(Angel_Steel_Left_Walking4, True, False)
Angel_Steel_Right_Attacking1 = pygame.transform.flip(Angel_Steel_Left_Attacking1, True, False)
Angel_Steel_Right_Attacking2 = pygame.transform.flip(Angel_Steel_Left_Attacking2, True, False)
Angel_Steel_Right_Attacking3 = pygame.transform.flip(Angel_Steel_Left_Attacking3, True, False)
Angel_Steel_Right_Attacking4 = pygame.transform.flip(Angel_Steel_Left_Attacking4, True, False)
Angel_Steel_Right_Attacking5 = pygame.transform.flip(Angel_Steel_Left_Attacking5, True, False)
Angel_Steel_Right_Attacking1_Swordtip = pygame.transform.flip(Angel_Steel_Left_Attacking1_Swordtip, True, False)
Angel_Steel_Right_Attacking2_Swordtip = pygame.transform.flip(Angel_Steel_Left_Attacking2_Swordtip, True, False)
Angel_Steel_Right_Attacking3_Swordtip = pygame.transform.flip(Angel_Steel_Left_Attacking3_Swordtip, True, False)
Angel_Steel_Right_Attacking4_Swordtip = pygame.transform.flip(Angel_Steel_Left_Attacking4_Swordtip, True, False)
Angel_Steel_Right_Attacking5_Swordtip = pygame.transform.flip(Angel_Steel_Left_Attacking5_Swordtip, True, False)

Angel_Steel_Get_Item = pygame.image.load("Genesis_Sprites/Angel_Steel_get_item.png").convert()

# Golden Armor and sword
Angel_Gold_Back_Idle = pygame.image.load("Genesis_Sprites/Angel_Gold_back_idle.png").convert()
Angel_Gold_Back_Walking1 = pygame.image.load("Genesis_Sprites/Angel_Gold_back_walking1.png").convert()
Angel_Gold_Back_Walking2 = Angel_Gold_Back_Idle
Angel_Gold_Back_Walking3 = pygame.transform.flip(Angel_Gold_Back_Walking1, True, False)
Angel_Gold_Back_Walking4 = Angel_Gold_Back_Idle 
Angel_Gold_Back_Attacking1 = Angel_Gold_Back_Idle
Angel_Gold_Back_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_Gold_back_Attacking2.png").convert()
Angel_Gold_Back_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_Gold_back_Attacking3.png").convert()
Angel_Gold_Back_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_Gold_back_Attacking4.png").convert()
Angel_Gold_Back_Attacking5 = Angel_Gold_Back_Idle
Angel_Gold_Back_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_back_Attacking2_swordtip.png").convert()
Angel_Gold_Back_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_back_Attacking3_swordtip.png").convert()
Angel_Gold_Back_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_back_Attacking4_swordtip.png").convert()

Angel_Gold_Front_Idle = pygame.image.load("Genesis_Sprites/Angel_Gold_front_idle.png").convert()
Angel_Gold_Front_Walking1 = pygame.image.load("Genesis_Sprites/Angel_Gold_front_walking1.png").convert()
Angel_Gold_Front_Walking2 = pygame.image.load("Genesis_Sprites/Angel_Gold_front_walking2.png").convert()
Angel_Gold_Front_Walking3 = pygame.image.load("Genesis_Sprites/Angel_Gold_front_walking3.png").convert()
Angel_Gold_Front_Walking4 = pygame.image.load("Genesis_Sprites/Angel_Gold_front_walking4.png").convert()
Angel_Gold_Front_Attacking1 = Angel_Gold_Front_Idle
Angel_Gold_Front_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_Gold_front_Attacking2.png").convert()
Angel_Gold_Front_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_Gold_front_Attacking3.png").convert()
Angel_Gold_Front_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_Gold_front_Attacking4.png").convert()
Angel_Gold_Front_Attacking5 = Angel_Gold_Front_Idle
Angel_Gold_Front_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_front_Attacking2_swordtip.png").convert()
Angel_Gold_Front_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_front_Attacking3_swordtip.png").convert()
Angel_Gold_Front_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_front_Attacking4_swordtip.png").convert()

Angel_Gold_Left_Idle = pygame.image.load("Genesis_Sprites/Angel_Gold_left_idle.png").convert()
Angel_Gold_Left_Walking1 = pygame.image.load("Genesis_Sprites/Angel_Gold_left_walking1.png").convert()
Angel_Gold_Left_Walking2 = pygame.image.load("Genesis_Sprites/Angel_Gold_left_walking2.png").convert()
Angel_Gold_Left_Walking3 = pygame.image.load("Genesis_Sprites/Angel_Gold_left_walking3.png").convert()
Angel_Gold_Left_Walking4 = pygame.image.load("Genesis_Sprites/Angel_Gold_left_walking4.png").convert()
Angel_Gold_Left_Attacking1 = Angel_Gold_Left_Idle
Angel_Gold_Left_Attacking2 = pygame.image.load("Genesis_Sprites/Angel_Gold_left_Attacking2.png").convert()
Angel_Gold_Left_Attacking3 = pygame.image.load("Genesis_Sprites/Angel_Gold_left_Attacking3.png").convert()
Angel_Gold_Left_Attacking4 = pygame.image.load("Genesis_Sprites/Angel_Gold_left_Attacking4.png").convert()
Angel_Gold_Left_Attacking5 = Angel_Gold_Left_Idle
Angel_Gold_Left_Attacking1_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_left_Attacking1_Swordtip.png").convert()
Angel_Gold_Left_Attacking2_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_left_Attacking2_Swordtip.png").convert()
Angel_Gold_Left_Attacking3_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_left_Attacking3_Swordtip.png").convert()
Angel_Gold_Left_Attacking4_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_left_Attacking4_Swordtip.png").convert()
Angel_Gold_Left_Attacking5_Swordtip = pygame.image.load("Genesis_Sprites/Angel_Gold_left_Attacking5_Swordtip.png").convert()

Angel_Gold_Right_Idle = pygame.transform.flip(Angel_Gold_Left_Idle, True, False)
Angel_Gold_Right_Walking1 = pygame.transform.flip(Angel_Gold_Left_Walking1, True, False)
Angel_Gold_Right_Walking2 = pygame.transform.flip(Angel_Gold_Left_Walking2, True, False)
Angel_Gold_Right_Walking3 = pygame.transform.flip(Angel_Gold_Left_Walking3, True, False)
Angel_Gold_Right_Walking4 = pygame.transform.flip(Angel_Gold_Left_Walking4, True, False)
Angel_Gold_Right_Attacking1 = pygame.transform.flip(Angel_Gold_Left_Attacking1, True, False)
Angel_Gold_Right_Attacking2 = pygame.transform.flip(Angel_Gold_Left_Attacking2, True, False)
Angel_Gold_Right_Attacking3 = pygame.transform.flip(Angel_Gold_Left_Attacking3, True, False)
Angel_Gold_Right_Attacking4 = pygame.transform.flip(Angel_Gold_Left_Attacking4, True, False)
Angel_Gold_Right_Attacking5 = pygame.transform.flip(Angel_Gold_Left_Attacking5, True, False)
Angel_Gold_Right_Attacking1_Swordtip = pygame.transform.flip(Angel_Gold_Left_Attacking1_Swordtip, True, False)
Angel_Gold_Right_Attacking2_Swordtip = pygame.transform.flip(Angel_Gold_Left_Attacking2_Swordtip, True, False)
Angel_Gold_Right_Attacking3_Swordtip = pygame.transform.flip(Angel_Gold_Left_Attacking3_Swordtip, True, False)
Angel_Gold_Right_Attacking4_Swordtip = pygame.transform.flip(Angel_Gold_Left_Attacking4_Swordtip, True, False)
Angel_Gold_Right_Attacking5_Swordtip = pygame.transform.flip(Angel_Gold_Left_Attacking5_Swordtip, True, False)

Angel_Gold_Get_Item = pygame.image.load("Genesis_Sprites/Angel_Gold_get_item.png").convert()

# Add global variables to hold String constants used in event processing and player direction
RIGHT = "RIGHT"
DOWN = "DOWN"
LEFT = "LEFT"
UP = "UP"

# WORLD_DATA is a large string that includes all the tile data copied from Tiled file.
# TODO: import this data from the .tmx file directly.
WORLD_DATA = """50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,22,41,41,41,41,41,41,41,41,41,41,41,41,41,41,21,50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49
22,44,44,44,44,44,53,57,57,53,44,44,44,44,44,21,22,44,44,44,44,44,44,44,44,44,44,44,44,48,48,21,22,41,41,41,41,41,41,41,41,41,41,41,41,41,41,21,22,48,48,48,44,44,44,44,44,44,44,44,48,48,48,21,22,44,48,48,44,44,44,44,44,48,48,48,48,48,48,21
22,44,44,45,45,45,45,54,54,45,45,45,45,44,44,21,22,44,44,44,44,44,44,44,44,44,44,44,44,44,48,21,22,41,41,41,41,41,41,41,42,41,41,41,41,41,41,21,22,48,44,44,44,44,44,44,44,44,44,44,44,44,48,21,22,48,48,44,55,55,59,55,55,44,48,48,48,48,48,21
22,44,44,45,45,45,45,54,54,45,45,45,45,45,44,17,18,45,45,45,45,45,45,45,45,45,44,44,44,44,44,21,22,48,48,48,48,48,48,56,41,48,48,48,48,47,48,21,22,48,44,44,44,44,45,45,45,45,44,44,44,44,48,21,22,48,44,54,54,54,54,54,54,54,44,48,48,47,48,21
22,48,45,45,45,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,45,44,44,44,44,44,21,22,45,45,45,45,45,48,54,54,48,45,45,45,45,45,21,22,44,44,44,44,45,45,45,45,45,45,44,44,44,44,17,18,44,54,54,54,54,54,54,54,54,54,44,48,48,48,21
22,48,48,45,45,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,45,44,44,44,44,44,21,22,45,45,45,45,45,48,54,54,48,45,45,45,45,45,21,22,44,44,44,44,45,45,45,45,45,45,44,44,44,44,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,48,21
22,48,45,45,45,45,45,45,45,45,45,45,45,45,44,19,20,45,45,45,45,45,45,54,54,45,44,44,44,44,44,21,22,44,45,45,45,45,48,54,54,48,45,45,45,45,44,21,22,44,44,44,44,45,45,45,45,45,45,44,44,44,44,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,48,21
22,44,44,45,45,45,45,45,45,45,45,45,45,44,44,21,22,44,45,45,45,45,45,54,54,45,44,44,44,44,44,21,22,44,45,45,45,45,48,54,54,48,45,45,45,45,44,21,22,48,44,44,44,44,45,45,45,45,44,44,44,44,48,19,20,44,54,54,54,54,54,54,54,54,54,45,54,54,44,21
22,44,44,44,44,44,44,44,44,44,44,44,44,44,44,21,22,44,44,45,45,45,45,54,54,45,44,44,44,44,44,21,22,44,44,45,45,45,48,54,54,48,45,45,45,44,44,21,22,48,44,44,44,44,44,44,44,44,44,44,44,44,48,21,22,48,44,54,54,54,54,54,54,54,45,45,54,54,44,21
22,44,44,48,48,48,48,47,48,48,48,48,48,44,44,21,22,47,44,44,45,45,45,54,54,45,44,44,44,44,44,21,22,44,44,44,44,45,48,54,54,48,45,44,44,44,44,21,22,48,48,48,44,44,44,44,44,44,44,44,48,48,47,21,22,48,48,44,54,54,54,54,54,45,45,45,54,54,44,21
52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,52,23,23,23,23,23,20,54,54,19,23,23,23,23,23,51,52,23,23,23,23,23,20,54,54,19,23,23,23,23,23,51,52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,52,23,23,23,23,23,23,23,23,23,23,20,54,54,19,51
50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,50,16,16,16,16,16,18,54,54,17,16,16,16,16,16,49,50,16,16,16,16,16,18,54,54,17,16,16,16,16,16,49,50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,50,16,16,16,16,16,16,16,16,16,16,18,54,54,17,49
22,48,48,48,48,48,44,44,44,44,44,44,44,44,44,21,22,44,44,44,44,45,45,54,54,45,45,45,48,48,48,21,22,44,45,45,45,45,45,54,54,44,45,44,45,45,45,21,22,44,44,44,44,45,45,44,44,44,44,44,44,44,44,21,22,45,45,45,45,45,45,45,45,45,45,45,54,54,45,21
22,48,47,48,48,44,44,44,44,44,44,44,44,44,44,21,22,44,44,44,44,45,45,54,54,45,45,45,45,48,48,21,22,45,45,44,45,45,45,54,54,45,45,45,45,45,45,21,22,44,44,44,44,45,45,45,45,45,45,45,44,45,48,21,22,48,45,45,45,45,45,45,45,45,45,45,54,54,45,21
22,48,48,48,44,44,44,53,44,44,44,44,44,44,44,17,18,53,44,44,44,45,45,54,54,45,45,45,45,45,48,17,18,45,45,45,45,45,45,54,54,45,44,45,45,45,44,17,18,45,45,45,45,45,45,45,45,45,45,45,45,53,48,17,18,48,45,45,45,45,45,45,45,45,45,45,54,54,45,21
22,48,48,44,44,44,44,45,45,45,45,45,45,45,45,45,45,48,44,44,44,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,55,54,54,55,54,54,54,54,54,54,54,54,54,54,54,54,44,21
22,48,44,44,44,44,44,45,45,45,45,45,45,45,45,45,45,48,44,44,44,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,55,54,54,55,54,54,54,54,54,54,54,54,54,54,54,54,44,21
22,44,44,44,44,44,53,45,45,44,44,44,44,44,44,19,20,44,44,44,44,45,45,45,45,45,45,45,45,45,45,19,20,45,45,45,45,45,45,54,54,45,45,45,45,45,45,19,20,45,45,45,45,45,45,45,45,45,45,45,45,45,48,19,20,48,45,45,45,45,45,45,45,45,45,45,44,44,44,21
22,44,44,44,44,44,44,45,45,44,44,44,44,44,48,21,22,48,44,44,44,45,45,45,45,45,45,45,45,45,45,21,22,45,58,45,45,45,53,54,54,45,45,45,45,45,44,21,22,45,44,44,45,45,45,45,45,45,44,44,45,45,48,21,22,48,45,45,45,45,45,45,45,45,45,44,44,44,48,21
22,44,44,44,44,44,44,45,45,44,44,44,44,48,48,21,22,48,47,44,44,44,44,44,44,44,44,44,44,44,44,21,22,45,45,45,44,45,45,54,54,45,45,44,45,45,45,21,22,45,44,44,45,45,45,45,45,45,44,44,44,45,45,21,22,45,45,45,45,45,45,45,45,45,44,44,44,48,48,21
22,44,44,44,44,44,53,45,45,44,44,44,48,48,47,21,22,48,48,48,44,44,44,44,44,44,44,44,44,44,44,21,22,45,45,45,45,45,45,54,54,45,45,45,45,44,45,21,22,45,45,45,45,45,45,45,45,45,45,45,45,45,45,21,22,45,45,45,45,45,45,45,45,44,44,44,48,48,47,21
52,23,23,23,23,23,20,45,45,19,23,23,23,23,23,51,52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,52,23,23,23,23,23,20,54,54,19,23,23,23,23,23,51,52,23,23,23,23,23,20,45,45,19,23,23,23,23,23,51,52,20,45,45,19,23,23,23,23,23,23,23,23,23,23,51
50,16,16,16,16,16,18,45,45,17,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,50,16,16,16,16,16,18,54,54,17,16,16,16,16,16,49,50,16,16,16,16,16,18,45,45,17,16,16,16,16,16,49,50,18,45,45,17,16,16,16,16,16,16,16,16,16,16,49
22,44,44,44,44,44,44,44,44,44,44,44,44,44,44,45,45,45,45,45,45,45,45,45,45,44,44,44,44,47,48,21,22,48,48,45,45,45,53,54,54,45,45,45,45,48,47,21,22,48,48,44,44,44,44,45,45,44,44,44,44,48,48,21,22,48,45,45,45,45,45,45,45,45,45,45,48,44,48,21
22,44,45,45,45,45,45,45,45,45,45,45,45,45,44,45,45,45,45,45,45,45,45,45,45,44,44,44,44,48,47,21,22,48,45,45,45,45,45,44,44,45,45,45,45,45,48,21,22,48,44,44,44,44,44,45,45,44,44,44,44,44,48,21,52,23,23,23,23,23,23,23,23,23,20,45,48,44,47,21
22,44,45,44,44,44,44,44,44,44,44,44,44,45,44,19,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,22,45,45,45,45,45,44,44,44,44,45,45,45,45,45,21,22,44,44,45,45,45,45,45,45,45,45,45,45,45,44,17,16,16,16,16,16,16,16,16,16,16,18,45,48,44,48,21
22,44,45,44,54,54,54,54,54,54,54,54,44,45,44,21,37,31,36,36,36,36,36,36,36,36,36,36,36,36,32,37,22,45,45,45,45,44,44,45,45,44,44,45,45,45,45,21,22,44,44,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,48,44,48,21
22,44,45,44,54,54,54,54,54,54,54,54,44,45,44,21,37,34,28,28,28,28,28,28,28,28,28,28,28,28,35,37,22,45,45,45,44,44,45,45,45,45,44,44,45,45,45,21,22,44,44,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,48,44,48,21
22,44,45,44,54,54,54,54,54,54,54,54,44,45,44,21,37,29,33,33,33,33,33,33,33,33,33,33,33,33,30,37,22,45,45,45,44,44,45,45,45,45,44,44,45,45,45,21,22,44,44,45,45,45,45,45,45,45,45,45,45,45,44,19,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51
22,44,45,44,44,44,44,44,44,44,44,44,44,45,44,21,27,37,37,37,37,37,37,37,37,37,37,37,37,37,37,26,22,45,45,45,45,44,44,45,45,44,44,45,45,45,45,21,22,44,44,45,45,45,45,45,45,45,45,45,45,45,44,21,26,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37
22,44,45,45,45,45,45,45,45,45,45,45,45,45,44,17,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,22,48,45,45,45,45,44,44,44,44,45,45,45,45,48,21,22,48,44,44,44,44,44,44,44,44,44,44,44,44,48,21,37,31,36,36,36,36,36,36,36,36,36,36,36,36,36,36
22,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,57,21,22,48,48,45,45,45,45,44,44,45,45,45,45,48,48,21,22,48,48,44,44,44,44,44,44,44,44,44,44,48,48,21,37,34,28,28,28,28,28,28,28,28,28,28,28,28,28,28
52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,37,34,28,28,28,28,28,28,28,28,28,28,28,28,28,28"""

# Split the WORLD_DATA string and sort it into a 2D array
global tile_Data
tile_Data = WORLD_DATA
tile_Data = tile_Data.split('\n')
tile_Data = [line.split(',') for line in tile_Data]

# This list represents the tile numbers of tiles the player and enemies shouldn't be able to walk through.
boundary_tiles = [15,16,17,18,19,20,21,22,23,24,25,26,28,29,30,31,32,33,34,35,36,37,40,41,4246,47,48,49,50,51,52,53,55,56,57,58,59,60]

# These lists represent tiles that are able to be interacted with
explodable_tiles = [44,47,48,55]
burnable_tiles = [44]
interactive_tiles = [41,53,56,57,58,59]
cuttable_tiles = [44]

# --- Classes ---
 
class Tile(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    global tile_Data
    def __init__(self, x, y, leftmostTile, topmostTile):
        """ Constructor, create the image of the block. """
        super().__init__()
        
        # Initialize the tiles size and locations
        self.image = pygame.Surface([25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION])
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
        """ This function is used to retrieve the sprite surfaces using the tile Number provided. """
        
        # Just in case, ensure tileNumber is an integer.
        tileNumber = int(tileNumber)
        
        # Run through each of the cases.
        if(tileNumber == 1):
            return Grass_cut
        elif(tileNumber == 2):
            return Rock_exploded
        elif(tileNumber == 3):
            return Rock_exploded_path
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
            return Clocktower_door_open
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
            return Chest_Open
        else:
            return Signpost_path

    
class Player(pygame.sprite.Sprite):
    # TODO: Player
    """ This class represents the player. """
    def __init__(self):
        
        # Call the superclass' constructor
        super().__init__()
        
        # This sets the player's current spell and potion to be used when using a potion
        self.currentPotion = 0
        self.currentSpell = 0
        
        # Initialize the Spell Sprites location
        self.spellx = 5000
        self.spelly = 5000
        
       
        # Initialize the spell sprite
        self.currentSpellSprite = pygame.sprite.Sprite()
        self.currentSpellSprite.image = pygame.Surface([11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION])
        self.currentSpellSprite.image = Blank
        self.currentSpellSprite.image.set_colorkey(COLORKEY)
        self.currentSpellSpritex = WINDOW_WIDTH - 23 * WINDOW_MAGNIFICATION
        self.currentSpellSpritey =  10 * WINDOW_MAGNIFICATION
        self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite.image, 
                                                         (11 * WINDOW_MAGNIFICATION,
                                                           15 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentSpellSprite, (self.currentSpellSpritex, self.currentSpellSpritey))
       
        # Initialize the SwordTip Sprites Location
        self.swordx = 5000
        self.swordy = 5000
        
        # Initialize the sword sprite for attacking
        self.currentSwordSprite = pygame.sprite.Sprite()
        self.currentSwordSprite.image = pygame.Surface([16 * WINDOW_MAGNIFICATION, 9 * WINDOW_MAGNIFICATION])
        self.currentSwordSprite.image = Blank
        self.currentSwordSprite.image.set_colorkey(COLORKEY)
        self.currentSwordSpritex = 0
        self.currentSwordSpritey =  0
        self.currentSwordSprite = pygame.transform.scale(self.currentSwordSprite.image,
                                                     (16 * WINDOW_MAGNIFICATION, 9 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentSwordSprite, (self.currentSwordSpritex, self.currentSwordSpritey))
        
        # Initialize the Interact Sprites Location
        self.interactx = 5000
        self.interacty = 5000
        
        # Initialize the interact sprite for interacting
        self.currentInteractSprite = pygame.sprite.Sprite()
        self.currentInteractSprite.image = pygame.Surface([16 * WINDOW_MAGNIFICATION,
                                                            21 * WINDOW_MAGNIFICATION])
        self.currentInteractSprite.image = Blank
        self.currentInteractSprite.image.set_colorkey(COLORKEY)
        self.currentInteractSpritex = 0
        self.currentInteractSpritey =  0
        self.currentInteractSprite = pygame.transform.scale(self.currentInteractSprite.image,
                                                     (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentInteractSprite, (self.currentInteractSpritex, self.currentInteractSpritey))
       
        # This sets the image to be the Angel surface defined above.
        self.image = pygame.Surface([16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION])
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
        self.mana =  50
        
        # Set the player's current money
        self.money = 0
        
        # Set the player's current quest 
        self.quest = "" 
        
        # Set the player's current Armor
        self.armor = "Wood"
        
        # Set the player's inventory
        self.inventory = [["Wood Armor", 1], ["Steel Armor", 0], ["Gold Armor", 0], ["Fireball Spell", 0],
                           ["Explosion Spell",0], ["Boss Key",0], ["Health Potion",0],
                            ["Lesser Health Potion",0], ["Mana Potion",0], ["Lesser Mana Potion",0]]
        
        
        # Set the players position in the world
        self.worldx = WORLD_WIDTH // 2
        self.worldy = (WORLD_HEIGHT * 5) // 6
        
        # Scale the image by the window magnification
        self.image = pygame.transform.scale(self.image,
                                             (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
        
        # Create a timer to keep track of spell longevity
        self.timer = 0
        
        # Initialize the elapsed variable
        self.elapsed = 0
        
        # Initialize what room the player is in currently
        self.room = 3
        
        # Initialize the defense and attack for the player
        self.defense = 1
        self.attack = 10
        
        # Initialize the counters for enemy kills
        self.rockTurtles = 13
        self.snakes = 0
        
        
    def update(self):
        """ Update the player location. """
        # Update a rect to be used in spell collision detection
        
        self.rect.x = self.x
        self.rect.y = self.y  
        
    def draw(self):
        """ Draw the Player sprite onto the back buffer. """
        
        # Scale the player's sprite and copy it to back buffer
        Angel = pygame.transform.scale(self.image, (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
        screen.blit(Angel,[self.x, self.y] )
        
        # Allow the spell sprite to exist for a few seconds
        previousElapsed = self.elapsed
        self.elapsed = pygame.time.get_ticks()
        self.timer += ((self.elapsed - previousElapsed)/100)
        if(self.timer < 3):
            self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite,
                                                     (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
            screen.blit(self.currentSpellSprite, (self.spellx, self.spelly))
        else:
            # Once time is up, move the sprite far away where it can't collide anymore
            self.spellx = 5000
            self.spelly = 5000
        
        # Change the dimensions of the swordtip sprite depending on the attack directions.    
        if self.direction == "RIGHT" or self.direction == "LEFT":
            magx = 9 * WINDOW_MAGNIFICATION 
            magy = 16 * WINDOW_MAGNIFICATION
        else: 
            magx = 16 * WINDOW_MAGNIFICATION 
            magy = 9 * WINDOW_MAGNIFICATION
            
        # Limit the time the player attacks. 
        if(self.timer < 3):
            self.currentSwordSprite = pygame.transform.scale(self.currentSwordSprite, (magx, magy))
            print(self.swordx, self.swordy)
            screen.blit(self.currentSwordSprite, (self.swordx, self.swordy))
        else: 
            # Once time is up, move the sword sprite far away
            self.changePlayerDirection(self.direction)
            self.swordx = 5000
            self.swordy = 5000
            
        screen.blit(self.currentInteractSprite, (self.interactx, self.interacty))
    def changePlayerDirection(self, direction):
        """ Change the player's sprite based on what direction the player\ moved and what armor they have. """
        
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
        self.image = pygame.transform.scale(self.image,
                                             (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
        self.image.set_colorkey(COLORKEY)
        

    def attackEnemy(self):
        """ Allow the player to attack. """
       
        # Depending on what direction and armor the player is in, change the sprites needed to attack.         
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
        
        # Depending on the user's direction change the location of the swordtip used in collision detection
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
        self.image = pygame.transform.scale(self.image, (9 * WINDOW_MAGNIFICATION, 16 * WINDOW_MAGNIFICATION))
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
        self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite, 
                                                        (11 * WINDOW_MAGNIFICATION + 1,
                                                        15 * WINDOW_MAGNIFICATION + 1))
        self.currentSpellSprite.set_colorkey(COLORKEY)
        
        # Reset the timer
        self.timer = 0
        
    def usePotion(self):
        """ This function allows the player to consume a potion and have it heal them or restore mana. """
        
        # Assume the player has no potions
        hasPotions = False
        
        # Grab the inventory slots of each potion
        potionInventory = [self.inventory[6][1], self.inventory[7][1], self.inventory[8][1], 
                           self.inventory[9][1]]
        
        # Check if the player has any potions at all. 
        for i in range(len(potionInventory)):
            if(potionInventory[i] >= 1):
                hasPotions = True
                
        # If they have potions check which one is selected ad use it.
        if hasPotions:
            if(potionInventory[self.currentPotion] > 0):
                
                # Decrement the number of potions the player has.
                self.inventory[self.currentPotion + 6][1] -= 1
                
                # Find the name of the potion we used and restore mana or health. 
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
        """ This function will allow the player to interact with certain tiles. """
        
        # This sets the image to be a Blank surface defined above.
        self.image = pygame.Surface([16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION])
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
        
class Enemy(pygame.sprite.Sprite):
    """ This class represents the enemy. The enemy can attack and move around the world. """
    
    def __init__(self, x, y): 
        """ Constructs the enemy object and Initializes variables. """
        
        # This calls the superconstructor
        super().__init__()
        
        # This sets the image to be the Snake surface defined above.
        self.image = pygame.Surface([25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION])
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
        
        # Initialize how close the player must be before the enemy starts to chase.
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
        
        # Initialize what direction the enemy is from the player's point of view. 
        self.sector = "TOP LEFT"
        
        # Initialize health, defense and attack
        self.health = 100
        self.defense = 1
        self.attackDamage = 10
        self.spellDefense = 1
        
    def update(self, player):
        """ Updates the Enemy's variables """
        
        # Calculate the distance from the player. 
        self.distancePlayerx = self.rect.x - player.rect.x
        self.distancePlayery = self.rect.y - player.rect.y
        self.distancePlayer = hypot(self.distancePlayerx, self.distancePlayery)
        
        # Allow the spell sprite to exist for a few seconds
        self.dt = self.clock.tick()
        self.elapsed += self.dt
        if(self.elapsed > 200):
            self.distancePlayerx = self.rect.x - player.rect.x
            self.distancePlayery = self.rect.y - player.rect.y
            self.distancePlayer = hypot(self.distancePlayerx, self.distancePlayery)
        
            # If the enemy is within aggroRange we chase after them, otherwise, the enemy wanders randomly. 
            if(self.distancePlayer > self.aggroRange):
                self.wander()
            else:
                self.attack()
                
        # Update where to set the image. 
        self.rect.x = self.x
        self.rect.y = self.y
        self.playerx1 = player.x
        self.playery1 = player.y
        self.playerx2 = player.x + (16 * WINDOW_MAGNIFICATION)
        self.playery2 = player.y + (21 * WINDOW_MAGNIFICATION)
        
    def draw(self, screen): 
        """ Draw the sprites in their new positions """
        Enemy = pygame.transform.scale(self.image, (25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION))
        screen.blit(Enemy,[self.x, self.y] )

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
            self.y += self.walkRate 
        elif self.direction == "UP":
            self.image = Snake_Back_1
            self.y -= self.walkRate
        elif self.direction == "RIGHT":
            self.image = Snake_Right_1
            self.x += self.walkRate
        elif self.direction == "LEFT":
            self.image = Snake_Left_1
            self.x -= self.walkRate
            
        # Rescale and set the background to be translucent
        self.image = pygame.transform.scale(self.image, 
                                            (25 * WINDOW_MAGNIFICATION , 25 * WINDOW_MAGNIFICATION ))
        self.image.set_colorkey(COLORKEY)
        
        # Reset the clock
        self.elapsed = 0
        
    def attack(self):
        """ Allows the enemy to attack. """  
        
        # Change the sector, image, and update the coordinates to reach the player. 
        if(self.x < self.playerx2 and self.x > self.playerx1 and self.y > self.playery2):
            self.sector = "BOTTOM"
            self.y -= self.walkRate
            self.image = Snake_Back_1
        elif(self.y < self.playery2 and self.y > self.playery1 and self.x < self.playerx1):
            self.sector = "LEFT"
            self.x += self.walkRate
            self.image = Snake_Right_1
        elif(self.y < self.playery2 and self.y > self.playery1 and self.x > self.playerx2):
            self.sector = "RIGHT"
            self.x += self.walkRate
            self.y += self.walkRate
            self.image = Snake_Left_1
        elif(self.x > self.playerx1 and self.x < self.playerx2 and self.y < self.playery1):
            self.sector = "UP"
            self.x += self.walkRate
            self.y += self.walkRate
            self.image = Snake_Forward_1
        elif(self.x < self.playerx1 and self.y < self.playery2):
            self.sector = "UP LEFT"
            self.x += self.walkRate
            self.y += self.walkRate
            self.image = Snake_Forward_1 
        elif(self.x < self.playerx1 and self.y > self.playery2):
            self.sector = "BOTTOM LEFT"
            self.x += self.walkRate
            self.y -= self.walkRate
            self.image = Snake_Back_1
        elif(self.x > self.playerx2 and self.y > self.playery2):
            self.sector = "BOTTOM RIGHT"
            self.x -= self.walkRate
            self.y -= self.walkRate
            self.image = Snake_Back_1
        elif(self.x < self.playerx2 and self.y < self.playery1):
            self.sector = "UP RIGHT"
            self.x -= self.walkRate
            self.y += self.walkRate
            self.image = Snake_Forward_1
       
        # Rescale the image and set the background to translucent
        self.image = pygame.transform.scale(self.image,
                                             (25 * WINDOW_MAGNIFICATION , 25 * WINDOW_MAGNIFICATION ))
        self.image.set_colorkey(COLORKEY)
        
        # Reset the clock
        self.elapsed = 0
        
class FeedbackSystem( ):      
    """ This class represents the Feedback system that displays health, mana, potions, spells, 
    current quest, and currency"""
    
    def __init__(self, player):
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
        
        # Set the player's ammount of money
        self.money = player.money
        
        # Initialize a copy of the player's inventory
        self.inventory = player.inventory
        
        # Initialize the coin Image
        self.coin_Image = pygame.sprite.Sprite()
        self.coin_Image.image = pygame.Surface([15 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION])
        self.coin_Image.image = Coin
        self.coin_Image.image.set_colorkey(COLORKEY)
        self.coin_Imagex = 10
        self.coin_Imagey = WINDOW_HEIGHT - 40
        self.coin_Image = pygame.transform.scale(self.coin_Image.image,
                                                  (15 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.coin_Image, (self.coin_Imagex, self.coin_Imagey))

        
        # Initialize the amount of money the player has
        money = str(self.money)
        money = "X " + money
        self.moneyText = self.font.render(money, True, WHITE)
        screen.blit(self.moneyText, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 150))
        
        # Initialize and draw the frame used for displaying the current potion
        self.potion_Frame = pygame.sprite.Sprite()
        self.potion_Frame.image = pygame.Surface([15 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION])
        self.potion_Frame.image = Potion_Frame
        self.potion_Frame.image.set_colorkey(COLORKEY)
        self.potion_Framex = WINDOW_WIDTH - 100
        self.potion_Framey =  10
        self.potion_Frame = pygame.transform.scale(self.potion_Frame.image,
                                         (15 * (WINDOW_MAGNIFICATION + 1), 15 * (WINDOW_MAGNIFICATION + 1)))
        screen.blit(self.potion_Frame, (self.potion_Framex, self.potion_Framey))
        
        # Initialize and draw the frame used for displaying the current spell
        self.spell_Frame = pygame.sprite.Sprite()
        self.spell_Frame.image = pygame.Surface([11 * WINDOW_MAGNIFICATION, 19 * WINDOW_MAGNIFICATION])
        self.spell_Frame.image = Spell_Frame
        self.spell_Frame.image.set_colorkey(COLORKEY)
        self.spell_Framex = WINDOW_WIDTH - 25 * WINDOW_MAGNIFICATION
        self.spell_Framey =  2 * WINDOW_MAGNIFICATION
        self.spell_Frame = pygame.transform.scale(self.spell_Frame.image,
                                         (11 * (WINDOW_MAGNIFICATION + 1), 19 * (WINDOW_MAGNIFICATION + 1)))
        screen.blit(self.spell_Frame, (self.spell_Framex, self.spell_Framey))
    
        # Initialize and draw the spell Sprite used for displaying the current spell
        self.currentSpellSprite = pygame.sprite.Sprite()
        self.currentSpellSprite.image = pygame.Surface([11 * WINDOW_MAGNIFICATION, 19 * WINDOW_MAGNIFICATION])
        self.currentSpellSprite.image = Blank
        self.currentSpellSprite.image.set_colorkey(COLORKEY)
        self.currentSpellSpritex = WINDOW_WIDTH - 23 * WINDOW_MAGNIFICATION
        self.currentSpellSpritey =  10 * WINDOW_MAGNIFICATION
        self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite.image,
                                                     (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentSpellSprite, (self.currentSpellSpritex, self.currentSpellSpritey))
       
        # Initialize and draw the potion Sprite used for displaying the current potion
        self.currentPotionSprite = pygame.sprite.Sprite()
        self.currentPotionSprite.image = pygame.Surface([11 * WINDOW_MAGNIFICATION,
                                                          19 * WINDOW_MAGNIFICATION])
        self.currentPotionSprite.image = Blank
        self.currentPotionSprite.image.set_colorkey(COLORKEY)
        self.currentPotionSpritex = WINDOW_WIDTH - 90
        self.currentPotionSpritey =  20
        self.currentPotionSprite = pygame.transform.scale(self.currentPotionSprite.image,
                                                     (11 * WINDOW_MAGNIFICATION , 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentPotionSprite, (self.currentPotionSpritex, self.currentPotionSpritey))
        
        # These 2 lines update the display frames for spells and potions. 
        self.switchPotionRight(player)
        self.switchSpellLeft(player)
    def update(self, player):
        """ Updates the information needed to run the feedbacksystem. """
        
        
        self.max_Health = player.max_Health
        self.max_Mana = player.max_Mana
        self.health = player.health
        self.mana = player.mana
        self.money = player.money
        self.currentQuest = player.quest
        self.inventory = player.inventory
        self.potion_Number = player.inventory[self.currentPotion + 6][1]
        
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
        
        # Initialize the text used to display how much mana the player has.
        manaText = str(self.mana) + "/" + str(self.max_Mana)
        self.manaText = self.font2.render(manaText, True, BLACK)
        
        # Draw all the sprites needed to the screen
        screen.blit(self.coin_Image, (self.coin_Imagex, self.coin_Imagey))
        screen.blit(self.moneyText, (self.coin_Imagex + 40, self.coin_Imagey + 5))
        screen.blit(self.potion_Frame, (self.potion_Framex, self.potion_Framey))
        screen.blit(self.spell_Frame, (self.spell_Framex, self.spell_Framey))
        screen.blit(self.currentSpellSprite, (self.currentSpellSpritex, self.currentSpellSpritey))
        screen.blit(self.currentPotionSprite, (self.currentPotionSpritex, self.currentPotionSpritey))
        screen.blit(potionText, (self.potion_Framex + 30, self.potion_Framey + 30))
        pygame.draw.rect(screen, GRAY, [10,10,self.max_Health * WINDOW_MAGNIFICATION,
                                         5 * WINDOW_MAGNIFICATION])
        pygame.draw.rect(screen, RED, [10,10,self.health * WINDOW_MAGNIFICATION,
                                        5 * WINDOW_MAGNIFICATION])
        screen.blit(self.healthText, (self.max_Health - 10, 8))
        pygame.draw.rect(screen, GRAY, [10,20,self.max_Mana * WINDOW_MAGNIFICATION,
                                         5 * WINDOW_MAGNIFICATION])
        pygame.draw.rect(screen, LIGHTBLUE, [10,20,self.mana * WINDOW_MAGNIFICATION,
                                              5 * WINDOW_MAGNIFICATION])
        screen.blit(self.manaText, (self.max_Mana - 10, 18))
        
    def switchPotionRight(self, player):
        """ Switches the potion selection forward. """
        
        # Assume the player has no potions
        hasPotions= False
        
        # Initialize the inventory
        inventory = player.inventory
        
        # Retrieve all the information about the potions
        potionInventory = [inventory[6][1], inventory[7][1], inventory[8][1], inventory[9][1]]
        
        # Check if the player has any potions
        for i in range(len(potionInventory)):
            if(potionInventory[i] >= 1):
                hasPotions = True
                
        # If the player has potions we will check to see if we have any other ones. 
        if hasPotions:        
            
            # Start the while loop
            startPoint = self.currentPotion + 1
            started = False
            while self.currentPotion != startPoint:
                if(not started): 
                    startPoint = self.currentPotion 
                started = True
                # Cycle through each potion until we find one the player has or we wind up where we started. 
                self.currentPotion += 1 
                if self.currentPotion > 3:
                    self.currentPotion = 0
                if potionInventory[self.currentPotion] > 0:
                    player.currentPotion = self.currentPotion
                    self.potion_Number = player.inventory[self.currentPotion + 6][1]
                    break
                
            # Check what potion is selected
            if inventory[self.currentPotion + 6][0] == "Health Potion":
                self.currentPotionSprite = Health_Potion
            elif inventory[self.currentPotion + 6][0] == "Lesser Health Potion":
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
        self.currentPotionSprite = pygame.transform.scale(self.currentPotionSprite,
                                                     (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentPotionSprite.set_colorkey(COLORKEY)
        
    def switchPotionLeft(self, player):
        """ Switches the potion selection backward. """
        
        # Assume the player has no potions
        hasPotions= False
        
        # Initialize the inventory
        inventory = player.inventory
        
        # Retrieve all the information about the potions
        potionInventory = [inventory[6][1], inventory[7][1], inventory[8][1], inventory[9][1]]
        
        # Check if the player has any potions
        for i in range(len(potionInventory)):
            if(potionInventory[i] >= 1):
                hasPotions = True
                
        # If the player has potions we will check to see if we have any other ones. 
        if hasPotions:        
            
            # Start the while loop
            startPoint = self.currentPotion + 1
            started = False
            while self.currentPotion != startPoint:
                if(not started): 
                    startPoint = self.currentPotion 
                started = True
                
                # Cycle through each potion until we find one the player has or we wind up where we started. 
                self.currentPotion -= 1 
                if self.currentPotion < 0:
                    self.currentPotion = 3
                if potionInventory[self.currentPotion] > 0:
                    player.currentPotion = self.currentPotion
                    self.potion_Number = player.inventory[self.currentPotion + 6][1]
                    break
                
            # Check what potion is selected
            if inventory[self.currentPotion + 6][0] == "Health Potion":
                self.currentPotionSprite = Health_Potion
            elif inventory[self.currentPotion + 6][0] == "Lesser Health Potion":
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
        self.currentPotionSprite = pygame.transform.scale(self.currentPotionSprite,
                                                     (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentPotionSprite.set_colorkey(COLORKEY)
        
    def switchSpellLeft(self, player):
        """ Switches the spell selection backward. """
        
        # Set the spellSprite far off screen
        player.spellx = 5000
        player.spelly = 5000
        
        # Assume the player has no spells
        hasSpells= False
        
        # initialize a copy of the player's inventory
        inventory = player.inventory
        
        # Retrieve all the information about the spells
        spellInventory = [inventory[3][1], inventory[4][1]]
        
        # Check if the player has any spells
        for i in range(len(spellInventory)):
            if(spellInventory[i] >= 1):
                hasSpells = True
                
        # If the player has spells we will check to see if we have any other ones. 
        if hasSpells:        
            
            # Start the while loop
            startPoint = self.currentSpell + 1
            started = False
            while self.currentSpell != startPoint:
                if(not started): 
                    startPoint = self.currentSpell 
                started = True
                
                # Cycle through each spell until we find one the player has or we wind up where we started. 
                self.currentSpell -= 1 
                if self.currentSpell < 0 :
                    self.currentSpell = 1
                if spellInventory[self.currentSpell] > 0:
                    player.currentSpell = self.currentSpell
                    self.spell_Number = player.inventory[self.currentSpell + 3][1]
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
        self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite,
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
                
        # If the player has spells we will check to see if we have any other ones. 
        if hasSpells:        
            
            # Start the while loop
            startPoint = self.currentSpell + 1
            started = False
            while self.currentSpell != startPoint:
                if(not started): 
                    startPoint = self.currentSpell 
                started = True
                
                # Cycle through each spell until we find one the player has or we wind up where we started. 
                self.currentSpell += 1 
                if self.currentSpell > 1 :
                    self.currentSpell = 0
                if spellInventory[self.currentSpell] > 0:
                    player.currentSpell = self.currentSpell
                    self.spell_Number = player.inventory[self.currentSpell + 3][1]
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
        self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite,
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
        
        # Create the player
        self.player = Player()
        
        # Add a super Enemy with 2 times the attack damage and defensive damage.
        superEnemy = Enemy(450,450)
        superEnemy.defense = 2
        superEnemy.attackDamage = superEnemy.attackDamage * 2
        
        # Add all the enemys for each room. 
        room1 = [Enemy(150,50), Enemy(150, 250), Enemy(300, 250)]
        room2 = [Enemy(100, 200), Enemy(500, 100), Enemy(150, 300), Enemy(200, 400), Enemy(500, 350)]
        room4 = [Enemy(150,100), Enemy(300, 100)]
        room5 = [superEnemy]
        room6 = [Enemy(150, 100), Enemy(400, 450), Enemy(600, 350)]
        room7 = [Enemy(150, 100), Enemy(400, 450), Enemy(600, 350)]
        room9 = [Enemy(100, 200), Enemy(500, 100), Enemy(150, 300), Enemy(200, 400), Enemy(500, 350)]
        room12 = [Enemy(600, 200), Enemy(600, 100), Enemy(600, 400), Enemy(400, 200), Enemy(400, 100),
                   Enemy(400, 400), Enemy(200, 200), Enemy(200, 100), Enemy(200, 400), Enemy(200, 200)]
        room14 = [Enemy(100, 200), Enemy(500, 100), Enemy(150, 300), Enemy(200, 400), Enemy(500, 350)]
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
                
        # Create a new feedback System
        self.feedback = FeedbackSystem(self.player)

        # Instantiate  starting variables for event handling
        self.upKeyPressed = False
        self.downKeyPressed = False
        self.rightKeyPressed = False
        self.leftKeyPressed = False
        self.DIRECTION = "UP"
        
        # Instantiate the starting dialog used in interactions
        self.dialog = ""
        
        # Instantiate variables for managing how long dialog is displayed. 
        # Allow the spell sprite to exist for a few seconds
        self.dt = 0
        self.elapsed = 0
        
        # Load in the music files
        pygame.mixer.music.load("Genesis_Sprites/Overworld.mp3")
        
        # Allow the music to play indefinitely
        pygame.mixer.music.play(-1)
        
        # Instantiate progress for NPC interactions
        self.merchant_dialog = 0
        self.old_man_dialog = 0
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
                CAMERA_TOP = ROOM_HEIGHT * 2
                
            # If the game hasn't started yet and the player clicks, advance to the next splash screen
            elif (not self.game_start and event.type == pygame.MOUSEBUTTONDOWN):
                self.splashNumber += 1
                
            # Detect when a key is pressed or held
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP:
                    self.upKeyPressed = True
                    self.downKeyPressed = False
                    
                    # DIRECTION is used later to determine movement direction
                    self.DIRECTION = "UP"
                    self.dialog = ""
                elif event.key == pygame.K_DOWN:
                    self.downKeyPressed = True
                    self.upKeyPressed = False
                    self.DIRECTION = "DOWN"
                    self.dialog = ""
                elif event.key == pygame.K_RIGHT:
                    self.rightKeyPressed = True
                    self.leftKeyPressed = False
                    self.DIRECTION = "RIGHT"
                    self.dialog = ""
                elif event.key == pygame.K_LEFT:
                    self.rightKeyPressed = False
                    self.leftKeyPressed = True
                    self.DIRECTION = "LEFT"  
                    self.dialog = ""
                elif event.key == pygame.K_q:
                    if(self.player.currentSpell == 0):
                        if self.player.mana >= 10:
                            self.player.useSpell()
                    if(self.player.currentSpell == 1):
                        if self.player.mana >= 25:
                            self.player.useSpell()                
                elif event.key == pygame.K_e:
                    self.player.usePotion()
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
                    self.player.interact()
                print(self.dialog)       
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
                        
        # If any directional key was pressed we now calculate the player's new coordinates
        if self.upKeyPressed or self.downKeyPressed or self.leftKeyPressed or self.rightKeyPressed:
            
            # Change the player sprite to match player direction
            self.player.changePlayerDirection(self.DIRECTION)

            # Actually move the position of the player
            # If the player exits the room we move to the next one. 
            if self.DIRECTION == "UP":
                self.player.y -= WALKRATE
                self.player.worldy -= WALKRATE
                if self.player.worldy < 0:
                    self.player.worldy = 0
                    self.player.worldy += WALKRATE
                elif self.player.y < 0:
                    self.player.y = WINDOW_WIDTH - 300
                    CAMERA_TOP -= ROOM_HEIGHT
                    self.player.room += 5

            if self.DIRECTION == "DOWN":
                self.player.y += WALKRATE
                self.player.worldy += WALKRATE
                if self.player.worldy > WORLD_HEIGHT:
                    self.player.worldy = WORLD_HEIGHT - 25 * WINDOW_MAGNIFICATION
                elif self.player.y  > WINDOW_HEIGHT:
                    self.player.y = 0
                    CAMERA_TOP += ROOM_HEIGHT
                    self.player.room -= 5

            if self.DIRECTION == "LEFT":
                self.player.x -= WALKRATE
                self.player.worldx -= WALKRATE
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
                if self.player.x  > WINDOW_WIDTH :
                    self.player.x = 0 
                    CAMERA_LEFT += ROOM_WIDTH
                    self.player.room -= 1
                if self.player.worldx + 25 > WORLD_WIDTH:
                    self.player.worldx = WORLD_WIDTH - 25
                    self.player.worldx -= WALKRATE
            
        return False
 
    
             
    def getRoomSurface(self, leftPixel, topPixel, tileData):
        """
        This method is used to fetch all tiles in a single room and expand them for easier viewing. 
        It is a great space optimization. 
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
                
                roomSurf.blit(tile.getTile(tile_number), ((tilex - leftmostTile) * 25,
                                                           (tiley - topmostTile) * 25))
               
                # Check if the tile at tilex and tiley is a boundary, burnable, or explodable
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
        roomSurf = pygame.transform.scale(roomSurf, (ROOM_WIDTH * WINDOW_MAGNIFICATION,
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
        self.feedback.update(self.player)
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
            
            # Update the player sprite
            self.player.update()
            
            # Check if there are any collisions between th eplayer and a boundary tile.
            bump_list = spritecollide(self.player, self.all_boundaries_Group, False)
            
            # If there is than we have to move the player back to where they were
            if(len(bump_list) >= 1):
                
                # Based on the direction we last moved the sprite in, move the sprite back.
                if(self.DIRECTION == "UP"):
                    self.player.y += WALKRATE
                    self.player.worldy += WALKRATE
                elif (self.DIRECTION == "DOWN"):
                    self.player.y -= WALKRATE
                    self.player.worldy -= WALKRATE
                elif (self.DIRECTION == "RIGHT"):
                    self.player.x -= WALKRATE 
                    self.player.worldx  -= WALKRATE
                elif (self.DIRECTION == "LEFT"):
                    self.player.x += WALKRATE
                    self.player.worldx += WALKRATE
            else: 
                
                # Set the new position of the player. 
                self.player = player
                
            # Get a list of all the enemies that collide with boundaries
            enemy_collision_list = groupcollide(group, self.all_boundaries_Group, False, False)
            
            # If there is than we have to move the enemy back to where they were
            if(len(enemy_collision_list) >= 1):
                for enemy in enemy_collision_list:
                    # Based on the direction we last moved the sprite in, move the sprite back.
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

            # Check to see collisions between the player and enemies in the current room
            player_collision_list = spritecollide(self.player, group, False)
            
            # If there are any collisions we knock the player backwards. 
            for enemy in player_collision_list:
                if(enemy.sector == "UP"):
                    self.player.y += 25 * WINDOW_MAGNIFICATION
                elif(enemy.sector == "DOWN"):
                    self.player.y -= 25 * WINDOW_MAGNIFICATION
                elif(enemy.sector == "RIGHT"):
                    self.player.x -= 25 * WINDOW_MAGNIFICATION
                elif(enemy.sector == "LEFT"):
                    self.player.x += 25 * WINDOW_MAGNIFICATION
                elif(enemy.sector == "UP LEFT"):
                    self.player.x += 25 * WINDOW_MAGNIFICATION
                    self.player.y += 25 * WINDOW_MAGNIFICATION
                elif(enemy.sector == "UP RIGHT"):
                    self.player.x -= 25 * WINDOW_MAGNIFICATION
                    self.player.y += 25 * WINDOW_MAGNIFICATION
                elif(enemy.sector == "DOWN LEFT"):
                    self.player.x += 25 * WINDOW_MAGNIFICATION
                    self.player.y -= 25 * WINDOW_MAGNIFICATION
                elif(enemy.sector == "DOWN RIGHT"):
                    self.player.x -= 25 * WINDOW_MAGNIFICATION
                    self.player.y -= 25 * WINDOW_MAGNIFICATION
                    
                # Take away health from the player
                self.player.health -= enemy.attackDamage // self.player.defense

            # Create a Rect to be used in attack collision detection
            swordTipRect = pygame.sprite.Sprite()
            if self.player.direction == "RIGHT" or self.player.direction == "LEFT":
                swordTipRect.image = pygame.Surface([9 * WINDOW_MAGNIFICATION, 16 * WINDOW_MAGNIFICATION])
            else: 
                swordTipRect.image = pygame.Surface([16 * WINDOW_MAGNIFICATION, 9 * WINDOW_MAGNIFICATION])
            swordTipRect.rect = swordTipRect.image.get_rect()
            
            # Move the swordtip's frame 
            swordTipRect.rect.x = self.player.swordx
            swordTipRect.rect.y = self.player.swordy
        
            # Check collisions between the enemies and the tip of the sword.
            attack_enemy_list = spritecollide(swordTipRect, group, False)
            for enemy in attack_enemy_list:
                # Decrement the enemy's health
                enemy.health -= self.player.attack
                if enemy.health <= 0:
                    group.remove(enemy)
                    
            # Check collisions between cuttable tiles and the player's sword. 
            cuttable_list = spritecollide(swordTipRect, self.all_cuttables_Group, False)
            
            # Change the tiles to a changed form. 
            for i in range(len(cuttable_list)):
                    tile = cuttable_list[i]
                    tilex = tile.x
                    tiley = tile.y
                    tileNumber = tile_Data[tiley][tilex]
                    
                    # If it does, replace the exploded tiles with the new tile
                    if(tileNumber == "44"):
                        tile_Data[tiley][tilex] = "1"
            
            # Create a rect to be used for checking collisions with interactive tiles
            interactRect = pygame.sprite.Sprite()
            interactRect.image = pygame.Surface([16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION])
            interactRect.rect = interactRect.image.get_rect()
            interactRect.rect.x = self.player.interactx
            interactRect.rect.y = self.player.interacty
            
            # Check to see if the interaction sprite collides with interactive tiles.
            interacted_list = spritecollide(interactRect, self.all_interactive_Group, False)
            
            # Change the tiles to a changed form after interacting with it 
            # This will also set dialog depending on the coordinates and room.
            for i in range(len(interacted_list)):
                tile = interacted_list[i]
                tilex = tile.x
                tiley = tile.y
                tileNumber = tile_Data[tiley][tilex]
                coords = (tile.x, tile.y)
                room = self.player.room
                
                # Depending on the room and tile that is interacted with, change the dialog.
                if(room == 3):
                    if(coords == (38,23)):
                        self.dialog = "Press Right Shift to attack"
                elif(room == 4):
                    if(coords == (30,31)):
                        self.dialog = "You found 5 Health Potions!"
                        self.player.inventory[6][1] += 5
                        tile_Data[31][30] = 60
                elif(room == 7):
                    if(coords == (61,14)):
                        self.dialog = "A rockslide has blocked this path! Sorry for the inconvenience!"
                elif(room == 8):
                    if(coords == (38,18)):
                        self.dialog = "North - Clocktower, South - Glade"
                    if(coords == (34,18)):
                        if self.merchant_dialog == 0:
                            self.dialog = "Hey there! I'll sell you a health potion for 10 coins. Just talk to me again."
                            self.merchant_dialog += 1
                        else: 
                            if(self.player.money >= 10):
                                self.player.money -= 10
                                self.player.inventory[6][1] += 1
                                self.dialog = "Thanks for the business!"
                            else:
                                self.dialog = "Sorry you dont have enough coins!"
                elif(room == 9):
                    if(coords == (17,14)):
                        self.dialog = "Please do not go any further, danger ahead"
                elif(room == 10):
                    if(coords == (7,14)):
                        self.dialog = "PLEASE DONT GO ANY FURTHER"
                    elif(coords == (6,17)):
                        self.dialog = "I MEAN IT"
                    elif(coords == (6,20)):
                        self.dialog = "DONT SAY I DIDNT WARN YOU"
                    
                elif(room == 11):
                    if(coords == (70,2)):
                        self.old_man_dialog += 1
                        if self.old_man_dialog == 0:
                            self.dialog = "Hey! I bet youre here for the clocktower key right?"
                            self.old_man_dialog += 1
                        elif self.old_man_dialog == 1:
                            self.dialog = "Well, first youll have to do a couple of favors for me."
                            self.old_man_dialog += 1
                        elif self.old_man_dialog == 2:
                            self.dialog = "You may have noticed there are a lot of snakes around here."
                            self.old_man_dialog += 1
                        elif self.old_man_dialog == 3:
                            self.dialog = "I need you to get rid of 20 of them for me."
                            self.old_man_dialog += 1
                        elif self.old_man_dialog == 4:
                            if(self.player.snakes < 20):
                                self.dialog = "Go out there and kill those snakes!"
                            elif(self.player.snakes >= 20):
                                self.dialog = "Nice Job!"
                                self.old_man_dialog += 1
                        elif self.old_man_dialog == 5:
                            self.dialog = "Here's the key, but I have another offer for you!."
                            self.old_man_dialog += 1
                        elif self.old_man_dialog == 6:
                            self.dialog = "You may have noticed some rock mimics here or there."
                            self.old_man_dialog += 1
                        elif self.old_man_dialog == 7:
                            self.dialog = "I need you to get rid of all 13 of them for me."
                            self.old_man_dialog += 1
                        elif self.old_man_dialog == 8:
                            self.dialog = "There's some shiny new armor in it for you!"
                            self.old_man_dialog += 1
                        elif self.old_man_dialog == 9:
                            if(self.player.snakes < 20):
                                self.dialog = "Go out there and kill those mimics!"
                            elif(self.player.rockTurtles <= 0):
                                self.dialog = "Nice Job, now i can sleep soundly with my eyes open!"  
                                self.old_man_dialog += 1 
                        else: 
                                self.dialog = "Zzz"  
                elif(room == 13):
                    if(coords == (39,3)):
                        self.dialog = "Clocktower is closed for maintenance. See Old Man for the key"
                    elif(coords == (40,3)):
                        if(self.player.inventory[5][1] == 1):
                            tile_Data[3][40] = "42"
                            self.dialog = "Door Opened"
                        else: 
                            self.dialog = "Door is locked"
                elif(room == 15):
                    if(coords == (6,1)):
                        self.dialog = "REMINDER: Use A and D to switch between potions and E to use them"
                    elif(coords == (7,1)):
                        self.dialog = "You found 5 Lesser Health Potions and 5 Lesser Mana Potions!"
                        self.player.inventory[9][1] += 5
                        self.player.inventory[7][1] += 5
                        tile_Data[1][7] = 60    
                    elif(coords == (8,1)):
                        self.dialog = "You found the Fireball Spell!" 
                        self.player.inventory[3][1] += 1
                        tile_Data[1][8] = 60                    
                    elif(coords == (9,1)):
                        self.dialog = "REMINDER: Use W and S to switch between potions and Q to use them"
                    
                    
            # Create a rect to be used in spell collision detection
            spellRect = pygame.sprite.Sprite()
            spellRect.image = pygame.Surface([11 * WINDOW_MAGNIFICATION, 16 * WINDOW_MAGNIFICATION])
            spellRect.rect = spellRect.image.get_rect()
            spellRect.rect.x = self.player.spellx
            spellRect.rect.y = self.player.spelly
            
            # Check to see if the fire spell collides with burnable objects
            if(self.player.currentSpell == 0):
                spell_burn_collision_list = spritecollide(spellRect, self.all_burnables_Group, False)
                for i in range(len(spell_burn_collision_list)):
                    tile = spell_burn_collision_list[i]
                    tilex = tile.x
                    tiley = tile.y
                    tileNumber = tile_Data[tiley][tilex]
                    
                    # If it does, replace the burned tiles with the new tile. 
                    if(tileNumber == "44"):
                        tile_Data[tiley][tilex] = "1"
                        
            # Check to see if the explosion spell collides with explodable objects
            if(self.player.currentSpell  == 1):
                spell_explode_collision_list = spritecollide(spellRect, self.all_explodables_Group, False)
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
                            self.player.rockTurtles -= 1
                    elif(tileNumber == "48"):
                        tile_Data[tiley][tilex] = "2"
                    elif(tileNumber == "55"):
                        tile_Data[tiley][tilex] = "3"
                    
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
                enemy.health -= spellDamage // enemy.spellDefense
                
                # Depending on the direction the player faces, the spell knocks back the enemy.
                if (self.player.direction == "LEFT"):
                    enemy.x -= 25 * WINDOW_MAGNIFICATION
                elif (self.player.direction == "RIGHT"):
                    enemy.x += 25 * WINDOW_MAGNIFICATION
                elif (self.player.direction == "UP"):
                    enemy.y -= 25 * WINDOW_MAGNIFICATION
                elif (self.player.direction == "DOWN"):
                    enemy.y += 25 * WINDOW_MAGNIFICATION
                    
                # If an enemy's health dies we increment the counter to be used in quests. 
                if enemy.health <= 0:
                    self.room1_enemies_Group.remove(enemy)
                    self.player.snakes += 1
                    
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
            
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        
        # Clear the screen to White
        screen.fill(WHITE)
        
        # If the game hasnt ended and the game has started draw he sprites
        if(not self.game_over and self.game_start):
            
            # Instantiate the font needed
            font = pygame.font.Font("SILKWONDER.ttf", 25)
            
            # Create a new surface for the current room
            roomSurface = self.getRoomSurface(CAMERA_LEFT, CAMERA_TOP, tile_Data)
            
            # Copy the background image to the viewport.
            screen.blit(roomSurface, (0,0))
            
            # Draw each of the sprites in the all_sprites_Group
            self.all_sprites_Group.draw(screen)
            
            # Draw the player
            self.player.draw()
            
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
            
            # Draw the dialog onto the screen. 
            dialog_text = font.render(self.dialog, True, WHITE)
            screen.blit(dialog_text, (120, WINDOW_HEIGHT - 150))
            # Copy back buffer onto the front buffer
            pygame.display.flip()
            
        # If the game is over display game over screen
        elif(self.game_over):
            
            font = pygame.font.Font("SILKWONDER.ttf", 50)
            text1 = font.render("GAME OVER", True, WHITE)
            playAgain = font.render("Click to play again", True, WHITE)
            screen.fill(BLACK)
            screen.blit(text1, (WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 150))
            screen.blit(playAgain, (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT - 150))
            pygame.display.flip()
            
            # If the game hasn't started yet, display the splash screen
        elif(not self.game_start):
            
            # Display the Splash screen
            if(self.splashNumber == 1):
                font = pygame.font.Font("SILKWONDER.ttf", 50)
                font2 = pygame.font.Font("SILKWONDER.ttf", 20)
                text1 = font.render("Genesis", True, WHITE)
                text2 = font.render("By Bradley Lamitie", True, (WHITE))
                text3 = font.render("Alpha Version (11/14/17)", True, (WHITE))
                continueText = font2.render("Click to continue", True, WHITE)

                screen.fill(BLACK)
                screen.blit(text1, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 150))
                screen.blit(text2, (WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2 - 50))
                screen.blit(text3, (WINDOW_WIDTH//2 - 280, WINDOW_HEIGHT//2 + 50))
                screen.blit(continueText, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 75))
                pygame.display.flip()
                
            # Display the Story screen
            elif(self.splashNumber == 2):
                font = pygame.font.Font("SILKWONDER.ttf", 25)
                font2 = pygame.font.Font("SILKWONDER.ttf", 20)
                text1 = font.render("You play as an angel cast onto Earth", True, WHITE)
                text2 = font.render("after having your wings stripped from you.", True, (WHITE))
                text3 = font.render("Your goal is to defeat all 7 virtues on Earth to redeem yourself",
                                     True, (WHITE))
                text4 = font.render("and earn your place in heaven.", True, (WHITE))
                text5 = font.render("Story:", True, WHITE)
                continueText = font2.render("Click to continue", True, WHITE)

                screen.fill(BLACK)
                screen.blit(text1, (WINDOW_WIDTH//2 - 220, WINDOW_HEIGHT//2 - 170))
                screen.blit(text2, (WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2 - 70))
                screen.blit(text3, (WINDOW_WIDTH//2 - 320, WINDOW_HEIGHT//2 + 30))
                screen.blit(text4, (WINDOW_WIDTH//2 - 175, WINDOW_HEIGHT//2 + 120))
                screen.blit(text5, (WINDOW_WIDTH//2 - 75, 25))

                screen.blit(continueText, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 75))

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
                screen.blit(text3, (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 -150))
                screen.blit(text4, (75, WINDOW_HEIGHT//2 - 100))
                screen.blit(text5, (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 - 100))
                screen.blit(text6, (75, WINDOW_HEIGHT//2 - 50))
                screen.blit(text7, (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 - 50))
                screen.blit(text8, (75, WINDOW_HEIGHT//2 ))
                screen.blit(text9, (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 ))
                screen.blit(text10, (75, WINDOW_HEIGHT//2 + 50))
                screen.blit(text11, (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 + 50))
                screen.blit(continueText, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 75))
                pygame.display.flip()
            else:
                
                # Start the game once we finish
                self.game_start = True
            
def main():
    """ Main program function. """
    global NEWGAME
    
    # Initialize Pygame and set up the window
    pygame.init()
    

    # Set the window title.
    pygame.display.set_caption("My Game")
    
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