import cv2
import config
from game_manager import GameManager

# --- SETUP ---
face_cascade = cv2.CascadeClassifier(config.FACE_CASCADE_PATH)
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.SCREEN_WIDTH)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.SCREEN_HEIGHT)

game_manager = GameManager()

# --- MAIN GAME LOOP ---
while True:
    ret, frame = video_capture.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    
    # Use the small frame optimization for face detection
    scale = config.DETECTION_SCALE_FACTOR
    small_frame = cv2.resize(frame, (frame.shape[1] // scale, frame.shape[0] // scale))
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    face_center_x = None
    if len(faces) > 0:
        # Get the center of the first detected face
        (x, y, w, h) = [v * scale for v in faces[0]]
        face_center_x = x + w // 2

    # --- DELEGATE ALL GAME LOGIC TO THE MANAGER ---
    game_manager.update(frame, face_center_x)

    cv2.imshow('Face Pong', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- CLEANUP ---
video_capture.release()
cv2.destroyAllWindows()