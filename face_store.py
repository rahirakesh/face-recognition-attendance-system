""" Face Data Capture Script Documentation

Introduction
This script allows users to capture and store face data for both students and teachers. The program uses the dlib library for
face detection and OpenCV for capturing images from the camera.


Setup
Before running the script, make sure you have the necessary libraries installed. You can install them using the following:
1. pip install opencv-python dlib
2. Shape_predictor_68_face_landmarks.dat     file for face landmark prediction



Structure od directory to save face data
face_data/
|-- department/
|   |-- course/  (for students)
|   |   |-- semester/  (for students)
|   |   |   |-- student_name/
|   |
|   |-- teachers/  (for teachers)
|       |-- teacher_name/

"""


"""
import cv2
import dlib
import os

def create_person_directory(data_directory, department, person_name, choice, course=None, semester=None):
    if choice == 2:
        # For teachers, set course and semester to None
        course = None
        semester = None

    # Create a subdirectory for the person
    if choice == 1:
        # For students, include course and semester in the path
        person_directory = os.path.join(data_directory, department, str(course), str(semester), person_name)
    elif choice == 2:
        # For teachers, use 'teachers' in the path
        person_directory = os.path.join(data_directory, department, 'teachers', person_name)
    else:
        raise ValueError("Invalid choice")

    os.makedirs(person_directory, exist_ok=True)
    return person_directory

# Create a directory to store face data
data_directory = 'face_data'
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Create a face detector and load the pre-trained shape predictor model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def capture_face_data(person_directory, num_images=50):
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
            # Get the face region coordinates
            x, y, w, h = face.left(), face.top(), face.width(), face.height()

            # Check if the face region is valid
            if 0 < x < frame.shape[1] and 0 < y < frame.shape[0]:
                # Save the face data to a file in the person's subdirectory
                face_data_file = os.path.join(person_directory, f"image_{image_counter}.jpg")
                cv2.imwrite(face_data_file, frame[y:y + h, x:x + w])

                # Increment the image counter
                image_counter += 1

                # Display the frame with the camera feed
                cv2.imshow("Capture Face Data", frame)

                # Break out of the loop after capturing the desired number of images
                if image_counter == num_images:
                    break

        # Check for the 'ESC' key to exit the loop
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
def main(choice):   

    if choice == "student":
        department_name = input("Enter the department: ")
        course_name = input("Enter the course: ")
        semester_name = input("Enter the semester: ")
        person_name = input("Enter the name of the person: ")
        directory = create_person_directory(data_directory, department_name, person_name, choice=1, course=course_name, semester=semester_name)
        capture_face_data(directory)
        return 

    elif choice == "teacher":
        department_name = input("Enter the department: ")
        person_name = input("Enter the name of the person: ")
        directory = create_person_directory(data_directory, department_name, person_name, choice=2)
        capture_face_data(directory)
        return 


