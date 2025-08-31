import cv2
import config

class Paddle:
    def __init__(self):
        """Initializes the paddle in the bottom-center of the screen."""
        self.w = config.PADDLE_WIDTH
        self.h = config.PADDLE_HEIGHT
        self.color = config.PADDLE_COLOR
        # Start in the middle of the screen horizontally
        self.x = (config.SCREEN_WIDTH - self.w) // 2
        # Position it near the bottom of the screen
        self.y = config.SCREEN_HEIGHT - self.h - 40

    def update(self, face_center_x):
        """Maps face position to paddle position and smoothly moves the paddle."""
        # --- 1. Define the control zone for the face ---
        control_zone_width = config.SCREEN_WIDTH * config.FACE_CONTROL_ZONE_PERCENT
        zone_margin = (config.SCREEN_WIDTH - control_zone_width) / 2
        input_min = zone_margin
        input_max = config.SCREEN_WIDTH - zone_margin

        # --- 2. Clamp the face position to be within the control zone ---
        clamped_face_x = max(input_min, min(face_center_x, input_max))

        # --- 3. Map the clamped face position to the full screen width for the paddle ---
        # Calculate how far into the control zone the face is (as a percentage from 0.0 to 1.0)
        input_range = input_max - input_min
        percent_in_zone = (clamped_face_x - input_min) / input_range
        
        # Define the output range for the paddle's x-position
        output_max = config.SCREEN_WIDTH - self.w
        output_min = 0
        output_range = output_max - output_min

        # Calculate the target paddle position
        target_x = output_min + (percent_in_zone * output_range)
        
        # --- 4. Apply the smoothing logic to the new target position ---
        # Note: We use self.x here, not the paddle_center, for direct movement
        move_x = (target_x - self.x) * config.PADDLE_SMOOTHING
        self.x += int(move_x)

        # Keep the paddle within the screen bounds (as a final safeguard)
        if self.x < 0:
            self.x = 0
        if self.x + self.w > config.SCREEN_WIDTH:
            self.x = config.SCREEN_WIDTH - self.w

    def draw(self, frame):
        """Draws the paddle on the frame."""
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), self.color, -1)

class Ball:
    def __init__(self):
        """Initializes the ball in the center of the screen with a velocity."""
        self.radius = config.BALL_RADIUS
        self.color = config.BALL_COLOR
        self.reset()

    def reset(self):
        """Resets the ball to the center with its initial velocity."""
        self.x = config.SCREEN_WIDTH // 2
        self.y = config.SCREEN_HEIGHT // 2
        self.vx = config.BALL_INITIAL_VX
        self.vy = config.BALL_INITIAL_VY

    def move(self):
        """Updates the ball's position based on its velocity."""
        self.x += self.vx
        self.y += self.vy

    def draw(self, frame):
        """Draws the ball on the frame."""
        cv2.circle(frame, (self.x, self.y), self.radius, self.color, -1)