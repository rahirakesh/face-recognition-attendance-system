'''---------------------------------------------------------------------------------------------------
About Author ->
        Name - Rakesh Kumar
               MCA 3 Semester
               9339rahi@gmail.com
        Date - 27-11-2023
--------------------------------------------------------------------------------------------------------    
The code is part of " Face Recognition Attendance system " for Pt. Ravishankar Shukla univercity Raipur
.......................................................................................................
This script interacts with a MySQL database to manage attendance records for students and teachers.

Classes:
    - TeachersAttendance: Handles attendance record functionalities for teachers.
    - Student: Manages attendance records for students.

Classes within TeachersAttendance:
    - InsertRecord: Handles the insertion of attendance records for teachers.
    - GetRecord: Manages the retrieval of attendance records for teachers.

Classes within Student:
    - InsertRecord: Manages the insertion of attendance records for students.
    - GetRecord: Handles the retrieval of attendance records for students.

Functions:
    - create_table(dpt_id, date, conn): Creates a table for teacher attendance.
    - insert_attendance(dpt_id, date, conn): Inserts teacher attendance records.
    - get_today_tcr_record(tcr_id, conn): Retrieves today's teacher attendance records.
    - get_month_tcr_record(teacher_id, conn, month=None, year=None): Retrieves monthly teacher attendance records.
    - calculate_attendance(teacher_id, table_name, conn): Calculates teacher attendance statistics.
    - get_tables_for_teacher(year, month, conn, dpt_id): Gets tables for a teacher based on year and month.
    - create_students_attendance_table(subject_id, conn): Creates a table for student attendance.
    - get_semester_ids(dpt_id, conn): Retrieves semester IDs for a department.
    - get_subject_ids(semester_id, conn): Retrieves subject IDs for a semester.
    - get_student_ids(subject_id, conn): Retrieves student IDs for a subject.
    - get_today_std_record(student_id, conn): Retrieves today's student attendance records.
    - get_number_of_days_in_month(year, month): Gets the number of days in a month.
    - get_monthly(student_id, conn): Retrieves monthly student attendance records.

Main Function:
    - main(): Serves as the entry point for user interactions. Connects to the database, creates instances of the
      Student and TeachersAttendance classes, and provides options to retrieve attendance records for students and
      teachers. Incorporates error handling for potential exceptions during execution.

Usage:
    - Run the script to interact with the attendance record system.
----------------------------------------------------------------------------------------------------------------
'''

import mysql.connector
import datetime
import calendar
from mysql.connector.errors import IntegrityError, ProgrammingError
from collections import defaultdict


'''
    The TeachersAttendance class manages the attendance records for teachers.

    Attributes
    ----------
    InsertRecord : class
        A nested class for inserting records into the database.
    GetRecord : class
        A nested class for retrieving records from the database.

    Methods
    -------
    (methods of TeachersAttendance class)
    ''' 
class TeachersAttendance:  
    '''
        The InsertRecord class handles the insertion of attendance records for teachers.

        Methods
        -------
        create_table(dpt_id, date, conn)
            Creates an attendance table for a department on a specific date.
        insert_attendance(dpt_id, date, conn)
            Inserts attendance records for teachers in a department on a specific date.
'''
    class InsertRecord:
        def create_table(self, dpt_id, date, conn):
            try:
                if datetime.datetime.now().weekday() == 6:
                    print("Skipping table creation on Sunday.")
                    return

                tbl_name = f"t_{dpt_id}_{date}"
                query = f"CREATE TABLE IF NOT EXISTS {tbl_name} (attendance_id INT AUTO_INCREMENT PRIMARY KEY, teachers_id INT NOT NULL, status CHAR(1));"

                with conn.cursor() as cursor:
                    cursor.execute(query)

            except Exception as e:
                print(f"Error creating table: {e}")

        def insert_attendance(self, dpt_id, date, conn):
            cursor = conn.cursor()

            try:
                self.create_table(dpt_id, date, conn)

                cursor.execute("SELECT id FROM teachers WHERE dpt_id = %s", (dpt_id,))
                teacher_ids = cursor.fetchall()

                for teacher_id in teacher_ids:
                    tbl_name = f"t_{dpt_id}_{date}"
                    query = f"INSERT INTO {tbl_name} (teachers_id, status) VALUES (%s, 'P');"

                    try:
                        cursor.execute(query, (teacher_id[0],))
                        conn.commit()
                    except IntegrityError as e:
                        print(f"Error inserting attendance for teacher {teacher_id[0]}: {e}")
                        conn.rollback()

            finally:
                cursor.close()
        
        
        '''
        The GetRecord class handles the retrieval of attendance records for teachers.
        Methods
        -------
        get_today_tcr_record(tcr_id, conn)
        Retrieves today's attendance records for a teacher.
        get_month_tcr_record(teacher_id, conn, month=None, year=None)
        Retrieves monthly attendance records for a teacher.
        calculate_attendance(teacher_id, table_name, conn)
        Calculates the attendance statistics for a teacher.
        get_tables_for_teacher(year, month, conn, dpt_id)
        Retrieves all tables for a given department, month, and year.
        '''
    class GetRecord:
        def get_today_tcr_record(self, tcr_id, conn):
            cursor = conn.cursor()

            try:
                # Retrieve the department ID for the given teacher ID from the database
                cursor.execute(f"SELECT dpt_id FROM teachers WHERE id = {tcr_id}")
                dpt_id = cursor.fetchone()[0]

                # Construct the table name based on department and current date
                today = datetime.date.today()
                tbl_name = f"t_{dpt_id}_{today.strftime('%Y-%m-%d')}"

                # Query to select records from the specified table
                query = f"SELECT * FROM {tbl_name} WHERE teachers_id = {tcr_id}"

                cursor.execute(query)
                records = cursor.fetchall()

                if records:
                    attendance_data = []
                    for record in records:
                        record_dict = {
                            'attendance_id': record[0],
                            'teachers_id': record[1],
                            'status': record[2]
                        }
                        attendance_data.append(record_dict)

                    return attendance_data
                else:
                    return []

            finally:
                cursor.close()

        def get_month_tcr_record(self, teacher_id, conn, month=None, year=None):
            if not month or not year:
                current_date = datetime.date.today()
                month = current_date.month
                year = current_date.year

            cursor = conn.cursor()

            try:
                # Fetch department ID for the given teacher
                cursor.execute(f"SELECT dpt_id FROM teachers WHERE id = {teacher_id}")
                dpt_id = cursor.fetchone()[0]

                # Fetch all tables for the specified month and year
                all_tables = self.get_tables_for_teacher(year, month, conn, dpt_id)

                total_working_days = 0
                total_present_days = 0

                for table_name in all_tables:
                    working_days, present_days = self.calculate_attendance(teacher_id, table_name, conn)

                    total_working_days += working_days
                    total_present_days += present_days

                print(f"Total working days for teacher ID {teacher_id}: {total_working_days}")
                print(f"Total present days for teacher ID {teacher_id}: {total_present_days}")
                return ((total_present_days * 100) / total_working_days) if total_working_days > 0 else 0

            finally:
                cursor.close()

        def calculate_attendance(self, teacher_id, table_name, conn):
            cursor = conn.cursor()

            try:
                # Fetch the count of total days and present days
                query = f"SELECT COUNT(*), SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) FROM {table_name} WHERE teachers_id = {teacher_id};"
                cursor.execute(query)
                result = cursor.fetchone()

                working_days, present_days = result[0], result[1]

                return working_days, present_days

            finally:
                cursor.close()

        def get_tables_for_teacher(self, year, month, conn, dpt_id):
            cursor = conn.cursor()

            try:
                # Fetch all tables for the given department, month, and year
                cursor.execute(f"SHOW TABLES LIKE 't_{dpt_id}%'")
                all_tables = cursor.fetchall()
                table_names = [table[0] for table in all_tables if f"{year}{month:02}" in table[0]]

                return table_names

            finally:
                cursor.close()


'''Class for handling students' attendance records.

    Attributes
    ----------
    InsertRecord : class
        A nested class for inserting records into the database.
    GetRecord : class
        A nested class for retrieving records from the database.

    Methods
    -------
    (methods of Student class)

    Examples
    --------
    Creating an instance of the Student class:
    >>> student_instance = Student()

    Accessing nested classes:
    >>> insert_instance = student_instance.InsertRecord()
    >>> get_instance = student_instance.GetRecord()

    (Detailed documentation for nested classes in their respective sections.)

'''
class Student:
    ''' A nested class for inserting records into the database.

        Methods
        -------
        create_students_attendance_table(subject_id, conn)
            Creates an attendance table for students based on the subject.

        get_semester_ids(dpt_id, conn)
            Retrieves semester IDs for a given department.

        get_subject_ids(semester_id, conn)
            Retrieves subject IDs for a given semester.

        get_student_ids(subject_id, conn)
            Retrieves student IDs for a given subject.

        insert_attendance(dpt_id, conn)
            Inserts attendance records into the database.

        Examples
        --------
        Creating an instance of the InsertRecord class:
        >>> insert_instance = Student.InsertRecord()

        Creating a students' attendance table:
        >>> insert_instance.create_students_attendance_table(subject_id, connection)

        (Other examples for methods.)'''
    class InsertRecord:
        def create_students_attendance_table(self, subject_id, conn):
            # Get the current date
            date = datetime.date.today().strftime("%Y-%m-%d")
            # Generate the table name using subject_id and date
            tbl_name = f"sub{subject_id}_{date}"
            # SQL query to create the table
            query = f"""CREATE TABLE IF NOT EXISTS {tbl_name} (
                attendance_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                status CHAR(1),
                FOREIGN KEY (student_id) REFERENCES students(id)
            );"""
            # Execute the query using a cursor
            with conn.cursor() as cursor:
                cursor.execute(query)

        def get_semester_ids(self, dpt_id, conn):
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM semesters WHERE dpt_id = %s", (dpt_id,))
            semester_ids = cursor.fetchall()
            cursor.close()
            return semester_ids

        def get_subject_ids(self, semester_id, conn):
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM subjects WHERE semester_id = %s", (semester_id,))
            subject_ids = cursor.fetchall()
            cursor.close()
            return subject_ids

        def get_student_ids(self, subject_id, conn):
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM students WHERE subject_id = %s", (subject_id,))
            student_ids = cursor.fetchall()
            cursor.close()
            return student_ids

        def insert_attendance(self, dpt_id, conn):
            pass
    '''
    A nested class for retrieving records from the database.

        Methods
        -------
        get_today_std_record(student_id, conn)
            Retrieves today's attendance records for a specific student.

        get_number_of_days_in_month(year, month)
            Gets the number of days in a specific month.

        get_monthly(student_id, conn)
            Retrieves monthly attendance data for a specific student.

        Examples
        --------
        Creating an instance of the GetRecord class:
        >>> get_instance = Student.GetRecord()

        Retrieving today's attendance records:
        >>> get_instance.get_today_std_record(student_id, connection)

        (Other examples for methods.)
    '''
    class GetRecord:
        def get_today_std_record(self, student_id, conn):
            cursor = conn.cursor()
            try:
                # Fetch subjects for the student
                cursor.execute("""
                    SELECT subjects.id, subjects.name
                    FROM students
                    JOIN semesters ON students.semester = semesters.id
                    JOIN classes ON semesters.class_id = classes.id
                    JOIN departments ON classes.dpt_id = departments.id
                    JOIN subjects ON subjects.semester = semesters.id
                    WHERE students.id = %s
                """, (student_id,))
                subjects_info = cursor.fetchall()

                attendance_data = {}

                # Get the current date
                today = datetime.date.today()

                for subject_id, subject_name in subjects_info:
                    # Construct the table name based on the current date
                    table_name = f"sub_{subject_id}_{today.year}_{today.month:02d}_{today.day:02d}"

                    # Query to retrieve attendance records for the specified student from the table
                    query = f"SELECT status FROM {table_name} WHERE student_id = %s;"

                    cursor.execute(query, (student_id,))
                    result = cursor.fetchone()

                    if result:
                        # Store the status in the attendance_data dictionary
                        attendance_data[subject_id] = {"subject_name": subject_name, "status": result[0]}

            finally:
                cursor.close()

            return attendance_data


        def get_number_of_days_in_month(self, year, month):
            # Check if the month is within the valid range (1 to 12)
            if 1 <= month <= 12:
                # Use calendar module to get the number of days in the specified month
                return calendar.monthrange(year, month)[1]
            else:
                # Handle invalid month
                print("Invalid month. Month should be between 1 and 12.")
                return 0

        def get_monthly(self, student_id, conn):
            cursor = conn.cursor()

            info = defaultdict(float)

            try:
                # Fetch subjects for the student
                cursor.execute("""
                    SELECT subjects.id, subjects.name
                    FROM students
                    JOIN semesters ON students.semester = semesters.id
                    JOIN classes ON semesters.class_id = classes.id
                    JOIN departments ON classes.dpt_id = departments.id
                    JOIN subjects ON subjects.semester = semesters.id
                    WHERE students.id = %s
                """, (student_id,))
                
                subjects_info = cursor.fetchall()

                for subject_id, subject_name in subjects_info:
                    total_class = 0
                    total_attendance = 0

                    # Get the current month and year
                    current_date = datetime.date.today()
                    year = current_date.year
                    month = current_date.month

                    # Get the number of days in the current month
                    month_date = calendar.monthrange(year, month)[1]

                    for day in range(1, month_date + 1):
                        table_name = f"sub_{subject_id}_{day:02d}_{month}"
                        # Adjust the query to get the attendance status for the specific day
                        query = "SELECT status FROM {} WHERE student_id = %s;".format(table_name)

                        cursor.execute(query, (student_id,))
                        result = cursor.fetchone()

                        if result and result[0] == 'P':
                            total_attendance += 1

                        total_class += 1

                    attendance_percentage = (total_attendance * 100) / total_class if total_class != 0 else 0
                    info[subject_name] = attendance_percentage

            except Exception as e:
                print(f"Error: {e}")

            finally:
                cursor.close()

            return info   


'''
    Main function to interact with the attendance record system.

    Establishes a connection to the MySQL database, creates instances of the Student and TeachersAttendance classes,
    and prompts the user to choose between student and teacher attendance records. Further options are provided for
    obtaining today's or monthly attendance records.

    Examples
    --------
    Running the main function:
    >>> main()
'''
def main():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rakesh9339",
            database="sas"
        )

        std_ins = Student()
        get_std = std_ins.GetRecord()

        tcr = TeachersAttendance()
        get_tcr = tcr.GetRecord()

        print("""Please select your option:
              1. Student Attendance Record
              2. Teachers Attendance Record
        """)
        user_choice = int(input("Please enter your choice: "))

        if user_choice == 1:
            print("""
                  1. Get Today Attendance Record
                  2. Get Monthly Attendance Record
            """)
            user_option = int(input("Please enter your option: "))
            student_id = int(input("Please enter student Id: "))

            try:
                if user_option == 1:
                    today_data = get_std.get_today_std_record(student_id, connection)
                    if today_data:
                        print(f"Today's student attendance records for student ID {student_id}:")
                        for record in today_data:
                            print(record)
                    else:
                        print(f"No attendance records found for today for student ID {student_id}.")
                elif user_option == 2:
                    month_data = get_std.get_monthly(student_id, connection)
                    if month_data:
                        print(f"Monthly attendance data for student ID {student_id}:")
                        for subject, percentage in month_data.items():
                            print(f"{subject}: {percentage}%")
                    else:
                        print(f"No attendance records found for the specified month for student ID {student_id}.")
                else:
                    print("Invalid option.")
            except ProgrammingError as pe:
                print(f"Error in SQL query: {pe}")

        elif user_choice == 2:
            print("""
                  1. Get Today Attendance Record
                  2. Get Monthly Attendance Record
            """)
            user_option = int(input("Please enter your option: "))
            tcr_id = int(input("Please enter the teacher id: "))

            try:
                if user_option == 1:
                    today_data = get_tcr.get_today_tcr_record(tcr_id, connection)
                    if today_data:
                        print(f"Today's teacher attendance records for teacher ID {tcr_id}:")
                        for record in today_data:
                            print(record)
                    else:
                        print(f"No attendance records found for today for teacher ID {tcr_id}.")
                elif user_option == 2:
                    month_data = get_tcr.get_month_tcr_record(tcr_id, connection)
                    if month_data:
                        print(f"Monthly attendance data for teacher ID {tcr_id}: {month_data}%")
                    else:
                        print(f"No attendance records found for the specified month for teacher ID {tcr_id}.")
                else:
                    print("Invalid option.")
            except ProgrammingError as pe:
                print(f"Error in SQL query: {pe}")

        else:
            print("Invalid option.")

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()