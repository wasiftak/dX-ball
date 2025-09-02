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

# --- UI Settings (Final Polish) ---
UI_FONT = cv2.FONT_HERSHEY_DUPLEX
UI_FONT_SCALE = 1.0
UI_FONT_THICKNESS = 2
UI_COLOR = (0, 255, 100) # Vibrant Green
UI_OUTLINE_COLOR = (0, 0, 0) # Black outline for text
SCORE_POSITION = (30, 50)
LIVES_POSITION = (SCREEN_WIDTH - 180, 50)
LEVEL_POSITION = (SCREEN_WIDTH // 2 - 80, 50)
GAME_OVER_POSITION = (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2)
POWERUP_TIMER_POSITION = (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 20)

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

# --- Ball Settings (Final Polish) ---
BALL_RADIUS = 18 
BALL_IMAGE_PATH = "assets/ball_3d.png"
BALL_INITIAL_VX = 7.2
BALL_INITIAL_VY = -7.2
BALL_SLOW_FACTOR = 0.5
BALL_FAST_FACTOR = 1.5

# --- Power-Up Settings ---
POWERUP_SIZE = 40
POWERUP_SPAWN_CHANCE = 0.3
POWERUP_SPEED_Y = 4
POWERUP_SPEED_X_MAX = 3
POWERUP_DURATION_SECONDS = 8.0
POWERUP_MAX_ON_SCREEN = {1: 0, 2: 1, 5: 2, 8: 3}
POWERUP_UNLOCK_LEVELS = {"wide_paddle": 2, "shrink_paddle": 3, "slow_ball": 4, "fast_ball": 5, "extra_life": 6}
POWERUP_TYPES = {
    "wide_paddle": {"image": "assets/powerup_wide.png"},
    "extra_life": {"image": "assets/powerup_life.png"},
    "slow_ball": {"image": "assets/powerup_slow.png"},
    "shrink_paddle": {"image": "assets/powerup_shrink.png"},
    "fast_ball": {"image": "assets/powerup_fast.png"}
}