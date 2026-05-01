import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
sender_email = "alexchidi11917@gmail.com"
sender_password = "hdjrldghmgzxczqc"  # Use Gmail App Password
receiver_email = "alexanderemmanuel1719@gmail.com"

# Create message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Hello from Python!"

body = "Hi there! This email was sent using Python. 🎉"
msg.attach(MIMEText(body, "plain"))

# Send email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
