import base64
import requests
import secrets

from flask import Flask, render_template, url_for, redirect, session, json, request
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from helpers import is_access_token_valid, is_id_token_valid, config
from user import User

app = Flask(__name__)
app.config.update({'SECRET_KEY': secrets.token_hex(64)})
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Parameter state should be something not guessable
APP_STATE = secrets.token_urlsafe(64)
NONCE = secrets.token_urlsafe(64)


# @app.route("/")
# def home():
#     return render_template("home.html")
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
@app.route("/login")
def login():
    bu = config['issuer'].split('/oauth2')[0]
    cid = config['client_id']
    issuer = config['issuer']
    redirect_uri = config['redirect_uri']
    return render_template(
        "login.html", baseUri=bu, clientId=cid, issuer=issuer, redirect_uri=redirect_uri, state=APP_STATE, nonce=NONCE)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


def base64_to_str(data):
    return str(base64.b64encode(json.dumps(data).encode('utf-8')), 'utf-8')


if __name__ == '__main__':
    app.run(host="localhost", port=8181, debug=True)
