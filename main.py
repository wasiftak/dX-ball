import cv2
import config
from game_manager import GameManager

# --- SETUP ---
face_cascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_alt.xml")
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.SCREEN_WIDTH)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.SCREEN_HEIGHT)

game_manager = GameManager()

# --- MAIN GAME LOOP ---
while True:
    ret, frame = video_capture.read()
    if not ret: break

    frame = cv2.flip(frame, 1)

    # --- PERFORMANCE OPTIMIZATION ---
    # Create a small frame for faster face detection
    scale = config.DETECTION_SCALE_FACTOR
    small_frame_dims = (frame.shape[1] // scale, frame.shape[0] // scale)
    small_frame = cv2.resize(frame, small_frame_dims, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the SMALL gray frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    catcher_rect = None
    if len(faces) > 0:
        # Scale the face coordinates back up to the original frame size
        (x, y, w, h) = [v * scale for v in faces[0]]
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), config.CATCHER_COLOR, config.CATCHER_THICKNESS)
        catcher_rect = (x, y, w, h)

    # --- GAME LOGIC (delegated to GameManager) ---
    game_manager.spawn_fruit()
    game_manager.update_and_draw_fruits(frame)
    if catcher_rect:
        game_manager.check_collisions(catcher_rect)

    # --- DRAW UI ---
    game_manager.draw_score(frame)
    
    cv2.imshow('Head Catcher Game', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- CLEANUP ---
video_capture.release()
cv2.destroyAllWindows()