"""
Create the main game for "Genesis"
 
Author: Bradley Lamitie
Date: 11/11/2017
Version Number: 1.75

What the Code Does: 
The code so far creates the world using the tiles provided by rendering one room at a time
and zooming in on it to make it more visible. 
Then, the player is put into the world and can use the directional 
keys( UpArrow, RightArrow, LeftArrow, and DownArrow ) to move around the world
The code runs through the events and moves the sprite. 
So far, the game doesnt have any real way to lose or win. 

How to Play: 
The player can use the directional keys( UpArrow, RightArrow, LeftArrow, and DownArrow )
 to move around the world

GitHub Repository: https://github.com/BradleyLamitie/Genesis

Credits: 
Silk Wonderland font by jelloween Found on https://jelloween.deviantart.com/art/Font-SILKY-WONDERLAND-free-45103645
"The White" By RoleMusic found on http://freemusicarchive.org/genre/Chiptune/

Changes in this version: 
- Added more sprites  
- Added Overworld Music
- Added a feedback system
- Added the ability to use and switch between potions
- Added a Splash Screen
- Added a Game Over Screen
- Added ability to switch between Spells

TODOs for  Demo/Final Project: 
- Finish building the world's second level. 
- Make it so that the WORLD_DATA is imported from a .tmx file. 
- If possible import a tileset from a Tiled file. 
- Learn to Use a sprite Sheet to load in sprites. 
- Animate the characters as they move throughout the world. 
- Add enemies with basic AI to fight.
- Replace all clocktower_door sprites with new sprites. 
- Add the ability to use magic and  
- Add ability to interact with things like chests, NPCs, and signposts. 
- Add Save states or a pause function.
- Add a menu.
- Add Sounds.
- Add cheat codes for quick demonstrations.
- Add Screen animations
- Add Collision detection for enemies
- 
"""
import pygame
from pygame.sprite import spritecollide
 
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
WALKRATE = 3

# How many seconds an animation frame should last. 
ANIMRATE = 0.15

# The width and height of the magnified window
WINDOW_WIDTH = ROOM_WIDTH * WINDOW_MAGNIFICATION
WINDOW_HEIGHT = ROOM_HEIGHT * WINDOW_MAGNIFICATION

# The Camera starts at the second room from the right, second room down.
CAMERA_LEFT = ROOM_WIDTH * 2
CAMERA_TOP = ROOM_HEIGHT * 2

# Set the need for a new game to false
global NEWGAME 
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
Map_Image = pygame.image.load("Genesis_Sprites/Genesis_Map.png").convert()

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
22,44,44,45,45,45,45,54,54,45,45,45,45,44,44,21,22,44,44,44,44,44,44,44,44,44,44,44,44,44,48,21,22,41,41,41,41,41,41,41,42,41,41,41,41,41,41,21,22,48,44,44,44,44,44,44,44,44,44,44,44,44,48,21,22,48,48,44,55,55,41,55,55,44,48,48,48,48,48,21
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
22,48,48,44,44,44,44,45,45,45,45,45,45,45,45,48,48,44,44,44,44,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,55,55,55,55,54,54,54,54,54,54,54,54,54,54,54,54,44,21
22,48,44,44,44,44,44,45,45,45,45,45,45,45,45,48,48,44,44,44,44,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,55,55,55,55,54,54,54,54,54,54,54,54,54,54,54,54,44,21
22,44,44,44,44,44,53,45,45,44,44,44,44,44,44,19,20,44,44,44,44,45,45,45,45,45,45,45,45,45,45,19,20,45,45,45,45,45,45,54,54,45,45,45,45,45,45,19,20,45,45,45,45,45,45,45,45,45,45,45,45,45,48,19,20,48,45,45,45,45,45,45,45,45,45,45,44,44,44,21
22,44,44,44,44,44,44,45,45,44,44,44,44,44,48,21,22,48,44,44,44,45,45,45,45,45,45,45,45,45,45,21,22,45,41,45,45,45,53,54,54,45,45,45,45,45,44,21,22,45,44,44,45,45,45,45,45,45,44,44,45,45,48,21,22,48,45,45,45,45,45,45,45,45,45,44,44,44,48,21
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
tile_Data = WORLD_DATA
tile_Data = tile_Data.split('\n')
tile_Data = [line.split(',') for line in tile_Data]

# This list represents the tile numbers of tiles th eplayer shouldn't be able to walk through.
boundary_tiles = [15,16,17,18,19,20,21,22,23,24,25,26,28,29,30,31,32,33,34,35,36,37,40,41,4246,47,48,49,50,51,52,53,55,56,57]

# --- Classes ---
 
class Tile(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
 
    def __init__(self, x, y, leftmostTile, topmostTile):
        """ Constructor, create the image of the block. """
        super().__init__()
        
        # Initialize the tiles size and locations
        self.image = pygame.Surface([25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION])
        self.rect = self.image.get_rect()
        self.x = (x - leftmostTile) * 25 * WINDOW_MAGNIFICATION
        self.y = (y - topmostTile) * 25 * WINDOW_MAGNIFICATION
        self.rect.x = self.x
        self.rect.y = self.y
        
    def getTileNumber(self, x, y):
        """ This function is used to fetch a tileNumber from the tile_Data """
        tileNumber = tile_Data[y][x]
        return tileNumber
    
    def getTile(self, tileNumber):
        """ This function is used to retrieve the sprite surfaces using the tile Number provided. """
        
        # Just in case, ensure tileNumber is an integer.
        tileNumber = int(tileNumber)
        
        # Run through each of the cases.
        if(tileNumber == 16):
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
        else:
            return Signpost_path

    
class Player(pygame.sprite.Sprite):
    # TODO: Player
    """ This class represents the player. """
    def __init__(self):
        super().__init__()
        
        # This sets the player's current spell and potion to be used when using a potion
        self.currentPotion = 0
        self.currentSpell = 0
        
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
        self.rect.y = self.y
        
        # Set the player's max Health and Mana
        self.max_Health = 100
        self.max_Mana = 50
        
        # Set the player's health and mana
        self.health = 25
        self.mana = 0
        
        # Set the player's current money
        self.money = 0
        
        # Set the player's current quest 
        self.quest = "" 
        
        # Set the player's current Armor
        self.armor = "Wood"
        
        # Set the player's inventory
        self.inventory = [["Wood Armor", 1], ["Steel Armor", 0], ["Gold Armor", 0], ["Fireball Spell", 0], ["Explosion Spell",0], ["Boss Key",0], ["Health Potion",1], ["Lesser Health Potion",1], ["Mana Potion",5], ["Lesser Mana Potion",1]]
        
        
        # Set the players position in the world
        self.worldx = WORLD_WIDTH // 2
        self.worldy = (WORLD_HEIGHT * 5) // 6
        
        # Scale the image by the window magnification
        self.image = pygame.transform.scale(self.image, (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
        
        # Copy the player to the screen
        screen.blit(self.image,[self.x, self.y] )

    def update(self):
        """ Update the player location. """
        
        self.rect.x = self.x
        self.rect.y = self.y  
        
    def draw(self):
        """ Draw the Player sprite onto the back buffer. """
        scale = 25 * WINDOW_MAGNIFICATION
        Angel = pygame.transform.scale(self.image, (scale, scale))
        screen.blit(Angel,[self.rect.x, self.rect.y] )
    
    def changePlayerDirection(self, direction):
        """ Change the player's sprite based on what direction the player last moved and what armor they have. """
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
        self.image = pygame.transform.scale(self.image, (16 * WINDOW_MAGNIFICATION, 21 * WINDOW_MAGNIFICATION))
        self.image.set_colorkey(COLORKEY)

    def attack(self):
        # TODO: add ability to attack
        print("HIYA")
        
    def useSpell(self):
        # TODO: add ability to use spells
        print("abracadabra")
        spellInventory = [self.inventory[3][1], self.inventory[4][1]]
        for i in range(len(spellInventory)):
            if(spellInventory[i] >= 1):
                hasSpells = True
        
    def usePotion(self):
        """ This function allows the player to consume a potion and have it heal them or restore mana. """
        # Assume the player has no potions
        hasPotions = False
        
        # Grab the inventory slots of each potion
        potionInventory = [self.inventory[6][1], self.inventory[7][1], self.inventory[8][1], self.inventory[9][1]]
        
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
                        
    def checkInventory(self, item):
        """ Checks the player's inventory to see how many of an item the player has. """
        for i in self.inventory:
            if(item == self.inventory[i][0]):
                return self.inventory[i][1]
            
class FeedbackSystem( ):      
    # TODO: Feedback System
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
        self.coin_Image = pygame.transform.scale(self.coin_Image.image, (15 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
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
        self.potion_Frame = pygame.transform.scale(self.potion_Frame.image, (15 * (WINDOW_MAGNIFICATION + 1), 15 * (WINDOW_MAGNIFICATION + 1)))
        screen.blit(self.potion_Frame, (self.potion_Framex, self.potion_Framey))
        
        # Initialize and draw the frame used for displaying the current spell
        self.spell_Frame = pygame.sprite.Sprite()
        self.spell_Frame.image = pygame.Surface([11 * WINDOW_MAGNIFICATION, 19 * WINDOW_MAGNIFICATION])
        self.spell_Frame.image = Spell_Frame
        self.spell_Frame.image.set_colorkey(COLORKEY)
        self.spell_Framex = WINDOW_WIDTH - 25 * WINDOW_MAGNIFICATION
        self.spell_Framey =  2 * WINDOW_MAGNIFICATION
        self.spell_Frame = pygame.transform.scale(self.spell_Frame.image, (11 * (WINDOW_MAGNIFICATION + 1), 19 * (WINDOW_MAGNIFICATION + 1)))
        screen.blit(self.spell_Frame, (self.spell_Framex, self.spell_Framey))
    
        # Initialize and draw the spell Sprite used for displaying the current spell
        self.currentSpellSprite = pygame.sprite.Sprite()
        self.currentSpellSprite.image = pygame.Surface([11 * WINDOW_MAGNIFICATION, 19 * WINDOW_MAGNIFICATION])
        self.currentSpellSprite.image = Blank
        self.currentSpellSprite.image.set_colorkey(COLORKEY)
        self.currentSpellSpritex = WINDOW_WIDTH - 23 * WINDOW_MAGNIFICATION
        self.currentSpellSpritey =  10 * WINDOW_MAGNIFICATION
        self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite.image, (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentSpellSprite, (self.currentSpellSpritex, self.currentSpellSpritey))
       
        # Initialize and draw the potion Sprite used for displaying the current potion
        self.currentPotionSprite = pygame.sprite.Sprite()
        self.currentPotionSprite.image = pygame.Surface([11 * WINDOW_MAGNIFICATION, 19 * WINDOW_MAGNIFICATION])
        self.currentPotionSprite.image = Blank
        self.currentPotionSprite.image.set_colorkey(COLORKEY)
        self.currentPotionSpritex = WINDOW_WIDTH - 90
        self.currentPotionSpritey =  20
        self.currentPotionSprite = pygame.transform.scale(self.currentPotionSprite.image, (11 * WINDOW_MAGNIFICATION , 15 * WINDOW_MAGNIFICATION))
        screen.blit(self.currentPotionSprite, (self.currentPotionSpritex, self.currentPotionSpritey))
        
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
        pygame.draw.rect(screen, GRAY, [10,10,self.max_Health * WINDOW_MAGNIFICATION, 5 * WINDOW_MAGNIFICATION])
        pygame.draw.rect(screen, RED, [10,10,self.health * WINDOW_MAGNIFICATION, 5 * WINDOW_MAGNIFICATION])
        screen.blit(self.healthText, (self.max_Health - 10, 8))
        pygame.draw.rect(screen, GRAY, [10,20,self.max_Mana * WINDOW_MAGNIFICATION, 5 * WINDOW_MAGNIFICATION])
        pygame.draw.rect(screen, LIGHTBLUE, [10,20,self.mana * WINDOW_MAGNIFICATION, 5 * WINDOW_MAGNIFICATION])
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
            print(inventory[self.currentPotion + 6][0])
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
        self.currentPotionSprite = pygame.transform.scale(self.currentPotionSprite, (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
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
            print(inventory[self.currentPotion + 6][0])
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
        self.currentPotionSprite = pygame.transform.scale(self.currentPotionSprite, (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentPotionSprite.set_colorkey(COLORKEY)
        
    def switchSpellLeft(self, player):
        """ Switches the spell selection backward. """
        
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
            print(inventory[self.currentSpell + 3][0])
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
        self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite, (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentSpellSprite.set_colorkey(COLORKEY)
                
    def switchSpellRight(self, player):
        """ Switches the spell selection backward. """
        
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
                self.currentSpell += 1 
                if self.currentSpell > 1 :
                    self.currentSpell = 0
                if spellInventory[self.currentSpell] > 0:
                    player.currentSpell = self.currentSpell
                    self.spell_Number = player.inventory[self.currentSpell + 3][1]
                    break
                
            # Check what spell iis selected
            print(inventory[self.currentSpell + 3][0])
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
        self.currentSpellSprite = pygame.transform.scale(self.currentSpellSprite, (11 * WINDOW_MAGNIFICATION, 15 * WINDOW_MAGNIFICATION))
        self.currentSpellSprite.set_colorkey(COLORKEY)
                

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """
        
        # Initialize the current splash screen number
        self.splashNumber = 1
        
        # Initialize that the game hasn't ended or started yet
        self.game_over = False
        self.game_start = False
        
        # Initialize the need foor a new game to start
        NEWGAME = False
        
        # Create sprite lists
        self.all_boundaries_Group = pygame.sprite.Group()
        self.all_sprites_Group = pygame.sprite.Group()
        
        # Create the player
        self.player = Player()
        
        # Create a new feedback System
        self.feedback = FeedbackSystem(self.player)

        # Add the player to the sprites group
        self.all_sprites_Group.add(self.player)
        
        # Instantiate  starting variables for event handling
        self.upKeyPressed = False
        self.downKeyPressed = False
        self.rightKeyPressed = False
        self.leftKeyPressed = False
        self.DIRECTION = "UP"
        
        # Load in the music files
        pygame.mixer.music.load("Genesis_Sprites/Overworld.mp3")
        
        # Allow the music to play indefinitely
        pygame.mixer.music.play(-1)
        
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
                elif event.key == pygame.K_DOWN:
                    self.downKeyPressed = True
                    self.upKeyPressed = False
                    self.DIRECTION = "DOWN"
                elif event.key == pygame.K_RIGHT:
                    self.rightKeyPressed = True
                    self.leftKeyPressed = False
                    self.DIRECTION = "RIGHT"
                elif event.key == pygame.K_LEFT:
                    self.rightKeyPressed = False
                    self.leftKeyPressed = True
                    self.DIRECTION = "LEFT"  
                elif event.key == pygame.K_q:
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
                

            if self.DIRECTION == "DOWN":
                self.player.y += WALKRATE
                self.player.worldy += WALKRATE
                if self.player.worldy > WORLD_HEIGHT:
                    self.player.worldy = WORLD_HEIGHT - 25 * WINDOW_MAGNIFICATION
                elif self.player.y  > WINDOW_HEIGHT:
                    self.player.y = 0
                    CAMERA_TOP += ROOM_HEIGHT
                    
            if self.DIRECTION == "LEFT":
                self.player.x -= WALKRATE
                self.player.worldx -= WALKRATE
                if self.player.x < 0:
                    self.player.x = WINDOW_WIDTH - 25 * WINDOW_MAGNIFICATION
                    CAMERA_LEFT -= ROOM_WIDTH
                if self.player.worldx < 0:
                    self.player.worldx = 0
                    self.player.worldx -= WALKRATE
                    
            if self.DIRECTION == "RIGHT":
                self.player.x += WALKRATE
                self.player.worldx += WALKRATE
                if self.player.x  > WINDOW_WIDTH :
                    self.player.x = 0 
                    CAMERA_LEFT += ROOM_WIDTH
                if self.player.worldx + 25 > WORLD_WIDTH:
                    self.player.worldx = WORLD_WIDTH - 25
                    self.player.worldx -= WALKRATE

        return False
 
    
             
    def getRoomSurface(self, leftPixel, topPixel, tileData):
        """
        This method is used to fetch all tiles in a single room and expand them for easier viewing. It is a great space optimization. 
        """
        # Get the leftmost and topmost tile numbers
        leftmostTile = leftPixel // 25
        topmostTile = topPixel // 25
        self.all_boundaries_Group.empty()
        
        # Get the initial room surface
        roomSurf = pygame.Surface((ROOM_WIDTH, ROOM_HEIGHT))
        
        # For each tile in the tile_Data we draw it at the room's coordinates. 
        for tiley in range(topmostTile, topmostTile + 11):
            for tilex in range(leftmostTile, leftmostTile + 16):
                tile = Tile(tilex, tiley, leftmostTile, topmostTile)
                tile_number = tile.getTileNumber(tilex, tiley)
                
                # Just in case, ensure tile_number is an integer.
                tile_number = int(tile_number)
                
                roomSurf.blit(tile.getTile(tile_number), ((tilex - leftmostTile) * 25, (tiley - topmostTile) * 25))
               
                # Check if the tile at tilex and tiley is a boundary
                if tile_number in boundary_tiles:
                    self.all_boundaries_Group.add(tile)
   
        # Zoom in on the room to make it more viewable and return the room
        roomSurf = pygame.transform.scale(roomSurf, (ROOM_WIDTH * WINDOW_MAGNIFICATION, ROOM_HEIGHT * WINDOW_MAGNIFICATION))
        return roomSurf
    
    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if(self.player.health <= 0):
            self.game_over = True
        
        # Updates the feedback system's information
        self.feedback.update(self.player)
        
        # If the game isnt over continue to update sprites
        if not self.game_over:
            player = self.player
            
            # Move all the sprites and update positions
            self.all_sprites_Group.update()
            self.all_boundaries_Group.update()
            
            # check if there are any collisions between th eplayer and a boundary tile.
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
        
# TODO: Add collision detection between the Player and the enemies     

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        
        # Clear the screen to White
        screen.fill(WHITE)
        
        # If the game hasnt ended and the game has started draw he sprites
        if(not self.game_over and self.game_start):
            
            # Create a new surface for the current room
            roomSurface = self.getRoomSurface(CAMERA_LEFT, CAMERA_TOP, tile_Data)
            
            # Copy the background image to the viewport.
            screen.blit(roomSurface, (0,0))
            
            # Draw each of the sprites in the all_sprites_Group
            self.all_sprites_Group.draw(screen)
            
            # Draw each of the feedback sprites and information
            self.feedback.draw()
            
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
                text3 = font.render("Your goal is to defeat all 7 sins on Earth to redeem yourself", True, (WHITE))
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