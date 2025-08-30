import cv2
import random
import config
from game_objects import Fruit

class GameManager:
    def __init__(self):
        self.score = 0
        self.fruits = [] # We now manage a list of fruits
        self.fruit_types = [
            config.APPLE_SETTINGS,
            config.BANANA_SETTINGS,
            config.STRAWBERRY_SETTINGS
        ]

    def spawn_fruit(self):
        """Spawns a new fruit of a random type and adds it to our list."""
        if random.random() < config.FRUIT_SPAWN_RATE:
            # Choose a random fruit type from our list of settings
            random_fruit_settings = random.choice(self.fruit_types)
            self.fruits.append(Fruit(random_fruit_settings))

    def update_and_draw_fruits(self, frame):
        """Moves, draws, and removes off-screen fruits."""
        # We iterate over a copy of the list to safely remove items
        for fruit in self.fruits[:]:
            fruit.move()
            fruit.draw(frame)
            # Remove fruit if it goes off the bottom of the screen
            if fruit.y > config.SCREEN_HEIGHT:
                self.fruits.remove(fruit)

    def check_collisions(self, catcher_rect):
        """Checks for collisions between the catcher and any fruit."""
        for fruit in self.fruits[:]:
            cx, cy, cw, ch = catcher_rect
            ax, ay, aw, ah = fruit.x, fruit.y, fruit.width, fruit.height

            # AABB collision detection
            if (cx < ax + aw and cx + cw > ax and
                cy < ay + ah and cy + ch > ay):
                self.increase_score(fruit.points)
                self.fruits.remove(fruit) # Remove the caught fruit

    def increase_score(self, points):
        """Increases the score by the given number of points."""
        self.score += points

    def draw_score(self, frame):
        """Draws the current score on the frame."""
        score_text = f"Score: {self.score}"
        cv2.putText(frame, score_text, config.SCORE_POSITION,
                    config.SCORE_FONT, config.SCORE_FONT_SCALE,
                    config.SCORE_COLOR, config.SCORE_FONT_THICKNESS)