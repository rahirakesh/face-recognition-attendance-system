import mysql.connector
import datetime
import logging
from mysql.connector.errors import IntegrityError

class Main:
    def __init__(self):
        print("""Please select you option : 
            1. Teachers Attendance Record
            2. StudentsAttendance Record
            3. Holiday
            4. Main Page """)
        ask  = int(input("Please enter selected option :"))
        if ask == 1:
            print("""
                """)
            dpt_id  = int(input("Please enter department id (enter 0 to find out departmetns id ):"))
            if dpt_id == 0:
                return              

            else:
                #self.TeachersAttendance.GetRecord.get_monthly(dpt_id,connection)
                pass
        elif ask == 2:
            print("""Please select your option : 
                  1. All Student in specific Department
                  2. All Student in specific Semester
                  3. All student in specific Subject""")
            ask =int(input("Please enter your choice : "))
            if ask == 1 :

                pass
            #self.StudentAttendance.GetRecord.get_monthly(dpt_id,connection)
            pass
class Holiday:
        def __init__(self):
            self.holidays = set()
            logging.basicConfig(level=logging.INFO)
        def unofficial_holiday(self):
            user_input = input("Enter the date for an unofficial holiday (YYYY-MM-DD): ")
            self.add_holiday(user_input)
            print(f"Added unofficial holiday on {user_input}.")
        def official_holiday(self):
            # Execute automatically on the first date of the month
            today = datetime.date.today()
            if today.day == 1 and today.weekday() == 6:  # Check if it's the first day of the month and Sunday (weekday() returns 6 for Sunday)
                first_day_of_month = today.strftime("%Y-%m-%d")
                self.add_holiday(first_day_of_month)
                print(f"Automatically added a holiday on {first_day_of_month} (Sunday).")
        def add_holiday(self, date_str):
            try:
                holiday_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                self.holidays.add(holiday_date)
                logging.info(f"Added holiday on {date_str}.")
            except ValueError:
                logging.error("Invalid date format. Please use YYYY-MM-DD.")
                
                raise
        def is_holiday(self, date):
            return date in self.holidays
class TeachersAttendance:
    
    class InsertRecord:
        def create_table(self, id, date, conn):
            try:
                # Check if the current day is Sunday (weekday() returns 6 for Sunday)
                if datetime.datetime.now().weekday() == 6:
                    print("Skipping table creation on Sunday.")
                    return

                # Create table if it does not exist
                tbl_name = f"{id}_{date}"
                query = f"CREATE TABLE IF NOT EXISTS {tbl_name} (attendance_id INT AUTO_INCREMENT PRIMARY KEY, teachers_id INT NOT NULL, status CHAR(1));"

                with conn.cursor() as cursor:
                    cursor.execute(query)

            except Exception as e:
                # Handle exceptions, log or print an error message if needed
                print(f"Error creating table: {e}")

        def insert_attendance(self, dpt_id, date, conn):
            cursor = conn.cursor()

            try:
                # Create the table
                self.create_table(dpt_id, date, conn)

                # Get all teachers in the specified department
                cursor.execute("SELECT id FROM teachers WHERE dpt_id = %s", (dpt_id,))
                teacher_ids = cursor.fetchall()

                # Iterate through all teachers and insert attendance records
                for teacher_id in teacher_ids:
                    tbl_name = f"{dpt_id}_{date}"
                    query = f"INSERT INTO {tbl_name} (teachers_id, status) VALUES (%s, 'P');"
                    
                    try:
                        cursor.execute(query, (teacher_id[0],))
                        conn.commit()
                    except IntegrityError as e:
                        # Handle duplicate entry error
                        print(f"Error inserting attendance for teacher {teacher_id[0]}: {e}")
                        conn.rollback()  # Rollback the transaction

            finally:
                # Close the cursor, do not close the connection here to allow reuse
                cursor.close()

    class GetRecord:
        
        def get_monthly(self, dpt_id, conn):
            cursor = conn.cursor()

            try:
                # Example: Fetching all teachers for a given department
                cursor.execute(f"SELECT * FROM teachers WHERE dpt_id = {dpt_id}")
                teachers = cursor.fetchall()

                for teacher in teachers:
                    monthly_data = self.calculate_attendance(teacher[0], dpt_id, conn)  # Pass dpt_id as an argument

            finally:
                # Close the cursor, do not close the connection here to allow reuse
                cursor.close()

        def calculate_attendance(self, teacher_id, dpt_id, conn):
            current_month = datetime.datetime.now().strftime("%Y%m")
            all_tables = self.get_tables_for_teacher(current_month, conn)

            total_days_present = 0

            for table_name in all_tables:
                cursor = conn.cursor()

                try:
                    # Count the number of rows (days) for the teacher in the current table
                    query = f"SELECT COUNT(*) FROM {table_name} WHERE teachers_id = {teacher_id} AND status = 'P';"
                    cursor.execute(query)
                    days_present = cursor.fetchone()[0]

                    total_days_present += days_present

                finally:
                    cursor.close()

            print(f"Total days present for teacher id -> {teacher_id}: {total_days_present}")
        def get_tables_for_teacher(self, current_month, conn):
            cursor = conn.cursor()

            try:
                # Fetch all tables for the current month
                cursor.execute(f"SHOW TABLES LIKE '%_{current_month}%'")
                all_tables = cursor.fetchall()

                # Extract table names
                table_names = [table[0] for table in all_tables]

                return table_names

            finally:
                cursor.close()
class Student:
    class InsertRecord:
        def create_students_attendance_table(self, dpt_id, conn):
            # get semester_ids based on dpt_id
            semester_ids = self.get_semester_ids(dpt_id, conn)

            for semester_id in semester_ids:
                # get subject_ids based on semester_id
                subject_ids = self.get_subject_ids(semester_id, conn)

                for subject_id in subject_ids:
                    #get students based on subject_id
                    student_ids = self.get_student_ids(subject_id, conn)

                    for student_id in student_ids:
                        date =  datetime.date.today().strftime("%Y-%m-%d")
                        subject_name = ""
                        self.create_table(subject_name, date, conn)
                        

        def insert_data(self):
            pass  
        def create_table(self, name, date, conn):
            try:
                # Check if the current day is Sunday (weekday() returns 6 for Sunday)
                if datetime.datetime.now().weekday() == 6:
                    print("Skipping table creation on Sunday.")
                    return

                # Create table if it does not exist
                tbl_name = f"{name}_{date}"
                query = f"CREATE TABLE IF NOT EXISTS {tbl_name} (attendance_id INT AUTO_INCREMENT PRIMARY KEY, std_id INT NOT NULL, status CHAR(1));"

                with conn.cursor() as cursor:
                    cursor.execute(query)

            except Exception as e:
                # Handle exceptions, log or print an error message if needed
                print(f"Error creating table: {e}")
       
        def get_semester_ids(self, dpt_id, conn):
            cursor = conn.cursor()

            try:
                # Fetch semester_ids based on dpt_id from the semesters table
                cursor.execute("SELECT id FROM semesters WHERE class_id IN (SELECT id FROM classes WHERE dpt_id = %s)", (dpt_id,))
                semester_ids = [row[0] for row in cursor.fetchall()]
                return semester_ids

            finally:
                cursor.close()

        def get_subject_ids(self, semester_id, conn):
            cursor = conn.cursor()

            try:
                # Fetch subject_ids based on semester_id from the subjects table
                cursor.execute("SELECT id FROM subjects WHERE semester = %s", (semester_id,))
                subject_ids = [row[0] for row in cursor.fetchall()]
                return subject_ids

            finally:
                cursor.close()

        def get_student_ids(self, subject_id, conn):
            cursor = conn.cursor()

            try:
                # Fetch student_ids based on subject_id from the students table
                cursor.execute("SELECT id FROM students WHERE semester = %s", (subject_id,))
                student_ids = [row[0] for row in cursor.fetchall()]
                return student_ids

            finally:
                cursor.close()
    class GetRecord:
        pass
try:
    # these values with your actual database credentials
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'rakesh9339',
        'database': 'sas'
    }

    # Connect to the database
    conn = mysql.connector.connect(**db_config)

    # Create an instance of the GetRecord class and retrieve monthly data
    get_record_instance = TeachersAttendance().GetRecord()
    get_record_instance.get_monthly(dpt_id=1, conn=conn)
     
    # Create an instance of the InsertRecord class and create attendance tables
    student_insert_record = Student().InsertRecord()
    student_insert_record.create_students_attendance_table(dpt_id=1, conn=conn)
finally:
    # Close the connection outside the classes
    conn.close()