from flask import current_app
from flask_mail import Message

from .. import mail


def send(to, subject, text_body, html_body):

    msg = Message(
        subject,
        sender=current_app.config["FLASKY_MAIL_SENDER"],
        recipients=[to],
    )

    msg.body = text_body
    msg.html = html_body

    mail.send(msg)