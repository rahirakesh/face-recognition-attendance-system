#just tryl not implement
import smtplib
import ssl
from email.message import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Define email sender and receiver
email_sender = 'sender.email.here.@mail.com'
email_password = 'senderpassword here'
email_receiver = 'recever.mail.@mail.com'

# Set the subject of the email
subject = 'Attendance record received from PRS University'

# Create a PDF from the body text
pdf_filename = 'attendance_report.pdf'

# Function to create a PDF
def create_pdf(filename, body):
    pdf = canvas.Canvas(filename, pagesize=letter)

    # Set font and size
    pdf.setFont("Helvetica", 12)

    # Set starting coordinates
    x = 100
    y = letter[1] - 100  # Starting from the top of the page

    # Adjust vertical spacing
    line_height = 14  # Adjust as needed

    # Draw text on the PDF
    for line in body.split('\n'):
        pdf.drawString(x, y, line)
        y -= line_height

    # Save the PDF to the file
    pdf.save()

# students record for parent in monthly
name = "Rakesh"
class_name = "MCA"
semester = 3
month = "January"
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
                 [Pt. Ravishankar Shukla University, Raipur]
"""

# Create the PDF
create_pdf(pdf_filename, body)

# Create the EmailMessage
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content('Please find the attached attendance report.')

# Attach the PDF to the email
with open(pdf_filename, 'rb') as pdf_file:
    em.add_attachment(pdf_file.read(), maintype='application', subtype='pdf', filename=pdf_filename)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
print("Message send successfully")
