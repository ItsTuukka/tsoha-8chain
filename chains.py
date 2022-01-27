from db import db
from flask import session
import users, topics, messages

def get_list(t_id):
    sql = "SELECT id, description, topic_id, user_id FROM chains WHERE topic_id=:t_id AND visible=TRUE"
    result = db.session.execute(sql, {"t_id":t_id})
    return result.fetchall()

def create_chain(chainname, content):
    visible = True
    user_id = users.user_id()
    topic_id = topics.topic_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO chains (description, topic_id, user_id, created_at, visible) VALUES (:chainname, :topic_id, :user_id, NOW(), :visible)"
    db.session.execute(sql, {"chainname":chainname, "topic_id":topic_id, "user_id":user_id, "visible":visible})
    db.session.commit()
    sql = "SELECT id FROM chains WHERE topic_id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    id = result.fetchone()
    set_chain_id(id[0])
    if messages.send(content):
        return True
    return False

def set_chain_id(id):
    session['chain_id'] = id

def chain_id():
    return session['chain_id']