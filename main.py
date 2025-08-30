import cv2

# --- CONSTANTS ---
# Using constants makes it easier to change settings later
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CATCHER_COLOR = (0, 255, 0) # Green in BGR format
CATCHER_THICKNESS = 2

# --- SETUP ---
# Load the pre-trained model for face detection
# The path now correctly points to our assets folder
face_cascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_alt.xml")

# Initialize video capture from the default webcam (usually index 0)
video_capture = cv2.VideoCapture(0)

# Set the resolution of the webcam feed
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

# --- MAIN GAME LOOP ---
while True:
    # Read a single frame from the webcam
    ret, frame = video_capture.read()

    # If the frame was not grabbed successfully, break the loop
    if not ret:
        print("Failed to grab frame")
        break

    # IMPORTANT: Flip the frame horizontally
    # This creates a 'mirror' effect, which is much more intuitive for a game.
    # When you move right, your catcher on screen moves right.
    frame = cv2.flip(frame, 1)

    # Convert the color frame to grayscale for the face detection algorithm
    # The algorithm works on grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform the face detection
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Process only the first detected face for our game
    if len(faces) > 0:
        # Get the coordinates and dimensions of the face bounding box
        (x, y, w, h) = faces[0]

        # Draw the 'catcher' rectangle on the color frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), CATCHER_COLOR, CATCHER_THICKNESS)

    # Display the final frame in a window
    cv2.imshow('Head Catcher Game', frame)

    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- CLEANUP ---
# Release the webcam resource
video_capture.release()
# Close all OpenCV windows
cv2.destroyAllWindows()