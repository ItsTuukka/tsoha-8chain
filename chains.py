from db import db
from flask import session
import users, topics, validate

def get_list():
    t_id = topics.topic_id()
    sql = "SELECT C.id, C.description, U.username, C.created_at, C.user_id FROM chains C, users U WHERE topic_id=:t_id AND C.user_id=U.id AND C.visible=TRUE ORDER BY C.id"
    result = db.session.execute(sql, {"t_id":t_id})
    return result.fetchall()

def create_chain(chainname):
    if not validate.chain(chainname):
        return False
    user_id = users.user_id()
    topic_id = topics.topic_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO chains (description, topic_id, user_id, created_at, visible) VALUES (:chainname, :topic_id, :user_id, NOW(), TRUE)"
    db.session.execute(sql, {"chainname":chainname, "topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    id = latest_chain_id()
    set_chain_id(id)
    topics.update_chain_count()
    return True

def latest_chain_id():
    topic_id = topics.topic_id()
    sql = "SELECT * FROM chains WHERE topic_id=:topic_id ORDER BY id DESC"
    result = db.session.execute(sql, {"topic_id":topic_id})
    id = result.fetchone()
    return id[0]

def get_chain_name():
    c_id = chain_id()
    sql = "SELECT description FROM chains WHERE id=:c_id"
    result = db.session.execute(sql, {"c_id":c_id})
    name = result.fetchone()
    return name[0]

def updatechain(newname, id):
    if not validate.chain(newname):
        return False
    try:
        sql = "UPDATE chains SET description=:newname WHERE id=:id"
        db.session.execute(sql, {"newname":newname, "id":id})
        db.session.commit()
        return True
    except:
        return False

def set_chain_id(id):
    session['chain_id'] = id

def chain_id():
    return session.get("chain_id")