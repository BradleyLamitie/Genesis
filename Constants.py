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
