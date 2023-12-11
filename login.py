import smtplib
import ssl
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("Welcome To Face Recognition Attendance System")

def send_otp_email(email):
    otp = generate_otp()
    
    # Set up the email server
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "prsu.attendance@gmail.com"
    smtp_password = "kcbbevsrbejxalbf"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Create the MIME object
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email
    msg['Subject'] = 'Your OTP for Verification'

    # Body of the email
    body = f'Your OTP is: {otp}'
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, msg.as_string())
        print("OTP successfull send ")

    return otp

def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))
def otp_verifier(otp_entered):
    # For simplicity, the correct OTP is hardcoded here.
    correct_otp = 123456

    return otp_entered == correct_otp


email_id = input("Email Id: ")
pc = input("Password: ")

if email_id == "" and pc == "#*06#":
    master_password = input("Master Password: ")
    if master_password == "database":
        print("Add New Account:")
        userName = input("Please enter User Name: ")
        username = input("Please enter Contact number: ")
        email = input("Please enter Email Id: ")
        
        # Send OTP and verify
        otp_enter = int(input("Enter OTP: "))
        send_otp_email(email)
        check = otp_verifier(otp_enter)        
        if check:
            print(f"User with email {email} has been successfully added.")
        else:
            print("OTP verification failed. Exiting.")
            exit()

elif email_id == "9339rahi@gmail.com" and pc == "raCase^9339":
    print("Login successful")
else:
    print("Please enter valid credentials")

