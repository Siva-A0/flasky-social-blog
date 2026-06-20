from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app
import base64


def send(to, subject, text_body, html_body):

    service = current_app.extensions["gmail_service"]

    msg = MIMEMultipart("alternative")
    msg["to"] = to
    msg["subject"] = subject

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    raw = base64.urlsafe_b64encode(
        msg.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()