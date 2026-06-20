import base64
import json
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.login_view='auth.login'


def _load_gmail_credentials(app):
    token_json = app.config.get("GMAIL_TOKEN_JSON")
    token_base64 = app.config.get("GMAIL_TOKEN_BASE64")
    token_file = app.config.get("GMAIL_TOKEN_FILE", "token.json")
    scopes = app.config.get(
        "GMAIL_OAUTH_SCOPES",
        ["https://www.googleapis.com/auth/gmail.send"],
    )

    if token_base64:
        token_json = base64.b64decode(token_base64).decode("utf-8")

    if token_json:
        token_data = json.loads(token_json)
        return Credentials.from_authorized_user_info(token_data, scopes)

    if os.path.exists(token_file):
        return Credentials.from_authorized_user_file(token_file, scopes)

    raise RuntimeError(
        "Gmail API credentials not configured. Set GMAIL_TOKEN_JSON or GMAIL_TOKEN_BASE64, "
        "or provide a valid token file at the path configured by GMAIL_TOKEN_FILE."
    )


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix='/api/v1')
    
    if app.config["EMAIL_PROVIDER"] == "gmail_api":
        creds = _load_gmail_credentials(app)
        app.extensions["gmail_service"] = build(
            "gmail",
            "v1",
            credentials=creds
        )
    
    return app
    