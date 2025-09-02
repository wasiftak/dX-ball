import cv2

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Performance settings
DETECTION_SCALE_FACTOR = 4
FACE_CASCADE_PATH = "assets/haarcascade_frontalface_alt.xml"
FACE_CONTROL_ZONE_PERCENT = 0.5 

# --- Game Rule Settings ---
INITIAL_LIVES = 3
POINTS_PER_HIT = 10
HITS_PER_LEVEL = 5
BALL_SPEED_INCREASE = 2.0

# --- UI Settings ---
UI_FONT = cv2.FONT_HERSHEY_SIMPLEX
UI_FONT_SCALE = 1.2
UI_FONT_THICKNESS = 2
UI_COLOR = (255, 255, 255) # White
SCORE_POSITION = (30, 50)
LIVES_POSITION = (SCREEN_WIDTH - 200, 50)
LEVEL_POSITION = (SCREEN_WIDTH // 2 - 100, 50)
GAME_OVER_POSITION = (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2)
POWERUP_TIMER_POSITION = (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 20)

# --- Paddle Settings ---
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 25
PADDLE_COLOR = (255, 0, 0)
PADDLE_SMOOTHING = 0.12
PADDLE_BOUNCE_INTENSITY = 8.0
PADDLE_WIDE_FACTOR = 1.5
PADDLE_SHRINK_FACTOR = 0.5

# --- Ball Settings ---
BALL_RADIUS = 15
BALL_COLOR = (255, 255, 255)
BALL_INITIAL_VX = 7.2
BALL_INITIAL_VY = -7.2
BALL_SLOW_FACTOR = 0.5
BALL_FAST_FACTOR = 1.5

# --- Power-Up Settings ---
POWERUP_SIZE = 40
POWERUP_SPAWN_CHANCE = 0.3 # 30% chance on each paddle hit
POWERUP_SPEED_Y = 4
POWERUP_SPEED_X_MAX = 3
POWERUP_DURATION_SECONDS = 8.0

# Defines max powerups on screen at once based on level
POWERUP_MAX_ON_SCREEN = {
    1: 0,  # Level 1: 0
    2: 1,  # Levels 2-4: 1
    5: 2,  # Levels 5-7: 2
    8: 3   # Levels 8+: 3
}

# Defines which powerups are available starting at which level
POWERUP_UNLOCK_LEVELS = {
    "wide_paddle": 2,
    "shrink_paddle": 3,
    "slow_ball": 4,
    "fast_ball": 5,
    "extra_life": 6
}

# Power-up types and their associated images
POWERUP_TYPES = {
    "wide_paddle": {"image": "assets/powerup_wide.png"},
    "extra_life": {"image": "assets/powerup_life.png"},
    "slow_ball": {"image": "assets/powerup_slow.png"},
    "shrink_paddle": {"image": "assets/powerup_shrink.png"},
    "fast_ball": {"image": "assets/powerup_fast.png"}
}