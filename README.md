# 🎮 dX-ball: Face tracking Arcade Game

dX-ball is an interactive arcade game built with Python and OpenCV that reimagines classic paddle-and-ball gameplay. The core feature is its hands-free control system, which uses a Haar Cascade classifier to detect the player's face in real-time via webcam. The horizontal position of the face is then smoothly mapped to the on-screen paddle, allowing for intuitive, motion-based control.

---

### ✨ Features

* ✅ **Real-Time Face Control:** Uses OpenCV to track your face and move the paddle smoothly and responsively.
* ✅ **Intelligent Physics:** The ball's bounce angle changes based on *where* it hits the paddle, allowing for skillful shots.
* ✅ **Dynamic Progression:** The game gets faster and more challenging as you advance through levels.
* ✅ **Power-Ups & Penalties:** Catch falling icons with your paddle to get advantages like a wider paddle or an extra life. But watch out for penalties that can shrink your paddle or speed up the ball!
* ✅ **Complete Game Loop:** Includes a scoring system, lives, and a 'Game Over' screen with a restart option.
* ✅ **Polished Visuals:** Features a 3D-style ball, a sleek gradient paddle, and a clean UI with outlined text for perfect readability.

---

### 🛠️ Technology Stack

* **Python 3** 🐍
* **OpenCV** (`cv2`): Used for all computer vision tasks (real-time face detection) and for creating the game window and drawing all the shapes and images.
* **NumPy:** Used for fast numerical calculations, primarily by OpenCV behind the scenes.

---

### 🚀 Getting Started

Getting the game running on your machine is simple.

1️⃣ **Clone the repository:**
```bash
git clone [https://github.com/wasiftak/dx-ball.git](https://github.com/wasiftak/dx-ball.git)
