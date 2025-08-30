import cv2

# Performance settings
DETECTION_SCALE_FACTOR = 4

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Catcher (face rectangle) properties
CATCHER_COLOR = (0, 250, 0)
CATCHER_THICKNESS = 3

# --- Game Object Settings ---

# General spawn settings
FRUIT_SPAWN_RATE = 0.03 # Lower is less frequent (e.g., 3% chance per frame)
FRUIT_PLAY_AREA_PERCENT = 0.7 # Percent of screen width for spawning fruits

# Apple properties
APPLE_SETTINGS = {
    "image_path": "assets/apple.png",
    "radius": 35,
    "speed": 7,
    "points": 10
}

# Banana properties
BANANA_SETTINGS = {
    "image_path": "assets/banana.png",
    "radius": 40,
    "speed": 8,
    "points": 15
}

# Strawberry properties
STRAWBERRY_SETTINGS = {
    "image_path": "assets/strawberry.png",
    "radius": 30,
    "speed": 9,
    "points": 20
}

# Score properties
SCORE_COLOR = (255, 255, 255)
SCORE_FONT = cv2.FONT_HERSHEY_SIMPLEX
SCORE_FONT_SCALE = 1.5
SCORE_FONT_THICKNESS = 2
SCORE_POSITION = (30, 50)