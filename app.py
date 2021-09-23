from re import I
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT * FROM boards;"
    result = db.session.execute(sql)
    boards = result.fetchall()
    return render_template("index.html", boards=boards)

@app.route("/login")
def loginPage():
    return render_template("login.html")

@app.route("/loginUser", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        print("Nono user")
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            return redirect("/")
    return "No logger"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/registerUser", methods=["POST"])
def register():
    hash_password = generate_password_hash(request.form["password"])
    username = request.form["username"]
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        print("Username already exists.")
        pass
    else:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_password})
    db.session.commit()
    return redirect("/")


@app.route("/boards/<name>")
def boards(name):
    sql = "SELECT * FROM posts WHERE board=(SELECT id FROM boards WHERE name=:name);"
    result = db.session.execute(sql, {"name": name})
    posts = result.fetchall()
    return render_template("/board.html", name=name, posts=posts)
