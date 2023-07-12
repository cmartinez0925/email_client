import os
import smtplib
import imghdr
import argparse

from email.message import EmailMessage

# Get username and password from environmental variables on system
GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_PW = os.environ.get('GMAIL_PW')

# Add arguments to script to run on terminal
parser = argparse.ArgumentParser(description="Sends an email w/attachments")
parser.add_argument("-i", "--image", dest="image_attachment", help="Attach an image to the email")
parser.add_argument("-f", "--file", dest="file_attachment", help="Attach a file to the email separated by a comma")
parser.add_argument("-s", "--subject", dest="subject", help="Add a subject line to the email")
parser.add_argument("-b", "--body", dest="body", help="Add text to the email")
args = parser.parse_args()

recipients = ["christopher.martinez0925@live.com"]

# Determine if a subject or body was provided
if not args.subject:
    subject = "No Subject"
else:
    subject = args.subject

if not args.body:
    body = ""
else:
    body = args.body

# Create the email object to be sent
msg = EmailMessage()
msg['From'] = GMAIL_USER
msg['To'] = recipients
msg['Subject'] = subject
msg.set_content(body)

files = []

# Add Attachments
if args.image_attachment:
    files.append(args.image_attachment)

    for file in files:
        # Check if file exits
        try:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name       
        except FileNotFoundError:
            print(f"[-] The specified file: {file} was not found.")
            continue
        else:
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)


# Clear the image files within the list to process the non-image attachments
files.clear()

if args.file_attachment:
    files = args.file_attachment.split(',')
    # files.append(args.file_attachment)

    for file in files:
        # Check if file exits
        try:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = f.name
        except FileNotFoundError:
            print(f"[-] The specified file: {file} was not found.")
            continue
        else:
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)


# Login to email and send the email message to the recipients
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(GMAIL_USER, GMAIL_PW)
    smtp.send_message(msg)
    
