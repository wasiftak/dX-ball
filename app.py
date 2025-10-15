from flask import Flask, render_template, Response, jsonify
import cv2
import config
from game_manager import GameManager

app = Flask(__name__)
face_cascade = cv2.CascadeClassifier(config.FACE_CASCADE_PATH)
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.SCREEN_WIDTH)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.SCREEN_HEIGHT)
game_manager = GameManager()

def generate_frames():
    global game_manager
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        scale = config.DETECTION_SCALE_FACTOR
        small_frame = cv2.resize(frame, (frame.shape[1] // scale, frame.shape[0] // scale))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        face_center_x = None
        if len(faces) > 0:
            (x, y, w, h) = [v * scale for v in faces[0]]
            face_center_x = x + w // 2

        game_manager.update(frame, face_center_x)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    global game_manager
    game_manager.reset_game()
    return render_template("game.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/status")
def status():
    return jsonify({"game_state": game_manager.game_state, "score": game_manager.score})

@app.route("/gameover")
def gameover():
    score = game_manager.score
    high_score = game_manager.high_score
    return render_template("gameover.html", score=score, high_score=high_score)

if __name__ == "__main__":
    app.run(debug=True)