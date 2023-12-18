'''---------------------------------------------------------------------------------------------------
About Author ->
        Name - Rakesh Kumar
               MCA 3 Semester
               9339rahi@gmail.com
        Date - 23-11-2023
--------------------------------------------------------------------------------------------------------    
The code is part of " Face Recognition Attendance system " for Pt. Ravishankar Shukla univercity Raipur
.......................................................................................................
Holiday Manager Class

This class manages holidays and their records in a MySQL database. It allows users to add, remove holidays,
add Sundays as holidays, and show holidays for a specific month.

Attributes:
    - holidays (set): A set to store holiday records.
    - db_connection: MySQL database connection.
    - cursor: Database cursor for executing queries.

Methods:
    - __init__(self): Initializes the Holiday Manager class.
    - connect_to_database(self): Establishes a connection to the MySQL database.
    - disconnect_from_database(self): Closes the database connection.
    - create_table(self, table_name): Creates a table for storing holidays.
    - add_holiday_to_database(self, date_str, description, table_name): Adds a holiday record to the database.
    - add_sundays_as_holidays(self): Adds Sundays as holidays for the current month.
    - show_all_holidays_from_database(self, table_name): Displays all holidays from the specified table.
    - mainMethod(self): Main method to interact with the Holiday Manager, providing options to the user.
    - remove_holiday_from_database(self, date_str, table_name): Removes a holiday record from the database.

'''
import mysql.connector
import datetime
import logging
from fuzzywuzzy import fuzz, process
from mysql.connector.errors import Error

class Holiday:
    def __init__(self):
        self.holidays = set()
        self.db_connection = None
        self.cursor = None
        logging.basicConfig(level=logging.INFO)

    def connect_to_database(self):
        try:
            self.db_connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='rakesh9339',
                database='sas'
            )
            self.cursor = self.db_connection.cursor()
            logging.info("Connected to the database.")
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to the database: {err}")

    def disconnect_from_database(self):
        try:
            if self.db_connection.is_connected():
                self.cursor.close()
                self.db_connection.close()
                logging.info("Disconnected from the database.")
        except mysql.connector.Error as err:
            logging.error(f"Error disconnecting from the database: {err}")

    def create_table(self, table_name):
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    holiday_date DATE,
                    description VARCHAR(255)
                );
            """)
            self.db_connection.commit()
            logging.info(f"Table '{table_name}' created.")
        except mysql.connector.Error as err:
            logging.error(f"Error creating table: {err}")

    def add_holiday_to_database(self, date_str, description, table_name):
        try:
            holiday_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            self.cursor.execute(f"INSERT INTO {table_name} (holiday_date, description) VALUES (%s, %s)", (holiday_date, description))
            self.db_connection.commit()
            logging.info(f"Added holiday to the table '{table_name}' on {date_str} with description: {description}.")
        except mysql.connector.Error as err:
            logging.error(f"Error adding holiday to the database: {err}")

    def add_sundays_as_holidays(self):
        try:
            today = datetime.date.today()

            if today.day == 1:
                table_name = today.strftime("%B").lower() + "_holiday"
                self.create_table(table_name)

                first_day_of_month = today.replace(day=1)
                current_date = first_day_of_month
                while current_date.month == first_day_of_month.month:
                    if current_date.weekday() == 6:  # Sunday
                        self.add_holiday_to_database(current_date.strftime("%Y-%m-%d"), "Sunday", table_name)
                    current_date += datetime.timedelta(days=1)
        except Exception as e:
            logging.error(f"Error adding Sundays as holidays: {e}")

    def show_all_holidays_from_database(self, table_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            holidays = self.cursor.fetchall()
            if holidays:
                print(f"All Holidays in {table_name}:")
                for holiday in holidays:
                    print(holiday[1], holiday[2])  # Assuming holiday_date is at index 1 and description is at index 2
            else:
                print(f"No holidays in the table '{table_name}'.")
        except mysql.connector.Error as err:
            logging.error(f"Error retrieving holidays from the database: {err}")

    def mainMethod(self):
        try:
            print("""Holiday Manager
1. Add Holiday
2. Remove Holiday
3. Add Sundays as Holidays
4. Show Holidays for a Specific Month""")
            choice = int(input("Please enter your option: "))

            if choice == 1:
                date = input("Enter the holiday date (YYYY-MM-DD): ")
                description = input("Enter the description: ")
                table_name = datetime.datetime.now().strftime("%B").lower() + "_holiday"
                self.add_holiday_to_database(date, description, table_name)
                print(f"Holiday on {date} added successfully with description: {description} to the table '{table_name}'.")
            elif choice == 2:
                remove_date = input("Enter the date to remove (YYYY-MM-DD): ")
                table_name = datetime.datetime.now().strftime("%B").lower() + "_holiday"
                self.remove_holiday_from_database(remove_date, table_name)
                print(f"Removed holiday on {remove_date} from the table '{table_name}'.")
            elif choice == 3:
                self.add_sundays_as_holidays()
                print("Sundays added as holidays for the current month.")
            elif choice == 4:
                month_name = {
                    1: "January", 2: "February", 3: "March", 4: "April",
                    5: "May", 6: "June", 7: "July", 8: "August",
                    9: "September", 10: "October", 11: "November", 12: "December"
                }

                input_text = input("Enter the month name or number: ")

                try:
                    choice = int(input_text)
                    month_name_str = month_name.get(choice)
                except ValueError:
                    matches = process.extractOne(input_text, month_name.values(), scorer=fuzz.token_sort_ratio)
                    threshold = 80

                    if matches[1] >= threshold:
                        month_name_str = matches[0]
                    else:
                        print(f"Couldn't find a close match for '{input_text}'.")
                        month_name_str = None

                if month_name_str:
                    self.show_all_holidays_from_database(month_name_str.lower() + "_holiday")
                else:
                    print(f"No holidays found for '{input_text}'.")
        except Exception as e:
            logging.error(f"Error in main method: {e}")

    def remove_holiday_from_database(self, date_str, table_name):
        try:
            holiday_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            self.cursor.execute(f"DELETE FROM {table_name} WHERE holiday_date = %s", (holiday_date,))
            self.db_connection.commit()
            logging.info(f"Removed holiday from the table '{table_name}' on {date_str}.")
        except mysql.connector.Error as err:
            logging.error(f"Error removing holiday from the database: {err}")

# Example Usage:
try:
    holiday_manager = Holiday()
    holiday_manager.connect_to_database()
    holiday_manager.add_sundays_as_holidays()
    holiday_manager.mainMethod()
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
finally:
    holiday_manager.disconnect_from_database()
