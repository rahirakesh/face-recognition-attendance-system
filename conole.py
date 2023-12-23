import mysql.connector
import re  # import regular expresion 
import smtplib
import ssl
from email.message import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import Face_Store
print("""
    WELCOME TO FACE RECOGNITION ATTENDANCE SYSTEM
""")

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
              4 -> Time Table            
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
        elif option == 4:
            print("""
                  Please select your option
                  1 -> Set Time Table
                  2 -> Update Time Table
                  3 -> Back 
                  4 -> Main Page""")  
            option ==  int(input("Please enter you option :"))
            if option == 1:
                self.set_time_table()
            elif option ==2:
                print("Under Construction")
                pass
            elif option ==3:
                self.display()
            else:
                db_manager.display_options()

        else:
            db_manager.display_options()
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
            self.display_options()
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
        elif not self.is_semester_id_valid(semester_id):
            print("Invalid Semester ID. Please enter a valid Semester ID.")
            self.add_new_subject() 

        no_of_subjects = int(input("Please enter the number of subjects available: "))
        for i in range(1, no_of_subjects + 1):
            subject_id = self.generate_subject_id()
            subject_name = input("Please enter subject name: ")
            teacher_id = int(input("Please enter teacher id (Enter 0 to find out teachers data): "))
            if teacher_id == 0:
                self.show_teacher_information()
                teacher_id = int(input("Please Enter Teacher Id: "))
            elif not self.is_teacher_id_valid(teacher_id):
                print("Invalid Teacher ID. Please enter a valid Teacher ID.")
                self.add_new_subject()

            self.insert_subject_data(self.database_connector, subject_name, teacher_id, semester_id)

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
     

    def insert_subject_data(self,database_connector, subject_name, teacher_id, semester_id):
        # Execute the MySQL query to insert data into the subjects table
        query_insert_subject = "INSERT INTO subjects (name, teacher, semester) VALUES (%s, %s, %s)"
        values_insert_subject = (subject_name, teacher_id, semester_id)

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
            self.self.department_database.display_semester_info()
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
    def update_teacher_department(self, teacher_id):
        # Display available departments to choose from
        self.DepartmentDatabase.display_department_details()
        # Take input for the updated department ID
        new_department_id = int(input("Enter the updated department ID: "))
        # Validate if the entered department ID is valid
        if self.DepartmentDatabase.is_valid_department(new_department_id):
            # Update the teacher's department
            query_update_department = "UPDATE teachers SET dpt_id = %s WHERE id = %s"
            self.database_connector.cursor.execute(query_update_department, (new_department_id, teacher_id))
            self.database_connector.db_connection.commit()
            print("Teacher department updated successfully.")
        else:
            print("Invalid department ID. Please enter a valid department ID.")
            self.update_teacher_department(teacher_id)
        self.display()
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
            self.update_teacher_department(teacher_id)
        elif ask == 5:
            db_manager.display_options()
    def remove_teacher_data(self):
        print("Under Construction baby but tension na le jaldi bana lega tu")
class TimeTableManager:    
    def __init__(self, database_connector,department):
        self.database_connector = database_connector
        self.department = department
    def display(self):
        print("""Please select Your Option :
            1 -> Add schedule
            2 -> Update Schedule
            3 -> Special Update
            4 -> Main Page""")
        ask = int(input("Please enter your option : "))
        
        if ask == 1:
            self.set_time_table()
        elif ask == 2:
            self.update_time_table()  # Call your update_time_table method here
        elif ask == 3:
            pass  # Implement your logic for option 3
        else:
            db_manager.display_options()
    def temporary_time_table(self):
        print("Under construction")
        pass
    def set_time_table(self):
        ask = int(input("Please enter semester id (Enter 0 for find out semester id : "))
        if ask ==0:
            self.department.display_semester_info()
        self.department.is_semester_id_valid(ask)
        #get the how many subject Available in entered semester       
        subjects =  self.get_subjects(ask)
        subjects = self.get_subjects(ask)
        number_of_subjects = len(subjects)
        start_time = [0]
        end_time = [0]
        for i in range(number_of_subjects):
            start_time[i] =input(f"Please enter start time for {subjects[i]}: " )
            end_time[i] = input(f"Please enter End time time for {subjects[i]}: ")
            #also check the coliision meanse if subject1's start tiem 11 o'clock and end time 12 o clock, then subject2 never start time not between 11 to 12 
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
    def create_time_table(self, semester_id):
        tablename = "time_table" + semester_id
        self.create_table(tablename=tablename)
        
        subjects = self.get_subjects(semester_id)

        for subject in subjects:
            print(f"{subject}")
            start_time = input("Please enter Start time: ")
            end_time = input("Please enter end time: ")

            # Corrected the query and added placeholders for values
            query = f"INSERT INTO {tablename} (subject, start_time, end_time) VALUES (%s, %s, %s);"
            values = (subject, start_time, end_time)

            try:
                # Execute the query
                self.database_connector.cursor.execute(query, values)

                # Commit the changes to the database
                self.database_connector.connection.commit()

                print("Timetable entry added successfully.")
            except Exception as e:
                print(f"Error: {e}")
            tablename ="time_table" + semester_id
            self.create_table(tablename=None)
            department_id = 1
            subjects = self.get_subjects(semester_id)
            for i in subjects:
                print(f"{subjects[i]}")
                start_time =input("Please enter Start time : ")
                end_time = input("Please enter end time : ")
                quary = f"insert into {tablename} values ({subjects[i]},start_time,end_time);"
    def create_table(self, tablename):
        query = f"CREATE TABLE {tablename} (\
            subject_name VARCHAR(50),\
            start_time TIME,\
            end_time TIME\
        );"

        try:
            # Execute the query to create the table
            self.database_connector.cursor.execute(query)
            # Commit the changes
            self.database_connector.db_connection.commit()
            print(f"Table '{tablename}' created successfully.")
        except Exception as e:
            # If an error occurs, print the error and rollback the changes
            print(f"Error creating table: {e}")
            self.database_connector.db_connection.rollback()
    def update_time_table(self):
        # Assuming you have a method to retrieve existing entries, implement it here
        existing_entries = self.retrieve_existing_entries()

        if not existing_entries:
            print("No entries found in the timetable.")
            return

        print("Existing entries:")
        for entry in existing_entries:
            print(f"Subject: {entry['subject']}, Start Time: {entry['start_time']}, End Time: {entry['end_time']}")

        entry_to_update = input("Enter the subject to update: ")
        new_start_time = input("Enter the new start time: ")
        new_end_time = input("Enter the new end time: ")

        # Assuming you have a method to update the entry, implement it here
        success = self.update_entry(entry_to_update, new_start_time, new_end_time)

        if success:
            print("Timetable entry updated successfully.")
        else:
            print("Failed to update timetable entry.")
    def retrieve_existing_entries(self):
        try:
            # Define the SQL query to retrieve existing entries
            query = "SELECT subject, start_time, end_time FROM your_timetable_table;"

            # Execute the query
            self.database_connector.cursor.execute(query)

            # Fetch all the rows
            entries_data = self.database_connector.cursor.fetchall()

            # Extract entry details from the result and return a list of dictionaries
            entries = [{'subject': row[0], 'start_time': row[1], 'end_time': row[2]} for row in entries_data]

            return entries
        except Exception as e:
            print(f"Error: {e}")
            return None
    def update_entry(self, subject, new_start_time, new_end_time):
        try:
            # Define the SQL query to update the entry
            query = "UPDATE your_timetable_table SET start_time = %s, end_time = %s WHERE subject = %s;"
            values = (new_start_time, new_end_time, subject)

            # Execute the query
            self.database_connector.cursor.execute(query, values)

            # Commit the changes to the database
            self.database_connector.connection.commit()

            # Check if any rows were affected (indicating a successful update)
            if self.database_connector.cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    def display_semester_info(self,id):        
        if id ==0:
            DatabaseManager.display_semester_information()
        else:
            self.create_time_table()
class CameraManager:
    def __init__(self, database_connector,department):
        self.database_connector = database_connector
        self.department = department
    def display(self):
        print(""""select Your Option :
              1 -> Assign Camera to class
              2 -> Remove Camera
              3 -> Main Page
              """)
        ask =int(input("Please enter your option :"))
        if ask == 1:
            pass
        elif ask == 2 :
            pass
        else:
            self.db_manager.display_optioion()
        def assign_camera(self):
            class_id =int(input("Please enter the class id (Enter 0 to find out class id) : "))
            if class_id ==0:
                self.class_info(self) 
        def class_info(self):
            dpt_id = int(input("Please enter the class id : "))
            #     if           
            # pass
class MessageFormate:
    def __init__(self):
        self.self =self
    def daily_formate(self):
        def for_student(self,id):
            pass
        def for_parent(self,id):
            name = "Rakesh"
            class_name = "MCA"
            semester = 3
            month = "Find_current_month"
            subjects = ["AI", "Big data", "CNDC", "Dot Net", "Cyber Security", "Lab/Seminar"]

            body = f"""
            Dear Parent,

            We hope this message finds you well. We would like to share
            the attendance record of your child for the month of November.

            Student Information:
            ___________________________________________________
            Name of Student    : {name}
            Class              : {class_name}
            Semester           : {semester}
            Attendance Month   : {month}
            ____________________________________________________

            Monthly Attendance Record:
            ____________________________________________________
            Subject Name  | Lectures Taken | Lectures Attended
            ----------------------------------------------------
            {subjects[0]} |       20        |         18
            {subjects[1]} |       20        |         18
            {subjects[2]} |       20        |         18
            {subjects[3]} |       20        |         18
            {subjects[4]} |       20        |         18
            {subjects[5]} |       20        |         18
            ----------------------------------------------------
            Total         |      120        |        108 (90%)
            ____________________________________________________

            We are pleased to inform you that your child has maintained
            a commendable attendance of 90% during this month.

            Thank you for your continuous support in ensuring the
            academic success of your child.

            Best Regards,
                            [Pt. Ravishankar Shukla University, Raipur]"""
            
        def for_teachers(self,id):
            pass
        def for_principle(self,id):
            pass
    def monthly_formate(self):
        def for_student(self,id):
            pass
        def for_parent(self,id):
            pass
        def for_teachers(self,id):
            pass
        def for_principle(self,id):
            pass
class MessageSender:
    def __init__(self, database_connector):
        self.department_info = self.get_department_info(database_connector)

    def department_info(self):
        for i in self.department_info:
            print(i)
            class course_info:
                def __init__(self,dpt_id):
                    self.dpt_id = dpt_id
                    print(dpt_id)
    
    def get_attendance_record(self,std_id,database_connector):
        #I need make this months attendance record
        pass
    def get_student_info(self,semester_id,database_connector):
        pass
    def get_subject_name(self, semester_id, database_connector):
        pass
    def get_semester_info(self,course_id,databsase_connector):
        pass
    def get_course_info(self, dpt_id, database_connector):
        pass

    def get_department_info(self, database_connector):
        query = "SELECT id, name FROM departments;"
        try:
            # Assuming database_connector has a cursor and connection
            database_connector.cursor.execute(query)

            # Fetch all the rows
            departments_data = database_connector.cursor.fetchall()

            # Extract department info and return as a list of tuples
            return departments_data
        except Exception as e:
            print(f"Error: {e}")
            return []
class Help:
    def display(self):
        print("You selected help.")
class DatabaseManager:
    def __init__(self):
        self.options = {
            1: StudentDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), department),
            2: TeacherDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas")),
            3: DepartmentDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), teachers_instance),
            4: TimeTableManager(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), department),
            5: CameraManager(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), department),
            6: MessageSender(DatabaseConnector("localhost", "root", "rakesh9339", "sas")),
            7: Help(),
        }

    def display_options(self):
        while True:
            print("""
_______________________________________________________
Please select an option:
1 -> Students information
2 -> Teachers information
3 -> Department information
4 -> Time Table
5 -> Camera Management
6 -> Setting
7 -> Help
8 -> Exit
-------------------------------------------------------""")
            try:
                ask = int(input("Please choose your option: "))
                if ask == 8:
                    exit()
                elif 1 <= ask <= 7:
                    self.options[ask].display()
                else:
                    print("Please enter a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def manage_database(self, option):
        selected_database = self.options.get(option)
        if selected_database:
            selected_database.display()
        else:
            print("Please select a valid option.")

def login(db_manager):
    print("Welcome To Face Recognition Attendance System")

    #function to validate entered email is correct formate or not 
    def is_valid_email(email):
        # Using a simple regular expression for basic email validation
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return bool(re.match(email_pattern, email))
    #function to validate entered contact number (10 digit) is correct or not
    def is_valid_contact(contact):
        # Using a simple regular expression for 10-digit phone number validation
        contact_pattern = re.compile(r'^\d{10}$')
        return bool(re.match(contact_pattern, contact))

    #function to send OTP using SMTP
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
    #function to generate OTP using random
    def generate_otp(length=6):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    #function to convert passcode into hashcode using hass library 
    def hash_password(password):
        # Use SHA-256 for password hashing
        hash_object = hashlib.sha256(password.encode())
        return hash_object.hexdigest()

    #to Verify OTP
    def otp_verifier(otp_entered, otp):
        # For simplicity, the correct OTP is hardcoded here.
        if otp_entered == otp:
            return True
        else:
            return False

    #convert hassed data into plain text for comparision passcode
    def retrieve_hashed_password(email):
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

    # Login process
    email_id = input("Email Id: ")
    pc = input("Password: ")

    #start here excution of pragram 
    def main():
        if email_id == "" and pc == "":  
            print("You entered add New user")
            otp=send_otp_email("prsu.attendance@gmail.com")
            entered_otp = input(("Please enter OTP : "))
            check = otp_verifier(entered_otp, otp)
            if check:
                print("Please Provide New Account details :")
                userName = input("Please enter User Name: ")
                contact_number = input("Please enter Contact number: ")
                email = input("Please enter Email Id: ")
                print("OTP sending. Please wait for a minute.")
                otp = send_otp_email(email)

                # Send OTP and verify
                max_attempts = 3
                for attempt in range(1, max_attempts + 1):
                    otp_enter = int(input("Enter OTP: "))
                    check = otp_verifier(otp_enter, otp)
                    if check:
                        print(f"User with email {email} has been successfully added.")
                        return
                    else:
                        print(f"Attempt {attempt}/{max_attempts}: OTP verification failed.")

                print("Maximum attempts reached. Exiting.")
                
            else:
                print("Invalid master password. Exiting.")
        else:
            # Retrieve hashed password from the database
            hashed_password_from_db = retrieve_hashed_password(email_id)

            if hashed_password_from_db:
                # Hash the entered password for comparison
                entered_password_hashed = hash_password(pc)

                # Compare hashed passwords
                if hashed_password_from_db == entered_password_hashed:
                    print("Login successful")            
                    
                    db_manager.display_options()
                else:
                    print("Invalid password. Please enter valid credentials.")
            else:
                print("Email not found. Please enter valid credentials.")

    # Call the main function, It start the login page
    main()

if __name__ == "__main__":
    teachers_instance = TeacherDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas"))
    department = DepartmentDatabase(DatabaseConnector("localhost", "root", "rakesh9339", "sas"), teachers_instance)
    db_manager = DatabaseManager()        
    login(db_manager)
    
