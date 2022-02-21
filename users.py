from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import validate

def login(username, password):
    sql = "SELECT id, password, admin FROM users WHERE username=:username AND visible=TRUE"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session['admin'] = user.admin
            return True
        else:
            False

def logout():
    del session["user_id"]
    del session['admin']

def register(username, password):
    if not validate.username(username) or not validate.password(password):
        return False
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,admin,visible) VALUES (:username,:password,FALSE,TRUE)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def get_usernames():
    sql = "SELECT username from users WHERE visible = TRUE"
    result = db.session.execute(sql)
    userdata = result.fetchall()
    users = []
    for user in userdata:
        users.append(user[0])
    return users

def username_taken(username):
    users = get_usernames()
    if username in users:
        return True
    return False