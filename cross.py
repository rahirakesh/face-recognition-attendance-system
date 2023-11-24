import cv2
import os
from datetime import datetime

# Load pre-trained SSD model for person detection
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')

# Initialize the video capture
cap = cv2.VideoCapture("test_video.mp4")  # Replace with your video file

# Define the imaginary line (start and end points)
line_start = (0, 630)  # Adjust the coordinates based on your video frame
line_end = (400, 400)  # Adjust the coordinates based on your video frame

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        break

    # Get current date and time
    current_time = datetime.now()
    date = current_time.strftime("%Y%m%d")
    time = current_time.strftime("%H%M%S")

    # Detect persons in the frame using SSD
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Initialize person ID
    person_id = 1

    # Process each detected person
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Confidence threshold
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (startX, startY, endX, endY) = box.astype("int")

            # Check if the person crosses the imaginary line
            if line_start[0] < startX < line_end[0]:
                # Create a unique ID for the person based on person coordinates
                unique_id = hashlib.md5(f"{startX}_{startY}_{endX}_{endY}".encode()).hexdigest()

                # Create a directory for the person if it doesn't exist
                class_id = "MCA1"
                person_directory = os.path.join('enter_person', class_id, date, time, unique_id)
                os.makedirs(person_directory, exist_ok=True)

                # Save person images in the person's folder with numeric person ID
                person_roi = frame[startY:endY, startX:endX]
                image_path = os.path.join(person_directory, f'person_{person_id}_{unique_id}.jpg')
                cv2.imwrite(image_path, person_roi)

                # Increment person ID for the next person
                person_id += 1

                # Draw rectangle around the detected person
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Draw the imaginary line on the frame
    cv2.line(frame, line_start, line_end, (0, 255, 0), 2)

    # Display the video stream
    cv2.imshow('Person Detection and Tracking', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
