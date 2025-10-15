# 🎮 dX-ball: The face tracking Arcade Game

DX-BALL is an interactive, retro-inspired arcade game built with Python and OpenCV, now with a full web interface powered by Flask. The game reimagines classic paddle-and-ball gameplay with a modern twist: a hands-free control system.

Using a Haar Cascade classifier, the game detects the player's face in real-time via webcam. The horizontal position of your face is then smoothly mapped to the on-screen paddle, allowing for intuitive, motion-based control right from your browser.

### 1️⃣ Features:
✅ Web-Based Gameplay: Play instantly from your web browser with a sleek, retro-themed UI.

✅ Real-Time Face Control: Uses OpenCV to track your face and move the paddle smoothly and responsively.

✅ Intelligent Physics: The ball's bounce angle changes based on where it hits the paddle, allowing for skillful shots.

✅ Dynamic Progression: The game gets faster and more challenging as you advance through levels.

✅ Power-Ups & Penalties: Catch falling icons to get advantages like a wider paddle or an extra life. But watch out for penalties that can shrink your paddle or speed up the ball!

✅ High Score System: Your high score is saved locally, so you can always compete against your personal best.

✅ Polished Visuals: Features a 3D-style ball, a sleek gradient paddle, and a clean UI with outlined text for perfect readability.

🛠️ Technology Stack
Python 3 🐍

Flask: Powers the web server and user interface.

OpenCV (cv2): Used for all computer vision tasks (real-time face detection) and for creating the game window and drawing all the shapes and images.

NumPy: Used for fast numerical calculations, primarily by OpenCV behind the scenes.

🚀 Getting Started
Getting the game running on your machine is simple.

### 2️⃣ Set up a Python environment:

A virtual environment or Conda is highly recommended to keep dependencies clean.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install the required libraries:

```bash
pip install opencv-python numpy
```

### 4️⃣ Run the game\! 🎉

```bash
python main.py
```

-----

## 🕹️ How to Play

  - Move your head left and right to control the paddle.
  - Hit the ball to score points. The level increases after every 5 paddle hits.
  - Catch falling icons with your paddle to get power-ups (or penalties\!).
  - Don't let the ball fall past your paddle, or you'll lose a life.
  - Press **'R'** to restart when the game is over.
  - Press **'Q'** to quit at any time.

-----

```
```

