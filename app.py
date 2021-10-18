from flask import Flask, flash
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
        flash("Username not found.", "warning")
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            session["user_id"] = user.id
            flash("Logged in as: " + username, "success")
            return redirect("/")
        flash("Username and password don't match.", "warning")
    return redirect(request.referrer)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    flash("You have been logged out.", "warning")
    return redirect("/")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/registerUser", methods=["POST"])
def register():
    hash_password = generate_password_hash(request.form["password"])
    username = request.form["username"]

    if not username:
        flash("Username can't be empty.")
        return redirect(request.referrer)
    elif not request.form["password"]:
        flash("Password can't be empty.")
        return redirect(request.referrer)

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
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
    sql = "SELECT * FROM posts WHERE board=(SELECT id FROM boards WHERE name=:name);"
    result = db.session.execute(sql, {"name": name})
    posts = result.fetchall()
    return render_template("/board.html", name=name, posts=posts, id=posts[0].board)

@app.route("/post/<id>")
def posts(id):
    sql = """SELECT m.id, m.post_id, m.user_id, m.content, m.created_at, m.visible, u.username 
    FROM messages as m INNER JOIN users AS u ON m.user_id=u.id AND m.post_id=:id AND m.visible=true ORDER BY m.created_at;"""
    result = db.session.execute(sql, {"id": id})
    messages = result.fetchall()
    sql = "SELECT title FROM posts WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    title = result.fetchone()[0]
    return render_template("post.html", messages=messages, id=id, title=title)

@app.route("/sendMessage", methods=["POST"])
def send_message():
    message = request.form["message"]
    id = request.form["id"]
    user_id = session["user_id"]
    sql = "INSERT INTO messages (post_id, user_id, content, created_at) VALUES(:id, :user, :message, NOW());"
    db.session.execute(sql, {"id": id, "user": user_id, "message": message})
    db.session.commit()
    return redirect(request.referrer)




@app.route("/addPost", methods=["POST"])
def add_post():
    title = request.form["title"]
    message = request.form["message"]
    board_id = request.form["id"]
    print(board_id)
    user_id = session["user_id"]
    sql = "INSERT INTO posts (post_owner, title, created_at, board) VALUES (:user_id, :title, NOW(), :board) RETURNING id;"
    result = db.session.execute(sql, {"user_id": user_id, "title": title, "board": board_id})
    
    post_id = result.fetchone().id
    sql = "INSERT INTO messages (post_id, user_id, content, created_at) VALUES(:id, :user, :message, NOW());"
    db.session.execute(sql, {"id": post_id, "user": user_id, "message": message})
    db.session.commit()

    return redirect(request.referrer)


@app.route("/deleteMessage", methods=["POST"])
def delete_message():
    if session["username"] != request.form["username"]:
        return "Forbidden - 403"
    else:
        id = request.form["id"]
        sql = "UPDATE messages SET visible = FALSE WHERE id=:id;"
        db.session.execute(sql, {"id": id})
        db.session.commit()
        return redirect(request.referrer)

@app.route("/result")
def result():
    query = request.args["query"]
    sql = "SELECT m.id, m.post_id, m.user_id, m.content, m.created_at FROM messages as m WHERE content ILIKE :query AND visible = true"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    messages = result.fetchall()
    print(messages)
    return render_template("result.html", messages=messages)
