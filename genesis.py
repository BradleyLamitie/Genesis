"""
Create the main game for "Genesis"
 
Author: Bradley Lamitie
Date: 10/27/2017
Version Number: 1.5
 
GitHub Repository: https://github.com/BradleyLamitie/Genesis

TODOs for Final Project: 
- Finish building the world.
- Make it so that the WORLD_DATA is imported from a .tmx file. 
- If possible import a tileset from a Tiled file. 
- Learn to Use a sprite Sheet to load in sprites. 
- Animate the characters as they move throughout the world. 
- Add enemies with basic AI to fight.
- Replace all clocktower_door sprites with new sprites. 
- Add a feedback system. 
- Add the ability to use magic, attack, and use potions. 
- Add Collision detection for boundary tiles.
- Add ability to interact with things like chests, NPCs, and signposts. 
- Add Save states or a pause function.
- Add a menu.
- Add Sounds.
- Add cheat codes for quick demonstrations.
- Add story.
"""
import pygame
 
# --- Global constants ---
# Colors: 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# The width and height of the viewport
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 825

# The width and height of the world
WORLD_WIDTH = 2000
WORLD_HEIGHT = 825

# For every frame the player sprite will be moved by the WALKRATE variable
WALKRATE = 3

# Set the screen as a global variable
# (This is necessary in order to load in the sprites)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
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
Angel = pygame.image.load("Genesis_Sprites/Signpost.png").convert()
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

# --- Classes ---
 
class Tile(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
 
    def __init__(self, x, y, tile_Number):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([25, 25])
        self.rect = self.image.get_rect()
        self.tileNumber = tile_Number
        self.x = x
        self.y = y
    def draw(self):  
        """ Draw the surface onto the back buffer. """  
        tile_surface = getTile(self.tile_Number)
        screen.blit(tile_surface,[self.x,self.y] )

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([25, 25])
        self.rect = self.image.get_rect()
        self.x = 988 # WORLD_WIDTH // 2
        self.y = 687 # ((5 * WORLD_HEIGHT) // 6)
        
    def update(self):
        """ Update the player location. """
        pos = [self.x,self.y]
        self.rect.x = pos[0]
        self.rect.y = pos[1]  
        
    def draw(self):
        """ Draw the Player sprite onto the back buffer. """
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
        self.all_Tiles_Group = pygame.sprite.Group()
        self.all_sprites_Group = pygame.sprite.Group()
 
        # Parse through the tiles and draw each one only once. 
        # These tiles sit behind the tile image to be used in Collision detection later. 
        for i in range(0,len(tile_Data)):
            for j in range(0,len(tile_Data[i])):
                y = i * 25
                x = j * 25
                tile_Number = tile_Data[i][j]
                tile_surface = getTile(tile_Number)
                screen.blit(tile_surface,[x,y] )
        
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
            if self.DIRECTION == "UP":
                self.player.y -= WALKRATE
            if self.DIRECTION == "DOWN":
                self.player.y += WALKRATE
            if self.DIRECTION == "LEFT":
                self.player.x -= WALKRATE
            if self.DIRECTION == "RIGHT":
                self.player.x += WALKRATE

            # Check the players coordinates. If they are about to move off the world
            # This will snap the player back into the world
            if self.player.y < 0:
                self.player.y = 0
            if self.player.y + 25 > WORLD_HEIGHT:
                self.player.y = WORLD_HEIGHT - 25
            if self.player.x < 0:
                self.player.x = 0
            if self.player.x + 25 > WORLD_WIDTH:
                self.player.x = WORLD_WIDTH - 25
            print(self.player.x)
        return False
 
    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.all_sprites_Group.update()
            
            # TODO: Add collision detection between the Player and the boundary tiles
            # TODO: Add collision detection between the Player and the enemies  
             
 
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        # TODO: Add a feedback display 
        
        # Clear the screen to White
        screen.fill(WHITE)
        
        # Copy the background image to the viewport.
        screen.blit(Map_Image, [0,0])
        
        # Draw each of the sprites in the all_sprites_Group
        self.all_sprites_Group.draw(screen)
        
        # Copy back buffer onto the front buffer
        pygame.display.flip()
        
def getTile(tileNumber):
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