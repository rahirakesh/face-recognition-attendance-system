
import cv2
import dlib
import os
print("""Please select Your option :
1 -> Store Student face data
2 -> store Teachers face data""")
def create_person_directory(data_directory, department, course, semester, person_name):
    # Create a subdirectory for the person
    person_directory = os.path.join(data_directory, department, course, semester, person_name)
    os.makedirs(person_directory, exist_ok=True)
    return person_directory

# Create a directory to store face data
data_directory = 'face_data'
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Create a face detector and load the pre-trained shape predictor model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def capture_face_data(department, course, semester, person_name, num_images=100):
    # Create a subdirectory for the person
    person_directory = create_person_directory(data_directory, department, course, semester, person_name)

    # Open a connection to the camera
    cap = cv2.VideoCapture(0)

    # Counter for the number of captured images
    image_counter = 0

    while image_counter < num_images:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = detector(gray)

        for face in faces:
            # Get the landmarks for the face
            landmarks = predictor(gray, face)

            # Draw a rectangle around the face
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Save the face data to a file in the person's subdirectory
            face_data_file = os.path.join(person_directory, f"{person_name}_{image_counter}.jpg")
            cv2.imwrite(face_data_file, frame[y:y+h, x:x+w])

            # Increment the image counter
            image_counter += 1

            # Display the frame with the rectangle around the face
            cv2.imshow("Capture Face Data", frame)

            # Break out of the loop after capturing the desired number of images
            if image_counter == num_images:
                break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

# Get information about the person
department = input("Enter the department: ")
course = input("Enter the course: ")
semester = input("Enter the semester: ")
person_name = input("Enter the name of the person: ")

# Capture and store face data (up to 100 images) in the person's subdirectory
capture_face_data(department, course, semester, person_name, num_images=100)
