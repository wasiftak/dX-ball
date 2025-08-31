import config
from game_objects import Paddle, Ball

class GameManager:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()

    def update(self, frame, face_center_x):
        """Main update loop for the game manager."""
        # Update paddle position if a face is detected
        if face_center_x:
            self.paddle.update(face_center_x)
        
        # Move the ball
        self.ball.move()
        
        # Check for collisions
        self.check_collisions()

        # Draw the objects
        self.paddle.draw(frame)
        self.ball.draw(frame)

    def check_collisions(self):
        """Handles collisions between the ball, walls, and paddle."""
        b = self.ball
        p = self.paddle

        # Wall collisions (left and right)
        if b.x - b.radius <= 0 or b.x + b.radius >= config.SCREEN_WIDTH:
            b.vx *= -1 # Reverse horizontal velocity

        # Wall collision (top)
        if b.y - b.radius <= 0:
            b.vy *= -1 # Reverse vertical velocity

        # Paddle collision (AABB check)
        # Check if the ball's bounding box intersects with the paddle's
        if (b.x > p.x and b.x < p.x + p.w and
            b.y + b.radius > p.y and b.y - b.radius < p.y + p.h):
            # Only trigger collision if ball is moving down
            if b.vy > 0:
                b.vy *= -1 # Reverse vertical velocity

        # For now, we will reset the ball if it goes off the bottom
        if b.y - b.radius > config.SCREEN_HEIGHT:
            b.reset()