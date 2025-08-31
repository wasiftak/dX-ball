import cv2
import config
from game_objects import Paddle, Ball

class GameManager:
    def __init__(self):
        """Initializes the game state, score, lives, and objects."""
        self.paddle = Paddle()
        self.ball = Ball()
        self.reset_game()

    def reset_game(self):
        """Resets the game to its initial state."""
        self.score = 0
        self.lives = config.INITIAL_LIVES
        self.game_state = "playing"
        self.ball.reset()

    def update(self, frame, face_center_x):
        """The main update function, now driven by the game state."""
        if self.game_state == "playing":
            # If we are in the 'playing' state, update all game logic
            if face_center_x:
                self.paddle.update(face_center_x)
            
            self.ball.move()
            self.check_collisions()

        elif self.game_state == "game_over":
            # If the game is over, just show the game over text
            cv2.putText(frame, "GAME OVER", config.GAME_OVER_POSITION,
                        config.UI_FONT, 2.5, config.UI_COLOR, 3)
            cv2.putText(frame, "Press 'R' to Restart", (config.GAME_OVER_POSITION[0] - 100, config.GAME_OVER_POSITION[1] + 60),
                        config.UI_FONT, 1.0, config.UI_COLOR, 2)
        
        # Always draw the objects and the UI
        self.paddle.draw(frame)
        self.ball.draw(frame)
        self.draw_ui(frame)

    def check_collisions(self):
        """Handles collisions and game rules."""
        b = self.ball
        p = self.paddle

        # Wall collisions (left and right)
        if b.x - b.radius <= 0 or b.x + b.radius >= config.SCREEN_WIDTH:
            b.vx *= -1

        # Wall collision (top)
        if b.y - b.radius <= 0:
            b.vy *= -1

        # Paddle collision
        if (b.x > p.x and b.x < p.x + p.w and
            b.y + b.radius > p.y and b.y - b.radius < p.y + p.h):
            if b.vy > 0:
                b.vy *= -1
                self.score += config.POINTS_PER_HIT # Increase score on hit!

        # Ball missed (bottom of screen)
        if b.y - b.radius > config.SCREEN_HEIGHT:
            self.lives -= 1 # Lose a life!
            if self.lives <= 0:
                self.game_state = "game_over" # Set game state to game over!
            else:
                b.reset() # Reset ball if lives are left

    def draw_ui(self, frame):
        """Draws the score and lives on the screen."""
        score_text = f"Score: {self.score}"
        lives_text = f"Lives: {self.lives}"
        cv2.putText(frame, score_text, config.SCORE_POSITION, config.UI_FONT,
                    config.UI_FONT_SCALE, config.UI_COLOR, config.UI_FONT_THICKNESS)
        cv2.putText(frame, lives_text, config.LIVES_POSITION, config.UI_FONT,
                    config.UI_FONT_SCALE, config.UI_COLOR, config.UI_FONT_THICKNESS)