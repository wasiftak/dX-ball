import cv2

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Performance settings
DETECTION_SCALE_FACTOR = 4
FACE_CASCADE_PATH = "assets/haarcascade_frontalface_alt.xml"
# Defines the horizontal area (as a percentage) of the screen used for face control
FACE_CONTROL_ZONE_PERCENT = 0.6

# --- Paddle Settings ---
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 25
PADDLE_COLOR = (255, 0, 0) # Blue
# Smoothing factor for paddle movement (a smaller value is smoother)
PADDLE_SMOOTHING = 0.08

# --- Ball Settings ---
BALL_RADIUS = 15
BALL_COLOR = (255, 255, 255) # White
# Initial velocity of the ball (pixels per frame)
BALL_INITIAL_VX = 6
BALL_INITIAL_VY = -6 # Start by moving up