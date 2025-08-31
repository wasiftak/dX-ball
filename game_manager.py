import cv2
import config
from game_objects import Paddle, Ball

class GameManager:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.lives = config.INITIAL_LIVES
        self.level = 1
        self.hits_this_level = 0
        self.game_state = "playing"
        self.ball.reset(level=1)

    def update(self, frame, face_center_x):
        if self.game_state == "playing":
            if face_center_x:
                self.paddle.update(face_center_x)
            self.ball.move()
            self.check_collisions()
        elif self.game_state == "game_over":
            cv2.putText(frame, "GAME OVER", config.GAME_OVER_POSITION, config.UI_FONT, 2.5, config.UI_COLOR, 3)
            cv2.putText(frame, "Press 'R' to Restart", (config.GAME_OVER_POSITION[0] - 100, config.GAME_OVER_POSITION[1] + 60), config.UI_FONT, 1.0, config.UI_COLOR, 2)
        
        self.paddle.draw(frame)
        self.ball.draw(frame)
        self.draw_ui(frame)

    def level_up(self):
        self.level += 1
        self.hits_this_level = 0
        # Increase ball's overall speed
        speed_increase = config.BALL_SPEED_INCREASE
        max_speed = 15 # Cap the max speed
        self.ball.vx = min(abs(self.ball.vx) + speed_increase, max_speed) * (1 if self.ball.vx > 0 else -1)
        self.ball.vy = min(abs(self.ball.vy) + speed_increase, max_speed) * (1 if self.ball.vy > 0 else -1)

    def check_collisions(self):
        b = self.ball
        p = self.paddle

        # Wall collisions
        if b.x - b.radius <= 0 or b.x + b.radius >= config.SCREEN_WIDTH: b.vx *= -1
        if b.y - b.radius <= 0: b.vy *= -1

        # Paddle collision with intelligent bounce
        if (b.x > p.x and b.x < p.x + p.w and b.y + b.radius > p.y and b.y - b.radius < p.y + p.h and b.vy > 0):
            b.vy *= -1
            paddle_center_x = p.x + p.w / 2
            offset = b.x - paddle_center_x
            normalized_offset = offset / (p.w / 2)
            b.vx = normalized_offset * config.PADDLE_BOUNCE_INTENSITY
            
            # --- SCORING AND LEVEL UP LOGIC ---
            self.score += config.POINTS_PER_HIT
            self.hits_this_level += 1
            if self.hits_this_level >= config.HITS_PER_LEVEL:
                self.level_up()
            
        # Ball missed
        if b.y - b.radius > config.SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0: self.game_state = "game_over"
            else: self.ball.reset(level=self.level)

    def draw_ui(self, frame):
        score_text = f"Score: {self.score}"
        lives_text = f"Lives: {self.lives}"
        level_text = f"Level: {self.level}"
        cv2.putText(frame, score_text, config.SCORE_POSITION, config.UI_FONT, config.UI_FONT_SCALE, config.UI_COLOR, config.UI_FONT_THICKNESS)
        cv2.putText(frame, lives_text, config.LIVES_POSITION, config.UI_FONT, config.UI_FONT_SCALE, config.UI_COLOR, config.UI_FONT_THICKNESS)
        cv2.putText(frame, level_text, config.LEVEL_POSITION, config.UI_FONT, config.UI_FONT_SCALE, config.UI_COLOR, config.UI_FONT_THICKNESS)