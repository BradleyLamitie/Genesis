import pygame
import random
import math
import Constants

class Tile(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    global tile_Data

    def __init__(self, x, y, leftmostTile, topmostTile):
        """ Constructor, create the image of the block. """
        super().__init__()

        # Initialize the tiles size and locations
        self.image = pygame.Surface(
            [25 * Constants.WINDOW_MAGNIFICATION, 25 * Constants.WINDOW_MAGNIFICATION])
        self.rect = self.image.get_rect()
        self.y = y
        self.x = x
        self.tilex = (x - leftmostTile) * 25 * Constants.WINDOW_MAGNIFICATION
        self.tiley = (y - topmostTile) * 25 * Constants.WINDOW_MAGNIFICATION
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
            return Constants.BLACKFloorTile
        elif(tileNumber == 135):
            return Constants.WHITEFloorTile
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
