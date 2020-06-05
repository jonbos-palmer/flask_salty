import os

from flask import Flask, request, redirect, url_for, session, flash, g
from flask.templating import render_template
from salty.db import get_db

from .password_util import hash_pass, salt_gen, verify_password


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "salty.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            password2 = request.form["password_confirm"]
            db = get_db()
            error = None
            if not username:
                error = "Username is required."
            elif not password:
                error = "Password is required."
            elif not password == password2:
                error = "Passwords don't match."

            elif (
                db.execute(
                    "SELECT id FROM user WHERE username = ?", (username,)
                ).fetchone()
                is not None
            ):
                error = "User {} is already registered.".format(username)

            if error is None:
                salt = salt_gen()
                hashed_pass = hash_pass(str.encode(password + salt))
                db.execute(
                    "INSERT INTO user (username, salt, password) VALUES (?, ?, ?)",
                    (username, salt, hashed_pass),
                )
                db.commit()
                return redirect(url_for("login"))
            flash(error)
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            error = None
            db = get_db()

            user = db.execute(
                "SELECT * FROM user WHERE username = ?", (username,)
            ).fetchone()

            if user is None:
                error = "That user doesn't exist"
            elif not verify_password(password, user["salt"], user["password"]):
                error = "Invalid password"
            
            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))
            
            flash(error)

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        if session['user']:
            session.clear()
            return redirect(url_for('index'))

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

    from . import db

    db.init_app(app)


    return app
