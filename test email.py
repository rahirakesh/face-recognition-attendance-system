import smtplib
import ssl
from email.message import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime
import calendar
import mysql.connector
from mysql.connector import Error
from AttendanceManager import Student ,TeachersAttendance

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                print(f"Connected to MySQL Database: {self.database}")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection closed")

class MessageFormat:
    class Student:
        class Daily:
            @staticmethod
            def format(name, class_name, semester, subjects, lectures_taken, lectures_attended):
                date = datetime.date.today()
                body = f"""
                Dear {name},

                Today's Attendance Record - {date}:
                ____________________________________________________
                Student Information:
                Name of Student    : {name}
                Class              : {class_name}
                Semester           : {semester}      
                ____________________________________________________
                Subject Name  | Lectures Taken | Lectures Attended
                ----------------------------------------------------
                {subjects[0]} |       {lectures_taken[0]}        |         {lectures_attended[0]}
                {subjects[1]} |       {lectures_taken[1]}        |         {lectures_attended[1]}
                {subjects[2]} |       {lectures_taken[2]}        |         {lectures_attended[2]}
                {subjects[3]} |       {lectures_taken[3]}        |         {lectures_attended[3]}
                {subjects[4]} |       {lectures_taken[4]}        |         {lectures_attended[4]}
                {subjects[5]} |       {lectures_taken[5]}        |         {lectures_attended[5]}
                ----------------------------------------------------

                We appreciate your consistent attendance.

                Best Regards,
                [Your University Name]
                """
                return body

        class Monthly:
            @staticmethod
            def format(name, class_name, semester, month, subjects, lectures_taken, lectures_attended, percentage):
                body = f"""
                Dear {name},

                Monthly Attendance Record for {month}:
                ____________________________________________________
                Student Information:
                Name of Student    : {name}
                Class              : {class_name}
                Semester           : {semester}
                Attendance Month   : {month}
                ____________________________________________________

                Monthly Attendance Record:
                ____________________________________________________
                Subject Name  | Lectures Taken | Lectures Attended
                ----------------------------------------------------
                {subjects[0]} |       {lectures_taken[0]}        |         {lectures_attended[0]}
                {subjects[1]} |       {lectures_taken[1]}        |         {lectures_attended[1]}
                {subjects[2]} |       {lectures_taken[2]}        |         {lectures_attended[2]}
                {subjects[3]} |       {lectures_taken[3]}        |         {lectures_attended[3]}
                {subjects[4]} |       {lectures_taken[4]}        |         {lectures_attended[4]}
                {subjects[5]} |       {lectures_taken[5]}        |         {lectures_attended[5]}
                ----------------------------------------------------
                Total         |      {sum(lectures_taken)}        |        {sum(lectures_attended)} ({percentage}%)
                ____________________________________________________

                Thank you for your dedication to attendance.

                Best Regards,
                [Your University Name]
                """
                return body

    class Parent:
        class Daily:
            @staticmethod
            def format(name,subjects, lectures_taken, lectures_attended):
                date = datetime.now().strftime("%Y-%m-%d")
                body = f"""
                Dear Parent,

                Today's Attendance Record - {date}:
                ____________________________________________________
                Student Information:
                Name of Student    : {name}
                Date              : {date}
                ____________________________________________________

                Subject Name  | Lectures Taken | Lectures Attended
                ----------------------------------------------------
                {subjects[0]} |       {lectures_taken[0]}        |         {lectures_attended[0]}
                {subjects[1]} |       {lectures_taken[1]}        |         {lectures_attended[1]}
                {subjects[2]} |       {lectures_taken[2]}        |         {lectures_attended[2]}
                {subjects[3]} |       {lectures_taken[3]}        |         {lectures_attended[3]}
                {subjects[4]} |       {lectures_taken[4]}        |         {lectures_attended[4]}
                {subjects[5]} |       {lectures_taken[5]}        |         {lectures_attended[5]}
                ----------------------------------------------------

                We appreciate your continued interest in your child's education.

                Best Regards,
                [Pt. Ravishankar Shukla University, Raipur]
                """
                return body

        class Monthly:            
            @staticmethod
            def format(name, class_name, semester, month, subjects, lectures_taken, lectures_attended, percentage):
                body = f"""
                Dear Parent,

                We hope this message finds you well. We would like to share
                the attendance record of your child for the month of {month}.

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
                {subjects[0]} |       {lectures_taken[0]}        |         {lectures_attended[0]}
                {subjects[1]} |       {lectures_taken[1]}        |         {lectures_attended[1]}
                {subjects[2]} |       {lectures_taken[2]}        |         {lectures_attended[2]}
                {subjects[3]} |       {lectures_taken[3]}        |         {lectures_attended[3]}
                {subjects[4]} |       {lectures_taken[4]}        |         {lectures_attended[4]}
                {subjects[5]} |       {lectures_taken[5]}        |         {lectures_attended[5]}
                ----------------------------------------------------
                Total         |      {sum(lectures_taken)}        |        {sum(lectures_attended)} ({percentage}%)
                ____________________________________________________

                We are pleased to inform you that your child has maintained
                a commendable attendance of {percentage}% during this month.

                Thank you for your continuous support in ensuring the
                academic success of your child.

                Best Regards,
                [Pt. Ravishankar Shukla University, Raipur]
                """
                return body

    class Teachers:
        class Daily:
            @staticmethod
            def format(date, subject_name, student_names, attendance_status):
                body = f"""
                Dear Teacher,

                Today's Attendance Record - {date} for {subject_name}:
                ____________________________________________________
                S. No. | Student Name | Status
                ------------------------------------
                {"".join([f"{i+1:<8} | {student_names[i]:<14} | {attendance_status[i]}/n" for i in range(len(student_names))])}
                ------------------------------------

                Total: {len(student_names)}   Absent: {attendance_status.count('A')}   Present: {attendance_status.count('P')}

                Thank you for your dedication to tracking attendance.

                Best Regards,
                [Your University Name]
                """
                return body

        class Monthly: 
            @staticmethod
            def format(month, subject_name, student_names, lectures_taken, lectures_attended):
                body = f"""
                Dear Teacher,

                Monthly Attendance Record for {month} - {subject_name}:
                ____________________________________________________
                S. No. | Student Name | Lectures Taken | Lectures Attended
                --------------------------------------------------------
                {"".join([f"{i+1:<8} | {student_names[i]:<14} | {lectures_taken[i]:<15} | {lectures_attended[i]}/n" for i in range(len(student_names))])}
                --------------------------------------------------------

                Total Lectures Taken: {sum(lectures_taken)}   Total Lectures Attended: {sum(lectures_attended)}

                Your efforts in monitoring attendance are appreciated.

                Best Regards,
                [Your University Name]
                """
                return body

    class Principal:
        @staticmethod
        def student(month, course_name, semester_name, students_above_75, students_60_to_75, students_below_60):
            body = f"""
            Dear Principal,

            Monthly Attendance Record for Students - {month}:
            ____________________________________________________
            Month: {month}
            Course Name: {course_name}
            Semester: {semester_name}

            Students with 75% or more attendance:
            - {', '.join(students_above_75)}

            Students with 60% to <75% attendance:
            - {', '.join(students_60_to_75)}

            Students with less than 60% attendance:
            - {', '.join(students_below_60)}

            Thank you for your attention to student attendance.

            Best Regards,
            [Your University Name]
            """
            return body

        class Teachers:
            @staticmethod
            def daily(present_teachers, absent_teachers):
                body = f"""
                Dear Principal,

                Today's Teachers Attendance Record:
                ____________________________________________________
                Present Teachers:
                S. No. | Name
                ------------------------------------
                {"".join([f"{i+1:<8} | {teacher}/n" for i, teacher in enumerate(present_teachers)])}
                ------------------------------------

                Absent Teachers:
                S. No. | Name
                ------------------------------------
                {"".join([f"{i+1:<8} | {teacher}/n" for i, teacher in enumerate(absent_teachers)])}
                ------------------------------------

                Thank you for your efforts in maintaining teacher attendance.

                Best Regards,
                [Your University Name]
                """
                return body

            @staticmethod
            def monthly(department_name, teachers_data):
                body = f"""
                Dear Principal,

                Monthly Teachers Attendance Record for {department_name}:
                ____________________________________________________
                Department Name: {department_name}
                ------------------------------------
                S. No. | Teacher Name       | Total Classes Taken | Scheduled Classes | Attendance Percent
                ------------------------------------
                {"".join([f"{i+1:<8} | {data['name']:<20} | {data['total_classes']:<19} | {data['scheduled_classes']:<18} | {data['attendance_percent']}/n" for i, data in enumerate(teachers_data)])}
                ------------------------------------

                Your leadership ensures the success of our academic community.

                Best Regards,
                [Your University Name]
                """
                return body

   
        # Formate for Monthly students and Teachers attendance all student on department
        @staticmethod
        def student(month, course_name, semester_name, students_above_75, students_60_to_75, students_below_60):
            body = f"""
            Dear Principal,

            Monthly Attendance Record for Students - {month}:
            ____________________________________________________
            Month: {month}
            Course Name: {course_name}
            Semester: {semester_name}

            Students with 75% or more attendance:
            - {', '.join(students_above_75)}

            Students with 60% to <75% attendance:
            - {', '.join(students_60_to_75)}

            Students with less than 60% attendance:
            - {', '.join(students_below_60)}

            Thank you for your attention to student attendance.

            Best Regards,
            [Your University Name]
            """
            return body

        class Teachers:
            @staticmethod
            def daily(present_teachers, absent_teachers):
                body = f"""
                Dear Principal,

                Today's Teachers Attendance Record:
                ____________________________________________________
                Present Teachers:
                S. No. | Name
                ------------------------------------
                {"".join([f"{i+1:<8} | {teacher}/n" for i, teacher in enumerate(present_teachers)])}
                ------------------------------------

                Absent Teachers:
                S. No. | Name
                ------------------------------------
                {"".join([f"{i+1:<8} | {teacher}/n" for i, teacher in enumerate(absent_teachers)])}
                ------------------------------------

                Thank you for your efforts in maintaining teacher attendance.

                Best Regards,
                [Your University Name]
                """
                return body

            @staticmethod
            def monthly(department_name, teachers_data):
                body = f"""
                Dear Principal,

                Monthly Teachers Attendance Record for {department_name}:
                ____________________________________________________
                Department Name: {department_name}
                ------------------------------------
                S. No. | Teacher Name       | Total Classes Taken | Scheduled Classes | Attendance Percent
                ------------------------------------
                {"".join([f"{i+1:<8} | {data['name']:<20} | {data['total_classes']:<19} | {data['scheduled_classes']:<18} | {data['attendance_percent']}/n" for i, data in enumerate(teachers_data)])}
                ------------------------------------

                Your leadership ensures the success of our academic community.

                Best Regards,
                [Your University Name]
                """
                return body
       
class DataProvider:
    class AnotherInfo:
        def __init__(self, database_connector):
            self.database_connector = database_connector

        #To get dpt id, name and email
        def get_departments_info(self):
            query_get_departments = "SELECT id, name, email FROM departments"
            departments_info = []

            try:
                cursor = self.database_connector.connection.cursor()
                cursor.execute(query_get_departments)
                dpts = cursor.fetchall()

                for dpt in dpts:
                    department_id, department_name, department_email = dpt
                    departments_info.append({"id": department_id, "name": department_name, "email": department_email})
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

            return departments_info

            # To get course id and name where pdt id pass
        
        def get_course_info(self, dpt_id):
            query_get_courses = "SELECT id, name FROM courses WHERE dpt_id = %s"
            courses_info = []

            try:
                cursor = self.database_connector.connection.cursor()
                cursor.execute(query_get_courses, (dpt_id,))
                courses = cursor.fetchall()

                for course in courses:
                    course_id, course_name = course
                    courses_info.append({"id": course_id, "name": course_name})
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

            return courses_info
            #To get semester infromation in course where pass
        
        def get_semester_info(self, course_id):
            query_get_semesters = "SELECT id, semester_name FROM semesters WHERE class_id IN (SELECT id FROM classes WHERE dpt_id = (SELECT dpt_id FROM courses WHERE id = %s));"
            semesters_info = []

            try:
                cursor = self.database_connector.connection.cursor()
                cursor.execute(query_get_semesters, (course_id,))
                semesters = cursor.fetchall()

                for semester in semesters:
                    semester_id, semester_name = semester
                    semesters_info.append({"id": semester_id, "name": semester_name})
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

            return semesters_info
        
        # To get all subjects name where semester id are pass
        def get_subjects(self, semester_id):
            query_get_subjects = "SELECT id, name FROM subjects WHERE semester_id = %s"
            subjects_info = []

            try:
                cursor = self.database_connector.connection.cursor()
                cursor.execute(query_get_subjects, (semester_id,))
                subjects = cursor.fetchall()

                for subject in subjects:
                    subject_id, subject_name = subject
                    subjects_info.append({"id": subject_id, "name": subject_name})
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

            return subjects_info

        # To get all astudent where semester id are pass
        def get_all_std(self, semester_id):
            query_get_students = "SELECT id FROM students WHERE semester = %s"
            students_info = []

            try:
                cursor = self.database_connector.connection.cursor()
                cursor.execute(query_get_students, (semester_id,))
                students = cursor.fetchall()

                for student in students:
                    student_id = student[0]
                    students_info.append({"id": student_id})
            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

            return students_info
        
        def get_std_info(self, student_id):
            query_get_student_info = "SELECT name, email, parent_email FROM students WHERE id = %s"
            student_info = {}

            try:
                cursor = self.database_connector.connection.cursor()
                cursor.execute(query_get_student_info, (student_id,))
                student_data = cursor.fetchone()

                if student_data:
                    name, email, parent_email = student_data
                    student_info = {"name": name, "email": email, "parent_email": parent_email}

            except Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()

            return student_info
       
        def get_teacher_info(self, semester_id):        
            query = """
                    SELECT teachers.name AS teacher_name, teachers.email, subjects.name AS subject_name
                    FROM teachers
                    JOIN subjects ON teachers.id = subjects.teacher
                    WHERE subjects.semester = %s
                """
            self.cursor.execute(query, (semester_id,))
            return self.cursor.fetchone()

        
            
                
        
    class AttendanceData:
        database_connector = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rakesh9339",
            database="sas")
        
        def __init__(self, database_connector):
            self.database_connector = database_connector
        def today_attendance(self, database_connector):
            def student(self, std_id, database_connector):           
                std_instance =Student()
                get_data = std_instance.GetRecord()                
                return get_data.get_today_std_record(std_id, database_connector)     #Import from AttendacneManager.py
            
            def teacher(self, teacher_id, database_connector):
                tcr_instance = TeachersAttendance()
                get_data = tcr_instance.GetRecord()
                return get_data.get_today_tcr_record(teacher_id, database_connector) #Import from AttendacneManager.py
        
        def monthly_attendance(self, database_connector):
            def student(self,student_id,database_connector):
                std_instance =Student()
                get_data = std_instance.GetRecord()                 
                return get_data.get_today_std_record(student_id,database_connector)
            def teachers(self, teacher_id, database_connector):
                tcr_instance = TeachersAttendance()
                get_data = tcr_instance.GetRecord()
                return get_data.get_month_tcr_record(teacher_id, database_connector, month=None, year=None)
            def get_monthly_std_record_for_teachers(self,teacher_id):
                
class MessageSender:
    def mailSender(self, receiver_mail, body):
        # Replace the placeholders with your email credentials
        sender_email = "your_sender_email@gmail.com"
        sender_password = "your_sender_password"

        # Create an EmailMessage object
        em = EmailMessage()
        em["From"] = sender_email
        em["To"] = receiver_mail
        em["Subject"] = "attendance Record from Pt. Ravishnkar Shukla Univercity Raipur"
        em.set_content(body)

        # Setup the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # For TLS

        try:
            # Connect to the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # Start TLS for security
                server.starttls()
                
                # Login to your email account
                server.login(sender_email, sender_password)

                # Send the email
                server.send_message(em)

            print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")
        
    data_provider = DataProvider()
    db_connector = DatabaseConnector(host="localhost", user="root", password="rakesh9339", database="sas")
    get_info = data_provider.AnotherInfo(db_connector)
    dpt_info = get_info.get_departments_info()
    attendance = data_provider.AttendanceData

    #stdudent dily formate
    message_instance = MessageFormat
    std_instance = message_instance.Student
    sdf = std_instance.Daily    #sdf = " student daily formate"

    #parent daily formate
    prt_instance = message_instance.Parent
    pdf = prt_instance.Daily   #pdf stance parent daily formate
    
    # Store department IDs in a list
    department_ids = [dpt["id"] for dpt in dpt_info]

    
    #daily basis message sending
    for dpt_id in department_ids:
        # Get course information for the current department
        course_info = get_info.get_course_info(dpt_id)

        # Extract course IDs from the course_info list
        course_ids = [course["id"] for course in course_info]

        # Get semester information for all courses in one query
        semester_info = get_info.get_semester_info_batch(course_ids)

        for semester in semester_info:
            semester_id = semester["id"]

            # Get subjects and students for the current semester
            subjects_info = get_info.get_subjects(semester_id)
            students_info = get_info.get_all_std(semester_id)

            for subject in subjects_info:
                subject_name = subject["name"]
                
            for student_id in students_info:
                student_info = get_info.get_std_info(student_id)
                todays_attendace = attendance.today_attendance(db_connector).student(student_id,db_connector)
                body = sdf.format(student_info["name"],semester_info["name"],subjects_info["name"],subjects_info["name"],todays_attendace)
                student_mail = student_info["email"]
                mailSender(student_mail,body)
                parentMail = student_info["parent_email"]                
                body = pdf.format(student_info["name"],subjects_info["name"],subjects_info["name"],todays_attendace)                
                mailSender(parentMail,)     
    
              






    
def main():
    db_connector = DatabaseConnector(host="localhost", user="root", password="rakesh9339", database="sas")
    
    data_provider_instance = DataProvider()
    another_info_instance = data_provider_instance.AttendanceData(db_connector)
    departments_info = another_info_instance.get_monthly(35,db_connector)

    print(departments_info)

if __name__ == "__main__":
    main()
  