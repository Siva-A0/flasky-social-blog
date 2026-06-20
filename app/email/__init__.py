from threading import Thread
from flask import current_app, render_template

from . import gmail_api_provider, flask_mail_provider


def _send_async(app, provider, to, subject, text_body, html_body):
    with app.app_context():
        if provider == "gmail_api":
            gmail_api_provider.send(
                to, subject, text_body, html_body
            )
        else:
            flask_mail_provider.send(
                to, subject, text_body, html_body
            )


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    subject = (
        app.config["FLASKY_MAIL_SUBJECT_PREFIX"]
        + " "
        + subject
    )

    text_body = render_template(
        template + ".txt",
        **kwargs
    )

    html_body = render_template(
        template + ".html",
        **kwargs
    )

    provider = app.config["EMAIL_PROVIDER"]

    thr = Thread(
        target=_send_async,
        args=(
            app,
            provider,
            to,
            subject,
            text_body,
            html_body,
        ),
    )

    thr.start()
    return thr