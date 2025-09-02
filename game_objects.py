import cv2
import config
import random
import numpy as np

class Paddle:
    def __init__(self):
        self.base_w = config.PADDLE_WIDTH    #to retain shape after power-up
        self.w = self.base_w
        self.h = config.PADDLE_HEIGHT
        self.x = (config.SCREEN_WIDTH - self.w) // 2
        self.y = config.SCREEN_HEIGHT - self.h - 40
    def update(self, face_center_x):
        control_zone_width = config.SCREEN_WIDTH * config.FACE_CONTROL_ZONE_PERCENT  # 50% of screen
        zone_margin = (config.SCREEN_WIDTH - control_zone_width) / 2
        input_min = zone_margin
        input_max = config.SCREEN_WIDTH - zone_margin
        clamped_face_x = max(input_min, min(face_center_x, input_max))  #position stops at edges of control zone
        input_range = input_max - input_min
        percent_in_zone = (clamped_face_x - input_min) / input_range  #converts head position to 0-1 range
        output_max = config.SCREEN_WIDTH - self.w
        output_min = 0
        output_range = output_max - output_min
        target_x = output_min + (percent_in_zone * output_range)   #maps 0-1 range to paddle position
        move_x = (target_x - self.x) * config.PADDLE_SMOOTHING     #glides to target
        self.x += int(move_x)
        if self.x < 0: self.x = 0
        if self.x + self.w > config.SCREEN_WIDTH: self.x = config.SCREEN_WIDTH - self.w
    def draw(self, frame):
        x, y, w, h = int(self.x), int(self.y), int(self.w), int(self.h)
        top_color = config.PADDLE_COLOR_TOP
        bottom_color = config.PADDLE_COLOR_BOTTOM
        for i in range(h):        #vertical gradient to give 3D effect
            inter_color = [bottom_color[j] + (top_color[j] - bottom_color[j]) * (i / h) for j in range(3)]
            cv2.line(frame, (x, y + i), (x + w, y + i), inter_color, 1)
        cv2.line(frame, (x, y), (x + w, y), config.PADDLE_HIGHLIGHT_COLOR, 2)
        cv2.line(frame, (x, y), (x, y + h), config.PADDLE_HIGHLIGHT_COLOR, 1)

class Ball:
    def __init__(self):
        self.radius = config.BALL_RADIUS
        self.speed_multiplier = 1.0   
        self.image = cv2.imread(config.BALL_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
        if self.image is not None:
            self.image = cv2.resize(self.image, (self.radius * 2, self.radius * 2))
            self.has_alpha = self.image.shape[2] == 4
        else:
            self.has_alpha = False
        self.reset()
    def reset(self, level=1):
        self.x = config.SCREEN_WIDTH // 2   #centered
        self.y = config.SCREEN_HEIGHT // 2
        total_speed_increase = (level - 1) * config.BALL_SPEED_INCREASE  #increases speed with level
        speed_magnitude_x = abs(config.BALL_INITIAL_VX) + total_speed_increase
        speed_magnitude_y = abs(config.BALL_INITIAL_VY) + total_speed_increase
        self.vy = -speed_magnitude_y   #always starts going up
        self.vx = random.uniform(speed_magnitude_x * 0.3, speed_magnitude_x) * random.choice([-1, 1]) #random left/right
    def move(self):    #updates position based on velocity
        self.x += self.vx * self.speed_multiplier
        self.y += self.vy * self.speed_multiplier
    def draw(self, frame):
        if self.image is not None and self.has_alpha:
            x, y, r = int(self.x), int(self.y), self.radius
            x1, y1 = x - r, y - r
            x2, y2 = x + r, y + r
            if x2 < 0 or x1 > config.SCREEN_WIDTH or y2 < 0 or y1 > config.SCREEN_HEIGHT: return
            img_x1, img_x2 = max(0, -x1), (r * 2) - max(0, x2 - config.SCREEN_WIDTH)
            img_y1, img_y2 = max(0, -y1), (r * 2) - max(0, y2 - config.SCREEN_HEIGHT)
            frame_x1, frame_x2 = max(x1, 0), min(x2, config.SCREEN_WIDTH)
            frame_y1, frame_y2 = max(y1, 0), min(y2, config.SCREEN_HEIGHT)
            if img_x1 >= img_x2 or img_y1 >= img_y2: return
            ball_slice = self.image[img_y1:img_y2, img_x1:img_x2]
            roi = frame[frame_y1:frame_y2, frame_x1:frame_x2]
            if roi.shape[:2] == ball_slice.shape[:2]:
                alpha_s = ball_slice[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                for c in range(3):
                    roi[:, :, c] = (alpha_s * ball_slice[:, :, c] + alpha_l * roi[:, :, c])
        else:
            cv2.circle(frame, (int(self.x), int(self.y)), self.radius, (0,0,255), -1)

class PowerUp:
    def __init__(self, type_name):
        self.w = config.POWERUP_SIZE
        self.h = config.POWERUP_SIZE
        self.type = type_name
        self.image = cv2.imread(config.POWERUP_TYPES[self.type]["image"], cv2.IMREAD_UNCHANGED)
        if self.image is not None:
            self.image = cv2.resize(self.image, (self.w, self.h))
            self.has_alpha = self.image.shape[2] == 4
        else:
            self.has_alpha = False
        self.x = random.randint(0, config.SCREEN_WIDTH - self.w)
        self.y = -self.h
        self.vy = config.POWERUP_SPEED_Y
        self.vx = random.uniform(-config.POWERUP_SPEED_X_MAX, config.POWERUP_SPEED_X_MAX)
    def move(self):
        self.y += self.vy
        self.x += self.vx
        if self.x <= 0 or self.x + self.w >= config.SCREEN_WIDTH: self.vx *= -1
    def draw(self, frame):
        if self.image is None or not self.has_alpha: return
        try:
            y1, y2 = int(self.y), int(self.y + self.h)
            x1, x2 = int(self.x), int(self.x + self.w)
            if y2 < 0 or y1 > config.SCREEN_HEIGHT or x2 < 0 or x1 > config.SCREEN_WIDTH: return
            img_y1, img_y2 = max(0, -y1), self.h - max(0, y2 - config.SCREEN_HEIGHT)
            img_x1, img_x2 = max(0, -x1), self.w - max(0, x2 - config.SCREEN_WIDTH)
            roi_y1, roi_y2 = max(y1, 0), min(y2, config.SCREEN_HEIGHT)
            roi_x1, roi_x2 = max(x1, 0), min(x2, config.SCREEN_WIDTH)
            if img_y1 >= img_y2 or img_x1 >= img_x2: return
            powerup_slice = self.image[img_y1:img_y2, img_x1:img_x2]
            roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
            if roi.shape[:2] == powerup_slice.shape[:2]:
                alpha_s = powerup_slice[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                for c in range(3):
                    roi[:, :, c] = (alpha_s * powerup_slice[:, :, c] + alpha_l * roi[:, :, c])
        except Exception: pass