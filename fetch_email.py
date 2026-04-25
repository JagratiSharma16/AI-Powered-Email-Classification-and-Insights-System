import imaplib, email
from email.header import decode_header
from db_set import Email, session
from datetime import datetime

def save_email(subject, sender, category, body):
    new_email = Email(
        subject=subject,
        sender=sender,
        category=category,
        body=body,
        date=datetime.utcnow()
    )
    session.add(new_email)
    session.commit()

def fetch_and_classify_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("dumyy543@gmail.com", "qufq nccu tqll wrrh")
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    for eid in email_ids[-5:]:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

        sender = msg.get("From")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        # Simple keyword-based classification
        if "complaint" in body.lower():
            category = "Complaint"
        elif "price" in body.lower() or "quote" in body.lower():
            category = "Sales Inquiry"
        elif "help" in body.lower() or "issue" in body.lower():
            category = "Customer Support"
        else:
            category = "Other"

        save_email(subject, sender, category, body)

    mail.logout()
