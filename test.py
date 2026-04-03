import smtplib
from time import sleep

# Email configuration
sender_email = "alexisenterprise977@gmail.com"
receiver_email = "alexanderemmanuel1719@gmail.com"
password = "qmypsjtmovydxtvx"  # Replace with App Password
import smtplib

fromaddr = "alexisenterprise977@gmail.com"
toaddrs  = "alexanderemmanuel1719@gmail.com"
msg = 'Why,Oh why!'
username = "alexisenterprise977@gmail.com"
password = "qmypsjtmovydxtvx"
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
