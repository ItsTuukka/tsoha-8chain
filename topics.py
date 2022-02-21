from db import db
from flask import session
import validate

def get_list():
    sql = "SELECT id, topicname FROM topics WHERE visible=TRUE ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def create_topic(topicname):
    if not validate.topic(topicname):
        return False
    sql = "INSERT INTO topics (topicname, visible) VALUES (:topicname, TRUE)"
    db.session.execute(sql, {"topicname":topicname})
    db.session.commit()
    return True

def get_chain_count(id):
    sql = "SELECT COUNT (*) FROM chains WHERE topic_id=:id and visible=TRUE"
    result = db.session.execute(sql, {"id":id})
    count = result.fetchone()
    return count[0]

def get_message_count(id):
    sql = "SELECT COUNT (*) FROM messages WHERE topic_id=:id and visible=TRUE"
    result = db.session.execute(sql, {"id":id})
    count = result.fetchone()
    return count[0]

def get_topic_name():
    sql = "SELECT topicname FROM topics WHERE id=:t_id"
    result = db.session.execute(sql, {"t_id":topic_id()})
    name = result.fetchone()
    return name[0]

def delete(id):
    sql = "UPDATE topics SET visible=FALSE WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def set_topic_id(id):
    session['topic_id'] = id

def topic_id():
    return session.get("topic_id")


