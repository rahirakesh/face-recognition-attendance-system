"""
ABOUT AUTHOR:
My name is Rakesh Kumar, and I am the author of this Face Recognition Attendance System. 
I am passionate about implement inovative ideas. With a background in Python developer,
I aimed to create a reliable and efficient system to streamline attendance management.

ABOUT PROJECT:
The Face Recognition Attendance System is a modern solution designed to automate and enhance the traditional attendance tracking process.
Leveraging face recognition technology, the system provides accurate and secure attendance records.

KEY FEATURES:
- Face recognition for secure and contactless attendance.
- Integration with the Attendance Manager for efficient tracking.
- User-friendly interface for both teachers and students.


I hope this system proves to be valuable in simplifying attendance management for educational institutions and organizations.

Feel free to contact me at 9339rahi@gmial.com for any inquiries or feedback.

Thank you for choosing the Face Recognition Attendance System!

Rakesh Kumar
Master of Computer Application 3rd semester
Student of School of Studies in Computer Science and Information Technology
Pt. Ravishankar Shukla University Raipur,(CG ,India)
E-Mail      9339rahi@gmail.com
linked-In   rahirakesh
github      rahirakesh
"""

import mysql.connector     # Using MySQL
import re                  # Import regular expression module 
import smtplib             # For sending email
import ssl                 # for secure email connection 
import random              # For OTP generation
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import Face_Store          # this is a custom module for face registration using OpenCV
from AttendanceManager import TeachersAttendance, Student, main
import settings            # this is a custom module for settings
import bcrypt              # For password hashing
import getpass             # For secure password input
print("""
    WELCOME TO FACE RECOGNITION ATTENDANCE SYSTEM
""")

"""
    The DatabaseConnector class handles the connection to a MySQL database.

    Parameters:
    - host (str): The host address of the database.
    - user (str): The username for accessing the database.
    - password (str): The password for the specified user.
    - database (str): The name of the database to connect to.

    Methods:
    - __init__(self, host, user, password, database):
        Initializes a DatabaseConnector instance and establishes a connection to the database.

    - close_connection(self):
        Closes the database connection and cursor. This method should be called when done with database operations.
    """
class DatabaseConnector:
    def __init__(self, host, user, password, database):
        """
        Initializes a DatabaseConnector instance and establishes a connection to the database.

        Parameters:
        - host (str): The host address of the database.
        - user (str): The username for accessing the database.
        - password (str): The password for the specified user.
        - database (str): The name of the database to connect to.
        """
        try:
            self.db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.db_connection.cursor()
            #print("Connected to the database successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
           
    def close_connection(self):
        """
        Closes the database connection and cursor.

        This method should be called when done with the database operations.
        """
        try:
            self.cursor.close()
            self.db_connection.close()
            print("Connection closed.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

"""
    The DepartmentDatabase class manages database operations related to departments, courses, subjects, and related functionalities.

    Parameters:
    - database_connector: An instance of the database connector used to interact with the database.
    - teachers_instance: An instance of the TeachersDatabase class for managing teachers' information.

    Methods:
    1. display(self): Displays the main menu for department database operations and handles user input.

    2. new_department(self): Adds a new department to the database.

    3. update_department_data(self): Updates department information such as name and email.

    4. remove_department_data(self): Removes department data (under construction).

    5. display_department_details(self): Displays details of existing departments.

    6. add_course_to_database(self, id, name, duration, department_id, exam_type): Adds a new course to the database.

    7. is_valid_department(self, department_id): Checks if a given department ID is valid.

    8. diplay_course_data(self): Displays course data from the database.

    9. update_course_data(self): Updates course information such as name, duration, and exam type.

    10. remove_course_data(self): Removes course data (under construction).

    11. generate_course_id(self, department_id): Generates a unique course ID based on the department ID.

    12. add_new_course(self): Adds a new course to the database.

    13. new_semester(self, class_id, no_of_semester): Adds a new semester for a given class.

    14. generate_semester_id(self): Generates a unique semester ID.

    15. generate_class_id(self, department_id): Generates a unique class ID based on the department ID.

    16. new_class(self, dpt_id, short_name, no_of_room): Adds a new class to the database.

    17. remove_class(self): Removes a class from the database (under construction).

    18. is_valid_class(self, class_id): Checks if a given class ID is valid.

    19. is_semester_id_valid(self, semester_id): Checks if a given semester ID is valid.

    20. display_semester_info(self): Displays information about semesters.

    21. generate_subject_id(self): Generates a unique subject ID.

    22. show_teacher_information(self): Displays information about teachers (delegated to TeachersDatabase instance).

    23. add_new_subject(self): Adds new subjects to the database.

    24. insert_subject_data(self, database_connector, id, subject_name, teacher_id, semester_id):
        Inserts subject data into the subjects table.

    25. show(self): Displays options for updating subjects.

    26. update_subject(self): Updates subject information.

    27. update_subject_name(self, subject_id): Updates the name of a subject.

    28. update_teacher_in_subject(self, subject_id): Updates the teacher associated with a subject.

    29. remove_subject(self): Removes a subject from the database (under construction).

    30. display_subject_details(self): Displays details of existing subjects.
    """
class DepartmentDatabase:
    def __init__(self, database_connector,teachers_instance):
        self.database_connector = database_connector
        self.teachers_bd = teachers_instance      
    def display(self):
        print("""
    _______________________________________________________
    You selected the department database.3
    -------------------------------------------------------
    Please Choose your option
    -------------------------------------------------------
              1 -> Departments 
              2 -> Courses
              3 -> Subjects                           
    -------------------------------------------------------""")
        option = int(input("Enter your choice: "))
        print("_______________________________________________________")
        if option == 1:
            print("""
                  1 -> Add New Department
                  2 -> Update Department Data
                  3 -> Remove Department Data            
                  4 -> Main Page""")
            
            option =int(input("Please enter option : "))
            if option == 1:
                self.new_department()
            elif option == 2:
                self.update_department_data()
            elif option == 3:
                self.remove_department_data()
            elif option == 4:
                self.display()            
            else:
                self.display()
        elif option == 2:
            print("""
                  1 -> Add New Course
                  2 -> Update Course Data
                  3 -> Remove Course Data
                  4 -> Main Page""")
            option=int(input("Please enter option"))
            if option == 1:
                self.add_new_course()
            elif option == 2:
                self.update_course_data()
            elif option == 3:
                self.remove_course_data()
            elif option == 4:
                self.display()
            else:
                self.didplay()
        elif option == 3:
            print("""
                  1 -> Add New Subject
                  2 -> Update Subject Data
                  3 -> Remove Subject
                  4 -> Back
                  5 -> Main Page""")
            option =int(input("Enter your option : "))
            if option == 1:
                self.add_new_subject()
            elif option == 2:
                self.update_subject()
            elif option == 3:
                self.remove_subject()
            elif option == 4:
                self.display()
            else:
                self.display()  
        
    def new_department(self):
        # Retrieve the highest current value of the 'id' column
        query_max_id = "SELECT MAX(id) FROM departments"
        self.database_connector.cursor.execute(query_max_id)
        max_id = self.database_connector.cursor.fetchone()[0]
        
        # Suggest the next available department ID
        next_id = max_id + 1 if max_id is not None else 1
        print("-------------------------------------------------------")
        print(f"Suggested department ID: {next_id}")
        name = input("Enter the department name : ").capitalize()
        short_name = input("Enter the department's short name : ").capitalize()
        number_of_room = int(input("Please enter how many class room available department : "))
        
        # Pass the next_id as a parameter to new_class
        
        
        while True:
            email = input("Enter the department email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                break
            else:
                print("Invalid email format. Please enter a valid email.")
        
        # Execute the MySQL query to insert a new department
        query_insert = "INSERT INTO departments (id, name, email, short_name) VALUES (%s, %s, %s, %s)"
        values_insert = (next_id, name, email, short_name)
        self.database_connector.cursor.execute(query_insert, values_insert)
        self.database_connector.db_connection.commit()
        self.new_class(next_id, short_name, number_of_room)

        print("-------------------------------------------------------")
        print("New department added successfully.")
        ask = input("Do you want to continue in Department? ( Y/N ) - > ")
        if ask.lower() in {'y', 'yes'}:
            self.display()
        elif ask.lower() in {'n', 'no'}:
            # Assuming that DatabaseManager is instantiated and available
            self.db_manager.display_options()
        else:
            print("Invalid option :")
        self.new_department()
        print("_______________________________________________________")

    def update_department_data(self): #update department information
        department_id = int(input("Enter the department ID you want to update  (enter 0 for department data) :"))
        if department_id ==0:
            self.display_department_details()
            department_id = int(input("Enter the department ID you want to update"))
           
        query_check_id = "SELECT id FROM departments WHERE id = %s"
        self.database_connector.cursor.execute(query_check_id, (department_id,))
        existing_id = self.database_connector.cursor.fetchone()
        if existing_id:
            print("""Please select your option 
1 -> Department Name
2 -> E-Mail address""")
            ask = int(input("Please enter your option: "))
            if ask == 1:
                new_name = input("Enter the new department name: ").capitalize()

                # Execute the MySQL query to update the department name
                query_update_name = "UPDATE departments SET name = %s WHERE id = %s"
                self.database_connector.cursor.execute(query_update_name, (new_name, department_id))
                self.database_connector.db_connection.commit()
                print("Department name updated successfully.")
                print("-------------------------------------------------------")
            elif ask == 2:
                while True:
                    new_email = input("Enter the department email: ")
                    if re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                        break
                    else:
                        print("Invalid email format. Please enter a valid email.")
                        self.update_department_data()
                # Execute the MySQL query to update the department email
                query_update_email = "UPDATE departments SET email = %s WHERE id = %s"
                self.database_connector.cursor.execute(query_update_email, (new_email, department_id))
                self.database_connector.db_connection.commit()
                print("Department email updated successfully.")
            else:
                print("Please enter a valid option")
                self.update_department_data()

        print("""Please select your option
1 -> Continue with Update
2 -> Go to Department Database
3 -> Go to Main Page
4 -> Exit
""")
        ask = int(input("Please enter your option "))
        if ask == 1:
            self.update_department_data()
        elif ask == 2:
            self.display()
        elif ask == 3:
            db_manager.display_options()
        elif ask == 4:
            exit()
        else:
            print("please enter a valid option")
            self.display()
    def remove_department_data(self):
        print("Under Construction baby , but tension na le jaldi bana lega tu")
        pass
    def display_department_details(self):
        # Execute the MySQL query to get department IDs and names
        query_get_departments = "SELECT id, name FROM departments"
        self.database_connector.cursor.execute(query_get_departments)
        departments = self.database_connector.cursor.fetchall()

        print("-------------------------------------------------------")
        print("Department Details:")
        print("ID\tName")
        print("-------------------------------------------------------")

        for department in departments:
            print(f"{department[0]}\t{department[1]}")

        print("-------------------------------------------------------")
    def add_course_to_database(self, id,name, duration, department_id, exam_type):
        # Execute the MySQL query to insert a new course
        query_insert_course = "INSERT INTO courses (id,name, duration, dpt_id, exam_type) VALUES (%s,%s, %s, %s, %s)"
        values_insert_course = (id,name, duration, department_id, exam_type)
        self.database_connector.cursor.execute(query_insert_course, values_insert_course)
        self.database_connector.db_connection.commit()
    def is_valid_department(self, department_id):
        query_check_id = "SELECT id FROM departments WHERE id = %s"
        self.database_connector.cursor.execute(query_check_id, (department_id,))
        result = self.database_connector.cursor.fetchone()
        return result is not None

    def diplay_course_data(self):
        # Execute the MySQL query to select all data from the courses table
        query_select_courses = "SELECT * FROM courses"
        self.database_connector.cursor.execute(query_select_courses)
        # Fetch all rows from the result set
        courses_data = self.database_connector.cursor.fetchall()
        # Display the header
        print("Course Data:")
        print("{:<5} {:<150} {:<10} {:<10} {:<5}".format("ID", "Name", "Duration", "Department ID", "Exam Type"))
        print("-" * 185)
        # Display each row of data
        for course in courses_data:
            print("{:<5} {:<150} {:<10} {:<10} {:<5}".format(course[0], course[1], course[2], course[3], course[4]))
        # check if there's no data to display
        if not courses_data:
            print("No course data available.")       

    def update_course_data(self):
        # Take input for the course ID
        course_id = int(input("Enter the course ID you want to update: (Press 0 to find out course id) : "))
        if course_id ==0:
            self.diplay_course_data()
            course_id = int(input("Enter the course ID you want to update : "))
        print("-------------------------------------------------------")

        # Check if the course ID exists
        query_check_id = "SELECT id, name, duration, exam_type FROM courses WHERE id = %s"
        self.database_connector.cursor.execute(query_check_id, (course_id,))
        existing_course = self.database_connector.cursor.fetchone()

        if existing_course:
            print("Existing Course Details:")
            print("ID\tName\tDuration\tExam Type")
            print("-------------------------------------------------------")
            print(f"{existing_course[0]}\t{existing_course[1]}\t{existing_course[2]}\t{existing_course[3]}")
            print("-------------------------------------------------------")

            print("""Please choose which you want to update
    1 -> Course Name
    2 -> Duration
    3 -> Exam Type""")
            ask = int(input("Please Choose your option: "))
            if ask == 1:
                new_name = input("Enter the new course name: ")
                self.update_course_name(course_id, new_name)
            elif ask == 2:
                new_duration = int(input("Enter the new course duration in years: "))
                self.update_course_duration(course_id, new_duration)
            elif ask == 3:
                new_exam_type = input("Enter the new exam type (semester/year): ").lower()
                new_exam_type = new_exam_type[0]
                while new_exam_type not in {"s", "y"}:
                    print("Please enter a valid exam type.")
                    new_exam_type = input("Enter the exam type (type 's' for semester and 'y' for year): ").lower()
                self.update_exam_type(course_id, new_exam_type)
            else:
                print("Please enter a valid option")
                self.display()

        self.handle_update_continue()
    def update_course_name(self, course_id, new_name):
        # Update course name
        query_update_name = "UPDATE courses SET name = %s WHERE id = %s"
        self.database_connector.cursor.execute(query_update_name, (new_name, course_id))
        self.database_connector.db_connection.commit()
        print("Course name updated successfully.")
        print("-------------------------------------------------------")
    def update_course_duration(self, course_id, new_duration):
        # Update course duration
        query_update_duration = "UPDATE courses SET duration = %s WHERE id = %s"
        self.database_connector.cursor.execute(query_update_duration, (new_duration, course_id))
        self.database_connector.db_connection.commit()
        print("Course duration updated successfully.")
        print("-------------------------------------------------------")
    def update_exam_type(self, course_id, new_exam_type):
        # Update exam type
        query_update_exam_type = "UPDATE courses SET exam_type = %s WHERE id = %s"
        self.database_connector.cursor.execute(query_update_exam_type, (new_exam_type, course_id))
        self.database_connector.db_connection.commit()
        print("Exam type updated successfully.")
        print("-------------------------------------------------------")
    def handle_update_continue(self):
        # Handle options after updating course data
        print("""Please select your option
    1 -> Continue with Update
    2 -> Go to Department Database
    3 -> Go to Main Page
    4 -> Exit
    """)
        ask = int(input("Please choose your option "))
        if ask == 1:
            self.update_course_data()
        elif ask == 2:
            self.display()
        elif ask == 3:
            # Assuming that DatabaseManager is instantiated and available
            db_manager.display_options()
        elif ask == 4:
            exit()
        else:
            print("please enter a valid option")
    def remove_course_data(self):
        print("Under Construction baby but tension na le jaldi bana lega tu")
        pass
    def generate_course_id(self, department_id):
        # Execute the MySQL query to get the maximum course ID for the given department
        query_max_course_id = "SELECT MAX(id) FROM courses "
        self.database_connector.cursor.execute(query_max_course_id)
        max_course_id = self.database_connector.cursor.fetchone()[0]

        # Calculate the next course ID
        next_course_id = max_course_id + 1 if max_course_id is not None else 1
        print("New course id is ",next_course_id)

        return next_course_id
    def add_new_course(self):
        department_id = int(input("Please Enter department Id (press 0 for find out department id): "))
        print("-------------------------------------------------------")

        if department_id == 0:
            self.display_department_details()
            department_id = int(input("Please Enter department Id for the new course: "))

        if self.is_valid_department(department_id):
            course_id = self.generate_course_id(department_id)
           

            name = input("Enter the course name: ")
            duration = int(input("Enter the course duration in years: "))
            exam_type = input("Enter the exam type (semester/year): ").lower()
            exam_type =exam_type[0]
            print("error posibale ", exam_type)
            if exam_type == "s":
                no_of_semester = ((duration * 12 )/6)
                print("no of semester", no_of_semester)
                self.new_semester(department_id,no_of_semester)
                print("pass the line")
            print("-------------------------------------------------------")

            #print("exam exam_type",exam_type)
            while exam_type[0] not in {"s", "y"}:
                print("Please enter a valid exam type.")
                exam_type = input("Enter the exam type (also type 's' for semester and 'y' for year): ").lower()

            # Other course details...
            self.add_course_to_database(course_id, name, duration, department_id, exam_type)
            print("""Course Data Add Successfully
-------------------------------------------------------
Please select your option
1 -> Continue with New course
2 -> Go to Department Database
3 -> Go to Main Page
4 -> Exit
_______________________________________________________
""")
            ask = int(input("Please choose your option "))
            
            if ask == 1:
                self.add_new_course()
            elif ask == 2:
                self.display()
            elif ask == 3:
                    # Assuming that DatabaseManager is instantiated and available
                db_manager.display_options()
            elif ask == 4:
                exit()
            else:
                print("Please enter a valid option")
        else:
            print("Invalid department ID.Enter a valid department ID.")
            self.add_new_course()  # Retry adding a new course
    def new_semester(self,class_id,no_of_semester):
        print("Adding a New Semester:")        
        if not self.is_valid_class(class_id):
            print("Invalid class ID. Please enter a valid class ID.")
            return
        short_dpt =input("Please enter short name of course : ")
        i = 1
        while i<=no_of_semester:
            # Generate the next available semester ID
            semester_id = self.generate_semester_id()            
            semester_name = f"{short_dpt}{i}"
            # Execute the MySQL query to insert a new semester
            query_insert_semester = "INSERT INTO semesters (id, class_id,semester_name) VALUES (%s, %s,%s)"
            values_insert_semester = (semester_id, class_id, semester_name)
            self.database_connector.cursor.execute(query_insert_semester, values_insert_semester)
            self.database_connector.db_connection.commit()
            i = i+1  
    def generate_semester_id(self):
        # Execute the MySQL query to get the maximum semester ID for the given class
        query_max_semester_id = "SELECT MAX(id) FROM semesters"
        self.database_connector.cursor.execute(query_max_semester_id)
        max_semester_id = self.database_connector.cursor.fetchone()[0]
        # Calculate the next semester ID
        next_semester_id = max_semester_id + 1 if max_semester_id is not None else 1
        return next_semester_id
    def generate_class_id(self, department_id):
        # Execute the MySQL query to get the maximum class ID for the given department
        query_max_class_id = "SELECT MAX(id) FROM classes WHERE dpt_id = %s"
        self.database_connector.cursor.execute(query_max_class_id, (department_id,))
        max_class_id = self.database_connector.cursor.fetchone()[0]

        # Calculate the next class ID for the given department
        next_class_id = max_class_id + 1 if max_class_id is not None else 1

        # Create a unique class ID by combining department_id and next_class_id
        unique_class_id = f"{department_id}-{next_class_id}"

        return unique_class_id
    def new_class(self,dpt_id,short_name,no_of_room):
        print("Adding a New Class:")        
        # Validate department ID
        if not self.is_valid_department(dpt_id):
            print("Invalid department ID. Please enter a valid department ID.")
            self.new_department()
        # Generate the next available class ID
        
        i = 1
        while i<= no_of_room:
            class_id = self.generate_class_id()
            class_name = f"{short_name}{i}"
            # Execute the MySQL query to insert a new class
            query_insert_class = "INSERT INTO classes (id, dpt_id,class_name) VALUES (%s, %s, %s)"
            values_insert_class = (class_id, dpt_id,class_name)
            self.database_connector.cursor.execute(query_insert_class, values_insert_class)
            self.database_connector.db_connection.commit()
            i = i+1
        print("add all classes successfuly")
    def remove_class(self):
        print("Under construction")
        self.new_class()
        pass
        # print("Removing Class:")
        # class_id = int(input("Enter the class ID you want to remove: "))
        # # Validate class ID
        # if self.is_valid_class(class_id):
        #     # Execute the MySQL query to remove the class
        #     query_remove_class = "DELETE FROM classes WHERE id = %s"
        #     self.database_connector.cursor.execute(query_remove_class, (class_id,))
        #     self.database_connector.db_connection.commit()

        #     print("Class removed successfully.")
        # else:
        #     print("Invalid class ID. Please enter a valid class ID.")       
    def is_valid_class(self, class_id):
        # Execute the MySQL query to check if the class ID exists
        query_check_class_id = "SELECT id FROM classes WHERE id = %s"
        self.database_connector.cursor.execute(query_check_class_id, (class_id,))
        existing_id = self.database_connector.cursor.fetchone()

        # Return True if the class ID exists, False otherwise
        return existing_id is not None
    def generate_class_id(self):
    # Execute the MySQL query to get the maximum class ID for the given department
        query_max_class_id = "SELECT MAX(id) FROM classes"
        self.database_connector.cursor.execute(query_max_class_id)
        max_class_id = self.database_connector.cursor.fetchone()[0]

        # Calculate the next class ID
        next_class_id = max_class_id + 1 if max_class_id is not None else 1

        return next_class_id
    
    
    
    #need to change  it must be return only true or false
    def is_semester_id_valid(self,semester_id):
        # Execute the MySQL query to check if the semester ID exists
        query_check_semester_id = "SELECT id FROM semesters WHERE id = %s"
        self.database_connector.cursor.execute(query_check_semester_id, (semester_id,))
        result = self.database_connector.cursor.fetchone()
        # Return True if the semester ID exists, False otherwise
        return result is not None 
    
    def display_semester_info(self):
        # Execute the MySQL query to retrieve semester information
        query_semester_info = """
            SELECT
                semesters.id AS semester_id,
                semesters.semester_name,
                departments.short_name AS dpt_short_name
            FROM
                semesters
            JOIN
                classes ON semesters.class_id = classes.id
            JOIN
                departments ON classes.dpt_id = departments.id
        """
        self.database_connector.cursor.execute(query_semester_info)
        semester_info = self.database_connector.cursor.fetchall()

        # Display the result
        print("{:<12} {:<20} {:<20}".format("Semester ID", "Semester Name", "Department Short Name"))
        print("-" * 52)
        for row in semester_info:
            print("{:<12} {:<20} {:<20}".format(row[0], row[1], row[2]))
        return 0
    def generate_subject_id(self):
        query_max_subject_id = "SELECT MAX(id) FROM subjects"
        self.database_connector.cursor.execute(query_max_subject_id)
        max_subject_id = self.database_connector.cursor.fetchone()[0]

        # Calculate the next subject ID
        next_subject_id = max_subject_id + 1 if max_subject_id is not None else 1

        return next_subject_id
    def show_teacher_information(self):
        # Delegate the call to the TeachersDatabase instance
        self.teachers_bd.show_teacher_information()
    def add_new_subject(self): 
        semester_id = int(input("Please Enter The Semester Id (Enter 0 for finding out semester's id): "))
        if semester_id == 0:
            self.display_semester_info()
            semester_id = int(input("Please Enter The Semester Id: "))
        # elif not self.is_semester_id_valid(semester_id):
        #     print("Invalid Semester ID. Please enter a valid Semester ID.")
        #     self.add_new_subject() 

        no_of_subjects = int(input("Please enter the number of subjects available: "))
        for i in range(1, no_of_subjects + 1):
            subject_id = self.generate_subject_id()
            subject_name = input("Please enter subject name: ")
            teacher_id = int(input("Please enter teacher id (Enter 0 to find out teachers data): "))
            if teacher_id == 0:
                self.show_teacher_information()
                teacher_id = int(input("Please Enter Teacher Id: "))
            elif not self.teachers_bd.teacher_id_valid_or_not(teacher_id):
                print("Invalid Teacher ID. Please enter a valid Teacher ID.")
                self.add_new_subject()

            self.insert_subject_data(self.database_connector,subject_id, subject_name, teacher_id, semester_id)

        print("""
            Select your option
            1 -> Continue to add subjects
            2 -> Back
            3 -> Main Page
            """)
        ask = int(input("Please Enter Your Option: "))
        if ask == 1:
            self.add_new_subject()
        elif ask == 2:
            self.display()
        else:
            db_manager.display_options()
     
    def insert_subject_data(self,database_connector,id, subject_name, teacher_id, semester_id):
        # Execute the MySQL query to insert data into the subjects table
        query_insert_subject = "INSERT INTO subjects (id, name, teacher, semester) VALUES (%s, %s, %s)"
        values_insert_subject = (id,subject_name, teacher_id, semester_id)

        try:
            database_connector.cursor.execute(query_insert_subject, values_insert_subject)
            database_connector.db_connection.commit()
            print("Subject data inserted successfully.")
        except Exception as e:
            print(f"Error: {e}")
            database_connector.db_connection.rollback()

    def show(self):
        print("""Select your option 
              1 -> Continue to Update
              2 -> Back 
              3 -> Main Page""")
        ask = int(input("Enter your optin : "))
        if ask == 1:
            self.update_subject()
        elif ask == 2:
            self.display()
        else:
            db_manager.display_options()
    def update_subject(self):
        print("""Select Your Option : 
            1 -> Update Subject Name
            2 -> Update Teacher Name""")
        
        option = int(input("Please choose your option: "))
        
        if option == 1:
            subject_id = int(input("Please enter the Subject ID to update: "))
            self.update_subject_name(subject_id)
            self.show()
        elif option == 2:
            subject_id = int(input("Please enter the Subject ID to update: "))
            self.update_teacher_in_subject(subject_id)
            self.show()
        else:
            print("Invalid option. Please select a valid option.")
            self.show()
        
    def update_subject_name(self, subject_id):
        new_name = input("Please enter the new name for the subject: ")

        # Execute the MySQL query to update the subject name in the subjects table
        query_update_name = "UPDATE your_table_name SET name = %s WHERE id = %s"
        values_update_name = (new_name, subject_id)

        try:
            self.database_connector.cursor.execute(query_update_name, values_update_name)
            self.database_connector.db_connection.commit()
            print("Subject name updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
            self.database_connector.db_connection.rollback()

    def update_teacher_in_subject(self, subject_id):
        new_teacher_id = int(input("Please enter the new Teacher ID for the subject: "))

        # Execute the MySQL query to update the teacher in the subject in the subjects table
        query_update_teacher = "UPDATE your_table_name SET teacher = %s WHERE id = %s"
        values_update_teacher = (new_teacher_id, subject_id)

        try:
            self.database_connector.cursor.execute(query_update_teacher, values_update_teacher)
            self.database_connector.db_connection.commit()
            print("Teacher in subject updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
            self.database_connector.db_connection.rollback()

    def remove_subject(self):
        print("Under Construction baby but tension na le jaldi bana lega tu")
        self.add_new_subject()
        pass
    
    def show_subjects(self, semester_id):
        # Retrieve the subjects for the given semester ID
        subjects = self.get_subjects(semester_id)

        if subjects:
            print(f"Subjects for Semester ID {semester_id}:\n")
            for subject in subjects:
                print(subject)
        else:
            print(f"No subjects found for Semester ID {semester_id}")

    def get_subjects(self, semester_id):
        # Define the SQL query to retrieve subject names for a given semester_id
        query = "SELECT name FROM subjects WHERE semester = %s"

        try:
            # Execute the query
            self.database_connector.cursor.execute(query, (semester_id,))

            # Fetch all the rows
            subjects_data = self.database_connector.cursor.fetchall()

            # Extract subject names from the result
            subjects_names = [row[0] for row in subjects_data]

            return subjects_names
        except Exception as e:
            print(f"Error: {e}")
            return None

"""
    The `StudentDatabase` class manages student-related functionalities, including adding, updating, and removing student data.

    Attributes:
    - database_connector: An instance of the `DatabaseConnector` class providing database connection.
    - department_database: An instance of the `DepartmentDatabase` class for accessing department-related functionalities.

    Methods:
    - __init__(self, database_connector, department): Initializes the `StudentDatabase` class.
    - display(self): Displays options for adding, updating, and removing student data, and navigating to other pages.
    - new_student(self): Adds a new student to the database.
    - update_student(self): Displays options for updating student data and initiates the update process.
    - update_name(self): Updates the student's name.
    - update_email(self): Updates the student's email.
    - update_parent_name(self): Updates the student's parent name.
    - update_parent_contact(self): Updates the student's parent contact number.
    - update_parent_email(self): Updates the student's parent email.
    - remove_student(self): Placeholder for removing student data (Under Construction).
    - student_information(self): Displays information for a specific student.
    """
class StudentDatabase:
    def __init__(self, database_connector,department):
        self.database_connector = database_connector
        self.department_database = department

    def display(self):
        print("""
              Please select your option
              1 -> Add new student
              2 -> Update student data
              3 -> Remove Student data
              4 -> Show Student Information
              5 -> Store or Update Face Data
              6 -> Main Page
        """)
        option = int(input("Please enter your option: "))
        if option == 1:
            self.new_student()
        elif option == 2:
            self.update_student()
        elif option == 3:
            self.remove_student()
        elif option == 4:
            self.student_information()
        elif option ==5:
            Face_Store.main("student")
        elif option == 6:
            db_manager.display_options()
        else:
            print("Invalid option. Please enter a valid option.")
            self.displa()

    def new_student(self):
        # Retrieve the highest current value of the 'id' column
        query_max_id = "SELECT MAX(id) FROM students"
        self.database_connector.cursor.execute(query_max_id)
        max_id = self.database_connector.cursor.fetchone()[0]

        # Suggest the next available student ID
        next_id = max_id + 1 if max_id is not None else 1
        print(f"Suggested student ID: {next_id}")

        # Get student details from user input
        name = input("Enter the student's name: ").capitalize()
        email = input("Enter the student's email: ")
        semester_id = int(input("Enter the semester ID (Enter 0 to find out semester): "))
        if semester_id == 0:
            self.department_database.display_semester_info()
        parent_name = input("Enter the parent's name: ").capitalize()
        parent_contact = input("Enter the parent's contact number: ")
        parent_email = input("Enter the parent's email: ")

        # Execute the MySQL query to insert a new student
        query_insert_student = """
            INSERT INTO students (id, name, email, semester, parent_name, parent_contact, parent_email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values_insert_student = (next_id, name, email, semester_id, parent_name, parent_contact, parent_email)
        self.database_connector.cursor.execute(query_insert_student, values_insert_student)
        self.database_connector.db_connection.commit()

        print("New student added successfully.")
        self.display()  # Go back to the main display

    def update_student(self):
        print("""Please select your option 
              1 -> update student name
              2 -> email              
              3 -> parent_name
              4 -> parent contact
              5 -> parent email
              6 -> Back
              7 -> Main Page
              """)
        option =int(input("Please enter your option :"))
        if option == 1:
            self.update_name()
        elif option == 2:
            self.update_email()        
        elif option == 3:
            self.update_parent_name()
        elif option == 4:
            self.update_parent_contact()
        elif option == 5:
            self.update_parent_email()
        elif option == 6:
            self.display()  # Go back to the main display
        elif option == 7:
           db_manager.display_options()
        else:
            print("Invalid option. Please enter a valid option.")
            self.update_student()    
    
    def update_name(self):
        student_id = int(input("Enter the student ID to update name: "))
        new_name = input("Enter the updated name: ").capitalize()
        # Execute the MySQL query to update the student's name
        query_update_name = "UPDATE students SET name = %s WHERE id = %s"
        values_update_name = (new_name, student_id)
        self.database_connector.cursor.execute(query_update_name, values_update_name)
        self.database_connector.db_connection.commit()
        print("Student name updated successfully.")
        self.display()  # Go back to the main display
    
    def update_email(self):
        student_id = int(input("Enter the student ID to update email: "))
        new_email = input("Enter the updated email: ")
        # Execute the MySQL query to update the student's email
        query_update_email = "UPDATE students SET email = %s WHERE id = %s"
        values_update_email = (new_email, student_id)
        self.database_connector.cursor.execute(query_update_email, values_update_email)
        self.database_connector.db_connection.commit()
        print("Student email updated successfully.")
        self.display()    
    
    def update_parent_name(self):
        student_id = int(input("Enter the student ID to update parent name: "))
        new_parent_name = input("Enter the updated parent name: ").capitalize()
        # Execute the MySQL query to update the student's parent name
        query_update_parent_name = "UPDATE students SET parent_name = %s WHERE id = %s"
        values_update_parent_name = (new_parent_name, student_id)
        self.database_connector.cursor.execute(query_update_parent_name, values_update_parent_name)
        self.database_connector.db_connection.commit()
        print("Student's parent name updated successfully.")
        self.display()  # Go back to the main display
    
    def update_parent_contact(self):
        student_id = int(input("Enter the student ID to update parent contact: "))
        new_parent_contact = input("Enter the updated parent contact number: ")
        # Execute the MySQL query to update the student's parent contact
        query_update_parent_contact = "UPDATE students SET parent_contact = %s WHERE id = %s"
        values_update_parent_contact = (new_parent_contact, student_id)
        self.database_connector.cursor.execute(query_update_parent_contact, values_update_parent_contact)
        self.database_connector.db_connection.commit()
        print("Student's parent contact updated successfully.")
        self.display()  # Go back to the main display
    
    def update_parent_email(self):
        student_id = int(input("Enter the student ID to update parent email: "))
        new_parent_email = input("Enter the updated parent email: ")
        # Execute the MySQL query to update the student's parent email
        query_update_parent_email = "UPDATE students SET parent_email = %s WHERE id = %s"
        values_update_parent_email = (new_parent_email, student_id)
        self.database_connector.cursor.execute(query_update_parent_email, values_update_parent_email)
        self.database_connector.db_connection.commit()
        print("Student's parent email updated successfully.")
        self.display()  # Go back to the main display
   
    def remove_student(self):
        print("Under Construction")  # the logic for removing student data here
   
    def student_information(self):
        student_id = int(input("Enter the student ID to view information: "))
        # Retrieve student information from the database
        query_student_info = """
            SELECT id, name, email, semester, parent_name, parent_contact, parent_email
            FROM students WHERE id = %s
        """
        self.database_connector.cursor.execute(query_student_info, (student_id,))
        student_info = self.database_connector.cursor.fetchone()
        if student_info:
            print("\nStudent Information:")
            print(f"ID: {student_info[0]}")
            print(f"Name: {student_info[1]}")
            print(f"Email: {student_info[2]}")
            print(f"Semester ID: {student_info[3]}")
            print(f"Parent's Name: {student_info[4]}")
            print(f"Parent's Contact: {student_info[5]}")
            print(f"Parent's Email: {student_info[6]}")
        else:
            print(f"Student with ID {student_id} not found.")
        self.display()  # Go back to the main display 

"""
    The `TeacherDatabase` class manages teacher-related functionalities, including adding, updating, and removing teacher data.

    Attributes:
    - database_connector: An instance of the `DatabaseConnector` class providing database connection.

    Methods:
    - __init__(self, database_connector): Initializes the `TeacherDatabase` class.
    - display(self): Displays options for adding, updating, and removing teacher data, and navigating to other pages.
    - display_department_details(self): Displays department details.
    - make_new_teacher_id(self): Generates a new teacher ID.
    - add_new_teacher(self): Adds a new teacher to the database.
    - show_teacher_information(self): Displays teacher information and prompts for teacher ID.
    - teacher_id_valid_or_not(self, teacher_id): Checks if a given teacher ID is valid.
    - update_teacher_name(self, teacher_id, new_name): Updates the teacher's name.
    - update_teacher_contact(self, teacher_id, new_contact): Updates the teacher's contact number.
    - update_teacher_email(self, teacher_id, new_email): Updates the teacher's email.
    - update_teacher_data(self, teacher_id): Displays options for updating teacher data and initiates the update process.
    - remove_teacher_data(self): Placeholder for removing teacher data (Under Construction).
    """
class TeacherDatabase:
    def __init__(self, database_connector):
        self.database_connector = database_connector        
    def display(self):
        print("""
              Please select option
              1 -> Add New Teacher's Data
              2 -> Update Teacher's Data
              3 -> Remove Teacher's Data
              4 -> Face Data
              5 -> Go To Main Page
              6 -> Exit""")
        ask = int(input("Choose your option: "))
        if ask not in {1, 2, 3, 4, 5}:
            print("Please enter a valid number.")
            self.display()
        elif ask == 1:
            self.add_new_teacher()
        elif ask == 2:
            id = int(input("Please enter teacher's id : (enter 0 for find out teachers id) "))            
            if id ==0:
                id=self.show_teacher_information()                
            self.update_teacher_data(id)  # Added parentheses for method call
        elif ask == 3:            
            self.remove_teacher_data()  # Added parentheses for method call
        elif ask == 4:
            Face_Store.main("teacher")
        elif ask == 5:
            db_manager.display_options()
        else:
            exit()
    def display_department_details(self):
        # Execute the MySQL query to get department IDs and names
        query_get_departments = "SELECT id, name FROM departments"
        self.database_connector.cursor.execute(query_get_departments)
        departments = self.database_connector.cursor.fetchall()
        print("-------------------------------------------------------")
        print("Department Details:")
        print("ID\tName")
        print("-------------------------------------------------------")
        for department in departments:
            print(f"{department[0]}\t{department[1]}")
        print("-------------------------------------------------------")
    def make_new_teacher_id(self):
        # Retrieve the highest current value of the 'id' column
        query_max_id = "SELECT MAX(id) FROM teachers"
        self.database_connector.cursor.execute(query_max_id)
        max_id = self.database_connector.cursor.fetchone()[0]
        # Suggest the next available teacher ID
        next_id = max_id + 1 if max_id is not None else 1
        return next_id
    def add_new_teacher(self):
        print("Adding a New Teacher:")    
        id =  self.make_new_teacher_id()
        # Take input for teacher details
        name = input("Enter the teacher's name: ").capitalize()
        dpt_id = int(input("Enter the department ID for the new teacher(press 0 to find out department id) "))
        if dpt_id ==0:
            self.display_department_details()
            dpt_id = int(input("Enter the department ID for the new teacher"))
        # Validate and prompt for email until a valid email is entered
        while True:
            email = input("Enter the teacher's email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                break
            else:
                print("Invalid email format. Please enter a valid email.")
        # Validate and prompt for contact until a valid 10-digit number is entered
        while True:
            contact = input("Enter the teacher's contact number: ")
            if contact.isdigit() and len(contact) == 10:
                break
            else:
                print("Invalid contact number. Please enter a 10-digit number.")
        # Execute the MySQL query to insert a new teacher
        query_insert_teacher = "INSERT INTO teachers (id,name, dpt_id, email, contact) VALUES (%s,%s, %s, %s, %s)"
        values_insert_teacher = (id,name, dpt_id, email, contact)
        self.database_connector.cursor.execute(query_insert_teacher, values_insert_teacher)
        self.database_connector.db_connection.commit()
        print("New teacher added successfully.")
        print("-------------------------------------------------------")
        self.display()
    def show_teacher_information(self):
        print("Displaying Teacher Information (ID and Name):")
        # Execute the MySQL query to get teacher IDs and names
        query_get_teachers = "SELECT id, name FROM teachers"
        self.database_connector.cursor.execute(query_get_teachers)
        teachers = self.database_connector.cursor.fetchall()
        print("-------------------------------------------------------")
        print("Teacher Information:")
        print("ID\tName")
        print("-------------------------------------------------------")
        for teacher in teachers:
            print(f"{teacher[0]}\t{teacher[1]}")
        print("-------------------------------------------------------")
        id = int(input("Please enter teacher's id "))
        return id       
    def teacher_id_valid_or_not(self, teacher_id):
        # Execute the MySQL query to check if the teacher ID exists
        query_check_id = "SELECT id FROM teachers WHERE id = %s"
        self.database_connector.cursor.execute(query_check_id, (teacher_id,))
        existing_id = self.database_connector.cursor.fetchone()
        # Return True if the teacher ID exists, False otherwise    
        return existing_id is not None
    def update_teacher_name(self, teacher_id, new_name):
        # Update teacher name
        query_update_name = "UPDATE teachers SET name = %s WHERE id = %s"
        self.database_connector.cursor.execute(query_update_name, (new_name, teacher_id))
        self.database_connector.db_connection.commit()
        print("Teacher name updated successfully.")
        self.display()
    def update_teacher_contact(self, teacher_id, new_contact):
        # Validate and prompt for updated contact until a valid 10-digit number is entered
        while not new_contact.isdigit() or len(new_contact) != 10:
            print("Invalid contact number. Please enter a valid 10-digit number.")
            new_contact = input("Enter the new contact number: ")
        # Update teacher contact
        query_update_contact = "UPDATE teachers SET contact = %s WHERE id = %s"
        self.database_connector.cursor.execute(query_update_contact, (new_contact, teacher_id))
        self.database_connector.db_connection.commit()
        print("Teacher contact updated successfully.")
        self.display()
    def update_teacher_email(self, teacher_id, new_email):
        # Validate and prompt for updated email until a valid email is entered
        while not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            print("Invalid email format. Please enter a valid email.")
            new_email = input("Enter the new email: ")
        # Update teacher email
        query_update_email = "UPDATE teachers SET email = %s WHERE id = %s"
        self.database_connector.cursor.execute(query_update_email, (new_email, teacher_id))
        self.database_connector.db_connection.commit()
        print("Teacher email updated successfully.")
        self.display()
    # def update_teacher_department(self, teacher_id):
    #     # Display available departments to choose from
    #     self.department.display_department_details()
    #     # Take input for the updated department ID
    #     new_department_id = int(input("Enter the updated department ID: "))
    #     # Validate if the entered department ID is valid
    #     if self.department.is_valid_department(new_department_id):
    #         # Update the teacher's department
    #         query_update_department = "UPDATE teachers SET dpt_id = %s WHERE id = %s"
    #         self.database_connector.cursor.execute(query_update_department, (new_department_id, teacher_id))
    #         self.database_connector.db_connection.commit()
    #         print("Teacher department updated successfully.")
    #     else:
    #         print("Invalid department ID. Please enter a valid department ID.")
    #         self.update_teacher_department(teacher_id)
    #     self.display()
    def update_teacher_data(self, teacher_id):
        print("""
Select the information you want to update:
1 -> Name
2 -> Contact
3 -> Email
4 -> Department
5 -> Go To Main Page
""")
        ask = int(input("Please enter your option: "))
        if ask not in {1, 2, 3, 4, 5}:
            print("Please enter a valid option.")
            self.update_teacher_data(teacher_id)
        elif ask == 1:
            new_name = input("Enter the new name: ").capitalize()
            self.update_teacher_name(teacher_id, new_name)
        elif ask == 2:
            new_contact = input("Enter the new contact number: ")
            self.update_teacher_contact(teacher_id, new_contact)
        elif ask == 3:
            new_email = input("Enter the new email: ")
            self.update_teacher_email(teacher_id, new_email)
        elif ask == 4:
            print("Under Cunstruction ")
            return
        #     self.update_teacher_department(teacher_id)
        elif ask == 5:
            db_manager.display_options()
    def remove_teacher_data(self):
        print("Under Construction baby but tension na le jaldi bana lega tu")


"""
    The `CameraManager` class handles camera assignments, removal, and information display.

    Attributes:
    - database_connector: An instance of the `DatabaseConnector` class providing database connection.
    - department: An instance of the `Department` class for department-related functionalities.

    Methods:
    - __init__(self, database_connector, department): Initializes the `CameraManager` class.
    - display(self): Displays options for assigning cameras, removing cameras, and returning to the main page.
    - camera_info(self, dpt_id): Retrieves and displays information about cameras assigned to classes in a department.
    - remove(self, camera_id): Removes a camera entry from the database.
    - save_data(self, camera_id, type, class_id): Saves camera assignment data to the database.
    - get_highest_camera_id(self): Retrieves the highest camera ID from the database.
    - assign_camera(self): Initiates the camera assignment process for a department.
    - class_info(self, dpt_id): Retrieves and displays information about classes in a department.

    """
class CameraManager:
    def __init__(self, database_connector, department):
        self.database_connector = database_connector
        self.department = department        

    def display(self):
        print("""Select Your Option:
              1 -> Assign Camera to class
              2 -> Remove Camera
              3 -> Main Page""")
        ask = int(input("Please enter your option: "))
        if ask == 1:
            camera_id = self.get_highest_camera_id()
            print("Camera id: ", camera_id)
            type = input("Please enter type (cover inside or outside): ")
            type = type[0]
            class_id = int(input("Please enter class _id (enter 0 to find out class id): "))
            while class_id == 0:
                self.department.display_department_details()
                class_id = int(input("Please enter class _id (enter 0 to find out class id): "))
            self.save_data(camera_id, type, class_id)
        elif ask == 2:
            camera_id = int(input("Please enter camera id: ( enter 0 to find out camera id )"))
            while camera_id ==0:
                dpt_id = int(input("Please enter department id ( enter 0 to find out Department id )"))
                while dpt_id == 0:
                    department.display_department_details()
                    dpt_id = int(input("Please enter department id ( enter 0 to find out Department id )"))                
                self.camera_info(dpt_id)
            self.remove(camera_id)
        else:
            self.db_manager.display_option()
    
    def camera_info(self, dpt_id):
        try:
            # Define the SQL query to retrieve information from both cameras and classes tables
            query = """
                SELECT c.id AS camera_id, c.inside, cl.id AS class_id, cl.class_name
                FROM cameras c
                JOIN classes cl ON c.class = cl.id
                WHERE cl.dpt_id = %s;
            """

            # Execute the query
            self.database_connector.cursor.execute(query, (dpt_id,))

            # Fetch all the rows
            camera_info_data = self.database_connector.cursor.fetchall()

            # Display the information
            if camera_info_data:
                print("Camera Information:")
                for row in camera_info_data:
                    print(f"Camera ID: {row[0]}, Inside: {'Yes' if row[1] else 'No'}, Class ID: {row[2]}, Class Name: {row[3]}")
            else:
                print("No camera information found for the given department ID.")

        except Exception as e:
            print(f"Error retrieving camera information: {e}")

    def remove(self, camera_id):
        try:
            # Define the SQL query to delete a camera entry
            query = "DELETE FROM cameras WHERE id = %s;"

            # Execute the query
            self.database_connector.cursor.execute(query, (camera_id,))

            # Commit the changes to the database
            self.database_connector.db_connection.commit()

            print(f"Camera with ID {camera_id} removed successfully.")
        except Exception as e:
            print(f"Error removing camera: {e}")

    def save_data(self, camera_id, type, class_id):
        try:
            # Define the SQL query to insert a new camera entry
            query = "INSERT INTO cameras (id, inside, class) VALUES (%s, %s, %s);"
            values = (camera_id, type == 'i', class_id)

            # Execute the query
            self.database_connector.cursor.execute(query, values)

            # Commit the changes to the database
            self.database_connector.db_connection.commit()

            print(f"Camera data saved successfully.")
        except Exception as e:
            print(f"Error saving camera data: {e}")

    def get_highest_camera_id(self):
        try:
            # Execute the SQL query to retrieve the highest camera ID
            query = "SELECT MAX(id) FROM cameras;"
            self.database_connector.cursor.execute(query)
            # Fetch the result
            result = self.database_connector.cursor.fetchone()
            # If result is not None, return the highest ID, otherwise return 0
            return result[0] if result[0] is not None else 0
        except Exception as e:
            print(f"Error retrieving highest camera ID: {e}")
            return 0

    def assign_camera(self):
        dpt_id = int(input("Please enter the department id (Enter 0 to find out class id): "))
        while dpt_id != 0:
            self.department.display_department_details()
            dpt_id = int(input("Please enter the department id (Enter 0 to find out class id): "))
            self.class_info(dpt_id)

    def class_info(self, dpt_id):
        try:
            # Define the SQL query to retrieve class information based on dpt_id
            query = "SELECT * FROM classes WHERE dpt_id = %s;"

            # Execute the query
            self.database_connector.cursor.execute(query, (dpt_id,))

            # Fetch all the rows
            class_data = self.database_connector.cursor.fetchall()

            # Display the information
            if class_data:
                print("Class Information:")
                for row in class_data:
                    print(f"Class ID: {row[0]}, Department ID: {row[1]}, Class Name: {row[2]}")
            else:
                print("No classes found for the given department ID.")

        except Exception as e:
            print(f"Error retrieving class information: {e}")


"""
    The `TimeTableManager` class manages the creation and update of time tables for different semesters.

    Attributes:
    - database_connector: An instance of the `DatabaseConnector` class providing database connection.
    - department: An instance of the `Department` class for department-related functionalities.

    Methods:
    - __init__(self, database_connector, department): Initializes the `TimeTableManager` class.
    - get_subjects(self, semester_id): Retrieves the list of subjects for a given semester.
    - create_table(self, table_name): Creates a new table in the database if it does not exist.
    - create_time_table(self, semester_id): Creates a new time table for the specified semester.
    - save_data(self, tablename, subject, start_time, end_time): Saves time table entry to the database.
    - check_table_available(self, tablename): Checks if a table exists in the database.
    - update_entry(self, semester_id): Updates the time table entries for a given semester.
    - display_semester_info(self): Displays information about semesters.
    - display(self): Displays options for adding, updating, and managing time tables.

    """
class TimeTableManager:    
    def __init__(self, database_connector, department):
        self.database_connector = database_connector
        self.department = department
            
    def get_subjects(self, semester_id):
        # Define the SQL query to retrieve subject names for a given semester_id
        query = "SELECT name FROM subjects WHERE semester = %s;"

        try:
            # Execute the query
            self.database_connector.cursor.execute(query, (semester_id,))

            # Fetch all the rows
            subjects_data = self.database_connector.cursor.fetchall()

            # Extract subject names from the result
            subjects_names = [row[0] for row in subjects_data]

            return subjects_names
        except Exception as e:
            print(f"Error: {e}")
            return None
   
    def create_table(self, table_name):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} (\
        subject_name VARCHAR(50),\
        start_time TIME,\
        end_time TIME\
        );"

        try:
            # Execute the query to create the table
            self.database_connector.cursor.execute(query)
            # Commit the changes
            self.database_connector.db_connection.commit()
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            # If an error occurs, print the error and rollback the changes
            print(f"Error creating table: {e}")
            self.database_connector.db_connection.rollback()

    def create_time_table(self, semester_id):
        tablename = "time_table" + str(semester_id)
        self.create_table(tablename)
        
        subjects = self.get_subjects(semester_id)

        for subject in subjects:
            print("________________________________________________")
            print(subject)
            start_time = input("Please enter Start time: ")
            end_time = input("Please enter end time: ")
            self.save_data(tablename,subject,start_time,end_time)
        print("Time table add successfully")
            
    def save_data(self, tablename, subject, start_time, end_time):
        try:
            # Construct the SQL query
            query = f"INSERT INTO {tablename} (subject_name, start_time, end_time) VALUES (%s, %s, %s);"
            values = (subject, start_time, end_time)

            # Execute the query
            self.database_connector.cursor.execute(query, values)

            # Commit the changes to the database
            self.database_connector.db_connection.commit()
            
        except Exception as e:            
            print(f"Error: {e}")
            # Rollback the changes if an error occurs
            self.database_connector.db_connection.rollback()

    def check_table_available(self, tablename):
        # Implement logic to check if the table exists in the MySQL database
        query = f"SHOW TABLES LIKE '{tablename}';"

        try:
            # Execute the query
            self.database_connector.cursor.execute(query)

            # Fetch the result
            result = self.database_connector.cursor.fetchone()

            # If result is not None, the table exists
            return result is not None
        except Exception as e:
            print(f"Error checking table availability: {e}")
            return False

    def update_entry(self, semester_id):
        tablename = "time_table" + str(semester_id)
        
        # Check if the table is available
        if not self.check_table_available(tablename):
            print(f"Table '{tablename}' not available. Creating a new table.")
            self.create_time_table(semester_id)
        else:
            subjects = self.get_subjects(semester_id)

            try:
                for subject in subjects:
                    print("________________________________________________")
                    print(f"{subject}")
                    start_time = input(f"Please enter updated Start time for : ")
                    end_time = input(f"Please enter updated End time for : ")

                    # Corrected the query and added placeholders for values
                    query = f"UPDATE {tablename} SET start_time = %s, end_time = %s WHERE subject_name = %s;"
                    values = (start_time, end_time, subject)

                    # Execute the query
                    self.database_connector.cursor.execute(query, values)

                # Commit the changes to the database after updating all subjects
                self.database_connector.db_connection.commit()

                print("Timetable entries updated successfully.")
            except Exception as e:
                print(f"Error updating timetable entries: {e}")
                # Rollback the changes if an error occurs
                self.database_connector.db_connection.rollback()

    def display_semester_info(self):
        ask = int(input("Enter semester id (Enter 0 to display all semester information): "))
        if ask == 0:
            department.display_semester_information()
        return
   
    def display(self):
        print("""Please select Your Option :
            1 -> Add schedule
            2 -> Update Schedule
            3 -> Special Update
            4 -> Main Page""")
        ask = int(input("Please enter your option: "))
        
        if ask == 1:
            semester_id = int(input("Please enter semester id : "))
            self.create_time_table(semester_id)
        elif ask == 2:
            semester_id = int(input("Please enter semester id : "))
            self.update_entry(semester_id)
        elif ask == 3:
            print("Under Construction - here we implement if Temporary divert timetable")
        else:
            # Assuming db_manager is an instance of some other class with display_options method
            self.db_manager.display_options()
 

"""
    The `DatabaseManager` class manages different functionalities related to the Face Recognition Attendance System.

    Attributes:
    - options (dict): A dictionary containing instances of various database-related classes.

    Methods:
    - __init__(self): Initializes the `DatabaseManager` class with instances of database-related classes.
    - execute_holiday_manager(self): Executes the functionality related to the Holiday Manager.
    - attendance_manager_execute(self): Executes the functionality related to the Attendance Manager.
    - display_options(self): Displays the available options for the user to choose from.
    - manage_database(self, option): Manages the selected database based on the user's choice.

    """ 
class DatabaseManager:
    def __init__(self):
        self.options = {            
            2: StudentDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), department),
            3: TeacherDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas")),
            4: DepartmentDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), teachers_instance),
            5: TimeTableManager(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), department),
            6: CameraManager(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), department),
            }
    """
        Executes the functionality related to the Holiday Manager.

        Parameters:
        None

        Returns:
        None

        """
    def excute_holiday_manager(self):
        from HolidayManager import Holiday
        holiday_instance = Holiday()
        # Use the desired functionalities
        holiday_instance.mainMethod()

    """
        Executes the functionality related to the Attendance Manager.

        Parameters:
        None

        Returns:
        None

        """    
    def attendanceManagerExcute(self):
        from AttendanceManager import main
        if __name__ == "__main__":
            main()

    """
        Displays the available options for the user to choose from.

        Parameters:
        None

        Returns:
        None

        """
    def display_options(self):
        while True:
            print("""
                  _______________________________________________________
                  Please select an option:
                  1 -> Attendance Data
                  2 -> Students information
                  3 -> Teachers information
                  4 -> Department information
                  5 -> Time Table
                  6 -> Camera Management
                  7 -> Setting
                  8 -> Holiday Manager
                  9 -> Help
                  10 -> Exit
                  -------------------------------------------------------""")
            try:
                ask = int(input("Please choose your option: "))
                if ask == 1:
                    if __name__ == "__main__":
                        main()
                elif ask == 9:
                    exit()
                elif 2 <= ask <= 6:
                    self.options[ask].display()
                elif ask ==7:
                    settings.main()
                elif ask == 8:
                    self.excute_holiday_manager()
                elif ask == 9:
                    print("Please go to website ")
                    return  
                elif ask ==10:
                    exit()          
                    
                else:
                    print("Please enter a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    """
        Manages the selected database based on the user's choice.

        Parameters:
        - option (int): The user's selected option.

        Returns:
        None

        """
    def manage_database(self, option):
        selected_database = self.options.get(option)
        if selected_database:
            selected_database.display()
        else:
            print("Please select a valid option.")


"""
    This function handles the user login process for the Face Recognition Attendance System.

    The user is prompted to enter their email and password. For administrators, an additional
    option is provided to add a new user with admin privileges.

    Parameters:
    - db_manager (object): An instance of the database manager class for handling system options.

    Returns:
    None

    Raises:
    None

    """    
def login(db_manager):  
    
    """
        Validate the entered email format.

        Parameters:
        - email (str): The email address entered by the user.

        Returns:
        bool: True if the email is in a valid format, False otherwise.

    """
    def is_valid_email(email):
                
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return bool(re.match(email_pattern, email))
    #function to validate entered contact number (10 digit) is correct or not
    def is_valid_contact(contact):
        # Using a simple regular expression for 10-digit phone number validation
        contact_pattern = re.compile(r'^\d{10}$')
        return bool(re.match(contact_pattern, contact))

    """
        Send an OTP (One-Time Password) to the user's email address.

        Parameters:
        - email (str): The email address to which the OTP should be sent.

        Returns:
        str: The generated OTP.

    """
    def send_otp_email(email):       
        # Set up the email server
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        smtp_username = "prsu.attendance@gmail.com"
        smtp_password = "fvynkkdppthnxtvf"

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Create the MIME object
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Your OTP for Verification'
        otp = generate_otp()
        # Body of the email
        body = f"""Hello,
    Your OTP for Face Recognition Attendance System is: {otp}
    Please enter this OTP to complete the verification process.
    Best regards,The Face Recognition Team.
    """
        msg.attach(MIMEText(body, 'plain'))
        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, email, msg.as_string())
            print("OTP successfully sent ")

        return otp
    
    """
        Generate a random OTP (One-Time Password).

        Parameters:
        - length (int): The length of the OTP.

        Returns:
        str: The generated OTP.

        """
    def generate_otp(length=6):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    """
        Hash the provided password using bcrypt.

        Parameters:
        - password (str): The user's password.

        Returns:
        str: The hashed password.

        """
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    """
        Verify the entered password against the stored hashed password.

        Parameters:
        - entered_password (str): The password entered by the user.
        - hashed_password (str): The hashed password stored in the database.

        Returns:
        bool: True if the entered password is correct, False otherwise.

        """
    def verify_password(entered_password, hashed_password):
        # Ensure both entered password and hashed password are encoded
        entered_password = entered_password.encode('utf-8')
        hashed_password = hashed_password.encode('utf-8')

        return bcrypt.checkpw(entered_password, hashed_password)
    
    """
        Verify the entered OTP against the generated OTP.

        Parameters:
        - otp_entered (str): The OTP entered by the user.
        - otp (str): The generated OTP.

        Returns:
        bool: True if the entered OTP is correct, False otherwise.

        """
    def otp_verifier(otp_entered, otp):
        # For simplicity, the correct OTP is hardcoded here.
        if int(otp_entered) == int(otp):
            return True
        else:
            return False

    """
        Retrieve the hashed password from the database for the given email.

        Parameters:
        - email (str): The user's email address.

        Returns:
        str: The hashed password retrieved from the database.

        """
    def retrieve_password_from_db(email):
        # Connect to MySQL 
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rakesh9339",
            database="sas"
        )

        cursor = conn.cursor()

        # Retrieve hashed password for the given email
        sql = "SELECT passcode FROM login_details WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if result:
            return result[0]  # Return the hashed password
        else:
            return None  # Email not found in the database
    
    """
        Save user data to the database.

        Parameters:
        - email (str): The user's email address.
        - name (str): The user's name.
        - contact (str): The user's contact number.
        - passcode (str): The hashed passcode.

        Returns:
        None

        """
    def save_data(email, name, contact, passcode):
        try:
            # Connect to MySQL 
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rakesh9339",
                database="sas"
            )

            # Create a cursor object
            cursor = conn.cursor()

            # SQL query to insert data into the login_details table
            sql = "INSERT INTO login_details (email, name, contact, passcode) VALUES (%s, %s, %s, %s)"
            data = (email, name, contact, passcode)

            # Execute the query
            cursor.execute(sql, data)

            # Commit the changes to the database
            conn.commit()

            print("Data successfully saved to the database.")
            return

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()
            return
      
    """
        The main function orchestrating the login process.

        Parameters:
        - email_id (str): The user's email address.
        - pc (str): The user's password.

        Returns:
        None

        """
    def main(email_id, pc):      

        if email_id == "Admin" and pc == "Admin":  
            print("""You entered add New user
                please wait for OTP""")
            otp = send_otp_email("prsu.attendance@gmail.com")
            print("OTP sent successfully to admin Email ")
            entered_otp = input(("Please enter OTP : "))
            check = otp_verifier(entered_otp, otp)
            if check:
                print("Please Provide New Account details :")
                userName = input("Please enter User Name: ")
                contact_number = input("Please enter Contact number: ")
                email = input("Please enter Email Id: ")
                
                print("OTP sending. Please wait for a minute.")
                user_otp = int(send_otp_email(email))          

                # Send OTP and verify
                max_attempts = 3
                for attempt in range(1, max_attempts + 1):                    
                    otp_entered = int(input("Enter OTP: "))
                    check = otp_verifier(otp_entered, user_otp) 
                                    
                    if check:
                        print("OTP verified Successfully : ")
                        password = input("Please enter password : ")
                        password_hashed = hash_password(password)
                        save_data(email, userName, contact_number, password_hashed)
                        print(f"User with email {email} has been successfully added.")                        
                        return
                    else:
                        print(f"Attempt {attempt}/{max_attempts}: OTP verification failed.")
                        

                print("Maximum attempts reached. Exiting.")
                
            else:
                print("Invalid OTP.")
                main()
        else:
            password_from_database = retrieve_password_from_db(email_id)
            if password_from_database and verify_password(pc, password_from_database):
                print("Login successful")
                db_manager.display_options()
            else:       
                exit()

    # Initial user input
    email_id = input("User id ( Email ) : ")
    pc =  getpass.getpass("Please enter password : ")

    # Call the main function, It starts the login page
    main(email_id, pc)

if __name__ == "__main__":
    teachers_instance = TeacherDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas"))
    department = DepartmentDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), teachers_instance)
    db_manager = DatabaseManager()        
    login(db_manager)
    
