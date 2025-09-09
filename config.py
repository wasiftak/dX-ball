import cv2
import os ### New: Import the os module to handle file paths robustly

### New: Get the absolute path to the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Performance settings
DETECTION_SCALE_FACTOR = 4   
### New: Create a robust, absolute path to the cascade file
FACE_CASCADE_PATH = os.path.join(BASE_DIR, "assets", "haarcascade_frontalface_alt.xml")
FACE_CONTROL_ZONE_PERCENT = 0.5 

# --- Game Rule Settings ---
INITIAL_LIVES = 3
POINTS_PER_HIT = 10
HITS_PER_LEVEL = 2 
BALL_SPEED_INCREASE = 2.0
HIGH_SCORE_FILE = os.path.join(BASE_DIR, "highscore.txt") ### New: Create a robust path for the high score file

# --- UI Settings ---
UI_FONT = cv2.FONT_HERSHEY_DUPLEX
UI_FONT_SCALE = 1.0
UI_FONT_THICKNESS = 2
UI_COLOR = (0, 255, 100) # Vibrant Green
UI_OUTLINE_COLOR = (0, 0, 0) # Black outline for text
SCORE_POSITION = (30, 50)    # Top-left corner
LIVES_POSITION = (SCREEN_WIDTH - 180, 50)  # Top-right corner
LEVEL_POSITION = (SCREEN_WIDTH // 2 - 80, 50)  # Top-center
GAME_OVER_POSITION = (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 50)  # Centered, adjusted for high score
HIGH_SCORE_POSITION = (GAME_OVER_POSITION[0], GAME_OVER_POSITION[1] + 120)
POWERUP_TIMER_POSITION = (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 20)  # Bottom-center

# --- Paddle Settings ---
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 25
PADDLE_SMOOTHING = 0.12     
PADDLE_BOUNCE_INTENSITY = 8.0   
PADDLE_WIDE_FACTOR = 1.5
PADDLE_SHRINK_FACTOR = 0.5
PADDLE_COLOR_TOP = (255, 100, 0)
PADDLE_COLOR_BOTTOM = (200, 50, 0)
PADDLE_HIGHLIGHT_COLOR = (255, 255, 255)

# --- Ball Settings ---
BALL_RADIUS = 18 
BALL_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "ball_3d.png") ### New: Create a robust path
BALL_INITIAL_VX = 7.2
BALL_INITIAL_VY = -7.2
BALL_SLOW_FACTOR = 0.5    #for power-up
BALL_FAST_FACTOR = 1.5    #for power-up

# --- Power-Up Settings ---
POWERUP_SIZE = 40
POWERUP_SPAWN_CHANCE = 0.3   # 30% chance on paddle hit
POWERUP_SPEED_Y = 4
POWERUP_SPEED_X_MAX = 3
POWERUP_DURATION_SECONDS = 8.0
POWERUP_MAX_ON_SCREEN = {1: 0, 2: 1, 5: 2, 8: 3}
POWERUP_UNLOCK_LEVELS = {"wide_paddle": 2, "shrink_paddle": 3, "slow_ball": 4, "fast_ball": 5, "extra_life": 6}

### New: Create robust paths for all power-up images
POWERUP_TYPES = {
    "wide_paddle": {"image": os.path.join(BASE_DIR, "assets", "powerup_wide.png")},
    "extra_life": {"image": os.path.join(BASE_DIR, "assets", "powerup_life.png")},
    "slow_ball": {"image": os.path.join(BASE_DIR, "assets", "powerup_slow.png")},
    "shrink_paddle": {"image": os.path.join(BASE_DIR, "assets", "powerup_shrink.png")},
    "fast_ball": {"image": os.path.join(BASE_DIR, "assets", "powerup_fast.png")}
}

