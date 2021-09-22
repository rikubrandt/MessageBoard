from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT * FROM users;"
    result = db.session.execute(sql)
    name = result.fetchone()[1]
    return render_template("index.html", test=name)

@app.route("/login")
def loginPage():
    return render_template("login.html")

@app.route("/boards")
def boards():
    sql = "SELECT * FROM boards;"
    result = db.session.execute(sql)

