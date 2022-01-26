from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username AND visible=TRUE"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            False

def logout():
    del session["user_id"]

def register(username, password, admin):
    visible = True
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,admin,visible) VALUES (:username,:password,:admin,:visible)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin, "visible":visible})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)