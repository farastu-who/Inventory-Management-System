import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, recipient):
    # Replace with your SMTP server details
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'farastu17@gmail.com'
    SMTP_PASSWORD = 'password'
    
    # Email setup
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
