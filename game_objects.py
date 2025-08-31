import cv2
import config
import random

class Paddle:
    def __init__(self):
        self.w = config.PADDLE_WIDTH
        self.h = config.PADDLE_HEIGHT
        self.color = config.PADDLE_COLOR
        self.x = (config.SCREEN_WIDTH - self.w) // 2
        self.y = config.SCREEN_HEIGHT - self.h - 40

    def update(self, face_center_x):
        control_zone_width = config.SCREEN_WIDTH * config.FACE_CONTROL_ZONE_PERCENT
        zone_margin = (config.SCREEN_WIDTH - control_zone_width) / 2
        input_min = zone_margin
        input_max = config.SCREEN_WIDTH - zone_margin
        clamped_face_x = max(input_min, min(face_center_x, input_max))
        input_range = input_max - input_min
        percent_in_zone = (clamped_face_x - input_min) / input_range
        output_max = config.SCREEN_WIDTH - self.w
        output_min = 0
        output_range = output_max - output_min
        target_x = output_min + (percent_in_zone * output_range)
        move_x = (target_x - self.x) * config.PADDLE_SMOOTHING
        self.x += int(move_x)
        if self.x < 0: self.x = 0
        if self.x + self.w > config.SCREEN_WIDTH: self.x = config.SCREEN_WIDTH - self.w

    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), self.color, -1)

class Ball:
    def __init__(self):
        self.radius = config.BALL_RADIUS
        self.color = config.BALL_COLOR
        self.reset()

    def reset(self, level=1):
        self.x = config.SCREEN_WIDTH // 2
        self.y = config.SCREEN_HEIGHT // 2
        total_speed_increase = (level - 1) * config.BALL_SPEED_INCREASE
        speed_magnitude_x = abs(config.BALL_INITIAL_VX) + total_speed_increase
        speed_magnitude_y = abs(config.BALL_INITIAL_VY) + total_speed_increase
        self.vy = -speed_magnitude_y # Always start moving up
        self.vx = random.uniform(speed_magnitude_x * 0.3, speed_magnitude_x) * random.choice([-1, 1])

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, frame):
        center_coords = (int(self.x), int(self.y))
        cv2.circle(frame, center_coords, self.radius, self.color, -1)