from app import app
from flask import render_template
from flask import Flask, flash
from flask import redirect, render_template, request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from db import db

@app.route("/")
def index():
    sql = "SELECT id, name FROM boards WHERE visible = TRUE;"
    result = db.session.execute(sql)
    boards = result.fetchall()
    return render_template("index.html", boards=boards)


@app.route("/login")
def loginPage():
    return render_template("login.html")


@app.route("/loginUser", methods=["POST"])
def login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    sql = "SELECT id, password, role_id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        flash("Username not found.", "warning")
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            session["user_id"] = user.id
            session["role"] = user.role_id
            session["csrf_token"] = secrets.token_hex(16)
            flash("Logged in as: " + username, "success")
            return redirect("/")
        flash("Username and password don't match.", "warning")
    return redirect(request.referrer)


@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["role"]
    del session["csrf_token"]
    flash("You have been logged out.", "warning")
    return redirect("/")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/registerUser", methods=["POST"])
def register():
    hash_password = generate_password_hash(request.form["password"].strip())
    username = request.form["username"].strip()

    if not username:
        flash("Username can't be empty.")
        return redirect(request.referrer)
    elif not request.form["password"]:
        flash("Password can't be empty.")
        return redirect(request.referrer)

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user:
        flash("Username already exists.")
    else:
        sql = "INSERT INTO users (username, password, role_id) VALUES (:username, :password, 1)"
        db.session.execute(sql, {"username": username, "password": hash_password})
        flash("Registered succesfully, login using your credentials", "success")
        db.session.commit()
        return redirect("/login")
    return redirect(request.referrer)


@app.route("/boards/<name>")
def boards(name):
    sql = "SELECT id from boards WHERE name=:name"
    result = db.session.execute(sql), {"name":name}
    get = result.fetchone()
    if not get:
        return render_template("error.html", error="Board name not found.")

    sql = "SELECT p.id, p.post_owner, p.title FROM posts AS p INNER JOIN boards as b ON p.board=b.id AND b.name=:name AND p.visible = TRUE"
    result = db.session.execute(sql, {"name": name})
    posts = result.fetchall()
    result = db.session.execute(
        "SELECT id FROM boards WHERE name=:name", {"name": name}
    )
    id = result.fetchone()[0]
    return render_template("/board.html", name=name, posts=posts, id=id)


@app.route("/post/<id>")
def posts(id):
    if not id.isdecimal():
        return render_template("error.html", error="Post not found.")
    sql = """SELECT m.id, m.post_id, m.user_id, m.content, m.created_at, m.visible, u.username 
    FROM messages as m INNER JOIN users AS u ON m.user_id=u.id AND m.post_id=:id AND m.visible=true ORDER BY m.created_at;"""
    result = db.session.execute(sql, {"id": id})
    messages = result.fetchall()
    if not messages:
        return render_template("error.html", error="Post not found.")

    sql = "SELECT title FROM posts WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    title = result.fetchone().title
    return render_template("post.html", messages=messages, post_id=id, title=title)


@app.route("/sendMessage", methods=["POST"])
def send_message():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", error="User cannot be validated.")
    message = request.form["message"].rstrip()
    if not message:
        flash("Please add your message.", "warning")
        return redirect(request.referrer)
    id = request.form["id"]
    user_id = session["user_id"]

    if not id or not user_id:
        flash("Something wen't wrong.", "danger")
        return redirect(request.referrer)

    sql = "INSERT INTO messages (post_id, user_id, content, created_at) VALUES(:id, :user, :message, NOW());"
    db.session.execute(sql, {"id": id, "user": user_id, "message": message})
    db.session.commit()
    return redirect(request.referrer)


@app.route("/addPost", methods=["POST"])
def add_post():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", error="User cannot be validated.")
    title = request.form["title"].rstrip()
    message = request.form["message"].rstrip()
    board_id = request.form["id"]
    if not title:
        flash("Title is needed.", "warning")
        return redirect(request.referrer)
    if not message:
        flash("Add message to your post.", "warning")
        return redirect(request.referrer)
    if not board_id:
        flash("Something wen't wrong.", "danger")
        return redirect(request.referrer)
    user_id = session["user_id"]
    sql = "INSERT INTO posts (post_owner, title, created_at, board) VALUES (:user_id, :title, NOW(), :board) RETURNING id;"
    result = db.session.execute(
        sql, {"user_id": user_id, "title": title, "board": board_id}
    )

    post_id = result.fetchone().id
    sql = "INSERT INTO messages (post_id, user_id, content, created_at) VALUES(:id, :user, :message, NOW());"
    db.session.execute(sql, {"id": post_id, "user": user_id, "message": message})
    db.session.commit()

    return redirect(request.referrer)


@app.route("/deleteMessage", methods=["POST"])
def delete_message():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", error="User cannot be validated.")
    if session["username"] != request.form["username"]:
        return render_template("error.html", error="User cannot be validated.")
    else:
        id = request.form["id"]

        # checks if the given message is the first of the post.
        sql = """SELECT m.id FROM messages as m INNER JOIN posts as p
        ON p.created_at=m.created_at AND m.post_id=p.id AND m.id=:id"""

        result = db.session.execute(sql, {"id": id})
        first = result.fetchone()
        # And delete the post if it is.
        if first:
            sql = "UPDATE posts SET visible = FALSE WHERE id=:id"
            db.session.execute(sql, {"id": id})
            db.session.commit()

            sql = "UPDATE messages SET visible = FALSE WHERE post_id=:id"
            db.session.execute(sql, {"id": id})
            db.session.commit()
            flash("Post was deleted.", "success")
            return redirect("/")
        else:
            sql = "UPDATE messages SET visible = FALSE WHERE id=:id;"
            db.session.execute(sql, {"id": id})
            db.session.commit()
            flash("Message deleted.", "success")
            return redirect(request.referrer)


@app.route("/result")
def result():
    query = request.args["query"]
    sql = """SELECT m.id, m.post_id, m.user_id, m.content, m.created_at
    FROM messages as m WHERE content ILIKE :query AND visible = true"""
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    messages = result.fetchall()
    return render_template("result.html", messages=messages)


@app.route("/createBoard", methods=["POST"])
def create_board():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", error="User cannot be validated.")
    name = request.form["name"].rstrip()
    if not name:
        flash("Board name can't be empty.", "warning")
        return request.referrer

    sql = "INSERT INTO boards (name) VALUES (:name)"
    db.session.execute(sql, {"name": name})
    db.session.commit()
    flash("Board created succesfully", "success")
    return redirect("/")


@app.route("/edit/<id>")
def edit_post(id):

    sql = "SELECT id, post_id, content FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    message = result.fetchone()
    if not message:
        return render_template("error.html", error="Message not found.")
    return render_template("edit.html", message=message)


@app.route("/updateMessage", methods=["POST"])
def update_message():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", error="User cannot be validated.")
    message = request.form["message"]
    id = request.form["id"]
    sql = "UPDATE messages SET content = :message WHERE id=:id"
    db.session.execute(sql, {"message": message, "id": id})
    db.session.commit()

    sql = "SELECT p.id FROM posts as p INNER JOIN messages as m ON m.post_id=p.id AND m.id=:id"
    result = db.session.execute(sql, {"id": id})
    post = result.fetchone()
    return redirect("post/" + str(post.id))


@app.route("/deletePost", methods=["POST"])
def delete_post():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", error="User cannot be validated.")
    id = request.form["id"]
    sql = "UPDATE posts SET visible = FALSE WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()
    return redirect(request.referrer)


@app.route("/deleteBoard", methods=["POST"])
def delete_board():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", error="User cannot be validated.")
    id = request.form["id"]
    if not id:
        flash("Something wen't wrong", "danger")
        return redirect(request.referrer)
    sql = "UPDATE boards SET visible = FALSE WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()
    flash("Board deleted successfully.", "success")
    return redirect(request.referrer)
