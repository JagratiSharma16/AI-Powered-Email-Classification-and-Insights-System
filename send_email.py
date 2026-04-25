

import smtplib
from email.mime.text import MIMEText

sender_email = "dumyy543@gmail.com"
app_password = "qufq nccu tqll wrrh"  # paste the generated app password here

test_emails = [
    ("Need help with account", "Hello, I need help with my login."),
    ("Request for price", "Could you send me your latest price list?"),
    ("Complaint about service", "I am unhappy with the last order."),
    ("Just saying hi", "This is a test email."),
]

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(sender_email, app_password)

for subject, body in test_emails:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = sender_email
    server.sendmail(sender_email, sender_email, msg.as_string())

server.quit()
print("Test emails sent!")
