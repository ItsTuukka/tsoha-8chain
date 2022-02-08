from db import db
from flask import session
import users

def get_list():
    sql = "SELECT id, topicname, chains, messages FROM topics WHERE visible=TRUE ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def create_topic(topicname):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO topics (topicname, chains, messages, visible) VALUES (:topicname, 0, 0, TRUE)"
    db.session.execute(sql, {"topicname":topicname})
    db.session.commit()
    return True

def update_chain_count():
    t_id = topic_id()
    sql = "UPDATE topics SET chains=chains+1 WHERE id=:t_id"
    db.session.execute(sql, {"t_id":t_id})
    db.session.commit()

def update_messages_count():
    t_id = topic_id()
    sql = "UPDATE topics SET messages=messages+1 WHERE id=:t_id"
    db.session.execute(sql, {"t_id":t_id})
    db.session.commit()

def get_topic_name():
    t_id = topic_id()
    sql = "SELECT topicname FROM topics WHERE id=:t_id"
    result = db.session.execute(sql, {"t_id":t_id})
    name = result.fetchone()
    return name[0]

def validate_topic(name):
    if not name or len(name) < 3 or len(name) > 100:
        return False
    return True

def set_topic_id(id):
    session['topic_id'] = id

def topic_id():
    return session.get("topic_id")


