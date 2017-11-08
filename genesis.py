"""
Create the main game for "Genesis"
 
Author: Bradley Lamitie
Date: 11/08/2017
Version Number: 1.70

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

Changes in this version: 
- Added Collision detection for boundary tiles.
  

TODOs for  Demo/Final Project: 
- Finish building the world's second level. 
- Make it so that the WORLD_DATA is imported from a .tmx file. 
- If possible import a tileset from a Tiled file. 
- Learn to Use a sprite Sheet to load in sprites. 
- Animate the characters as they move throughout the world. 
- Add enemies with basic AI to fight.
- Replace all clocktower_door sprites with new sprites. 
- Add a feedback system. 
- Add the ability to use magic, attack, and use potions. 
- Add ability to interact with things like chests, NPCs, and signposts. 
- Add Save states or a pause function.
- Add a menu.
- Add Sounds.
- Add cheat codes for quick demonstrations.
- Add story.
- Add Splash Screen
- Add Screen animations
- Add Collision detection for enemies
- Add Game Over Screen
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

# The width and height of the magnified window
WINDOW_WIDTH = ROOM_WIDTH * WINDOW_MAGNIFICATION
WINDOW_HEIGHT = ROOM_HEIGHT * WINDOW_MAGNIFICATION

# The Camera starts at the second room from the right, second room down.
CAMERA_LEFT = ROOM_WIDTH * 2
CAMERA_TOP = ROOM_HEIGHT * 2

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
Angel = pygame.image.load("Genesis_Sprites/Angel_steel_front_Attacking1.png").convert()
Map_Image = pygame.image.load("Genesis_Sprites/Genesis_Map.png").convert()
# WORLD_DATA is a large string that includes all the tile data copied from Tiled file.
# TODO: import this data from the .tmx file directly.
WORLD_DATA = """50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,22,41,41,41,41,41,41,41,41,41,41,41,41,41,41,21,50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49,50,16,16,16,16,16,16,16,16,16,16,16,16,16,16,49
22,44,44,44,44,44,44,44,44,44,44,44,44,44,44,21,22,44,44,44,44,44,44,44,44,44,44,44,44,48,48,21,22,41,41,41,41,41,41,41,41,41,41,41,41,41,41,21,22,48,48,48,44,44,44,44,44,44,44,44,48,48,48,21,22,44,48,48,44,44,44,44,44,48,48,48,48,48,48,21
22,44,44,45,45,45,45,45,45,45,45,45,45,44,44,21,22,44,44,44,44,44,44,44,44,44,44,44,44,44,48,21,22,41,41,41,41,41,41,41,42,41,41,41,41,41,41,21,22,48,44,44,44,44,44,44,44,44,44,44,44,44,48,21,22,48,48,44,55,55,41,55,55,44,48,48,48,48,48,21
22,53,45,45,45,45,45,45,45,45,45,45,45,45,44,17,18,45,45,45,45,45,45,45,45,45,44,44,44,44,44,21,22,48,48,48,48,48,48,56,41,48,48,48,48,47,48,21,22,48,44,44,44,44,45,45,45,45,44,44,44,44,48,21,22,48,44,54,54,54,54,54,54,54,44,48,48,47,48,21
22,41,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,45,44,44,44,44,44,21,22,45,45,45,45,45,48,54,54,48,45,45,45,45,45,21,22,44,44,44,44,45,45,45,45,45,45,44,44,44,44,17,18,44,54,54,54,54,54,54,54,54,54,44,48,48,48,21
22,41,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,45,44,44,44,44,44,21,22,45,45,45,45,45,48,54,54,48,45,45,45,45,45,21,22,44,44,44,44,45,45,45,45,45,45,44,44,44,44,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,48,21
22,53,45,45,45,45,45,45,45,45,45,45,45,45,44,19,20,45,45,45,45,45,45,54,54,45,44,44,44,44,44,21,22,44,45,45,45,45,48,54,54,48,45,45,45,45,44,21,22,44,44,44,44,45,45,45,45,45,45,44,44,44,44,45,45,54,54,54,54,54,54,54,54,54,54,54,54,54,48,21
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
22,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,41,21,22,48,48,45,45,45,45,44,44,45,45,45,45,48,48,21,22,48,48,44,44,44,44,44,44,44,44,44,44,48,48,21,37,34,28,28,28,28,28,28,28,28,28,28,28,28,28,28
52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,52,23,23,23,23,23,23,23,23,23,23,23,23,23,23,51,37,34,28,28,28,28,28,28,28,28,28,28,28,28,28,28"""

# Split the WORLD_DATA string and sort it into a 2D array
tile_Data = WORLD_DATA
tile_Data = tile_Data.split('\n')
tile_Data = [line.split(',') for line in tile_Data]

# This list represents the tile numbers of tiles th eplayer shouldn't be able to walk through.
boundary_tiles = [15,16,17,18,19,20,21,22,23,24,25,26,28,29,30,31,32,33,34,35,36,37,40,41,4246,47,48,49,50,51,52,53,55,56]

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
        else:
            return Signpost_path
        

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    def __init__(self):
        super().__init__()
        
        # This sets the image to be the Angel surface defined above.
        self.image = pygame.Surface([25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION])
        self.rect = self.image.get_rect()
        self.image = Angel
#         self.rect = self.image.get_rect()
        
        # Set the players starting position to center screen
        # NOTE: The player's x position is not centered at WINDOW_HEIGHT//2
        self.x = WINDOW_WIDTH // 2 - 36
        self.y = WINDOW_HEIGHT // 2
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Set the players position in the world
        self.worldx = WORLD_WIDTH // 2
        self.worldy = (WORLD_HEIGHT * 5) // 6
        
        # Scale the image by the window magnification
        self.image = pygame.transform.scale(self.image, (25 * WINDOW_MAGNIFICATION, 25 * WINDOW_MAGNIFICATION))
        
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
        
        
class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """
 
        self.game_over = False
 
        # Create sprite lists
        self.all_boundaries_Group = pygame.sprite.Group()
        self.all_sprites_Group = pygame.sprite.Group()
 
        # Create the player
        self.player = Player()
        
        # Add the player to the sprites group
        self.all_sprites_Group.add(self.player)
        
        # Instantiate  starting variables for event handling
        self.upKeyPressed = False
        self.downKeyPressed = False
        self.rightKeyPressed = False
        self.leftKeyPressed = False
        self.DIRECTION = "UP"
        
    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """
        global CAMERA_LEFT, CAMERA_TOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
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
        # TODO: Add a feedback display 
        
        # Clear the screen to White
        screen.fill(WHITE)
        
        # TODO: Potential for optimization here: render new Room surface only once. 
        # Only render again when room is exited then reentered. 
        # Create a new surface for the current room
        roomSurface = self.getRoomSurface(CAMERA_LEFT, CAMERA_TOP, tile_Data)
        
        # Copy the background image to the viewport.
        screen.blit(roomSurface, (0,0))
        
        # Draw each of the sprites in the all_sprites_Group
        self.all_sprites_Group.draw(screen)

        # Copy back buffer onto the front buffer
        pygame.display.flip()


def main():
    """ Main program function. """
    
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
 
    # Close window and exit
    pygame.quit()
 
# Call the main function, start up the game
if __name__ == "__main__":
    main()