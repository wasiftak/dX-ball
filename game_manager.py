import cv2
import config
import random
import time
from game_objects import Paddle, Ball, PowerUp

class GameManager:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.powerups = []
        self.active_effects = {}
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.lives = config.INITIAL_LIVES
        self.level = 1
        self.hits_this_level = 0
        self.game_state = "playing"
        self.powerups = []
        self.deactivate_all_effects()
        self.ball.reset(level=1)

    def level_up(self):
        self.level += 1
        self.hits_this_level = 0
        speed_increase = config.BALL_SPEED_INCREASE
        max_speed = 15
        self.ball.vx = min(abs(self.ball.vx) + speed_increase, max_speed) * (1 if self.ball.vx > 0 else -1)
        self.ball.vy = min(abs(self.ball.vy) + speed_increase, max_speed) * (1 if self.ball.vy > 0 else -1)

    def update(self, frame, face_center_x):
        if self.game_state == "playing":
            if face_center_x: self.paddle.update(face_center_x)
            self.ball.move()
            self.update_powerups()
            self.update_effects()
            self.check_collisions()
        elif self.game_state == "game_over":
     
                 # Draw the main "GAME OVER" text
            self.draw_text_with_outline(frame, "GAME OVER", config.GAME_OVER_POSITION, config.UI_FONT, 2.5, config.UI_COLOR, 5)
            
            # Define the restart text and get its size
            restart_text = "Press 'R' to Restart"
            text_size = cv2.getTextSize(restart_text, config.UI_FONT, 1.0, 3)[0]
            
            # Calculate the centered position for the restart text
            restart_pos_x = (config.SCREEN_WIDTH - text_size[0]) // 2
            restart_pos_y = config.GAME_OVER_POSITION[1] + 60
            
            # Draw the restart text
            self.draw_text_with_outline(frame, restart_text, (restart_pos_x, restart_pos_y), config.UI_FONT, 1.0, config.UI_COLOR, 3)
        
        for p in self.powerups: p.draw(frame)
        self.paddle.draw(frame)
        self.ball.draw(frame)
        self.draw_ui(frame)

    def draw_text_with_outline(self, frame, text, pos, font, scale, color, thickness):
        # Draw the black outline
        cv2.putText(frame, text, (pos[0]+2, pos[1]+2), font, scale, config.UI_OUTLINE_COLOR, thickness + 2)
        # Draw the main text
        cv2.putText(frame, text, pos, font, scale, color, thickness)

    def draw_ui(self, frame):
        score_text = f"Score: {self.score}"
        lives_text = f"Lives: {self.lives}"
        level_text = f"Level: {self.level}"
        
        self.draw_text_with_outline(frame, score_text, config.SCORE_POSITION, config.UI_FONT, config.UI_FONT_SCALE, config.UI_COLOR, config.UI_FONT_THICKNESS)
        self.draw_text_with_outline(frame, lives_text, config.LIVES_POSITION, config.UI_FONT, config.UI_FONT_SCALE, config.UI_COLOR, config.UI_FONT_THICKNESS)
        self.draw_text_with_outline(frame, level_text, config.LEVEL_POSITION, config.UI_FONT, config.UI_FONT_SCALE, config.UI_COLOR, config.UI_FONT_THICKNESS)

        # --- REMOVED DEBUG TEXT ---
        # The "Hits:" counter is no longer drawn here.

        effect_text = ""
        for effect, end_time in self.active_effects.items():
            remaining_time = max(0, (end_time - time.time()))
            effect_text += f"{effect.replace('_', ' ').title()}: {int(remaining_time) + 1}s  "
        self.draw_text_with_outline(frame, effect_text, config.POWERUP_TIMER_POSITION, config.UI_FONT, 1.0, config.UI_COLOR, config.UI_FONT_THICKNESS)
        
    def check_collisions(self):
        b = self.ball
        p = self.paddle
        if b.x - b.radius <= 0 or b.x + b.radius >= config.SCREEN_WIDTH: b.vx *= -1 #left/right walls, so reverse x velocity
        if b.y - b.radius <= 0: b.vy *= -1  #top wall, so reverse y velocity
        if (b.x > p.x and b.x < p.x + p.w and b.y + b.radius > p.y and b.y - b.radius < p.y + p.h and b.vy > 0):  #checks for collision with paddle
            b.vy *= -1
            paddle_center_x = p.x + p.w / 2
            offset = b.x - paddle_center_x  #negative if left, positive if right
            normalized_offset = offset / (p.w / 2)   #converts offset to -1 to 1 range
            b.vx = normalized_offset * config.PADDLE_BOUNCE_INTENSITY
            self.score += config.POINTS_PER_HIT
            self.hits_this_level += 1
            if self.hits_this_level >= config.HITS_PER_LEVEL:
                self.level_up()
            if random.random() < config.POWERUP_SPAWN_CHANCE:
                self.spawn_powerup()
        if b.y - b.radius > config.SCREEN_HEIGHT:   #gone past bottom edge
            self.lives -= 1
            self.deactivate_all_effects()
            if self.lives <= 0: self.game_state = "game_over"
            else: self.ball.reset(level=self.level)
            
    def spawn_powerup(self):
        max_for_level = 0
        for level_thresh, max_count in config.POWERUP_MAX_ON_SCREEN.items():
            if self.level >= level_thresh: max_for_level = max_count
        if len(self.powerups) < max_for_level:
            available_pool = [ptype for ptype, unlock_level in config.POWERUP_UNLOCK_LEVELS.items() if self.level >= unlock_level]
            if available_pool:
                self.powerups.append(PowerUp(random.choice(available_pool)))
    def update_powerups(self):
        for p in self.powerups[:]:
            p.move()
            if (p.x < self.paddle.x + self.paddle.w and p.x + p.w > self.paddle.x and
                p.y < self.paddle.y + self.paddle.h and p.y + p.h > self.paddle.y):
                self.activate_powerup(p.type)
                self.powerups.remove(p)
            elif p.y > config.SCREEN_HEIGHT:
                self.powerups.remove(p)
    def activate_powerup(self, effect_type):
        opposites = {"wide_paddle": "shrink_paddle", "shrink_paddle": "wide_paddle",
                     "slow_ball": "fast_ball", "fast_ball": "slow_ball"}
        if effect_type in opposites and opposites[effect_type] in self.active_effects:
            self.deactivate_effect(opposites[effect_type])
        if effect_type == "extra_life":
            self.lives += 1
        else:
            self.active_effects[effect_type] = time.time() + config.POWERUP_DURATION_SECONDS
            if effect_type == "wide_paddle": self.paddle.w = self.paddle.base_w * config.PADDLE_WIDE_FACTOR
            elif effect_type == "shrink_paddle": self.paddle.w = self.paddle.base_w * config.PADDLE_SHRINK_FACTOR
            elif effect_type == "slow_ball": self.ball.speed_multiplier = config.BALL_SLOW_FACTOR
            elif effect_type == "fast_ball": self.ball.speed_multiplier = config.BALL_FAST_FACTOR
    def update_effects(self):
        current_time = time.time()
        expired_effects = [effect for effect, end_time in self.active_effects.items() if current_time > end_time]
        for effect in expired_effects:
            self.deactivate_effect(effect)
    def deactivate_effect(self, effect_type):
        if effect_type in self.active_effects: del self.active_effects[effect_type]
        if effect_type == "wide_paddle" or effect_type == "shrink_paddle": self.paddle.w = self.paddle.base_w
        if effect_type == "slow_ball" or effect_type == "fast_ball": self.ball.speed_multiplier = 1.0
    def deactivate_all_effects(self):
        self.paddle.w = self.paddle.base_w
        self.ball.speed_multiplier = 1.0
        self.active_effects = {}