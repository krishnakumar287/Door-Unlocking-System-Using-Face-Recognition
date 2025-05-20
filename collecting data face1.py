import cv2
import os
import numpy as np

# Specify the path to your Haar cascade model
model_path = 'D:/Face_detection_for_door_lock/face_model.xml'  # Use the absolute path to the model
face_classifier = cv2.CascadeClassifier(model_path)

# Check if the Haar cascade model is loaded properly
if face_classifier.empty():
    raise IOError(f"Error: Haar cascade model not loaded. Check the file path: {model_path}")

def face_extractor(img):
    """
    Extract the face from an image.

    Args:
        img: The input image.

    Returns:
        The cropped face if detected; otherwise, None.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)  # Detect faces

    if len(faces) == 0:  # No faces detected
        return None

    for (x, y, w, h) in faces:
        cropped_face = img[y:y + h, x:x + w]
        return cropped_face  # Return the first detected face

# Initialize webcam
cap = cv2.VideoCapture(0)
count = 0

# Directory to save captured images
save_dir = r'D:\Face_detection_for_door_lock\Samples'
os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from webcam.")
        break

    face = face_extractor(frame)
    if face is not None:
        count += 1

        # Resize and convert the face to grayscale
        face = cv2.resize(face, (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # Save the cropped face
        file_name_path = os.path.join(save_dir, f'user{count}.jpg')
        cv2.imwrite(file_name_path, face)

        # Display the face with count
        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Face Cropper", face)
    else:
        print("Face not found.")
        pass

    # Break if 'Enter' is pressed (ASCII 13) or 500 samples are collected
    if cv2.waitKey(1) == 13 or count == 500:
        break

cap.release()
cv2.destroyAllWindows()
print("Collecting samples complete.")
