import cv2
import random
import config

class Fruit:
    def __init__(self, settings):
        self.points = settings["points"]
        self.speed = settings["speed"]
        self.image = cv2.imread(settings["image_path"], cv2.IMREAD_UNCHANGED)
        if self.image is None:
            print(f"Error: Could not load image from {settings['image_path']}")
            self.width, self.height = 0, 0
        else:
            target_size = settings["radius"] * 2
            self.image = cv2.resize(self.image, (target_size, target_size), interpolation=cv2.INTER_AREA)
            self.width = self.image.shape[1]
            self.height = self.image.shape[0]
            self.has_alpha = self.image.shape[2] == 4
        
        self.reset()

    def reset(self):
        """Resets fruit's position, respecting the playable area."""
        self.y = -self.height
        
        # --- THIS IS THE UPDATED LOGIC ---
        play_area_width = config.SCREEN_WIDTH * config.FRUIT_PLAY_AREA_PERCENT
        margin = (config.SCREEN_WIDTH - play_area_width) / 2
        min_x = int(margin)
        max_x = int(config.SCREEN_WIDTH - margin - self.width)
        self.x = random.randint(min_x, max_x)
        # --- END OF UPDATE ---

    def move(self):
        self.y += self.speed

    def draw(self, frame):
        if self.image is None: return
        x_int, y_int = int(self.x), int(self.y)
        y1, y2 = max(0, y_int), min(config.SCREEN_HEIGHT, y_int + self.height)
        x1, x2 = max(0, x_int), min(config.SCREEN_WIDTH, x_int + self.width)
        
        if y1 >= y2 or x1 >= x2: return
        img_y1, img_y2 = max(0, -y_int), self.height - max(0, (y_int + self.height) - config.SCREEN_HEIGHT)
        img_x1, img_x2 = max(0, -x_int), self.width - max(0, (x_int + self.width) - config.SCREEN_WIDTH)
        visible_slice = self.image[img_y1:img_y2, img_x1:img_x2]
        roi = frame[y1:y2, x1:x2]

        if self.has_alpha and visible_slice.shape[0] > 0 and visible_slice.shape[1] > 0:
            alpha_s = visible_slice[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                roi[:, :, c] = (alpha_s * visible_slice[:, :, c] + alpha_l * roi[:, :, c])